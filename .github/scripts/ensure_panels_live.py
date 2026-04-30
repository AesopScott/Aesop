#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ensure_panels_live.py — Make every disk-built course's panel actually
look live in ai-academy/courses.html.

Background: there's a recurring failure mode where a panel gets
re-templated as "Coming Soon" on top of a previously-live state — we
end up with both a `core-badge-live` span AND a `core-badge-cs`
("Coming Soon") badge inside the same panel, AND the outer div carries
`core-panel--cs`, AND the CTA is "In Development" instead of an actual
"Enter Course →" link. Students see the button lit up green but click
into a dead panel. This script restores the live state for every
course that has actually been built.

For every registry entry that:
  - has status=="live"
  - has a /ai-academy/modules/<slug>/ url
  - has the matching <slug>-m1.html present on disk

…this script ensures the panel in courses.html (matched by the
`data-course="<slug>"` attribute) carries the canonical live state:

  outer div:    class="core-panel"  (no `core-panel--cs`)
  badges:       has exactly one <span class="core-badge-live"><span
                  class="live-dot"></span> Live</span>; no
                  <span class="core-badge-cs">…</span>
  CTA:          <a href="/ai-academy/modules/electives-hub.html?course=<id>"
                  class="core-panel__cta">Enter Course →</a>
                (where <id> is the registry's id, NOT the slug —
                this is the convention used by the existing live
                panels and the electives-hub router)

Idempotent. Already-correct panels are not modified.

Usage:
    python .github/scripts/ensure_panels_live.py             # dry-run
    python .github/scripts/ensure_panels_live.py --apply     # write

Designed to run as a step inside reconcile_all.py and on a daily cron,
so a panel that gets stomped between commits is brought back within a
day at most.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO         = Path(__file__).resolve().parents[2]
COURSES_HTML = REPO / "ai-academy" / "courses.html"
MODULES_DIR  = REPO / "ai-academy" / "modules"
REGISTRY     = MODULES_DIR / "course-registry.json"


# ── Read disk-truth + registry ─────────────────────────────────────────

def disk_built_slugs() -> set[str]:
    """Slugs of courses with at least <slug>-m1.html on disk."""
    return {
        d.name for d in MODULES_DIR.iterdir()
        if d.is_dir() and (d / f"{d.name}-m1.html").exists()
    }


def live_courses_from_registry() -> dict[str, dict]:
    """Map slug -> registry entry for entries that are url-backed +
    status=live."""
    try:
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    except Exception:
        return {}
    out = {}
    for entry in data.values():
        if not isinstance(entry, dict):
            continue
        if entry.get("status") != "live":
            continue
        url = entry.get("url") or ""
        m = re.search(r"/modules/([^/]+)/", url)
        if not m:
            continue
        slug = m.group(1)
        out[slug] = entry
    return out


# ── Per-panel surgery ─────────────────────────────────────────────────

PANEL_OPEN_RE = re.compile(
    r'<div\s+class="(core-panel(?:[ ][^"]*)?)"([^>]*)>'
)


def find_panels_for_slug(html: str, slug: str) -> list[tuple[int, int]]:
    """Locate EVERY panel block whose opening tag has
    data-course="<slug>". Return a list of (start, end) byte-offset
    pairs. End is the position just AFTER each panel's outermost
    closing </div>.

    Multiple panels for the same slug exist for some courses (e.g. one
    in "Society & Domain" and a duplicate in a youth section). The
    repair must visit all of them so a duplicate's stale Coming-Soon
    state can't keep haunting the live state of its sibling.
    """
    out: list[tuple[int, int]] = []
    for m in PANEL_OPEN_RE.finditer(html):
        attrs = m.group(2) or ""
        if f'data-course="{slug}"' not in attrs:
            continue
        i = m.end()
        depth = 1
        while depth > 0 and i < len(html):
            nxt_open  = html.find("<div", i)
            nxt_close = html.find("</div>", i)
            if nxt_close == -1:
                break
            if nxt_open != -1 and nxt_open < nxt_close:
                depth += 1
                i = nxt_open + 4
            else:
                depth -= 1
                i = nxt_close + len("</div>")
        if depth == 0:
            out.append((m.start(), i))
    return out


