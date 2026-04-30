#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_courses_html_sanity.py — Defensive guard against accidental
overwrites of ai-academy/courses.html.

Compares an "old" version of courses.html against a "new" one and
fails (exit 1) if the new version looks like a stale-working-tree
clobber rather than a legitimate edit.

Heuristics it checks (any one triggers a fail):
  * mega-cat section count dropped by more than 2
  * mega-link button count dropped by more than 15
  * file shrank by more than 25% in characters
  * 3 or more mega-cat section headings present in OLD are missing in NEW

Bypass: include the literal token [skip-courses-guard] anywhere in the
commit message (or set the COURSES_GUARD_SKIP=1 env var) when you are
intentionally shrinking the file. The bypass is logged so curators can
tell why a guard didn't fire.

Why this exists: on 2026-04-29, commit 4f03424c (Module-Test-gate
retrofit) shipped a stale local courses.html alongside the m*.html
retrofit; that 30-version-behind copy overwrote main and silently
removed all 6 Youth sub-sections, the live-typeahead search, the
second Cybersecurity section, and ~100 nav buttons. The diff went
unnoticed because it was buried inside a 1,048-file commit. This
guard catches that exact pattern next time.

Usage:
  python check_courses_html_sanity.py <old.html> <new.html>
  python check_courses_html_sanity.py --old-rev HEAD~1 --new-rev HEAD

Exit codes:
  0  - new file is within tolerance
  1  - new file looks like an accidental overwrite, fail loudly
  2  - usage / IO error
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

MEGA_CAT_RE  = re.compile(r'<div\s+class="mega-cat">([^<]+)</div>')
MEGA_LINK_RE = re.compile(r'class="mega-link[^"]*"')


def metrics(text: str) -> dict:
    cats = [c.strip() for c in MEGA_CAT_RE.findall(text)]
    return {
        "size":         len(text),
        "n_cats":       len(cats),
        "cats":         cats,
        "n_mega_link":  len(MEGA_LINK_RE.findall(text)),
    }


def read_at_revision(rev: str, path: str) -> str:
    """Run `git show <rev>:<path>` and return its stdout. Empty string
    on failure (e.g. file did not exist at that rev)."""
    try:
        return subprocess.check_output(
            ["git", "show", f"{rev}:{path}"],
            stderr=subprocess.DEVNULL,
            encoding="utf-8",
            errors="replace",
        )
    except Exception:
        return ""


def commit_message_for(rev: str) -> str:
    try:
        return subprocess.check_output(
            ["git", "log", "-1", "--format=%B", rev],
            encoding="utf-8",
            errors="replace",
        )
    except Exception:
        return ""


def evaluate(old: dict, new: dict, *, label_old: str, label_new: str) -> tuple[bool, list[str]]:
    failures: list[str] = []

    # 1. mega-cat section count
    cats_dropped = old["n_cats"] - new["n_cats"]
    if cats_dropped > 2:
        failures.append(
            f"mega-cat section count dropped by {cats_dropped} "
            f"({old['n_cats']} → {new['n_cats']})"
        )

    # 2. specific section headings missing
    missing_cats = [c for c in old["cats"] if c not in new["cats"]]
    if len(missing_cats) > 2:
        failures.append(
            f"{len(missing_cats)} mega-cat headings present in {label_old} "
            f"are missing in {label_new}: " +
            ", ".join(repr(c) for c in missing_cats[:6]) +
            (f", … and {len(missing_cats)-6} more" if len(missing_cats) > 6 else "")
        )

    # 3. mega-link button count
    btns_dropped = old["n_mega_link"] - new["n_mega_link"]
    if btns_dropped > 15:
        failures.append(
            f"mega-link button count dropped by {btns_dropped} "
            f"({old['n_mega_link']} → {new['n_mega_link']})"
        )

    # 4. file size
    if old["size"] > 0:
        shrink_pct = (old["size"] - new["size"]) / old["size"] * 100.0
        if shrink_pct > 25.0:
            failures.append(
                f"file size shrank by {shrink_pct:.1f}% "
                f"({old['size']:,} → {new['size']:,} chars)"
            )

    return (len(failures) == 0, failures)


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser()
    ap.add_argument("old_path", nargs="?",
                    help="Path to the OLD courses.html (or omit and use --old-rev).")
    ap.add_argument("new_path", nargs="?",
                    help="Path to the NEW courses.html (or omit and use --new-rev).")
    ap.add_argument("--old-rev", default="",
                    help="Read OLD from this git revision instead of a path.")
    ap.add_argument("--new-rev", default="",
                    help="Read NEW from this git revision instead of a path.")
    ap.add_argument("--git-path",
                    default="ai-academy/courses.html",
                    help="When using --old-rev/--new-rev, the repo-relative path "
                         "to read from (default ai-academy/courses.html).")
    return ap.parse_args()


