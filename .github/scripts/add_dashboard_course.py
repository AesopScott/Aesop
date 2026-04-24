#!/usr/bin/env python3
"""
add_dashboard_course.py — Add a course to the K-12 teacher dashboard (dashboard.html)

Usage:
    python .github/scripts/add_dashboard_course.py

Also importable: call add_to_dashboard(**kwargs) directly from the superscript.
"""

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
DASHBOARD_HTML = REPO / "ai-academy" / "dashboard.html"

BAR_COLORS = ["gold", "teal", "purple", "navy", "green", "amber", "red", "blue"]


def prompt(label: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    val = input(f"{label}{suffix}: ").strip()
    return val or default


def add_to_dashboard(
    course_id: str,
    title: str,
    sub: str,
    icon: str,
    bar: str,
    n_mods: int,
    url: str,
) -> None:
    """Insert a course entry into the COURSES array in dashboard.html."""
    html = DASHBOARD_HTML.read_text(encoding="utf-8")

    # Locate the COURSES array
    courses_match = re.search(r"(const COURSES\s*=\s*\[)(.*?)(\s*\];)", html, re.DOTALL)
    if not courses_match:
        print("ERROR: Could not find COURSES array in dashboard.html")
        sys.exit(1)

    # Check for duplicates
    if f"id:'{course_id}'" in courses_match.group(2):
        print(f"  ⚠  '{course_id}' already exists in dashboard.html — skipping.")
        return

    new_entry = (
        f"      {{ id:'{course_id}', title:'{title}', sub:'{sub}', "
        f"icon:'{icon}', bar:'{bar}', modules:{n_mods}, url:'{url}' }},"
    )

    # Insert before the closing ];
    insert_pos = courses_match.start(3)
    html = html[:insert_pos] + "\n" + new_entry + html[insert_pos:]

    DASHBOARD_HTML.write_text(html, encoding="utf-8")
    print(f"  ✓ Added '{course_id}' to dashboard.html")


def main() -> None:
    print("\n=== Add Course to K-12 Dashboard ===\n")

    course_id = prompt("Course ID (e.g., ai-governance)")
    if not course_id:
        print("Course ID is required.")
        sys.exit(1)

    title = prompt("Course title")
    sub = prompt("Subtitle (e.g., Course 8 — Ethics)")
    icon = prompt("Icon emoji", "📘")
    bar = prompt(f"Progress bar color ({', '.join(BAR_COLORS)})", "teal")
    n_mods = int(prompt("Number of modules", "8"))
    url = prompt("URL path", f"/ai-academy/{course_id}.html")

    add_to_dashboard(course_id, title, sub, icon, bar, n_mods, url)
    print("\nDone.\n")


if __name__ == "__main__":
    main()
