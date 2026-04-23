#!/usr/bin/env python3
"""
add_coming_soon_course.py — Add a Coming Soon course panel to courses.html
and a stub entry to courses-data.json, ready for ModGen.

Usage:
    python .github/scripts/add_coming_soon_course.py

You will be prompted for:
  - Course name
  - Short description (1-2 sentences)
  - Category  (Development / Core / Elective)
  - Icon emoji
  - Number of modules (default 8)
  - Module titles and subtitles (one per line, or press Enter to skip subtitles)

The script assigns the next available dv-XX panel ID automatically.
"""

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
COURSES_HTML = REPO / "ai-academy" / "courses.html"
COURSES_DATA = REPO / "ai-academy" / "modules" / "courses-data.json"


def slugify(name: str) -> str:
    s = name.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def next_dv_id(html: str) -> int:
    nums = [int(m) for m in re.findall(r'id="dv-(\d+)"', html)]
    return max(nums, default=0) + 1


def prompt(label: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    val = input(f"{label}{suffix}: ").strip()
    return val or default


def build_panel(dv: int, slug: str, name: str, desc: str, category: str,
                icon: str, n_mods: int, modules: list, total_dv: int) -> str:
    badges = f'<span class="core-badge-cs">Coming Soon</span>\n            <span class="core-badge-mods">{n_mods} Modules</span>'
    mod_rows = ""
    for m in modules:
        title = m["title"]
        sub = m.get("sub", "")
        sub_html = f'<div class="core-mod__sub">{sub}</div>' if sub else ""
        mod_rows += (
            f'          <div class="core-mod"><div class="core-mod__num">M{m["n"]}</div>'
            f'<div class="core-mod__info"><div class="core-mod__title">{title}</div>'
            f'{sub_html}</div></div>\n'
        )

    return f"""
      <div class="core-panel" id="dv-{dv}">
        <div class="core-panel__header">
          <span class="core-panel__icon">{icon}</span>
          <div class="core-panel__meta">
            <div class="core-panel__num">{category} · Course {dv} of {total_dv}</div>
            <div class="core-panel__title">{name}</div>
            <div class="core-panel__desc">{desc}</div>
          </div>
          <div class="core-panel__badges">
            {badges}
          </div>
        </div>
        <div class="core-modules-label">Course modules</div>
        <div class="core-modules-grid">
{mod_rows.rstrip()}
        </div>
      </div>
"""


def main():
    print("\n=== Aesop Coming Soon Course Builder ===\n")

    name = prompt("Course name")
    if not name:
        print("Course name is required.")
        sys.exit(1)

    slug = prompt("URL slug", slugify(name))
    desc = prompt("Short description (1-2 sentences)")
    category = prompt("Category", "Development")
    icon = prompt("Icon emoji", "📘")
    n_mods = int(prompt("Number of modules", "8"))

    print(f"\nEnter {n_mods} module titles (and optional subtitles).")
    print("Format: Title | Subtitle  (subtitle is optional)\n")

    modules = []
    for i in range(1, n_mods + 1):
        raw = input(f"  M{i}: ").strip()
        if "|" in raw:
            parts = raw.split("|", 1)
            modules.append({"n": i, "title": parts[0].strip(), "sub": parts[1].strip()})
        else:
            modules.append({"n": i, "title": raw})

    # --- courses.html ---
    html = COURSES_HTML.read_text(encoding="utf-8")
    dv = next_dv_id(html)
    total_dv = dv  # this course becomes the new max

    panel = build_panel(dv, slug, name, desc, category, icon, n_mods, modules, total_dv)

    # Insert before the closing </div> of the dev courses grid
    insert_marker = "    </div>"  # the closing tag after the last dv panel
    # Find last occurrence of the dv panel section closing
    last_dv = max(m.start() for m in re.finditer(r'id="dv-\d+"', html))
    close_pos = html.find("    </div>", last_dv)
    if close_pos == -1:
        print("ERROR: Could not find insertion point in courses.html")
        sys.exit(1)

    html = html[:close_pos] + panel + html[close_pos:]
    COURSES_HTML.write_text(html, encoding="utf-8")
    print(f"\n✓ Added panel dv-{dv} to courses.html")

    # --- courses-data.json ---
    raw = COURSES_DATA.read_text(encoding="utf-8-sig")
    data = json.loads(raw)
    data["courses"].append({
        "id": slug,
        "name": name,
        "icon": icon,
        "category": category,
        "panelId": f"dv-{dv}",
        "description": desc,
        "live": False,
        "modules": modules,
    })
    COURSES_DATA.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8"
    )
    print(f"✓ Added '{slug}' to courses-data.json")
    print(f"\nDone. Review dv-{dv} in courses.html, then tell ModGen to build it when ready.\n")


if __name__ == "__main__":
    main()
