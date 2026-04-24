#!/usr/bin/env python3
"""
add_i18n_course.py — Add a new course's translatable strings to all 13 i18n files.

Adds three keys per course:
  - Sub-label  e.g. "Course 8 — Ethics"
  - Title      e.g. "AI Ethics & Decision-Making"
  - Description (full text shown on the course card)

Non-English files receive the English string as a placeholder, consistent with
how the rest of the partially-translated files are structured.

Usage:
    python .github/scripts/add_i18n_course.py

Also importable: call add_to_i18n(sub_label, title, desc) directly.
"""

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
I18N_DIR = REPO / "i18n"

LANG_FILES = [
    "courses.ar.json",
    "courses.de.json",
    "courses.en.json",
    "courses.es.json",
    "courses.fa.json",
    "courses.fr.json",
    "courses.hi.json",
    "courses.ja.json",
    "courses.ko.json",
    "courses.ru.json",
    "courses.sw.json",
    "courses.ur.json",
    "courses.zh.json",
]


def prompt(label: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    val = input(f"{label}{suffix}: ").strip()
    return val or default


def add_to_i18n(sub_label: str, title: str, desc: str) -> None:
    """
    Append sub_label, title, and desc to every i18n/courses.*.json file.
    English file gets value == key. All others get English string as placeholder.
    """
    new_keys = {
        sub_label: sub_label,
        title: title,
        desc: desc,
    }

    for filename in LANG_FILES:
        path = I18N_DIR / filename
        if not path.exists():
            print(f"  ⚠  {filename} not found — skipping.")
            continue

        data = json.loads(path.read_text(encoding="utf-8"))

        added = []
        for key, en_value in new_keys.items():
            if key in data:
                print(f"  ⚠  Key already exists in {filename}: {key[:60]}…")
                continue
            # English file: value == key (it's its own translation)
            # All others: English placeholder (consistent with existing pattern)
            data[key] = en_value
            added.append(key[:60])

        path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        if added:
            print(f"  ✓ {filename}: added {len(added)} key(s)")
        else:
            print(f"  — {filename}: no new keys needed")


def main() -> None:
    print("\n=== Add Course Strings to i18n Files ===\n")

    sub_label = prompt('Sub-label (e.g., "Course 8 — Ethics")')
    if not sub_label:
        print("Sub-label is required.")
        sys.exit(1)

    title = prompt("Course title (e.g., AI Ethics & Decision-Making)")
    desc = prompt("Course description (full text shown on course card)")

    print()
    add_to_i18n(sub_label, title, desc)
    print("\nDone. Translate non-English values manually when ready.\n")


if __name__ == "__main__":
    main()
