#!/usr/bin/env python3
"""
add_course.py — Complete "add a course" superscript for Aesop AI Academy.

Collects all course info once, then updates every location that must know
about the course:

  1. courses-data.json          (module metadata for the generator tool)
  2. courses.html               (public courses page — panel + mega-menu)
  3. dashboard.html             (K-12 teacher dashboard)
  4. i18n/courses.*.json        (all 13 language files — English placeholder)
  5. course-registry.json       (rebuilt by build_registry.py)
  6. stats.json                 (rebuilt by build_stats.py)

Usage:
    python .github/scripts/add_course.py

The script adds the course as Coming Soon. Run auto_activate_courses.py
after module HTML files have been written to mark it live.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

# ── Repo paths ─────────────────────────────────────────────────────────────────
REPO = Path(__file__).resolve().parent.parent.parent
SCRIPTS = REPO / ".github" / "scripts"

# ── Import helpers from sibling scripts ────────────────────────────────────────
sys.path.insert(0, str(SCRIPTS))
from add_coming_soon_course import (
    slugify,
    next_dv_id,
    build_panel,
    insert_mega_menu_entry,
    COURSES_HTML,
    COURSES_DATA,
    CATEGORY_TO_MEGA_CAT,
)
from add_dashboard_course import add_to_dashboard, BAR_COLORS
from add_i18n_course import add_to_i18n

BUILD_REGISTRY = SCRIPTS / "build_registry.py"
BUILD_STATS    = SCRIPTS / "build_stats.py"


# ── Prompt helper ──────────────────────────────────────────────────────────────
def prompt(label: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    val = input(f"  {label}{suffix}: ").strip()
    return val or default


# ── Input collection ───────────────────────────────────────────────────────────
def collect_inputs() -> dict:
    print("\n╔══════════════════════════════════════════════════╗")
    print("║       Aesop AI Academy — Add a New Course        ║")
    print("╚══════════════════════════════════════════════════╝\n")

    name = prompt("Course name")
    if not name:
        print("Course name is required.")
        sys.exit(1)

    slug = prompt("URL slug", slugify(name))
    desc = prompt("Short description (1-2 sentences for courses.html)")
    category = prompt(
        f"Category ({', '.join(CATEGORY_TO_MEGA_CAT.keys())})", "Development"
    )
    icon = prompt("Icon emoji", "📘")
    n_mods = int(prompt("Number of modules", "8"))

    print(f"\n  Enter {n_mods} module titles (and optional subtitles).")
    print("  Format:  Title | Subtitle   (subtitle optional)\n")
    modules = []
    for i in range(1, n_mods + 1):
        raw = input(f"    M{i}: ").strip()
        if "|" in raw:
            parts = raw.split("|", 1)
            modules.append({"n": i, "title": parts[0].strip(), "sub": parts[1].strip()})
        else:
            modules.append({"n": i, "title": raw})

    print()
    course_num   = prompt("Course number for sub-label (e.g., 8)")
    sub_category = prompt("Sub-label category word (e.g., Ethics, Careers)", category.title())
    sub_label    = f"Course {course_num} — {sub_category}"

    print()
    bar = prompt(f"Dashboard progress bar color ({', '.join(BAR_COLORS)})", "teal")
    url = prompt("Dashboard URL path", f"/ai-academy/{slug}.html")

    return {
        "name":        name,
        "slug":        slug,
        "desc":        desc,
        "category":    category,
        "icon":        icon,
        "n_mods":      n_mods,
        "modules":     modules,
        "sub_label":   sub_label,
        "bar":         bar,
        "url":         url,
    }


# ── Step runners ───────────────────────────────────────────────────────────────
def step_courses_html(info: dict) -> int:
    """Add panel + mega-menu entry to courses.html. Returns the dv panel number."""
    html = COURSES_HTML.read_text(encoding="utf-8")
    dv = next_dv_id(html)

    panel = build_panel(
        dv, info["slug"], info["name"], info["desc"],
        info["category"], info["icon"], info["n_mods"], info["modules"], dv,
    )

    # Insert panel before the closing tag of the dv section
    last_dv = max(m.start() for m in re.finditer(r'id="dv-\d+"', html))
    close_pos = html.find("    </div>", last_dv)
    if close_pos == -1:
        print("  ERROR: Could not find insertion point in courses.html")
        sys.exit(1)

    html = html[:close_pos] + panel + html[close_pos:]
    html = insert_mega_menu_entry(html, dv, info["name"], info["category"])

    COURSES_HTML.write_text(html, encoding="utf-8")
    print(f"  ✓ courses.html — panel dv-{dv} + mega-menu entry added")
    return dv


def step_courses_data(info: dict, dv: int) -> None:
    """Append stub entry to courses-data.json."""
    raw = COURSES_DATA.read_text(encoding="utf-8-sig")
    data = json.loads(raw)

    if any(c.get("id") == info["slug"] for c in data.get("courses", [])):
        print(f"  ⚠  '{info['slug']}' already in courses-data.json — skipping.")
        return

    data["courses"].append({
        "id":          info["slug"],
        "name":        info["name"],
        "icon":        info["icon"],
        "category":    info["category"],
        "panelId":     f"dv-{dv}",
        "description": info["desc"],
        "live":        False,
        "modules":     info["modules"],
    })
    COURSES_DATA.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"  ✓ courses-data.json — '{info['slug']}' stub added")


def step_dashboard(info: dict) -> None:
    """Add course to K-12 dashboard."""
    add_to_dashboard(
        course_id=info["slug"],
        title=info["name"],
        sub=info["sub_label"],
        icon=info["icon"],
        bar=info["bar"],
        n_mods=info["n_mods"],
        url=info["url"],
    )


def step_i18n(info: dict) -> None:
    """Add translatable strings to all 13 i18n files."""
    print("  Adding i18n strings…")
    add_to_i18n(
        sub_label=info["sub_label"],
        title=info["name"],
        desc=info["desc"],
    )


def step_rebuild(script: Path, label: str) -> None:
    """Run a rebuild script and report the result."""
    result = subprocess.run(
        [sys.executable, str(script)],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print(f"  ✓ {label} rebuilt successfully")
    else:
        print(f"  ✗ {label} failed:")
        print(result.stdout[-500:] if result.stdout else "")
        print(result.stderr[-500:] if result.stderr else "")


# ── Main ───────────────────────────────────────────────────────────────────────
def main() -> None:
    info = collect_inputs()

    print("\n── Updating all course locations ──────────────────────\n")

    dv = step_courses_html(info)        # 1 + 2: courses.html (panel + mega-menu)
    step_courses_data(info, dv)         # 3: courses-data.json
    step_dashboard(info)                # 4: dashboard.html
    step_i18n(info)                     # 5: i18n/*.json (13 files)
    step_rebuild(BUILD_REGISTRY, "course-registry.json")   # 6: registry
    step_rebuild(BUILD_STATS,    "stats.json")              # 7: stats

    print(f"""
╔══════════════════════════════════════════════════╗
║  '{info["name"]}' added as Coming Soon  ║
╚══════════════════════════════════════════════════╝

Next steps:
  1. Use the Module Generator to write the {info["n_mods"]} module HTML files.
  2. Run:  python .github/scripts/auto_activate_courses.py --apply
     (marks the course live once all modules are written)
  3. Translate non-English strings in i18n/courses.*.json when ready.
  4. Commit and push.
""")


if __name__ == "__main__":
    main()
