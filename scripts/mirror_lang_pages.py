#!/usr/bin/env python3
"""
mirror_lang_pages.py — Mirror /es language pages into a new language root.

Usage:
    python mirror_lang_pages.py <src_lang> <dst_lang> [--dry-run]

Example:
    python mirror_lang_pages.py es hi
    python mirror_lang_pages.py es ar --dry-run

What it does (per pair: index.html, ai-academy/courses.html, ai-academy/modules/electives-hub.html):
  1. Copies <src_lang>/<page> to <dst_lang>/<page>
  2. Rewrites <html lang="<src>"> → <html lang="<dst>">
  3. Adds dir="rtl" if dst_lang is RTL (ar, ur, fa, he)
  4. Rewrites href/src/url paths starting with /<src>/ → /<dst>/
  5. Rewrites localStorage 'aesop-lang' default value occurrences
  6. Optional title-prefix tag so the page is identifiable in browser history

Reads language config from ai-academy/modules/course-registry.json (_meta.languages).
"""
from __future__ import annotations
import json
import re
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REGISTRY = REPO_ROOT / "ai-academy" / "modules" / "course-registry.json"

PAGES = [
    "index.html",
    "ai-academy/courses.html",
    "ai-academy/modules/electives-hub.html",
]

RTL_LANGS = {"ar", "ur", "fa", "he"}


def load_lang_meta() -> dict:
    """Return {code: {name, nativeName, flag, urlPrefix, dir}} from registry."""
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    langs = data.get("_meta", {}).get("languages", [])
    return {l["code"]: l for l in langs}


def transform_html(text: str, src: str, dst: str, dst_meta: dict) -> str:
    # 1. <html lang="...">
    text = re.sub(
        r'(<html[^>]*\blang=)"' + re.escape(src) + r'"',
        r'\1"' + dst + '"',
        text,
        count=1,
    )

    # 2. dir="rtl" injection for RTL languages (only if not already present)
    if dst in RTL_LANGS:
        # ensure dir="rtl" exists on <html>
        if not re.search(r'<html[^>]*\bdir=', text[:500]):
            text = re.sub(
                r'(<html\b)([^>]*)>',
                r'\1\2 dir="rtl">',
                text,
                count=1,
            )

    # 3. Path rewrites: /es/ → /hi/  (in href, src, url(), and bare strings)
    text = re.sub(r'(["\'(])/' + re.escape(src) + '/', r'\1/' + dst + '/', text)
    # also /es" or /es' (no trailing slash) at end of href
    text = re.sub(r'(["\'(])/' + re.escape(src) + '(["\')])', r'\1/' + dst + r'\2', text)

    # 4. localStorage default lang value
    text = re.sub(
        r"(['\"])aesop-lang\1\s*,\s*(['\"])" + re.escape(src) + r"\2",
        r"\1aesop-lang\1, \2" + dst + r"\2",
        text,
    )

    # 5. data-lang="es" attribute defaults
    text = re.sub(
        r'data-lang="' + re.escape(src) + '"',
        f'data-lang="{dst}"',
        text,
    )

    # 6. activeLang fallback: `localStorage.getItem('aesop-lang') || 'es'` → '...|| 'hi''
    text = re.sub(
        r"(localStorage\.getItem\(\s*['\"]aesop-lang['\"]\s*\)\s*\|\|\s*['\"])"
        + re.escape(src) + r"(['\"])",
        r"\1" + dst + r"\2",
        text,
    )

    return text


def main() -> int:
    args = sys.argv[1:]
    dry = "--dry-run" in args
    args = [a for a in args if not a.startswith("--")]
    if len(args) != 2:
        print(__doc__)
        return 2
    src, dst = args
    if src == dst:
        print("source and destination languages must differ")
        return 2

    meta = load_lang_meta()
    if src not in meta:
        print(f"source language '{src}' not in registry _meta.languages")
        return 2
    if dst not in meta:
        print(f"destination language '{dst}' not in registry _meta.languages")
        return 2

    src_root = REPO_ROOT / src
    dst_root = REPO_ROOT / dst
    if not src_root.exists():
        print(f"source root /{src} does not exist")
        return 2

    dst_meta = meta[dst]
    print(f"Mirror /{src} → /{dst}  ({dst_meta['nativeName']}, dir={dst_meta.get('dir', 'ltr')})")

    for rel in PAGES:
        src_path = src_root / rel
        dst_path = dst_root / rel
        if not src_path.exists():
            print(f"  ✗ skip {rel} — source missing")
            continue
        if not dry:
            dst_path.parent.mkdir(parents=True, exist_ok=True)
        text = src_path.read_text(encoding="utf-8")
        new_text = transform_html(text, src, dst, dst_meta)
        if dry:
            changed = sum(1 for a, b in zip(text.splitlines(), new_text.splitlines()) if a != b)
            print(f"  · {rel}: would write {len(new_text):,} bytes ({changed} lines changed)")
        else:
            dst_path.write_text(new_text, encoding="utf-8")
            print(f"  ✓ wrote {dst_path.relative_to(REPO_ROOT)} ({len(new_text):,} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
