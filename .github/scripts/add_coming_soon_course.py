#!/usr/bin/env python3
"""
add_coming_soon_course.py — Add a Coming Soon course panel to courses.html
and a stub entry to courses-data.json, ready for ModGen.

Usage:
    python .github/scripts/add_coming_soon_course.py

You will be prompted for:
  - Course name
  - Short description (1-2 sentences)
  - Category  (Development / Core / Elective / etc.)
  - Icon emoji
  - Number of modules (default 8)
  - Module titles and subtitles (one per line, or press Enter to skip subtitles)

The script assigns the next available dv-XX panel ID automatically and
inserts a Coming Soon entry into the correct mega-menu section.
"""

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
COURSES_HTML = REPO / "ai-academy" / "courses.html"
COURSES_DATA = REPO / "ai-academy" / "modules" / "courses-data.json"

# Maps the category prompt value to the mega-cat label text in courses.html
CATEGORY_TO_MEGA_CAT = {
    "development": "⚙️ Development",
    "core":        "📚 Core Courses",
    "art":         "🎨 Art",
    "business":    "💼 Business",
    "models":      "📡 AI Models",
    "progress":    "🔭 AI Progress",
    "start here":  "🤖 Start Here",
}


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
    """Build the HTML for a Coming Soon course panel.

    Fixes vs. old version:
      1. Uses core-panel--cs class so the panel is visually faded/grayed.
      2. Includes the ghost CTA so clicking the panel shows a 'Coming Soon'
         button instead of a blank action area.
    """
    badges = (
        f'<span class="core-badge-cs">Coming Soon</span>\n'
        f'            <span class="core-badge-mods">{n_mods} Modules</span>'
    )
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

    # FIX 1: core-panel--cs added to div class
    # FIX 2: ghost CTA added after modules grid
    return f"""
      <div class="core-panel core-panel--cs" id="dv-{dv}">
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
        <span class="core-panel__cta core-panel__cta--ghost">Coming Soon</span>
      </div>
"""


def insert_mega_menu_entry(html: str, dv: int, name: str, category: str) -> str:
    """Insert a mega-link--soon button into the correct mega-menu section,
    in alphabetical order among existing buttons in that section.

    FIX 3: the old script never added a mega-menu entry, leaving new courses
    invisible in the dropdown navigation.
    """
    cat_key = category.lower()
    mega_cat_label = CATEGORY_TO_MEGA_CAT.get(cat_key)

    if not mega_cat_label:
        print(f"  ⚠  No mega-menu section mapped for category '{category}'. "
              f"Add the entry manually under the correct <div class=\"mega-cat\">.")
        return html

    # Find the position of the mega-cat header for this category
    cat_marker = f'<div class="mega-cat">{mega_cat_label}</div>'
    cat_pos = html.find(cat_marker)
    if cat_pos == -1:
        print(f"  ⚠  Could not find mega-cat '{mega_cat_label}' in courses.html. "
              f"Add the mega-menu entry manually.")
        return html

    # Find the end of this section (next mega-cat or end of mega-menu)
    next_cat_pos = html.find('<div class="mega-cat">', cat_pos + len(cat_marker))
    section_end = next_cat_pos if next_cat_pos != -1 else html.find('</div>', cat_pos + len(cat_marker))

    section = html[cat_pos:section_end]

    # Collect existing buttons and their positions in the section
    btn_pat = re.compile(r'        <button class="mega-link[^"]*"[^>]*>([^<]+)</button>')
    buttons = list(btn_pat.finditer(section))

    new_btn = (
        f'        <button class="mega-link mega-link--soon" '
        f'data-panel="dv-{dv}" onclick="megaSelect(this,\'dv-{dv}\')">'
        f'{name}</button>'
    )

    # Find insertion point: first existing button whose label sorts after name
    insert_offset = None
    for btn in buttons:
        if btn.group(1).lower() > name.lower():
            insert_offset = btn.start()
            break

    if insert_offset is None:
        # Append after the last button in the section
        if buttons:
            last = buttons[-1]
            insert_offset = last.end() + 1  # after the newline
        else:
            # No buttons yet — insert right after the mega-cat header
            insert_offset = len(cat_marker)

    # Translate offset from section-relative to full-html absolute
    abs_insert = cat_pos + insert_offset
    html = html[:abs_insert] + new_btn + "\n" + html[abs_insert:]

    return html


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

    # Insert panel before the closing </div> of the dv panel section
    last_dv = max(m.start() for m in re.finditer(r'id="dv-\d+"', html))
    close_pos = html.find("    </div>", last_dv)
    if close_pos == -1:
        print("ERROR: Could not find insertion point in courses.html")
        sys.exit(1)

    html = html[:close_pos] + panel + html[close_pos:]

    # FIX 3: Add mega-menu entry
    html = insert_mega_menu_entry(html, dv, name, category)

    COURSES_HTML.write_text(html, encoding="utf-8")
    print(f"\n✓ Added panel dv-{dv} to courses.html")
    print(f"✓ Added mega-menu entry for dv-{dv} under '{category}'")

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
