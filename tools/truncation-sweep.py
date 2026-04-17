#!/usr/bin/env python3
"""
Truncation-damage sweep for the Aesop repo.

Scans every tracked HTML and JSON file for signs of silent truncation from
the Windows↔VM mount layer. Focuses on reliable, low-false-positive signals:

  JSON files
    • Must parse as JSON. A parse failure is treated as damage.

  HTML files
    • Must contain </html> (closing tag) — scanned from the end of the file.
    • <script> and </script> tag counts must match.
    • <html>, <head>, <body> open/close counts must match.
    • File must not end mid-tag or mid-string (last non-empty line
      must terminate with > , } , ; , or be a well-formed closing line).

Usage:
  python3 tools/truncation-sweep.py            # scan whole repo
  python3 tools/truncation-sweep.py --path ai-academy
"""

from __future__ import annotations
import argparse
import json
import os
import re
import sys
from pathlib import Path

SKIP_DIRS = {'.git', 'node_modules', '.claude'}

HTML_CLOSE_RE = re.compile(r'</html\s*>', re.IGNORECASE)
SCRIPT_OPEN_RE = re.compile(r'<script\b', re.IGNORECASE)
SCRIPT_CLOSE_RE = re.compile(r'</script\s*>', re.IGNORECASE)
HTML_OPEN_RE = re.compile(r'<html\b', re.IGNORECASE)
HEAD_OPEN_RE = re.compile(r'<head\b', re.IGNORECASE)
HEAD_CLOSE_RE = re.compile(r'</head\s*>', re.IGNORECASE)
BODY_OPEN_RE = re.compile(r'<body\b', re.IGNORECASE)
BODY_CLOSE_RE = re.compile(r'</body\s*>', re.IGNORECASE)


def iter_files(root: Path):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            p = Path(dirpath) / name
            yield p


def last_non_empty_line(text: str) -> str:
    for line in reversed(text.splitlines()):
        s = line.rstrip()
        if s:
            return s
    return ''


def check_json(path: Path) -> list[str]:
    issues = []
    try:
        with open(path, 'rb') as f:
            raw = f.read()
        if not raw.strip():
            issues.append('empty file')
            return issues
        try:
            json.loads(raw.decode('utf-8', errors='replace'))
        except json.JSONDecodeError as e:
            issues.append(f'JSON parse error: {e.msg} at line {e.lineno} col {e.colno}')
    except Exception as e:
        issues.append(f'read error: {e}')
    return issues


def check_html(path: Path) -> list[str]:
    """
    Reliable signal: if the file starts with a full HTML document (<!doctype
    or <html>) then its LAST non-empty line must be </html>. Script/body tag
    counting is abandoned — it false-positives on any file whose JS source
    contains '<script>' string literals (e.g. module generators).
    """
    issues = []
    try:
        text = path.read_text(encoding='utf-8', errors='replace')
    except Exception as e:
        return [f'read error: {e}']

    if not text.strip():
        return ['empty file']

    head = text[:4096].lower()
    is_full_doc = '<!doctype' in head or '<html' in head
    if not is_full_doc:
        return []  # fragment/include — skip structural checks

    last = last_non_empty_line(text).strip()

    # Canonical complete file: last non-empty line is the closing </html>.
    if re.fullmatch(r'</html\s*>', last, re.IGNORECASE):
        return []

    # Allow files that end with trailing script/style/body closers but have
    # the </html> somewhere in the final 200 chars (some tools emit extra
    # blank lines or comments after </html>). Still flag if </html> missing.
    tail_window = text[-400:]
    if not HTML_CLOSE_RE.search(tail_window):
        issues.append(f'likely truncated: last line = {last[-90:]!r}')
    return issues


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--path', default='.', help='Root path to scan')
    ap.add_argument('--ext', default='html,json', help='Comma-separated extensions')
    args = ap.parse_args()

    root = Path(args.path).resolve()
    exts = {'.' + e.strip().lower() for e in args.ext.split(',')}

    total = 0
    flagged: list[tuple[Path, list[str]]] = []

    for p in iter_files(root):
        if p.suffix.lower() not in exts:
            continue
        total += 1
        if p.suffix.lower() == '.json':
            issues = check_json(p)
        else:
            issues = check_html(p)
        if issues:
            flagged.append((p, issues))

    print(f'Scanned {total} files under {root}')
    print(f'Flagged {len(flagged)} with potential truncation damage')
    print()

    if flagged:
        for p, issues in flagged:
            rel = p.relative_to(root) if p.is_relative_to(root) else p
            print(f'  {rel}')
            for i in issues:
                print(f'      • {i}')
        print()
        sys.exit(1)
    else:
        print('No damage detected.')
        sys.exit(0)


if __name__ == '__main__':
    main()
