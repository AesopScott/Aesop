#!/usr/bin/env python3
"""
AIP Auto-Patch — adds approved AIP drafts to courses.html

Reads all JSON files in aip/drafts/, finds approved ones not yet in
courses.html, and injects:
  1. A sidebar tab button (Coming Soon) in the Core Courses group
  2. A course panel with title, synopsis, and module list

Panels use id="aip-{draft_id}" to avoid clashing with existing IDs.
Tab buttons are inserted alphabetically within the Core Courses group.
"""

import json
import os
import re
import sys
from pathlib import Path

DRAFTS_DIR = Path("aip/drafts")
COURSES_HTML = Path("ai-academy/courses.html")

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
    """Check if a draft's panel ID already exists in courses.html."""
    panel_id = f'id="aip-{draft_id}"'
    return panel_id in html


def build_tab_button(draft):
    """Build a sidebar tab button for a draft (Coming Soon)."""
    draft_id = draft["id"]
    title = draft["title"]
    panel_id = f"aip-{draft_id}"
    return (
        f'        <button class="core-tab coming" data-panel="{panel_id}" '
        f'data-cat="Core Courses" data-type="Core" '
        f'onclick="openTab(this,\'{panel_id}\')">'
        f'{title} <span class="tab-cs-badge">Soon</span></button>'
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

    return f"""      <div class="core-panel core-panel--cs" id="{panel_id}">
        <div class="core-panel__header">
          <span class="core-panel__icon">{icon}</span>
          <div class="core-panel__meta">
            <div class="core-panel__num">AIP Draft</div>
            <div class="core-panel__title">{title}</div>
            <div class="core-panel__desc">{synopsis}</div>
          </div>
          <div class="core-panel__badges">
            <span class="core-badge-cs">Coming Soon</span>
            <span class="core-badge-mods">{num_modules} Modules</span>
          </div>
        </div>
        <div class="core-modules-label">Proposed modules</div>
        <div class="core-modules-grid">{module_html}
        </div>
        <span class="core-panel__cta core-panel__cta--ghost">In Development</span>
      </div>"""


def insert_tab_button(html, tab_html, draft_title):
    """Insert tab button alphabetically into the Core Courses sidebar group."""
    # Find the Core Courses group
    marker = '<div class="core-sidebar-cat">📚 Core Courses</div>'
    marker_pos = html.find(marker)
    if marker_pos == -1:
        print("  ERROR: Could not find Core Courses sidebar group")
        return html

    # Find the closing </div> of the sidebar group after this marker
    # We need to find where buttons end — look for the next </div> that closes the group
    # The group ends with </div>\n    </nav> or the next <div class="core-sidebar-group">
    group_end = html.find("</div>\n    </nav>", marker_pos)
    if group_end == -1:
        group_end = html.find("    </nav>", marker_pos)

    # Extract just the buttons section
    buttons_start = marker_pos + len(marker) + 1  # +1 for newline
    buttons_section = html[buttons_start:group_end]

    # Parse existing button titles to find alphabetical position
    existing_buttons = re.findall(
        r'(<button class="core-tab[^"]*"[^>]*>)([^<]+)',
        buttons_section
    )

    # Find insertion point — after the last button whose title comes before ours
    insert_after_pos = buttons_start  # default: after the category header
    for match in re.finditer(
        r'<button class="core-tab[^"]*"[^>]*>[^<]+(?:<[^>]+>[^<]*</[^>]+>)?</button>',
        buttons_section
    ):
        # Extract the visible text (title) from the button
        btn_text = re.sub(r'<[^>]+>', '', match.group()).strip()
        if btn_text.lower() <= draft_title.lower():
            insert_after_pos = buttons_start + match.end()

    # Insert the new button
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

    new_count = 0
    for i, draft in enumerate(drafts):
        draft_id = draft["id"]
        title = draft["title"]

        if draft_already_in_html(html, draft_id):
            print(f"  ✓ Already in courses.html: {title}")
            continue

        print(f"  + Adding: {title}")

        # Build HTML fragments
        tab_btn = build_tab_button(draft)
        panel = build_course_panel(draft, i)

        # Insert into courses.html
        html = insert_tab_button(html, tab_btn, title)
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
        print("\nNo new courses to add.")


if __name__ == "__main__":
    main()
