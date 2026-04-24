#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sync_registry_to_disk.py — Add registry entries for disk courses that
aren't yet in course-registry.json, marked status="live".

Source of truth: ai-academy/modules/<slug>/ with <slug>-m1.html present.
If such a folder exists but the slug (taken from the URL field of an
existing registry entry) isn't present, this script creates a new entry
with the minimum required fields.

Fields filled in:
  id, title, desc, icon, status=live, modCount, modules, url,
  category ("") and type ("Elective") as placeholders.

Editorial fields (accent, accentRgb, pts, days, sub) are left at
sensible defaults; the user can refine them later.

What this script does NOT do:
  - Does not modify courses.html (nav and panels are already reconciled).
  - Does not modify dashboard.html.
  - Does not modify i18n files.
  - Does not remove stale registry entries (coming-soon placeholders
    are left alone).

Idempotent: slugs already in the registry are skipped.

Usage:
    python .github/scripts/sync_registry_to_disk.py           # dry-run
    python .github/scripts/sync_registry_to_disk.py --apply   # write
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

REPO        = Path(__file__).resolve().parents[2]
MODULES_DIR = REPO / "ai-academy" / "modules"
REGISTRY    = MODULES_DIR / "course-registry.json"

# Rotating pool used for new-course icons (inherited from legacy add_course.py).
ICON_POOL = ["🧩", "🌐", "💡", "🔬", "📊", "🚀", "🎯", "⚙️", "🔭", "🖥️",
             "🤝", "🎨", "💼", "📡", "🛡️", "🧠", "⚡", "🔮"]


def extract_title(m1_html: str, slug: str) -> str:
    m = re.search(r'class="lesson-kicker">([^·<]+)', m1_html)
    if m:
        return _html_mod.unescape(m.group(1).strip())
    name = slug.replace("-", " ").replace("_", " ").title()
    return re.sub(r"\bAi\b", "AI", name)


def extract_desc(m1_html: str) -> str:
    m = re.search(
        r'id="p-intro".*?<div class="tagline">(.*?)</div>',
        m1_html, re.DOTALL,
    )
    if m:
        txt = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        if txt:
            return _html_mod.unescape(txt)
    m = re.search(r'class="tagline">(.*?)</div>', m1_html, re.DOTALL)
    if m:
        return _html_mod.unescape(re.sub(r"<[^>]+>", "", m.group(1)).strip())
    return ""


def extract_module_stubs(slug: str, files: list[Path]) -> list[dict]:
    """Minimal module stubs: id, title (from lesson-kicker / h1)."""
    mods = []
    for i, f in enumerate(files, 1):
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except Exception:
            text = ""
        h1 = re.search(
            r'class="lesson-kicker">[^<]*\s*Lesson\s*1.*?<h1>(.*?)</h1>',
            text, re.DOTALL,
        )
        title = re.sub(r"<[^>]+>", "", h1.group(1)).strip() if h1 else f"Module {i}"
        mods.append({
            "id":    f"{slug}-m{i}",
            "title": _html_mod.unescape(title),
        })
    return mods


def disk_courses() -> dict[str, dict]:
    out = {}
    for d in sorted(MODULES_DIR.iterdir()):
        if not d.is_dir() or d.name.startswith("."):
            continue
        m1 = d / f"{d.name}-m1.html"
        if not m1.exists():
            continue
        modules = sorted(d.glob(f"{d.name}-m*.html"))
        try:
            m1_html = m1.read_text(encoding="utf-8", errors="replace")
        except Exception:
            m1_html = ""
        out[d.name] = {
            "title":    extract_title(m1_html, d.name),
            "desc":     extract_desc(m1_html),
            "modCount": len(modules),
            "modules":  extract_module_stubs(d.name, modules),
        }
    return out


def registered_slugs(registry: dict) -> set[str]:
    """Slugs taken from the url field of each registry entry."""
    slugs = set()
    for entry in registry.values():
        if not isinstance(entry, dict):
            continue
        url = entry.get("url") or ""
        m = re.search(r"/modules/([^/]+)/", url)
        if m:
            slugs.add(m.group(1))
    return slugs


def next_icon(registry: dict) -> str:
    """Deterministic icon rotation — pick the next icon not yet used
    heavily. Simple round-robin by existing registry count."""
    used_count = sum(
        1 for v in registry.values()
        if isinstance(v, dict) and v.get("icon")
    )
    return ICON_POOL[used_count % len(ICON_POOL)]


def build_entry(slug: str, meta: dict, icon: str) -> dict:
    return {
        "id":         slug,
        "title":      meta["title"],
        "icon":       icon,
        "sub":        "",
        "accent":     "#64748b",
        "accentRgb":  "100,116,139",
        "pts":        2,
        "days":       2,
        "desc":       meta["desc"],
        "category":   "",
        "type":       "Elective",
        "status":     "live",
        "modCount":   meta["modCount"],
        "modules":    meta["modules"],
        "url":        f"/ai-academy/modules/{slug}/",
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    disk = disk_courses()
    reg_slugs = registered_slugs(registry)

    to_add = [s for s in sorted(disk) if s not in reg_slugs]
    print(f"Disk:       {len(disk)} courses")
    print(f"Registered: {len(reg_slugs)}")
    print(f"To add:     {len(to_add)}")
    print()

    if not to_add:
        print("Nothing to add.")
        return

    # Build entries
    icon_base_count = sum(1 for v in registry.values()
                          if isinstance(v, dict) and v.get("icon"))
    added_entries = []
    for i, slug in enumerate(to_add):
        icon = ICON_POOL[(icon_base_count + i) % len(ICON_POOL)]
        entry = build_entry(slug, disk[slug], icon)
        added_entries.append(entry)
        print(f"  + {slug}  ({entry['modCount']} mods)  {entry['title']!r}")

    if not args.apply:
        print("\nDry run — use --apply to write to course-registry.json.")
        return

    # Insert into registry dict, keyed by slug
    for entry in added_entries:
        registry[entry["id"]] = entry

    REGISTRY.write_text(
        json.dumps(registry, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"\nWrote {REGISTRY.relative_to(REPO)}")


if __name__ == "__main__":
    main()
