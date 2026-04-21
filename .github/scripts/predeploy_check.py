#!/usr/bin/env python3
"""
Pre-Deploy Truncation Guard

Runs as a deploy workflow step BEFORE the FTP upload.

For every HTML/CSS/JS/JSON file changed in this push, compares the
current version against its previous committed version.  If a file
looks truncated it is REPAIRED in-place (restored from the most
recent intact git version) so the deploy continues with the good file.

Exit codes:
  0  — all clear (or all repairs succeeded)
  1  — one or more truncated files could NOT be repaired; deploy blocked

After the deploy workflow the repaired files are committed back to
main by a separate "Commit repairs" step in deploy.yml.
"""

from __future__ import annotations

import json as _json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(".").resolve()

SHRINK_RATIO     = 0.25   # 25% byte-count drop triggers inspection
MIN_PREV_SIZE    = 200    # ignore truly tiny files
MAX_HISTORY_LOOK = 30     # how many commits back to search for intact version

STRUCTURAL_MARKERS = (
    "</html>", "</body>", "</head>",
    "</svg>", "</script>", "</style>",
)

INCLUDE_EXTS = {".html", ".htm", ".css", ".js", ".json", ".xml", ".svg"}

SKIP_DIRS = {".git", "node_modules", "TEMP", "archive", "es_old",
             "phpmailer", ".claude", ".github"}


# ── git helpers ──────────────────────────────────────────────────────────────

def git_text(*args: str) -> str:
    r = subprocess.run(["git", *args], cwd=REPO_ROOT,
                       capture_output=True, check=False)
    return r.stdout.decode("utf-8", errors="replace")


def git_raw(*args: str) -> bytes | None:
    r = subprocess.run(["git", *args], cwd=REPO_ROOT,
                       capture_output=True, check=False)
    return r.stdout if r.returncode == 0 else None


def changed_files() -> list[str]:
    """Modified files between HEAD~1 and HEAD."""
    out = git_text("diff", "--name-only", "--diff-filter=M", "HEAD~1", "HEAD")
    return [l.strip() for l in out.splitlines() if l.strip()]


def commit_history(rel: str) -> list[str]:
    out = git_text("log", f"-{MAX_HISTORY_LOOK}", "--pretty=format:%H",
                   "--follow", "--", rel)
    return [l.strip() for l in out.splitlines() if l.strip()]


# ── truncation detection ─────────────────────────────────────────────────────

def _json_valid(raw: bytes) -> bool:
    try:
        _json.loads(raw.decode("utf-8"))
        return True
    except Exception:
        return False


def lost_markers(prev: str, curr: str) -> list[str]:
    pl, cl = prev.lower(), curr.lower()
    return [m for m in STRUCTURAL_MARKERS if m in pl and m not in cl]


def ends_abruptly(text: str) -> bool:
    s = text.rstrip()
    if not s:
        return True
    if s[-1] == "<":
        return True
    tail = s[-256:]
    return tail.rfind("<") > tail.rfind(">")


def truncation_reasons(rel: str, prev_raw: bytes, curr_raw: bytes) -> list[str]:
    reasons: list[str] = []
    ext = Path(rel).suffix.lower()

    # JSON fast path
    if ext == ".json" and len(prev_raw) >= MIN_PREV_SIZE:
        if _json_valid(prev_raw) and not _json_valid(curr_raw):
            try:
                _json.loads(curr_raw.decode("utf-8"))
                err = "unknown"
            except Exception as e:
                err = str(e)[:120]
            reasons.append(f"JSON was valid, now broken: {err}")
            return reasons
        if _json_valid(curr_raw):
            return reasons

    prev_size, curr_size = len(prev_raw), len(curr_raw)
    if prev_size < MIN_PREV_SIZE or curr_size >= prev_size:
        return reasons

    shrink = (prev_size - curr_size) / prev_size
    if shrink < SHRINK_RATIO:
        return reasons

    try:
        prev = prev_raw.decode("utf-8", errors="replace")
        curr = curr_raw.decode("utf-8", errors="replace")
    except Exception:
        return reasons

    missing = lost_markers(prev, curr)
    abrupt  = ends_abruptly(curr)

    if prev.rstrip().endswith(("}", "]")) and curr.rstrip() and \
       not curr.rstrip().endswith(("}", "]")):
        missing = missing + ["top-level } or ]"]

    if missing:
        reasons.append(
            f"shrank {shrink:.0%} ({prev_size}→{curr_size} bytes), "
            f"lost markers: {', '.join(missing)}"
            + (", ends abruptly" if abrupt else "")
        )
    elif abrupt and curr_size < MIN_PREV_SIZE:
        reasons.append(
            f"collapsed to {curr_size} bytes from {prev_size}, ends abruptly"
        )

    return reasons


# ── repair ───────────────────────────────────────────────────────────────────

def find_intact_version(rel: str, bad_raw: bytes) -> tuple[str, bytes] | None:
    """
    Walk git history newest-first; return the first version that
    (a) differs from the broken bytes and (b) is not itself truncated
    vs its own predecessor.
    """
    commits = commit_history(rel)
    for i, commit in enumerate(commits):
        content = git_raw("show", f"{commit}:{rel}")
        if content is None or content == bad_raw:
            continue
        # Validate against its own predecessor
        if i + 1 < len(commits):
            older = git_raw("show", f"{commits[i+1]}:{rel}")
        else:
            older = None
        if older is None or not truncation_reasons(rel, older, content):
            return commit, content
    return None


def repair(rel: str, bad_raw: bytes) -> tuple[bool, str]:
    """Repair file in-place. Returns (success, message)."""
    result = find_intact_version(rel, bad_raw)
    if result is None:
        return False, "no intact version found in recent history"
    commit, good_bytes = result
    try:
        Path(rel).write_bytes(good_bytes)
        return True, f"restored from commit {commit[:12]}"
    except OSError as e:
        return False, f"write failed: {e}"


# ── main ─────────────────────────────────────────────────────────────────────

def main() -> int:
    # No HEAD~1 on first commit — nothing to compare
    check = subprocess.run(
        ["git", "rev-parse", "--verify", "HEAD~1"],
        cwd=REPO_ROOT, capture_output=True
    )
    if check.returncode != 0:
        print("Pre-deploy guard: no previous commit — skipping.")
        return 0

    files = changed_files()
    repaired: list[str]  = []
    blocked:  list[str]  = []

    for rel in files:
        p = Path(rel)
        if p.suffix.lower() not in INCLUDE_EXTS:
            continue
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if not p.exists():
            continue

        prev_raw = git_raw("show", f"HEAD~1:{rel}")
        if prev_raw is None:
            continue
        curr_raw = p.read_bytes()

        reasons = truncation_reasons(rel, prev_raw, curr_raw)
        if not reasons:
            continue

        print(f"\n⚠️  Truncated: {rel}")
        for r in reasons:
            print(f"     {r}")

        ok, msg = repair(rel, curr_raw)
        if ok:
            print(f"   ✅ Repaired — {msg}")
            repaired.append(rel)
        else:
            print(f"   ❌ Repair failed — {msg}")
            blocked.append(rel)

    print()
    total = len(repaired) + len(blocked)
    if total == 0:
        print(f"Pre-deploy guard: {len(files)} changed files checked — all clean. ✅")
        return 0

    if repaired:
        print(f"Pre-deploy guard: {len(repaired)} file(s) repaired and will deploy correctly.")
    if blocked:
        print(f"Pre-deploy guard: {len(blocked)} file(s) COULD NOT be repaired — deploy blocked. 🚨")
        print("  Blocked files:")
        for f in blocked:
            print(f"    {f}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
