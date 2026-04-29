#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
move_youth_buttons_to_new_sections.py — One-shot rearrangement of
existing Youth mega-menu buttons.

After the 6-category Youth expansion, 16 buttons in courses.html still
live under the old (How AI Works / Make & Create / Truth & Safety)
section headers, even though their drafts now declare different
mega_group values (AI Toolbox, AI in School, Code with AI). The
autopatch script only INSERTS new buttons — it doesn't move existing
ones — so the new section headers stay empty until we physically
relocate the buttons.

This script:
  1. Reads each K-12 draft and notes its current mega_group.
  2. For each draft, locates the matching button in courses.html
     (by data-course=<slug> if present, falling back to button text).
  3. If the button is currently inside a different mega-group than
     its mega_group implies, splice it out of the old group and
     append it to the correct one.

Idempotent. Safe to re-run.
"""

import re
import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO = Path(__file__).resolve().parent.parent

COURSES_HTML = REPO / "ai-academy" / "courses.html"
K12_DRAFTS   = REPO / "aip" / "k12-drafts"

# The text of each Youth section's mega-cat header. Keep in lock-step
# with aip_autopatch.py CAT_MARKERS and the courses.html sources.
GROUP_HEADER = {
    "How AI Works":   '<div class="mega-cat">🧠 How AI Works</div>',
    "Make & Create":  '<div class="mega-cat">✏️ Make &amp; Create</div>',
    "Truth & Safety": '<div class="mega-cat">🛡️ Truth &amp; Safety</div>',
    "AI Toolbox":     '<div class="mega-cat">🛠️ AI Toolbox</div>',
    "AI in School":   '<div class="mega-cat">🎓 AI in School</div>',
    "Code with AI":   '<div class="mega-cat">💻 Code with AI</div>',
}


def load_target_megagroup_by_slug() -> dict[str, str]:
    """Return {slug: mega_group} for every K-12 draft that has a valid
    mega_group set."""
    out = {}
    for f in sorted(K12_DRAFTS.glob("*.json")):
        if f.name == "index.json":
            continue
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(d, dict):
            continue
        slug = d.get("id")
        mg   = d.get("mega_group")
        if slug and mg in GROUP_HEADER:
            out[slug] = mg
    return out


def find_button(html: str, slug: str) -> tuple[int, int, str] | None:
    """Locate the button line for this slug. Returns (start, end, full
    button-line text including trailing newline) or None if not found."""
    pat = re.compile(
        rf'^[ \t]*<button[^>]*data-course="{re.escape(slug)}"[^>]*>[^<]+</button>\n',
        re.MULTILINE,
    )
    m = pat.search(html)
    if not m:
        return None
    return (m.start(), m.end(), m.group(0))


def find_group_block(html: str, header: str) -> tuple[int, int] | None:
    """Find the start of a mega-group block beginning with the given header,
    and the position right before the </div> that closes it. The autopatch
    in aip_autopatch.py uses the same insertion strategy: insert before the
    closing </div> of the mega-group."""
    h_pos = html.find(header)
    if h_pos == -1:
        return None
    # Search backwards for the enclosing <div class="mega-group">
    open_pos = html.rfind('<div class="mega-group">', 0, h_pos)
    if open_pos == -1:
        return None
    # Find the matching closing </div>. mega-group contains exactly one
    # mega-cat plus a flat list of buttons — no nested divs — so the
    # next '</div>' after the header is the closer.
    close_pos = html.find('</div>', h_pos + len(header))
    if close_pos == -1:
        return None
    return (open_pos, close_pos)


def current_group_for(html: str, btn_start: int) -> str | None:
    """Walk back from btn_start to the most recent mega-cat header line
    and return the matching key in GROUP_HEADER, or None."""
    snippet = html[:btn_start]
    last_cat = snippet.rfind('<div class="mega-cat">')
    if last_cat == -1:
        return None
    line_end = snippet.find('</div>', last_cat) + len('</div>')
    header = snippet[last_cat:line_end]
    for key, expected in GROUP_HEADER.items():
        if expected == header:
            return key
    return None


def main() -> int:
    targets = load_target_megagroup_by_slug()
    print(f"K-12 drafts with a valid mega_group: {len(targets)}")
    if not targets:
        print("Nothing to do.")
        return 0

    html = COURSES_HTML.read_text(encoding="utf-8")
    moved = 0
    skipped_already = 0
    skipped_not_found = []
    for slug, target_group in targets.items():
        loc = find_button(html, slug)
        if not loc:
            skipped_not_found.append(slug)
            continue
        btn_start, btn_end, btn_line = loc
        cur = current_group_for(html, btn_start)
        if cur == target_group:
            skipped_already += 1
            continue

        # Splice button out
        new_html = html[:btn_start] + html[btn_end:]

        # Find target group in the modified html (positions shift after splice)
        target_block = find_group_block(new_html, GROUP_HEADER[target_group])
        if not target_block:
            print(f"  WARN: target group {target_group!r} header not found, skipping {slug}")
            continue
        _open_pos, close_pos = target_block

        # Insert button right before the </div> of the target group
        # Make sure there's a newline before the close so the insertion
        # is visually clean.
        # Use indent matching other buttons (10 spaces is the convention
        # in this file's youth-groups-row).
        indented_btn = btn_line.lstrip()
        if not indented_btn.endswith("\n"):
            indented_btn += "\n"
        indented_btn = "          " + indented_btn   # 10-space indent
        new_html = (
            new_html[:close_pos]
            + indented_btn
            + new_html[close_pos:]
        )
        html = new_html
        moved += 1
        print(f"  {slug}: {cur!r} → {target_group!r}")

    if moved:
        COURSES_HTML.write_text(html, encoding="utf-8")
        print()
        print(f"Moved {moved} button(s).")
    else:
        print()
        print("All buttons already in the correct sections.")

    print(f"Already in place: {skipped_already}")
    if skipped_not_found:
        print(f"Buttons not found in courses.html: {len(skipped_not_found)}")
        for s in skipped_not_found:
            print(f"  - {s}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
