#!/usr/bin/env python3
"""
Add the shared top-banner.js script tag to a curated list of HTML pages.

Target scope: every non-archive HTML page except the 544 module files
and ai-academy/modules/electives-hub.html. Root index.html is also
skipped because it already embeds the banner inline.

For each target file:
  - Skip if the script tag is already present.
  - Insert `<script src="/assets/top-banner.js"></script>` immediately
    before the closing </body> tag.
  - If the file has no </body> (truncated/broken), skip and report.

Run from the repo root. Writes changes in place. Idempotent — safe to
re-run after new pages are added or after a merge accidentally drops
the tag from some files.
"""
from __future__ import annotations

import sys
from pathlib import Path

BANNER_TAG = '<script src="/assets/top-banner.js"></script>'

REPO_ROOT = Path(__file__).resolve().parent.parent

EXCLUDE_DIRS = {
    'archive',
    'review/archive',
    'es_old',
    '.git',
    'TEMP',
    'ai-academy/archive',
    'policies/archive',
    'ai-academy/modules',  # skip all 544 module files
    '.claude',
}

EXCLUDE_FILES = {
    'index.html',                                        # root: banner is inline
    'ai-academy/modules/electives-hub.html',             # the hub (already excluded by dir)
}


def is_excluded(rel: Path) -> bool:
    parts = rel.as_posix()
    for d in EXCLUDE_DIRS:
        if parts.startswith(d + '/') or parts == d:
            return True
    if parts in EXCLUDE_FILES:
        return True
    return False


def collect_targets(root: Path) -> list[Path]:
    targets = []
    for p in root.rglob('*.html'):
        rel = p.relative_to(root)
        if is_excluded(rel):
            continue
        targets.append(p)
    return sorted(targets)


def patch_file(path: Path) -> str:
    """Return one of: 'added', 'already', 'no-body', 'error:<msg>'"""
    try:
        text = path.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        try:
            text = path.read_text(encoding='cp1252')
        except Exception as e:
            return f'error:read:{e}'

    if 'top-banner.js' in text:
        return 'already'

    idx = text.lower().rfind('</body>')
    if idx == -1:
        return 'no-body'

    new_text = text[:idx] + BANNER_TAG + '\n' + text[idx:]
    # Preserve original line endings (don't translate).
    path.write_bytes(new_text.encode('utf-8'))
    return 'added'


def main():
    targets = collect_targets(REPO_ROOT)
    counts: dict[str, int] = {}
    issues: list[tuple[str, Path]] = []

    for t in targets:
        rel = t.relative_to(REPO_ROOT)
        status = patch_file(t)
        counts[status] = counts.get(status, 0) + 1
        if status == 'no-body' or status.startswith('error'):
            issues.append((status, rel))

    print(f'Scanned {len(targets)} files.')
    for k, v in sorted(counts.items()):
        print(f'  {k:<16} {v}')
    if issues:
        print('\nIssues:')
        for s, r in issues:
            print(f'  [{s}] {r}')


if __name__ == '__main__':
    sys.exit(main())
