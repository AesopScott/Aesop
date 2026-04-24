#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dedup_mega_buttons.py — Collapse duplicate mega-menu buttons down to one
per course (keyed by data-course).

When multiple mega-link buttons share the same data-course attribute,
keep exactly one and remove the rest. Preference rules:

  1. If any duplicate is ``mega-link--live``, keep the first live one.
  2. Otherwise keep the first button seen.

This also **promotes** the kept button to ``mega-link--live`` if the
course has a folder on disk, regardless of what the kept button's
original class was — a course that exists on disk should be live.

Idempotent.

Usage:
    python .github/scripts/dedup_mega_buttons.py           # dry-run
    python .github/scripts/dedup_mega_buttons.py --apply   # write changes
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO         = Path(__file__).resolve().parents[2]
COURSES_HTML = REPO / "ai-academy" / "courses.html"
MODULES_DIR  = REPO / "ai-academy" / "modules"


def disk_slugs() -> set[str]:
    return {d.name for d in MODULES_DIR.iterdir()
            if d.is_dir() and (d / f"{d.name}-m1.html").exists()}


def _is_live(classes: str) -> bool:
    return "mega-link--live" in classes


def _set_live(classes: str) -> str:
    """Return classes with exactly one of mega-link--live / --soon, set to live."""
    classes = re.sub(r"\bmega-link--soon\b", "", classes)
    classes = re.sub(r"\s+", " ", classes).strip()
    if "mega-link--live" not in classes:
        classes += " mega-link--live"
    return classes


def reconcile(html: str) -> tuple[str, dict]:
    """Walk every mega-link button with a data-course; within each slug
    group, keep one button (prefer --live), remove the rest, and force
    the kept button to --live if the slug exists on disk."""
    on_disk = disk_slugs()

    btn_line = re.compile(
        r'([ \t]*<button\s+class="([^"]+)"[^>]*data-course="([^"]+)"[^>]*>[^<]+</button>\n)',
    )

    # First pass: collect every match with its offset, classes, slug
    matches = list(btn_line.finditer(html))

    # Group indices by slug
    from collections import defaultdict
    groups: dict[str, list[int]] = defaultdict(list)
    for i, m in enumerate(matches):
        groups[m.group(3)].append(i)

    # Decide which index to keep per slug
    keep_idx: set[int] = set()
    for slug, idxs in groups.items():
        first_live = next((i for i in idxs if _is_live(matches[i].group(2))), None)
        keep_idx.add(first_live if first_live is not None else idxs[0])

    # Plan: for each match, either drop, promote-to-live, or leave as-is
    removed: list[dict] = []
    promoted: list[dict] = []

    # Build the new HTML by walking matches in order, replacing or deleting.
    # We rebuild as string slices for simplicity.
    out_parts = []
    last = 0
    for i, m in enumerate(matches):
        out_parts.append(html[last:m.start()])
        line      = m.group(1)
        classes   = m.group(2)
        slug      = m.group(3)

        if i not in keep_idx:
            # drop this line entirely
            removed.append({"slug": slug, "classes": classes, "line": line.strip()})
            # don't append anything
        elif slug in on_disk and not _is_live(classes):
            new_classes = _set_live(classes)
            new_line = line.replace(f'class="{classes}"', f'class="{new_classes}"', 1)
            promoted.append({"slug": slug, "was": classes, "now": new_classes})
            out_parts.append(new_line)
        else:
            out_parts.append(line)
        last = m.end()

    out_parts.append(html[last:])
    new_html = "".join(out_parts)

    return new_html, {"removed": removed, "promoted": promoted,
                      "kept_total": len(keep_idx),
                      "total_seen": len(matches)}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    html = COURSES_HTML.read_text(encoding="utf-8")
    new_html, stats = reconcile(html)

    print(f"Seen:     {stats['total_seen']} tagged buttons")
    print(f"Removed:  {len(stats['removed'])}")
    for r in stats["removed"]:
        print(f"  data-course={r['slug']!r}  was-live={_is_live(r['classes'])}")
        print(f"    {r['line'][:120]}")
    print(f"Promoted to --live (course has disk folder): {len(stats['promoted'])}")
    for p in stats["promoted"]:
        print(f"  {p['slug']}  {p['was']!r} → {p['now']!r}")
    print(f"Kept:     {stats['kept_total']} (one per data-course)")

    if not args.apply:
        print("\nDry run — use --apply to write.")
        return

    if new_html == html:
        print("\nNo changes.")
        return

    COURSES_HTML.write_text(new_html, encoding="utf-8")
    print(f"\nWrote {COURSES_HTML.relative_to(REPO)}")


if __name__ == "__main__":
    main()
