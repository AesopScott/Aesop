#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sync_i18n_to_registry.py — Add missing course-title entries to every
i18n/courses.<lang>.json file.

Source of truth: ``course-registry.json`` entries whose status == "live"
and whose url field points to /ai-academy/modules/<slug>/ (matching a
disk folder). The set of canonical titles from these registry entries
must all be present as keys in every i18n translation file.

This script is additive only:
  - For each i18n file, compute the set of missing titles (registry
    title not currently a key).
  - For each missing title, add a placeholder entry whose value equals
    the English title itself. (New courses haven't been translated yet;
    placeholders mean the site renders the English name rather than
    the key.)
  - Never removes keys — the i18n files contain many non-course UI
    strings that aren't in our scope.

Usage:
    python .github/scripts/sync_i18n_to_registry.py           # dry-run
    python .github/scripts/sync_i18n_to_registry.py --apply   # write
"""

from __future__ import annotations

import argparse
import html as _html_mod
import json
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO         = Path(__file__).resolve().parents[2]
REGISTRY     = REPO / "ai-academy" / "modules" / "course-registry.json"
I18N_DIR     = REPO / "i18n"


def canonical_live_titles() -> list[str]:
    """Return sorted, de-entitied titles of every disk-backed live
    registry entry."""
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    titles: set[str] = set()
    for entry in data.values():
        if not isinstance(entry, dict):
            continue
        if entry.get("status") != "live":
            continue
        url = entry.get("url") or ""
        if not re.search(r"/modules/([^/]+)/", url):
            continue
        title = _html_mod.unescape(entry.get("title") or "").strip()
        if title:
            titles.add(title)
    return sorted(titles)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    titles = canonical_live_titles()
    print(f"Canonical titles from registry (live + disk-backed): {len(titles)}")

    files = sorted(I18N_DIR.glob("courses.*.json"))
    total_added = 0

    for f in files:
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"  {f.name}: SKIP (unreadable: {e})")
            continue
        if not isinstance(data, dict):
            print(f"  {f.name}: SKIP (not a JSON object)")
            continue

        missing = [t for t in titles if t not in data]
        if not missing:
            print(f"  {f.name}: already complete")
            continue

        print(f"  {f.name}: adding {len(missing)} missing keys")
        for t in missing:
            data[t] = t   # English placeholder — matches add_course.py convention

        if args.apply:
            f.write_text(
                json.dumps(data, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
        total_added += len(missing)

    print()
    print(f"Total entries {'added' if args.apply else 'would be added'}: {total_added}")
    if not args.apply:
        print("Dry run — use --apply to write.")


if __name__ == "__main__":
    main()
