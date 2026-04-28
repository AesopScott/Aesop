#!/usr/bin/env python3
"""
AIP Auto-Patch — adds approved AIP drafts to courses.html and courses-data.json

Reads all JSON files in aip/drafts/ (or --drafts-dir), finds approved ones not
yet in courses.html, and injects:
  1. A sidebar tab button (Coming Soon) in the appropriate group
  2. A course panel with title, synopsis, and module list

Also syncs approved drafts into courses-data.json so they appear in the
module generator dropdown with proper {n, title, sub} module objects.

Panels use id="aip-{draft_id}" to avoid clashing with existing IDs.
Tab buttons are inserted alphabetically within the target sidebar group.

Usage:
    python aip_autopatch.py                            # general drafts
    python aip_autopatch.py --drafts-dir aip/k12-drafts --category Youth
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

COURSES_HTML = Path("ai-academy/courses.html")
COURSES_DATA = Path("ai-academy/modules/courses-data.json")

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--drafts-dir", default="aip/drafts",
                        help="Directory containing draft JSON files (default: aip/drafts)")
    parser.add_argument("--category", default="Core Courses",
                        help="Sidebar group label to insert tab buttons into (default: Core Courses)")
    return parser.parse_args()

args = parse_args()
DRAFTS_DIR = Path(args.drafts_dir)
TARGET_CATEGORY = args.category  # e.g. "Core Courses" or "Youth"

# Icons to cycle through for AIP courses
ICONS = ["🧠", "🔬", "🌐", "⚡", "🔮", "📊", "🛡️", "🎯", "💡", "🚀"]


def load_approved_drafts():
    """Load all approved draft JSONs."""
    drafts = []
    for f in sorted(DRAFTS_DIR.glob("*.json")):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            # Skip non-dict files (e.g. index.json is a list of filenames)
            if not isinstance(data, dict):
                continue
            if data.get("status") == "approved":
                drafts.append(data)
        except (json.JSONDecodeError, KeyError) as e:
            print(f"  Skipping {f.name}: {e}")
    return drafts


def draft_already_in_html(html, draft_id):
    """Check if a draft is already represented in courses.html.

    Checks three patterns to prevent duplicates:
    - id="aip-{draft_id}"         new-style panel div
    - data-panel="aip-{draft_id}" nav button (catches nav-only duplicates)
    - data-course="{draft_id}"    live course already has a full panel
    """
    return (
        f'id="aip-{draft_id}"' in html
        or f'data-panel="aip-{draft_id}"' in html
        or f'data-course="{draft_id}"' in html
    )


def build_tab_button(draft):
    """Build a mega-menu button for a draft (Coming Soon).

    Appends the module count in parentheses so the button label matches
    the convention used across the rest of the course selector, e.g.
    "Real or Generated: You Decide (6)".
    """
    draft_id = draft["id"]
    title = draft["title"]
    num_modules = len(draft.get("modules", []))
    label = f"{title} ({num_modules})" if num_modules else title
    panel_id = f"aip-{draft_id}"
    return (
        f'        <button class="mega-link mega-link--soon" '
        f'data-panel="{panel_id}" onclick="megaSelect(this,\'{panel_id}\')">'
        f'{label}</button>'
    )


def build_course_panel(draft, index):
    """Build a full course panel for an approved draft."""
    draft_id = draft["id"]
    title = draft["title"]
    synopsis = draft["synopsis"]
    modules = draft.get("modules", [])
    panel_id = f"aip-{draft_id}"
    icon = ICONS[index % len(ICONS)]
    num_modules = len(modules)

    # Build module grid
    module_html = ""
    for i, mod_title in enumerate(modules, 1):
        module_html += f"""
          <div class="core-mod">
            <div class="core-mod__num">M{i}</div>
            <div class="core-mod__info">
              <div class="core-mod__title">{mod_title}</div>
            </div>
          </div>"""

    audience = draft.get("audience", "")
    category = draft.get("category", "")
    age_range = draft.get("age_range", "")

    if audience == "youth" or category == "Youth":
        panel_num = f"Youth · Ages {age_range}" if age_range else "Youth"
        age_badge = f'<span class="core-badge-age">Ages {age_range}</span>\n            ' if age_range else ""
    elif audience == "young-adult" or category == "Young Adult":
        panel_num = f"Young Adult · Ages {age_range}" if age_range else "Young Adult"
        age_badge = f'<span class="core-badge-age">Ages {age_range}</span>\n            ' if age_range else ""
    elif audience == "professional" or category == "Professional":
        panel_num = "Professional"
        age_badge = ""
    else:
        panel_num = "AIP Draft"
        age_badge = ""

    return f"""      <div class="core-panel core-panel--cs" id="{panel_id}">
        <div class="core-panel__header">
          <span class="core-panel__icon">{icon}</span>
          <div class="core-panel__meta">
            <div class="core-panel__num">{panel_num}</div>
            <div class="core-panel__title">{title}</div>
            <div class="core-panel__desc">{synopsis}</div>
          </div>
          <div class="core-panel__badges">
            {age_badge}<span class="core-badge-cs">Coming Soon</span>
            <span class="core-badge-mods">{num_modules} Modules</span>
          </div>
        </div>
        <div class="core-modules-label">Proposed modules</div>
        <div class="core-modules-grid">{module_html}
        </div>
        <span class="core-panel__cta core-panel__cta--ghost">In Development</span>
      </div>"""


def insert_tab_button(html, tab_html, draft_title, target_group=None):
    """Insert mega-menu button alphabetically into the target mega-group.

    target_group overrides TARGET_CATEGORY when the draft supplies a
    ``mega_group`` field (e.g. "How AI Works", "Truth & Safety").
    Falls back to TARGET_CATEGORY if target_group is None or empty.
    """
    CAT_MARKERS = {
        # Age-tier defaults (one staging group per tier)
        "Youth":           '<div class="mega-cat">🧠 How AI Works</div>',
        "Young Adult":     '<div class="mega-cat">🛠️ AI Tools &amp; Apps</div>',
        "Professional":    '<div class="mega-cat">📋 Strategy &amp; Org</div>',
        # Youth sub-categories
        "How AI Works":    '<div class="mega-cat">🧠 How AI Works</div>',
        "Make & Create":   '<div class="mega-cat">✏️ Make &amp; Create</div>',
        "Truth & Safety":  '<div class="mega-cat">🛡️ Truth &amp; Safety</div>',
        # Sub-category aliases — use these in draft JSON "mega_group" field for
        # precise placement without having to edit courses.html manually
        "Strategy":        '<div class="mega-cat">📋 Strategy &amp; Org</div>',
        "AI Models":       '<div class="mega-cat">📡 AI Models &amp; Research</div>',
        "AI Frontier":     '<div class="mega-cat">🔭 AI Frontier</div>',
        "Development":     '<div class="mega-cat">⚙️ Development</div>',
        "Art":             '<div class="mega-cat">🎨 Art &amp; Creativity</div>',
        "Society":         '<div class="mega-cat">🌐 Society &amp; Domain</div>',
        "Applied":         '<div class="mega-cat">🚀 Applied Foundations</div>',
        "Business":        '<div class="mega-cat">💡 Business Essentials</div>',
        "Cybersecurity":   '<div class="mega-cat">🔒 Cybersecurity</div>',
        "AI Tools":        '<div class="mega-cat">🛠️ AI Tools &amp; Apps</div>',
        # Legacy alias
        "Core Courses":    '<div class="mega-cat">📋 Strategy &amp; Org</div>',
    }
    resolved = target_group or TARGET_CATEGORY
    marker = CAT_MARKERS.get(resolved, f'<div class="mega-cat">{resolved}</div>')
    marker_pos = html.find(marker)
    if marker_pos == -1:
        print(f"  ERROR: Could not find '{resolved}' mega-group in courses.html")
        return html

    # Group ends at the closing </div> before the next mega-group or mega-panel close
    next_group = html.find('<div class="mega-group">', marker_pos + len(marker))
    group_end = html.find("      </div>", marker_pos + len(marker))
    if next_group != -1 and next_group < group_end:
        group_end = html.rfind("      </div>", marker_pos, next_group)

    buttons_start = marker_pos + len(marker)
    buttons_section = html[buttons_start:group_end]

    # Find alphabetical insertion point among existing mega-link buttons
    insert_after_pos = buttons_start
    for match in re.finditer(r'<button class="mega-link[^"]*"[^>]*>([^<]+)</button>',
                              buttons_section):
        btn_text = match.group(1).strip()
        if btn_text.lower() <= draft_title.lower():
            insert_after_pos = buttons_start + match.end()

    html = html[:insert_after_pos] + "\n" + tab_html + html[insert_after_pos:]
    return html


def insert_course_panel(html, panel_html):
    """Insert course panel before the closing </div><!-- /.core-tab-content --> marker."""
    # Anchor to the explicit closing comment — this is far more reliable than
    # counting nested </div> tags, and immune to new panels or sections being added.
    CLOSE_MARKER = "</div><!-- /.core-tab-content -->"
    close_pos = html.find(CLOSE_MARKER)
    if close_pos == -1:
        # Fallback: try without the comment (older file format)
        marker = '<div class="core-tab-content">'
        content_start = html.find(marker)
        if content_start == -1:
            print("  ERROR: Could not find core-tab-content close marker")
            return html
        section_end = html.find("</section>", content_start)
        if section_end == -1:
            print("  ERROR: Could not find closing </section>")
            return html
        close_pos = html.rfind("</div>", content_start, section_end)
        if close_pos == -1:
            html = html[:section_end] + panel_html + "\n" + html[section_end:]
            return html

    html = html[:close_pos] + panel_html + "\n" + html[close_pos:]
    return html


def sync_to_courses_data(drafts):
    """Add approved drafts to courses-data.json with proper module format."""
    if not COURSES_DATA.exists():
        print("  courses-data.json not found — skipping mod-gen sync.")
        return 0

    data = json.loads(COURSES_DATA.read_text(encoding="utf-8"))
    existing_ids = {c["id"] for c in data.get("courses", [])}

    added = 0
    for draft in drafts:
        draft_id = draft["id"]
        if draft_id in existing_ids:
            continue

        raw_modules = draft.get("modules", [])
        modules = [
            {"n": i + 1, "title": m if isinstance(m, str) else m.get("title", ""), "sub": ""}
            for i, m in enumerate(raw_modules)
        ]

        # Derive ageGroup from audience or category fields in the draft
        audience = draft.get("audience", "")
        category = draft.get("category", "")
        if audience == "youth" or category == "Youth":
            age_group = "youth"
        elif audience in ("young-adult", "young_adult") or category == "Young Adult":
            age_group = "young_adult"
        else:
            age_group = "professional"  # default for all pro/unspecified drafts

        entry = {
            "id": draft_id,
            "name": draft["title"],
            "ageGroup": age_group,
            "live": False,
            "modules": modules,
        }
        if draft.get("category"):
            entry["category"] = draft["category"]
        if draft.get("tier"):
            entry["tier"] = draft["tier"]
        data.setdefault("courses", []).append(entry)
        existing_ids.add(draft_id)
        print(f"  + courses-data.json: {draft['title']} ({len(modules)} modules)")
        added += 1

    if added:
        COURSES_DATA.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"  ✅ courses-data.json updated with {added} new course(s)")
    else:
        print("  ✓ courses-data.json already up to date")

    return added


def main():
    if not DRAFTS_DIR.exists():
        print("No drafts directory found. Exiting.")
        return

    if not COURSES_HTML.exists():
        print("courses.html not found. Exiting.")
        sys.exit(1)

    html = COURSES_HTML.read_text(encoding="utf-8")
    drafts = load_approved_drafts()

    if not drafts:
        print("No approved drafts found. Nothing to patch.")
        return

    print(f"Found {len(drafts)} approved draft(s)")

    # ── Sync to courses-data.json (mod gen) ──────────────────────────────
    print("\n── Syncing to courses-data.json ──")
    sync_to_courses_data(drafts)

    # ── Patch courses.html ────────────────────────────────────────────────
    print("\n── Patching courses.html ──")
    new_count = 0
    for i, draft in enumerate(drafts):
        draft_id = draft["id"]
        title = draft["title"]

        if draft_already_in_html(html, draft_id):
            print(f"  ✓ Already in courses.html: {title}")
            continue

        print(f"  + Adding: {title}")

        tab_btn = build_tab_button(draft)
        panel = build_course_panel(draft, i)

        mega_group = draft.get("mega_group") or None
        html = insert_tab_button(html, tab_btn, title, target_group=mega_group)
        html = insert_course_panel(html, panel)
        new_count += 1

    if new_count > 0:
        # Safety check: never write a file that lost its closing tags
        if not html.rstrip().endswith("</html>"):
            print("\n❌ ABORT: patched HTML does not end with </html> — file NOT written to prevent truncation.")
            sys.exit(1)
        COURSES_HTML.write_text(html, encoding="utf-8")
        print(f"\n✅ Patched courses.html with {new_count} new course(s)")
    else:
        print("\nNo new courses to add to courses.html.")


if __name__ == "__main__":
    main()
