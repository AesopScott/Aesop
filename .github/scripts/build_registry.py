#!/usr/bin/env python3
"""
build_registry.py — Generate course-registry.json from courses.html

courses.html is the single source of truth for all course data.
This script parses it and produces a clean registry that the electives hub consumes.

Usage:
    python .github/scripts/build_registry.py

Reads:  ai-academy/courses.html
Writes: ai-academy/modules/course-registry.json
"""

import json
import os
import re
import sys
from html.parser import HTMLParser

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
COURSES_HTML = os.path.join(REPO_ROOT, "ai-academy", "courses.html")
REGISTRY_OUT = os.path.join(REPO_ROOT, "ai-academy", "modules", "course-registry.json")

# ── Accent colors assigned by category ──
# The hub needs accent/accentRgb for styling. courses.html doesn't carry these,
# so we assign them by category. New categories get a default.
CATEGORY_ACCENTS = {
    "AI Models":    ("#6366f1", "99,102,241"),
    "AI Progress":  ("#8b5cf6", "139,92,246"),
    "Art":          ("#9333ea", "147,51,234"),
    "Business":     ("#d97706", "217,119,6"),
    "Development":  ("#059669", "5,150,105"),
    "Education":    ("#6366f1", "99,102,241"),
    "Engineering":  ("#ca8a04", "202,138,4"),
    "Ethics":       ("#e84545", "232,69,69"),
    "Health":       ("#e05a9c", "224,90,156"),
    "Law":          ("#4a90d9", "74,144,217"),
    "Safety":       ("#dc2626", "220,38,38"),
    "Science":      ("#0891b2", "8,145,178"),
}
DEFAULT_ACCENT = ("#64748b", "100,116,139")


def parse_courses_html(path):
    """Parse courses.html and return a list of course dicts."""
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    courses = []

    # ── Step 1: Parse sidebar tabs to build panel_id -> metadata map ──
    # <button class="core-tab ..." data-panel="am-1" data-cat="AI Models" data-type="Core" onclick="...">Title <span>Soon</span></button>
    tab_pattern = re.compile(
        r'<button\s+class="core-tab[^"]*"\s+'
        r'data-panel="([^"]+)"\s+'
        r'data-cat="([^"]+)"\s+'
        r'data-type="([^"]+)"\s+'
        r'onclick="[^"]*">'
        r'(.*?)</button>',
        re.DOTALL
    )
    tab_meta = {}  # panel_id -> {cat, type, is_coming}
    for m in tab_pattern.finditer(html):
        panel_id = m.group(1)
        cat = m.group(2)
        ctype = m.group(3)
        inner = m.group(4)
        is_coming = "coming" in m.group(0).split(">")[0]  # check class
        tab_meta[panel_id] = {"cat": cat, "type": ctype, "is_coming": is_coming}

    # ── Also handle the original 18 core course tabs (cp1..cp18) ──
    # These use a different format — they have data-panel="cpN" in the tab
    core_tab_pattern = re.compile(
        r'<button\s+class="core-tab([^"]*?)"\s+'
        r'data-panel="(cp\d+)"[^>]*>'
        r'(.*?)</button>',
        re.DOTALL
    )
    for m in core_tab_pattern.finditer(html):
        classes = m.group(1)
        panel_id = m.group(2)
        is_coming = "coming" in classes
        # For these, we'll derive category from the panel content later
        tab_meta[panel_id] = {"cat": "", "type": "Core", "is_coming": is_coming}

    # ── Step 2: Parse each panel div ──
    # Find all <div class="core-panel..." id="XXX"> blocks
    panel_pattern = re.compile(
        r'<div\s+class="core-panel[^"]*"\s+id="([^"]+)">(.*?)</div>\s*(?=<div\s+class="core-panel|</div>\s*</div>\s*</section)',
        re.DOTALL
    )

    # More reliable: find panels by splitting on panel opening tags
    panel_starts = [(m.start(), m.group(1)) for m in re.finditer(r'<div\s+class="core-panel[^"]*"\s+id="([^"]+)">', html)]

    for idx, (start, panel_id) in enumerate(panel_starts):
        # Get content until next panel or section end
        end = panel_starts[idx + 1][0] if idx + 1 < len(panel_starts) else len(html)
        block = html[start:end]

        # Extract icon
        icon_m = re.search(r'core-panel__icon[^>]*>(.*?)</span>', block)
        icon = icon_m.group(1).strip() if icon_m else ""

        # Extract course number
        num_m = re.search(r'core-panel__num[^>]*>(.*?)</div>', block)
        course_num = num_m.group(1).strip() if num_m else ""

        # Extract title
        title_m = re.search(r'core-panel__title[^>]*>(.*?)</div>', block)
        title = title_m.group(1).strip() if title_m else ""

        # Extract description
        desc_m = re.search(r'core-panel__desc[^>]*>(.*?)</div>', block, re.DOTALL)
        desc = desc_m.group(1).strip() if desc_m else ""
        desc = re.sub(r'\s+', ' ', desc)  # normalize whitespace

        # Extract module count
        mods_m = re.search(r'core-badge-mods[^>]*>(\d+)\s*Modules', block)
        mod_count = int(mods_m.group(1)) if mods_m else 0

        # Check status
        is_live = 'core-badge-live' in block
        is_coming = 'core-badge-cs' in block
        has_link = 'electives-hub.html?course=' in block

        # Extract hub course ID from link (if live)
        course_id = None
        folder_name = None
        if has_link:
            link_m = re.search(r'electives-hub\.html\?course=([^"&]+)', block)
            if link_m:
                course_id = link_m.group(1)

        # Extract modules
        modules = []
        mod_pattern = re.compile(
            r'core-mod__num[^>]*>(M\d+)</div>.*?'
            r'core-mod__title[^>]*>(.*?)</div>.*?'
            r'core-mod__sub[^>]*>(.*?)</div>',
            re.DOTALL
        )
        for mm in mod_pattern.finditer(block):
            mod_num = mm.group(1)  # M1, M2, etc.
            mod_title = mm.group(2).strip()
            mod_sub = mm.group(3).strip()
            modules.append({
                "num": int(mod_num[1:]),
                "title": mod_title,
                "subtitle": mod_sub
            })

        # Get category from tab metadata
        meta = tab_meta.get(panel_id, {})
        category = meta.get("cat", "")

        # If no category from tab (core courses), try to derive from course_num
        if not category and course_num:
            # "Core Course 1 of 18" -> try to find in sidebar
            for pid, m in tab_meta.items():
                if pid == panel_id:
                    category = m.get("cat", "")
                    break

        courses.append({
            "panel_id": panel_id,
            "title": title,
            "icon": icon,
            "desc": desc,
            "course_num": course_num,
            "category": category,
            "type": meta.get("type", "Core"),
            "mod_count": mod_count,
            "modules": modules,
            "is_live": is_live,
            "is_coming": is_coming,
            "course_id": course_id,  # None if not yet active
        })

    return courses