def find_panel_for_slug(html: str, slug: str) -> tuple[int, int] | None:
    """Backwards-compat wrapper — returns the first panel, or None.
    Prefer find_panels_for_slug() in new code."""
    panels = find_panels_for_slug(html, slug)
    return panels[0] if panels else None


def fix_panel_block(panel_html: str, registry_id: str) -> tuple[str, list[str]]:
    """Apply the four normalisations and return (new_html, changes_made)."""
    out = panel_html
    changes: list[str] = []

    # 1. Strip `core-panel--cs` from the outer div's class list.
    m = re.match(r'(<div\s+class=")(core-panel(?:[ ][^"]*)?)("[^>]*>)', out)
    if m:
        prefix, classes, suffix = m.group(1), m.group(2), m.group(3)
        new_classes = re.sub(r'\s*\bcore-panel--cs\b', '', classes).strip()
        new_classes = re.sub(r'\s+', ' ', new_classes)
        if new_classes != classes:
            out = prefix + new_classes + suffix + out[m.end():]
            changes.append("removed core-panel--cs from outer div class")

    # 2. Remove any <span class="core-badge-cs">…</span> badges. Trim
    #    surrounding whitespace so we don't leave dangling blank lines.
    cs_pat = re.compile(
        r'\s*<span\s+class="core-badge-cs"[^>]*>[^<]*</span>',
    )
    if cs_pat.search(out):
        out = cs_pat.sub('', out)
        changes.append("removed core-badge-cs 'Coming Soon' badge")

    # 3. Ensure exactly one canonical core-badge-live span.
    canonical_live = '<span class="core-badge-live"><span class="live-dot"></span> Live</span>'
    live_pat = re.compile(
        r'<span\s+class="core-badge-live"[^>]*>'      # opening
        r'(?:<span\s+class="live-dot"></span>)?'       # optional live-dot
        r'\s*[^<]*'                                     # text
        r'</span>'                                      # close
    )
    live_matches = list(live_pat.finditer(out))
    if len(live_matches) > 1:
        # Keep the first, drop the rest, normalise the kept one.
        first = live_matches[0]
        # Remove others in reverse order so indices stay valid.
        for m in reversed(live_matches[1:]):
            # Also nibble preceding whitespace
            ws_start = m.start()
            while ws_start > 0 and out[ws_start - 1] in ' \t':
                ws_start -= 1
            if ws_start > 0 and out[ws_start - 1] == '\n':
                ws_start -= 1
            out = out[:ws_start] + out[m.end():]
        # Re-find first and replace with canonical
        first2 = live_pat.search(out)
        if first2 and first2.group(0) != canonical_live:
            out = out[:first2.start()] + canonical_live + out[first2.end():]
        changes.append("collapsed duplicate core-badge-live spans → one canonical")
    elif len(live_matches) == 1:
        existing = live_matches[0].group(0)
        if existing != canonical_live and 'live-dot' not in existing:
            out = out[:live_matches[0].start()] + canonical_live + out[live_matches[0].end():]
            changes.append("normalised core-badge-live to canonical (added live-dot)")
    else:
        # No live badge at all — inject canonical inside core-panel__badges.
        badges_open = '<div class="core-panel__badges">'
        i = out.find(badges_open)
        if i != -1:
            ins = i + len(badges_open)
            out = out[:ins] + "\n            " + canonical_live + out[ins:]
            changes.append("added missing core-badge-live")

    # 4. CTA: replace span CTA ("In Development") with real <a> link, OR
    #    repair an anchor whose href is wrong.
    real_cta = (f'<a href="/ai-academy/modules/electives-hub.html?course='
                f'{registry_id}" class="core-panel__cta">Enter Course &rarr;</a>')
    span_cta_pat = re.compile(
        r'<span[^>]*class="[^"]*core-panel__cta[^"]*"[^>]*>[^<]*</span>'
    )
    sm = span_cta_pat.search(out)
    if sm:
        out = out[:sm.start()] + real_cta + out[sm.end():]
        changes.append("replaced span CTA ('In Development') with <a> Enter Course")
    else:
        a_cta_pat = re.compile(
            r'<a[^>]*class="[^"]*core-panel__cta[^"]*"[^>]*>[^<]*</a>'
        )
        am = a_cta_pat.search(out)
        if am:
            current = am.group(0)
            expected_href = f'href="/ai-academy/modules/electives-hub.html?course={registry_id}"'
            if expected_href not in current:
                out = out[:am.start()] + real_cta + out[am.end():]
                changes.append(f"repaired anchor CTA href to course={registry_id}")

    return out, changes


