#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sync_courses.py — Reconcile UI surfaces with course-registry.json.

The registry is the single source of truth for which courses are live.
Over time, the mega-menu in courses.html drifts because add_course.py
only ever appends — it never flips an existing button from --live to
--soon when a course's status changes, and it never strips entries for
courses removed from the registry. This script closes that gap.

What it syncs (v1):
  courses.html mega-menu buttons — each button's "mega-link--live" vs
  "mega-link--soon" class is corrected to match the course's registry
  status. Matching is done by button display text against registry
  `title` (with HTML entities normalised on both sides). If a title
  appears multiple times in the registry, the button is marked live if
  ANY matching entry is live.

Not yet synced (future passes):
  - courses.html panels (core-badge-live / draft badge)
  - dashboard.html COURSES array membership
  - i18n/courses.*.json entry presence

Usage:
    python .github/scripts/sync_courses.py           # dry-run
    python .github/scripts/sync_courses.py --apply   # write changes
"""

from __future__ import annotations

import argparse
import html as _html_mod
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO         = Path(__file__).resolve().parents[2]
COURSES_HTML = REPO / "ai-academy" / "courses.html"
REGISTRY     = REPO / "ai-academy" / "modules" / "course-registry.json"


def _norm(text: str) -> str:
    """Normalise a title for matching — unescape HTML entities and strip
    whitespace. Case-preserving so the caller can still compare exactly
    against the registry."""
    return _html_mod.unescape(text or "").strip()


def load_registry_title_status() -> dict[str, str]:
    """Return {normalised_title: 'live' or 'soon'}. If multiple registry
    entries share a title, 'live' wins."""
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    by_title: dict[str, set[str]] = defaultdict(set)
    for entry in data.values():
        if not isinstance(entry, dict):
            continue
        title = entry.get("title")
        if not title:
            continue
        by_title[_norm(title)].add(entry.get("status") or "coming-soon")

    out: dict[str, str] = {}
    for title, statuses in by_title.items():
        out[title] = "live" if "live" in statuses else "soon"
    return out


def target_class(status: str) -> str:
    return "mega-link mega-link--live" if status == "live" else "mega-link mega-link--soon"


def reconcile_mega_menu(html: str, title_status: dict[str, str]) -> tuple[str, dict]:
    """Return (new_html, stats) with every mega-menu button's class
    corrected to match the registry status keyed by normalised title."""
    btn_pat = re.compile(r'<button\s+([^>]*?)>([^<]+)</button>', re.DOTALL)
    class_attr_pat = re.compile(r'class="([^"]*)"')

    changed_to_live = 0
    changed_to_soon = 0
    unchanged = 0
    unmatched: list[str] = []

    def replace(m: re.Match) -> str:
        nonlocal changed_to_live, changed_to_soon, unchanged
        attrs = m.group(1)
        raw_name = m.group(2)

        cm = class_attr_pat.search(attrs)
        if not cm:
            return m.group(0)

        classes = cm.group(1)
        if "mega-link" not in classes:
            return m.group(0)  # not a mega-menu button

        name = _norm(raw_name)
        status = title_status.get(name)
        if status is None:
            unmatched.append(name)
            return m.group(0)  # no registry entry — leave class as-is

        desired = target_class(status)
        if classes == desired:
            unchanged += 1
            return m.group(0)

        if "--live" in desired:
            changed_to_live += 1
        else:
            changed_to_soon += 1

        new_attrs = class_attr_pat.sub(f'class="{desired}"', attrs, count=1)
        return f'<button {new_attrs}>{raw_name}</button>'

    new_html = btn_pat.sub(replace, html)

    return new_html, {
        "changed_to_live": changed_to_live,
        "changed_to_soon": changed_to_soon,
        "unchanged":       unchanged,
        "unmatched":       unmatched,
    }


def count_live_buttons(html: str) -> int:
    return len(re.findall(r'class="mega-link[^"]*mega-link--live', html))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true",
                    help="Write the reconciled courses.html. Without this, runs dry.")
    args = ap.parse_args()

    title_status = load_registry_title_status()
    live_titles = sum(1 for s in title_status.values() if s == "live")
    print(f"Registry: {live_titles} live / {len(title_status)} distinct titles")

    html = COURSES_HTML.read_text(encoding="utf-8")
    before = count_live_buttons(html)
    print(f"Before:   {before} buttons marked mega-link--live")

    new_html, stats = reconcile_mega_menu(html, title_status)
    after = count_live_buttons(new_html)
    print(f"After:    {after} buttons marked mega-link--live")
    print()
    print(f"  Flipped to --live:  {stats['changed_to_live']}")
    print(f"  Flipped to --soon:  {stats['changed_to_soon']}")
    print(f"  Already correct:    {stats['unchanged']}")
    if stats["unmatched"]:
        print(f"  Unmatched (no registry title): {len(stats['unmatched'])}")
        for u in stats["unmatched"][:10]:
            print(f"    - {u!r}")
        if len(stats["unmatched"]) > 10:
            print(f"    … and {len(stats['unmatched']) - 10} more")

    if not args.apply:
        print("\nDry run — no files written. Re-run with --apply to save.")
        return

    if new_html == html:
        print("\nNothing to change.")
        return

    COURSES_HTML.write_text(new_html, encoding="utf-8")
    print(f"\nWrote {COURSES_HTML.relative_to(REPO)}")


if __name__ == "__main__":
    main()
