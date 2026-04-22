#!/usr/bin/env python3
"""
sync-live-status.py
-------------------
Syncs live/coming-soon status from course-registry.json into courses-data.json.

Run this any time a course is activated in the registry to keep courses-data.json
in sync — so the module generator's isLive() fallback always reflects reality.

Usage:
    python ai-academy/modules/sync-live-status.py

Matches courses by: registry key == course id, or by title (case-insensitive).
"""

import json
import sys
from pathlib import Path

BASE = Path(__file__).parent

def load(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)

def save(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    registry_path   = BASE / 'course-registry.json'
    courses_data_path = BASE / 'courses-data.json'

    registry = load(registry_path)
    data     = load(courses_data_path)

    # Build lookup tables from registry
    id_to_status   = {}   # all ID variants -> status
    title_to_status = {}  # lowercase title -> status

    for k, v in registry.items():
        if not isinstance(v, dict) or 'status' not in v:
            continue
        status = v['status']
        for variant in [k, k.replace('-', '_'), k.replace('_', '-')]:
            id_to_status[variant] = status
        if 'title' in v:
            title_to_status[v['title'].strip().lower()] = status

    marked_live    = []
    marked_soon    = []
    unchanged      = []
    not_in_registry = []

    for course in data.get('courses', []):
        cid   = course['id']
        cname = course.get('name', '')

        # Resolve status: ID match first, then title match
        status = (id_to_status.get(cid)
                  or id_to_status.get(cid.replace('-', '_'))
                  or title_to_status.get(cname.strip().lower()))

        if status == 'live':
            if not course.get('live'):
                course['live'] = True
                marked_live.append(cid)
            else:
                unchanged.append(cid)
        elif status == 'coming-soon':
            if course.get('live'):
                del course['live']
                marked_soon.append(cid)
            else:
                unchanged.append(cid)
        else:
            not_in_registry.append(cid)

    save(courses_data_path, data)

    print(f'Marked live:true  ({len(marked_live)}): {", ".join(marked_live) or "none"}')
    print(f'Cleared live flag ({len(marked_soon)}): {", ".join(marked_soon) or "none"}')
    print(f'Already correct   ({len(unchanged)})')
    print(f'Not in registry   ({len(not_in_registry)}): {", ".join(not_in_registry) or "none"}')
    print(f'\ncourses-data.json updated.')

if __name__ == '__main__':
    main()