def main() -> int:
    args = parse_args()

    if args.old_rev:
        old_text = read_at_revision(args.old_rev, args.git_path)
        old_label = f"{args.old_rev}:{args.git_path}"
    elif args.old_path:
        old_text = Path(args.old_path).read_text(encoding="utf-8", errors="replace")
        old_label = args.old_path
    else:
        print("ERROR: pass either old_path positional or --old-rev", file=sys.stderr)
        return 2

    if args.new_rev:
        new_text = read_at_revision(args.new_rev, args.git_path)
        new_label = f"{args.new_rev}:{args.git_path}"
    elif args.new_path:
        new_text = Path(args.new_path).read_text(encoding="utf-8", errors="replace")
        new_label = args.new_path
    else:
        print("ERROR: pass either new_path positional or --new-rev", file=sys.stderr)
        return 2

    if not new_text:
        print(f"ERROR: could not read {new_label}", file=sys.stderr)
        return 2

    if not old_text:
        # Old version doesn't exist (e.g. file was just added) — nothing
        # to compare against, so pass.
        print(f"INFO: {old_label} not found / empty — skipping guard.")
        return 0

    om = metrics(old_text)
    nm = metrics(new_text)

    print(f"sanity check  {old_label}  →  {new_label}")
    print(f"  size:        {om['size']:>10,} → {nm['size']:>10,} chars")
    print(f"  mega-cats:   {om['n_cats']:>10} → {nm['n_cats']:>10}")
    print(f"  mega-links:  {om['n_mega_link']:>10} → {nm['n_mega_link']:>10}")

    ok, failures = evaluate(om, nm, label_old=old_label, label_new=new_label)
    if ok:
        print("  result:      OK — within tolerance.")
        return 0

    # Bypass: explicit env var or commit-message marker on the new rev.
    skip_env = os.environ.get("COURSES_GUARD_SKIP", "").strip()
    msg = ""
    if args.new_rev:
        msg = commit_message_for(args.new_rev)
    bypass = bool(skip_env) or "[skip-courses-guard]" in msg

    print()
    print(f"⚠ {len(failures)} sanity-check finding(s):")
    for f in failures:
        print(f"  - {f}")

    if bypass:
        print()
        print("BYPASS: COURSES_GUARD_SKIP env var or [skip-courses-guard] marker "
              "in commit message — exiting 0 despite findings.")
        return 0

    print()
    print("This pattern matches the 2026-04-29 incident where a stale local")
    print("courses.html was committed alongside an unrelated mass retrofit and")
    print("silently destroyed the mega-menu structure.")
    print()
    print("To fix:")
    print("  1. Pull latest main:        git pull --rebase --autostash origin main")
    print("  2. Re-stage only the files you actually meant to change.")
    print("  3. Recommit and re-push.")
    print()
    print("If the change is genuinely intentional (e.g. you're restructuring")
    print("the nav on purpose), bypass with one of:")
    print("  - add literal token [skip-courses-guard] to your commit message")
    print("  - export COURSES_GUARD_SKIP=1 before the push")
    return 1


if __name__ == "__main__":
    sys.exit(main())