# ── Top-level driver ─────────────────────────────────────────────────

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true",
                    help="Write changes back to courses.html. Without "
                         "this, runs as a dry-run.")
    args = ap.parse_args()

    disk = disk_built_slugs()
    live = live_courses_from_registry()

    targets = {slug: entry for slug, entry in live.items() if slug in disk}
    print(f"Disk-built courses: {len(disk)}")
    print(f"Registry-live courses: {len(live)}")
    print(f"Targets (registry-live AND disk-built): {len(targets)}")

    if not COURSES_HTML.exists():
        print(f"ERROR: {COURSES_HTML} not found", file=sys.stderr)
        return 2
    html = COURSES_HTML.read_text(encoding="utf-8")
    new_html = html

    repaired_panels = 0       # count of individual panels fixed
    repaired_slugs  = 0       # count of slugs that had ≥1 panel fixed
    not_found       = []
    no_change_slugs = 0
    panels_seen     = 0
    for slug in sorted(targets):
        entry = targets[slug]
        registry_id = entry.get("id") or slug
        # Re-find panels every iteration. We mutate new_html in place
        # so offsets shift; safest is to look up freshly.
        locs = find_panels_for_slug(new_html, slug)
        if not locs:
            not_found.append(slug)
            continue
        panels_seen += len(locs)
        slug_changes_logged = False
        # Process panels right-to-left so earlier offsets stay valid
        # while we splice; this lets us mutate without re-finding
        # between iterations.
        for start, end in sorted(locs, reverse=True):
            block = new_html[start:end]
            fixed, changes = fix_panel_block(block, registry_id)
            if not changes:
                continue
            new_html = new_html[:start] + fixed + new_html[end:]
            repaired_panels += 1
            if not slug_changes_logged:
                print(f"  ✓ {slug}  ({len(locs)} panel(s) for this slug)")
                slug_changes_logged = True
                repaired_slugs += 1
            for c in changes:
                print(f"      - {c}")
        if not slug_changes_logged:
            no_change_slugs += 1

    print()
    print(f"Slugs scanned: {len(targets)}")
    print(f"Slugs with at least one panel repaired: {repaired_slugs}")
    print(f"Individual panels repaired (incl. duplicates): {repaired_panels}")
    print(f"Slugs already correct (no change needed): {no_change_slugs}")
    print(f"Total panels visited across all target slugs: {panels_seen}")
    print(f"No panel found in courses.html: {len(not_found)}")
    if not_found:
        for s in not_found[:10]:
            print(f"    {s}")
        if len(not_found) > 10:
            print(f"    … and {len(not_found) - 10} more")

    if not args.apply:
        if repaired_panels:
            print()
            print("Dry run — re-run with --apply to write the fixes.")
        return 0

    if new_html == html:
        print("No change — courses.html already correct.")
        return 0

    COURSES_HTML.write_text(new_html, encoding="utf-8")
    print(f"\nWrote {COURSES_HTML.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
