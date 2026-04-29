#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validate_draft_schema.py — Fail-fast guard for the autopatch workflows.

Reads every approved draft in the given drafts folder and verifies it
conforms to the current schema:
  - mega_group is set and is one of the allowed values for that audience
  - modules is a non-empty list
  - every module is an object with non-empty title, sub, and description

Approved drafts that fail any check cause this script to exit non-zero
with a per-draft list of problems. The autopatch workflow then aborts
before bad drafts can land in courses.html.

Drafts with status != "approved" are ignored — the validator only cares
about drafts that are about to be patched into the live nav.

Usage (from a workflow step):
    python .github/scripts/validate_draft_schema.py --drafts-dir aip/k12-drafts --audience Youth

Exit codes:
    0  — all approved drafts pass
    1  — at least one approved draft fails validation
    2  — usage / config error
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ALLOWED_GROUPS = {
    "Professional": [
        "AI Tools", "Strategy", "AI Models", "AI Frontier", "Development",
        "Society", "Applied", "Business", "Cybersecurity",
    ],
    "Young Adult": [
        "AI Tools", "Make & Create", "How AI Works", "Truth & Safety",
        "Strategy", "Society", "Business",
    ],
    "Youth": [
        "How AI Works", "Make & Create", "Truth & Safety",
        "AI Toolbox", "AI in School", "Code with AI",
    ],
    "Cybersecurity": [
        "Cybersecurity",
    ],
}


def validate_module(i: int, m) -> list[str]:
    """Return a list of error strings for module index i. Empty list = ok."""
    errs = []
    if not isinstance(m, dict):
        errs.append(f"M{i}: module is not an object (got {type(m).__name__})")
        return errs
    if not (m.get("title") or "").strip():
        errs.append(f"M{i}: empty 'title'")
    if not (m.get("sub") or "").strip():
        errs.append(f"M{i}: empty 'sub'")
    if not (m.get("description") or "").strip():
        errs.append(f"M{i}: empty 'description'")
    return errs


def validate_draft(draft: dict, allowed_groups: list[str]) -> list[str]:
    """Return a list of error strings for the draft. Empty list = ok."""
    errs = []

    mg = (draft.get("mega_group") or "").strip()
    if not mg:
        errs.append("missing 'mega_group'")
    elif mg not in allowed_groups:
        errs.append(f"mega_group {mg!r} is not in allowed list: {allowed_groups}")

    modules = draft.get("modules", [])
    if not modules:
        errs.append("modules array is empty")
    elif not isinstance(modules, list):
        errs.append(f"modules is not a list (got {type(modules).__name__})")
    else:
        for i, m in enumerate(modules, 1):
            errs.extend(validate_module(i, m))

    return errs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--drafts-dir", required=True,
                    help="e.g. aip/k12-drafts")
    ap.add_argument("--audience", required=True,
                    choices=list(ALLOWED_GROUPS.keys()),
                    help="Picks the allowed mega_group list to validate against.")
    ap.add_argument("--warn-only", action="store_true",
                    help="Print failures but always exit 0. Use this until "
                         "the legacy drafts have been backfilled so autopatch "
                         "runs aren't blocked by pre-existing schema gaps.")
    args = ap.parse_args()

    drafts_dir = Path(args.drafts_dir)
    if not drafts_dir.exists():
        print(f"ERROR: drafts dir not found: {drafts_dir}", file=sys.stderr)
        return 2

    allowed = ALLOWED_GROUPS[args.audience]

    failed = []
    checked = 0
    skipped_nonapproved = 0
    for f in sorted(drafts_dir.glob("*.json")):
        if f.name == "index.json":
            continue
        try:
            draft = json.loads(f.read_text(encoding="utf-8"))
        except Exception as e:
            failed.append((f, [f"could not parse JSON: {e}"]))
            continue
        if not isinstance(draft, dict) or not draft.get("title"):
            continue
        if draft.get("status") != "approved":
            skipped_nonapproved += 1
            continue
        checked += 1
        errs = validate_draft(draft, allowed)
        if errs:
            failed.append((f, errs))

    print(f"Validated {checked} approved {args.audience} draft(s) "
          f"in {drafts_dir} (skipped {skipped_nonapproved} non-approved).")

    if not failed:
        print("All approved drafts conform to the current schema.")
        return 0

    print(f"\n{len(failed)} approved draft(s) FAILED validation:\n")
    for f, errs in failed:
        print(f"  ✗ {f.relative_to(Path('.')) if str(f).startswith(str(Path('.'))) else f}")
        for e in errs:
            print(f"      {e}")

    print()
    print("To fix:")
    print("  1. Run the backfill workflow with apply=true to add the missing fields, OR")
    print("  2. Edit the failing draft(s) by hand to add 'mega_group' (one of the")
    print(f"     allowed labels above) and module objects with title+sub+description.")
    print()
    print("This validator runs at the top of each autopatch workflow to prevent")
    print("incomplete drafts from reaching courses.html. Address the failures, then")
    print("the autopatch will run automatically on the next push.")
    if args.warn_only:
        print()
        print("(--warn-only mode: exiting 0 despite failures so the autopatch chain")
        print(" continues. Once all legacy drafts pass, drop --warn-only from each")
        print(" autopatch workflow's validate step to make this a hard gate.)")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
