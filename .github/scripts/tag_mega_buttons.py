#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tag_mega_buttons.py — Add data-course="<slug>" to every mega-link button
in ai-academy/courses.html, so future reconciliation against disk truth
is a trivial key-based lookup.

Resolution order for a button's slug:
  1. If data-panel starts with "aip-", strip the prefix.
  2. Hand-curated name→slug HARD_MAP covers buttons whose display text
     differs substantially from the disk folder name.
  3. Registry URL lookup: if a registry entry's title matches the
     button's display text, extract the slug from its URL field.
  4. Direct name_to_slug() — only accepted if the result is a real
     disk folder or a recognised AIP slug.

Buttons that cannot be resolved by any of the above are left unchanged
(no data-course added). They're reported at the end for manual review.

Idempotent: re-running won't duplicate the attribute.

Usage:
    python .github/scripts/tag_mega_buttons.py           # dry-run
    python .github/scripts/tag_mega_buttons.py --apply   # write changes
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


def disk_slugs() -> set[str]:
    return {d.name for d in MODULES_DIR.iterdir()
            if d.is_dir() and (d / f"{d.name}-m1.html").exists()}


def registry_title_to_slug() -> dict[str, str]:
    """Build {normalised_title: url_slug} from course-registry.json.
    Only entries with a /modules/<slug>/ URL are usable."""
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
        # live entries win over coming-soon if both map to same title
        if title not in out or entry.get("status") == "live":
            out[_norm_key(title)] = m.group(1)
    return out


def _norm_key(s: str) -> str:
    """Normalise a display name for map lookups."""
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


# Hand-curated mapping where the nav display name doesn't slugify to the
# disk folder. Keys are _norm_key() output, values are disk slugs.
HARD_MAP: dict[str, str] = {
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


def resolve(panel: str, raw_name: str,
            known_disk: set[str],
            reg_title_to_slug: dict[str, str]) -> str | None:
    """Return the best-guess slug, or None if unresolvable."""
    name = _html_mod.unescape(raw_name).strip()

    # 1. aip- prefix encodes the slug
    if panel.startswith("aip-"):
        return panel[4:]

    # 2. Hand-curated map (display name → disk slug)
    key = _norm_key(name)
    if key in HARD_MAP:
        return HARD_MAP[key]
    # Drop em-dash subtitle and retry
    main = re.split(r"\s*[\u2014\u2013]\s*", name, maxsplit=1)[0]
    main_key = _norm_key(main)
    if main_key in HARD_MAP:
        return HARD_MAP[main_key]

    # 3. Registry title lookup (by URL) — works for --soon entries that
    # are properly registered even if the disk folder doesn't exist yet.
    if key in reg_title_to_slug:
        return reg_title_to_slug[key]
    if main_key in reg_title_to_slug:
        return reg_title_to_slug[main_key]

    # 4. Direct slug from name — accept only if it matches a real disk slug
    slug = _name_to_slug(name)
    if slug in known_disk:
        return slug
    slug_main = _name_to_slug(main)
    if slug_main in known_disk:
        return slug_main

    return None


def tag_buttons(html: str) -> tuple[str, dict]:
    known = disk_slugs()
    reg_title_to_slug = registry_title_to_slug()

    btn_pat = re.compile(
        r'(<button\s+)([^>]*?class="mega-link[^"]*"[^>]*?)(>)([^<]+)(</button>)',
        re.DOTALL,
    )

    tagged = 0
    already_tagged = 0
    unresolved: list[dict] = []

    def replace(m: re.Match) -> str:
        nonlocal tagged, already_tagged
        head, attrs, gt, name, tail = m.groups()

        # Already has data-course — leave it
        if re.search(r'\bdata-course="[^"]*"', attrs):
            already_tagged += 1
            return m.group(0)

        dm = re.search(r'data-panel="([^"]+)"', attrs)
        if not dm:
            return m.group(0)

        slug = resolve(dm.group(1), name, known, reg_title_to_slug)
        if slug is None:
            unresolved.append({"panel": dm.group(1), "name": _html_mod.unescape(name).strip()})
            return m.group(0)

        new_attrs = attrs.rstrip() + f' data-course="{slug}"'
        tagged += 1
        return f"{head}{new_attrs}{gt}{name}{tail}"

    new_html = btn_pat.sub(replace, html)

    return new_html, {
        "tagged":         tagged,
        "already_tagged": already_tagged,
        "unresolved":     unresolved,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    html = COURSES_HTML.read_text(encoding="utf-8")
    new_html, stats = tag_buttons(html)

    print(f"Newly tagged: {stats['tagged']}")
    print(f"Already had data-course: {stats['already_tagged']}")
    print(f"Unresolved (no data-course added): {len(stats['unresolved'])}")
    for u in stats["unresolved"]:
        print(f"  panel={u['panel']!r}  name={u['name']!r}")

    if not args.apply:
        print("\nDry run — use --apply to write.")
        return

    if new_html == html:
        print("\nNo changes.")
        return

    COURSES_HTML.write_text(new_html, encoding="utf-8")
    print(f"\nWrote {COURSES_HTML.relative_to(REPO)}")


if __name__ == "__main__":
    main()
