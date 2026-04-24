#!/usr/bin/env python3
"""
build_registry.py — Generate course-registry.json from courses.html

courses.html is the single source of truth for all course data.
This script parses it and produces a clean registry that the electives hub consumes.

The registry includes lesson names extracted from the actual module HTML files on disk
for live courses.

Usage:
    python .github/scripts/build_registry.py

Reads:  ai-academy/courses.html
        ai-academy/modules/<course_folder>/*.html
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
MODULES_DIR = os.path.join(REPO_ROOT, "ai-academy", "modules")

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

        # Tighten the block: for live panels that have a proper closing </div>,
        # stop at the CTA link closing tag to avoid capturing content from
        # adjacent panels that follow without a new <div class="core-panel"...> tag.
        cta_end = re.search(r'</a>\s*\n\s*</div>', block)
        if cta_end:
            block = block[:cta_end.end()]

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

        # Extract modules — split on <div class="core-mod"> so each piece
        # contains one module's content. This avoids the subtitle-borrow
        # problem where a module without a subtitle steals the next one's.
        modules = []
        num_pat   = re.compile(r'core-mod__num[^>]*>(M\d+)</div>')
        title_pat = re.compile(r'core-mod__title[^>]*>(.*?)</div>')
        sub_pat   = re.compile(r'core-mod__sub[^>]*>(.*?)</div>')
        mod_pieces = re.split(r'<div\s+class="core-mod">', block)
        for piece in mod_pieces[1:]:  # skip content before first module
            num_m   = num_pat.search(piece)
            title_m = title_pat.search(piece)
            if not num_m or not title_m:
                continue
            mod_num   = num_m.group(1)
            mod_title = title_m.group(1).strip()
            sub_m     = sub_pat.search(piece)
            mod_sub   = sub_m.group(1).strip() if sub_m else ""
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
        folder = None
        url = None
        if c["course_id"]:
            # Live courses: folder is on disk, derive from actual modules
            folder = _resolve_folder(c["course_id"])
            url = f"/ai-academy/modules/{folder}/"

        # Build module list with IDs and extracted lessons
        # For live courses, use the prefix from _MODULE_ID_PREFIXES
        # For coming-soon courses, use panel_id-based prefix (doesn't matter much)
        if c["course_id"] and c["course_id"] in _MODULE_ID_PREFIXES:
            prefix = _MODULE_ID_PREFIXES[c["course_id"]]
        else:
            # Fallback: use first 3 chars of panel_id
            prefix = c["panel_id"].replace("-", "")[:3]

        modules = []
        for m in c["modules"]:
            mod_id = f"{prefix}-m{m['num']}"

            # Extract lessons from HTML if this is a live course
            lessons = []
            if c["is_live"] and folder:
                module_filename = f"{folder}-m{m['num']}.html"
                module_path = os.path.join(MODULES_DIR, folder, module_filename)
                lessons = _extract_lessons_from_module_html(module_path)

            modules.append({
                "id": mod_id,
                "title": m["title"],
                "subtitle": m.get("subtitle", ""),
                "lessons": lessons
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


# Map of course IDs to their module ID prefixes for live courses
_MODULE_ID_PREFIXES = {
    "governance": "gov",
    "society": "soc",
    "ethics": "eth",
    "building": "bld",
    "careers": "car",
    "ai-in-healthcare": "hlth",
    "ai-and-education": "edu",
    "ai-leadership": "lead",
    "building-ai-agents-i-use-cases": "ba1",
    "building-ai-agents-ii-skills": "ba2",
    "building-ai-agents-iii-tools": "ba3",
    "building-ai-agents-iv-openclaw": "ba4",
    "building-ai-agents-v-optimization": "ba5",
    "prompt-engineering-for-developers": "pro",
    "rag-systems-from-scratch": "rag",
    "ai-and-the-future-of-work": "fow",
    "ai-for-marketing-and-growth": "mkg",
    "ai-for-small-business-managers": "sbm",
    "ai-in-game-design-i": "gd1",
    "ai-psychology-and-behavior": "psy",
    "ai-risk-for-business-leaders": "rsk",
    "ai-tools-for-solo-founders": "tsf",
    "ai-security-and-red-teaming": "sec",
    "building-an-ai-first-business": "baf",
    "gpt-vs-claude-vs-gemini": "gcg",
    "photography-and-ai": "pho",
    "ai-and-creativity": "cre",
    "ai-and-national-security": "ans",
    "how-large-language-models-work": "llm",
    "whats-really-inside-ai": "wha",
    "ai-and-fake-information": "afk",
    "coded-unfair-ai-bias-exposed": "cui",
    "make-it-yours-creating-with-ai": "miy",
    "ai-and-climate": "clm",
    "ai-bias-and-fairness": "abf",
    "ai-careers-and-research": "acr",
    "ai-in-society": "ais",
    "building-with-ai": "bwa",
    "the-context-window-race": "cwr",
    "the-future-of-intelligence": "foi",
}

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


def _extract_lessons_from_module_html(module_path):
    """
    Extract lesson names from a module HTML file.

    Handles two formats:
    1. Standalone: <button class="sb-btn"><span class="sb-icon">EMOJI</span> Lesson Name</button>
    2. Injection: <div class="page" id="p-lN">...<h1>Lesson Name</h1>...

    Returns a list of lesson names in order (e.g., ["Lesson 1", "Lesson 2", ...])
    """
    try:
        with open(module_path, 'r', encoding='utf-8') as f:
            html = f.read()
    except Exception as e:
        print(f"  Warning: Could not read {module_path}: {e}", file=sys.stderr)
        return []

    lessons = {}

    # Try the standalone format first:
    # <button class="sb-btn[^"]*" id="sbi-lN" ...><span class="sb-icon">...</span> LESSON_NAME</button>
    # Match sb-btn but NOT sb-sub (which are Quiz/Lab buttons)
    standalone_pattern = re.compile(
        r'<button\s+class="sb-btn(?:\s|").*?\sid="[^-]*-l(\d+)".*?<span\s+class="sb-icon">[^<]*</span>\s*([^<]+)</button>',
        re.DOTALL
    )
    for m in standalone_pattern.finditer(html):
        lesson_num = int(m.group(1))
        lesson_name = m.group(2).strip()
        lessons[lesson_num] = lesson_name

    # If standalone found lessons, return them
    if lessons:
        sorted_lessons = [lessons[i] for i in sorted(lessons.keys())]
        return sorted_lessons

    # Try the injection format:
    # <div class="page[^"]*" id="p-lN">...<h1>LESSON_TITLE</h1>...
    injection_pattern = re.compile(
        r'<div\s+class="page[^"]*"\s+id="p-l(\d+)"[^>]*>.*?<h1[^>]*>([^<]+)</h1>',
        re.DOTALL
    )
    for m in injection_pattern.finditer(html):
        lesson_num = int(m.group(1))
        lesson_name = m.group(2).strip()
        lessons[lesson_num] = lesson_name

    if lessons:
        sorted_lessons = [lessons[i] for i in sorted(lessons.keys())]
        return sorted_lessons

    # If no lessons found, return empty list
    return []


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
