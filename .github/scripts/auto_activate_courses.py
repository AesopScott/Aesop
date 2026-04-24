#!/usr/bin/env python3
"""
Auto-activate courses that have written module HTML files but aren't live yet.

Criteria for auto-activation:
  1. Directory under ai-academy/modules/ contains at least 1 file named {dirname}-m*.html
  2. Course has an entry in courses-data.json (source of title/desc/modules)
  3. Course is NOT already status=live in course-registry.json

The script builds a minimal registry entry and sets live=True in courses-data.json.
It also recomputes stats.json after any activations.

Usage:
    python auto_activate_courses.py              # dry-run: show what would be activated
    python auto_activate_courses.py --apply      # actually apply changes
    python auto_activate_courses.py --apply --stats-only  # only rebuild stats.json
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT    = Path(__file__).resolve().parents[2]
MODULES_DIR  = REPO_ROOT / "ai-academy" / "modules"
REGISTRY     = MODULES_DIR / "course-registry.json"
COURSES_DATA = MODULES_DIR / "courses-data.json"
STATS_JSON   = REPO_ROOT / "stats.json"

# Icon cycling pool
ICONS = ["🧩", "🌐", "💡", "🔬", "📊", "🚀", "🎯", "⚙️", "🔭", "🖥️",
         "🤝", "🎨", "💼", "📡", "🛡️", "🧠", "⚡", "🔮"]

# Best-guess sub-label from course ID keywords
SUB_HINTS = {
    "governance": "Society",
    "society":    "Society",
    "ethics":     "Ethics",
    "bias":       "Ethics",
    "fairness":   "Ethics",
    "job":        "Society",
    "work":       "Society",
    "automation": "Society",
    "graphic":    "Art & Design",
    "design":     "Art & Design",
    "art":        "Art & Design",
    "business":   "Business",
    "venture":    "Business",
    "pitch":      "Business",
    "funding":    "Business",
    "model":      "AI Models",
    "llm":        "AI Models",
    "language":   "AI Models",
    "context":    "AI Progress",
    "hardware":   "AI Progress",
    "future":     "AI Progress",
    "agent":      "Development",
    "build":      "Development",
    "dev":        "Development",
    "code":       "Development",
    "vertex":     "Development",
    "local":      "Development",
    "running":    "Development",
    "synthetic":  "Development",
    "evaluation": "Development",
    "testing":    "Development",
    "chatbot":    "AI Models",
    "conversat":  "AI Models",
    "autonomous": "AI Progress",
    "social":     "Society",
    "media":      "Society",
}


def infer_sub(course_id: str) -> str:
    lower = course_id.lower()
    for kw, sub in SUB_HINTS.items():
        if kw in lower:
            return sub
    return "Elective"


def load_json(path: Path) -> dict | list:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def find_candidates(registry: dict, courses_data_map: dict) -> list[dict]:
    candidates = []
    icon_idx = len([v for v in registry.values()
                    if isinstance(v, dict) and v.get("status") == "live"])

    for d in sorted(MODULES_DIR.iterdir()):
        if not d.is_dir():
            continue
        module_files = sorted(d.glob(f"{d.name}-m*.html"))
        if not module_files:
            continue
        if d.name not in courses_data_map:
            continue
        reg_entry = registry.get(d.name, {})
        if isinstance(reg_entry, dict) and reg_entry.get("status") == "live":
            continue

        cd = courses_data_map[d.name]
        icon_idx += 1
        candidates.append({
            "id":        d.name,
            "title":     cd.get("name", d.name),
            "desc":      cd.get("description", ""),
            "modCount":  len(module_files),
            "icon":      ICONS[icon_idx % len(ICONS)],
            "sub":       infer_sub(d.name),
            "cd_live":   cd.get("live", False),
            "cd_modules": cd.get("modules", []),
        })

    return candidates


def build_registry_entry(c: dict) -> dict:
    entry = {
        "id":          c["id"],
        "title":       c["title"],
        "icon":        c["icon"],
        "sub":         c["sub"],
        "accent":      "#64748b",
        "accentRgb":   "100,116,139",
        "pts":         2,
        "days":        2,
        "desc":        c["desc"],
        "category":    "",
        "type":        "Core",
        "status":      "live",
        "modCount":    c["modCount"],
        "url":         f"/ai-academy/modules/{c['id']}/",
        "_meta":       {"languages": ["en"]},
        "langUrls":    {
            "en": f"/ai-academy/modules/{c['id']}/{c['id']}-m1.html"
        },
    }
    return entry


def rebuild_stats(registry: dict) -> int:
    live_count = sum(
        1 for v in registry.values()
        if isinstance(v, dict) and v.get("status") == "live"
    )
    stats = load_json(STATS_JSON)
    stats["coursesLive"] = live_count
    from datetime import datetime, timezone
    stats["updatedAt"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")
    save_json(STATS_JSON, stats)
    return live_count


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply",      action="store_true", help="Actually apply changes (default: dry-run)")
    parser.add_argument("--stats-only", action="store_true", help="Only rebuild stats.json")
    args = parser.parse_args()

    registry      = load_json(REGISTRY)
    cdata         = load_json(COURSES_DATA)
    courses_data_map = {c["id"]: c for c in cdata.get("courses", [])}

    if args.stats_only:
        live = rebuild_stats(registry)
        print(f"stats.json rebuilt: coursesLive={live}")
        return

    candidates = find_candidates(registry, courses_data_map)

    if not candidates:
        print("No new courses to activate.")
        # Still rebuild stats to stay in sync
        if args.apply:
            rebuild_stats(registry)
        return

    print(f"Found {len(candidates)} course(s) to activate:")
    for c in candidates:
        print(f"  {'[DRY RUN] ' if not args.apply else ''}+ {c['id']} ({c['modCount']} modules)")

    if not args.apply:
        print("\nRun with --apply to activate these courses.")
        return

    # Apply registry additions
    for c in candidates:
        registry[c["id"]] = build_registry_entry(c)
        print(f"  -> Registry: {c['title']} added")

    save_json(REGISTRY, registry)

    # Apply courses-data live=True
    updated_cd = 0
    for course in cdata.get("courses", []):
        if course.get("id") in {c["id"] for c in candidates}:
            course["live"] = True
            updated_cd += 1

    save_json(COURSES_DATA, cdata)
    print(f"  -> courses-data.json: {updated_cd} course(s) set live=True")

    # Rebuild stats
    live_count = rebuild_stats(registry)
    print(f"  -> stats.json: coursesLive={live_count}")

    print(f"\nActivated {len(candidates)} course(s).")


if __name__ == "__main__":
    main()
