#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
reconcile_panels.py — Sync the core-panel badges in courses.html with
disk truth.

Each panel is a <div class="core-panel" id="dv-N"> ... </div>. Inside
it is a <div class="core-panel__title"> with the display name. We
resolve the title to a disk slug using the same HARD_MAP + registry
lookup as tag_mega_buttons.py, then:

  - Add data-course="<slug>" to the panel's opening <div> tag
    (idempotent — skip if already present).
  - Ensure a `core-badge-live` <span> is present iff the slug exists
    on disk. If a panel's course is not on disk, the live badge is
    removed (panels without a live badge just render without one — no
    "draft" class exists in the codebase today).

Panels whose title cannot be resolved to any registry or disk slug
are left untouched and reported for manual review.

Usage:
    python .github/scripts/reconcile_panels.py           # dry-run
    python .github/scripts/reconcile_panels.py --apply   # write
"""

from __future__ import annotations

import argparse
import html as _html_mod
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


# Keep in lock-step with tag_mega_buttons.py. If one changes, mirror the other.
HARD_MAP = {
    "ai in social media":                         "ai-social-media",
    "ai and misinformation":                      "ai-misinformation",
    "ai ethics and decision making":              "ai-ethics",
    "ais impact on jobs":                         "ai-job-market-impact",
    "ai work and your career":                    "ai-work-and-automation-realities",
    "conversational ai and chatbots":             "conversational-ai-chatbots",
    "autonomous ai systems":                      "ai-autonomous-systems",
    "building production agents with vertex ai":  "building-agents-vertex-ai",
    "agentic data workflows on google cloud":     "vertex-ai-data-agents",
    "say it right talk to ai":                    "talking-to-ai-prompt-writing",
    "security auditing for ai generated code":    "security-auditing-ai-generated-code",
    "code audit workflows and team standards":    "code-audit-workflows-team-standards",
    "dont get fooled ai and lies":                "ai-and-fake-information",
    "make it yours create with ai":               "make-it-yours-creating-with-ai",
    "whats really inside ai":                     "whats-really-inside-ai",
    "understanding ai bias and fairness":         "ai-bias-and-fairness",
    "building ai agents i":                       "building-ai-agents-i-use-cases",
    "building ai agents ii":                      "building-ai-agents-ii-skills",
    "building ai agents iii":                     "building-ai-agents-iii-tools",
    "building ai agents iv":                      "building-ai-agents-iv-openclaw",
    "building ai agents v":                       "building-ai-agents-v-optimization",
}


def disk_slugs() -> set[str]:
    return {d.name for d in MODULES_DIR.iterdir()
            if d.is_dir() and (d / f"{d.name}-m1.html").exists()}


def _norm_key(s: str) -> str:
    s = _html_mod.unescape(s).lower()
    s = s.replace("\u2014", " ").replace("\u2013", " ").replace("-", " ")
    s = s.replace("&", " and ")
    s = re.sub(r"[^a-z0-9 ]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def _name_to_slug(s: str) -> str:
    s = _html_mod.unescape(s).lower()
    s = s.replace("&", "and").replace("'", "").replace("\u2019", "")
    s = s.replace("\u2014", "-").replace("\u2013", "-")
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s


def registry_title_to_slug() -> dict[str, str]:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    out: dict[str, str] = {}
    for entry in data.values():
        if not isinstance(entry, dict):
            continue
        url = entry.get("url") or ""
        m = re.search(r"/modules/([^/]+)/", url)
        if not m:
            continue
        title = _html_mod.unescape(entry.get("title") or "").strip()
        if not title:
            continue
        key = _norm_key(title)
        if key not in out or entry.get("status") == "live":
            out[key] = m.group(1)
    return out


def resolve(title: str, known: set[str],
            reg: dict[str, str]) -> str | None:
    name = _html_mod.unescape(title).strip()
    key = _norm_key(name)
    if key in HARD_MAP:
        return HARD_MAP[key]
    main = re.split(r"\s*[\u2014\u2013]\s*", name, maxsplit=1)[0]
    main_key = _norm_key(main)
    if main_key in HARD_MAP:
        return HARD_MAP[main_key]
    if key in reg:
        return reg[key]
    if main_key in reg:
        return reg[main_key]
    slug = _name_to_slug(name)
    if slug in known:
        return slug
    slug_main = _name_to_slug(main)
    if slug_main in known:
        return slug_main
    return None


def reconcile(html: str) -> tuple[str, dict]:
    """Walk every <div class="core-panel" id="dv-N"> ... </div></div> block
    and (a) tag it with data-course, (b) ensure core-badge-live matches
    disk truth."""
    known = disk_slugs()
    reg = registry_title_to_slug()

    # Locate every panel opening. The panel body extends from this opening
    # to the character before the next panel opening, or to end-of-file for
    # the last panel. Within each body we search for the title and badge
    # and rewrite the body in place.
    # Match any <div> whose class list starts with "core-panel" (includes
    # variants like "core-panel core-panel--cs" and "core-panel active").
    # The class value is captured so we can preserve it when rewriting.
    open_pat = re.compile(
        r'<div\s+class="(core-panel(?:[ ][^"]*)?)"([^>]*)>'
    )
    title_pat = re.compile(r'class="core-panel__title">([^<]+)</div>')
    # Badges may contain a nested <span class="live-dot"></span> before
    # the visible "Live" text, so match non-greedily through the outer </span>.
    live_badge_pat = re.compile(
        r'[ \t]*<span\s+class="core-badge-live">.*?</span>\s*</span>\n?'
        r'|[ \t]*<span\s+class="core-badge-live">.*?</span>\n?',
        re.DOTALL,
    )
    live_badge_detect = re.compile(r'<span\s+class="core-badge-live"')

    opens = list(open_pat.finditer(html))
    changed_to_live = 0
    removed_live    = 0
    tagged          = 0
    already_tagged  = 0
    unresolved      = []

    # Build new HTML piece by piece. For each panel: replace its opening
    # tag (possibly adding data-course) and mutate the body (badge toggle).
    parts = []
    cursor = 0
    for i, m in enumerate(opens):
        # Panel body extends until the next panel opens, or EOF
        body_end = opens[i + 1].start() if i + 1 < len(opens) else len(html)
        open_start = m.start()
        open_end   = m.end()
        class_val   = m.group(1)  # e.g. "core-panel" or "core-panel core-panel--cs"
        other_attrs = m.group(2) or ""

        body = html[open_end:body_end]
        tm = title_pat.search(body)
        if not tm:
            parts.append(html[cursor:body_end])
            cursor = body_end
            continue

        title = tm.group(1).strip()
        slug  = resolve(title, known, reg)
        if slug is None:
            unresolved.append({"title": title})
            parts.append(html[cursor:body_end])
            cursor = body_end
            continue

        # (a) data-course tagging
        if 'data-course="' in other_attrs:
            already_tagged += 1
            new_other = other_attrs
        else:
            new_other = other_attrs + f' data-course="{slug}"'
            tagged += 1

        new_open = f'<div class="{class_val}"{new_other}>'

        # (b) badge toggling — detect with a simple signature; remove with
        # the full (nested-aware) pattern.
        has_live = bool(live_badge_detect.search(body))
        should_be_live = slug in known
        new_body = body
        if should_be_live and not has_live:
            badges_div = re.search(r'(<div\s+class="core-panel__badges">)', new_body)
            if badges_div:
                new_body = new_body.replace(
                    badges_div.group(0),
                    badges_div.group(0) + '\n            <span class="core-badge-live">Live</span>',
                    1,
                )
                changed_to_live += 1
        elif has_live and not should_be_live:
            new_body = live_badge_pat.sub("", new_body, count=1)
            removed_live += 1

        parts.append(html[cursor:open_start])
        parts.append(new_open)
        parts.append(new_body)
        cursor = body_end

    parts.append(html[cursor:])
    new_html = "".join(parts)
    return new_html, {
        "tagged":          tagged,
        "already_tagged":  already_tagged,
        "added_live":      changed_to_live,
        "removed_live":    removed_live,
        "unresolved":      unresolved,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    html = COURSES_HTML.read_text(encoding="utf-8")
    new_html, stats = reconcile(html)

    print(f"Panels tagged with data-course: {stats['tagged']}")
    print(f"Panels already tagged:          {stats['already_tagged']}")
    print(f"Live badge ADDED (course on disk, badge missing):   {stats['added_live']}")
    print(f"Live badge REMOVED (course not on disk):            {stats['removed_live']}")
    print(f"Unresolved panels (title couldn't be matched): {len(stats['unresolved'])}")
    for u in stats["unresolved"]:
        print(f"  title={u['title']!r}")

    if not args.apply:
        print("\nDry run — use --apply to write.")
        return

    if new_html == html:
        print("\nNo changes needed.")
        return

    COURSES_HTML.write_text(new_html, encoding="utf-8")
    print(f"\nWrote {COURSES_HTML.relative_to(REPO)}")


if __name__ == "__main__":
    main()