def build_registry(courses):
    """Convert parsed courses into the registry format the hub expects."""
    registry = {}

    for c in courses:
        # Use existing course_id for live courses, panel_id as fallback
        cid = c["course_id"] or c["panel_id"]

        # Determine accent color
        accent, accent_rgb = CATEGORY_ACCENTS.get(c["category"], DEFAULT_ACCENT)

        # Build URL — for live courses we know the folder; for others, derive from course_id
        if c["course_id"]:
            # Live courses: folder is on disk, derive from actual modules
            folder = _resolve_folder(c["course_id"])
            url = f"/ai-academy/modules/{folder}/"
        else:
            # Not yet active — no URL
            url = None

        # Build module list with IDs
        # The hub needs module IDs like "gov-m1". We use a short prefix from the panel_id.
        prefix = c["panel_id"].replace("-", "")[:3]
        modules = []
        for m in c["modules"]:
            mod_id = f"{prefix}-m{m['num']}"
            modules.append({
                "id": mod_id,
                "title": m["title"],
                "subtitle": m.get("subtitle", ""),
                "lessons": []  # Lesson titles aren't in courses.html — populated by generator
            })

        entry = {
            "id": cid,
            "title": c["title"],
            "icon": c["icon"],
            "sub": c["course_num"] or c["category"],
            "accent": accent,
            "accentRgb": accent_rgb,
            "pts": 2 if c["mod_count"] >= 8 else 1,
            "days": 2 if c["mod_count"] >= 8 else 1,
            "desc": c["desc"],
            "category": c["category"],
            "type": c["type"],
            "status": "live" if c["is_live"] else "coming-soon",
            "modCount": c["mod_count"],
            "modules": modules,
        }
        if url:
            entry["url"] = url

        registry[cid] = entry

    return registry


# Map of course IDs whose folder name doesn't match the ID
_FOLDER_OVERRIDES = {
    "governance": "ai-governance",
    "society": "ai-in-society",
    "ethics": "ai-ethics",
    "building": "building-with-ai",
    "creativity": "ai-and-creativity",
    "careers": "ai-careers",
}

def _resolve_folder(course_id):
    """Resolve a course ID to its folder name on disk."""
    if course_id in _FOLDER_OVERRIDES:
        return _FOLDER_OVERRIDES[course_id]
    return course_id


def main():
    if not os.path.exists(COURSES_HTML):
        print(f"ERROR: {COURSES_HTML} not found", file=sys.stderr)
        sys.exit(1)

    courses = parse_courses_html(COURSES_HTML)
    print(f"Parsed {len(courses)} courses from courses.html")

    live = [c for c in courses if c["is_live"]]
    coming = [c for c in courses if c["is_coming"]]
    print(f"  Live: {len(live)}, Coming Soon: {len(coming)}")

    registry = build_registry(courses)

    with open(REGISTRY_OUT, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)

    print(f"Wrote {len(registry)} entries to {REGISTRY_OUT}")


if __name__ == "__main__":
    main()
