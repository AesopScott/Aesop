#!/usr/bin/env python3
"""
Rebuild the draft index.json for one or more draft directories.

Usage:
    python rebuild_index.py [<dir1> [<dir2> ...]]

Defaults to rebuilding all three draft directories if no arguments are given:
    aip/drafts
    aip/ya-drafts
    aip/k12-drafts

The index.json is a JSON array of filenames (strings), sorted alphabetically,
excluding 'index.json' itself.  This is the canonical format consumed by the
aip-drafts.html review page.
"""

import json
import os
import sys
from pathlib import Path


def rebuild(drafts_dir: str) -> int:
    """Rebuild index.json in `drafts_dir`. Returns the number of files indexed."""
    d = Path(drafts_dir)
    if not d.exists():
        print(f"  [skip] {drafts_dir} — directory does not exist")
        return 0

    files = sorted(
        f.name
        for f in d.iterdir()
        if f.suffix == ".json" and f.name != "index.json"
    )

    index_path = d / "index.json"
    index_path.write_text(
        json.dumps(files, indent=2),
        encoding="utf-8",
    )
    print(f"  Rebuilt {index_path}: {len(files)} draft(s)")
    return len(files)


def main():
    dirs = sys.argv[1:] if len(sys.argv) > 1 else [
        "aip/drafts",
        "aip/ya-drafts",
        "aip/k12-drafts",
    ]
    total = 0
    for d in dirs:
        total += rebuild(d)
    print(f"Done. {total} total draft(s) indexed across {len(dirs)} director(ies).")


if __name__ == "__main__":
    main()
