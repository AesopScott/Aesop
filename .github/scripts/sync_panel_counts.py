#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sync_panel_counts.py — Keep "Category · Course N of TOTAL" labels in
core-panel__num divs accurate.

The source of truth for TOTAL is the number of mega-link buttons in that
category's section of the courses.html mega-menu. Whenever a new course is
added to the mega-menu, the panel count in every existing panel for that
category must be updated to reflect the new total.

Previously add_coming_soon_course.py set the total only in the *new* panel,
leaving every older panel stale. This script fixes all of them idempotently.

Usage:
    python .github/scripts/sync_panel_counts.py           # dry-run
    python .github/scripts/sync_panel_counts.py --apply   # write
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


def count_category_buttons(html: str) -> dict[str, int]:
    """Return {category_label: button_count} by counting mega-link buttons
    in each mega-cat section of the courses.html mega-menu."""

    mega_cat_pat = re.compile(r'<div\s+class="mega-cat">([^<]+)</div>')
    btn_pat      = re.compile(r'class="mega-link')

    counts: dict[str, int] = {}
    cat_positions = [(m.start(), m.group(1).strip()) for m in mega_cat_pat.finditer(html)]

    for i, (pos, label) in enumerate(cat_positions):
        end = cat_positions[i + 1][0] if i + 1 < len(cat_positions) else len(html)
        section   = html[pos:end]
        n_buttons = len(btn_pat.findall(section))
        counts[label] = n_buttons

    return counts


def update_panel_counts(html: str, counts: dict[str, int]) -> tuple[str, list[dict]]:
    """Replace stale 'Category · Course N of OLD' with 'Category · Course N of NEW'
    wherever the category total has changed."""

    panel_num_pat = re.compile(
        r'(<div\s+class="core-panel__num">)'
        r'([^<·]+)'          # category prefix, e.g. "Development "
        r'·\s*Course\s+'
        r'(\d+)'             # course index N
        r'\s+of\s+'
        r'(\d+)'             # old total
        r'(</div>)',
        re.IGNORECASE,
    )

    fixes: list[dict] = []

    def replace_count(m: re.Match) -> str:
        open_tag   = m.group(1)
        cat_prefix = m.group(2).strip()
        n          = int(m.group(3))
        old_total  = int(m.group(4))
        close_tag  = m.group(5)

        # Match the panel category to a mega-cat label (emoji-prefixed).
        new_total = None
        for label, count in counts.items():
            label_text = re.sub(r'^[^\w]+', '', label).strip()
            if (label_text.lower() == cat_prefix.lower() or
                    cat_prefix.lower() in label_text.lower()):
                new_total = count
                break

        if new_total is None or new_total == old_total:
            return m.group(0)

        fixes.append({
            "category": cat_prefix,
            "n": n,
            "old": old_total,
            "new": new_total,
        })
        return f'{open_tag}{cat_prefix} · Course {n} of {new_total}{close_tag}'

    new_html = panel_num_pat.sub(replace_count, html)
    return new_html, fixes


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    html = COURSES_HTML.read_text(encoding="utf-8")

    counts = count_category_buttons(html)
    print("Mega-menu button counts per category:")
    for label, n in counts.items():
        print(f"  {label!r}: {n}")

    new_html, fixes = update_panel_counts(html, counts)

    if not fixes:
        print("\nAll panel counts are already correct.")
    else:
        print(f"\nPanel counts to update ({len(fixes)}):")
        for f in fixes:
            print(f"  {f['category']} Course {f['n']}: of {f['old']} → of {f['new']}")

    if not args.apply:
        print("\nDry run — use --apply to write.")
        return

    if new_html == html:
        print("\nNo changes needed.")
        return

    COURSES_HTML.write_text(new_html, encoding="utf-8")
    print(f"\nWrote {COURSES_HTML.relative_to(REPO)}")


if __name__ == "__main__":
    main()
