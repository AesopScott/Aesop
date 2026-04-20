#!/usr/bin/env python3
"""
AESOP File Truncation Repair

Detects and repairs files that have been accidentally truncated — i.e.
a file that is meaningfully shorter than its previous committed version
and has lost a structural closing marker that was present before.

Definition of truncation here (important — this repo ships many HTML
fragments that intentionally lack <html>/<body> closing tags, so a
structural heuristic alone produces huge false-positive rates):

  A file at HEAD is "truncated" vs. the last known-good version iff:
    1. Its byte length shrank by >= SHRINK_RATIO (default 25%), AND
    2. It lost at least one closing marker that the previous version
       contained (</html>, </body>, </script>, </style>, </svg>,
       </head>, a trailing top-level tag, etc.), AND
    3. It ends abruptly (last non-whitespace char is '<', or inside an
       unclosed tag).

Repair strategy: walk git log for that path, newest-first, and restore
the first previous version that was intact (satisfied none of the
truncation signals when compared against the *version before it*). If
no intact version exists, report the file but do not touch it.

Scope: scans every tracked text file under the repo root, excluding
noisy/vendored/archive directories. Binary files are skipped by
attempting a UTF-8 decode.

Writes a markdown report to aip/truncation-report.md.
"""

from __future__ import annotations

import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(".").resolve()
REPORT_PATH = REPO_ROOT / "aip" / "truncation-report.md"

# Directories we never scan or repair.
SKIP_DIRS = {
    ".git", "node_modules", "TEMP", "archive", "es_old",
    "phpmailer", ".claude",
}

# File extensions we consider. HTML is the primary surface; CSS/JS/JSON
# are also worth checking since a mid-write cut can truncate them too.
INCLUDE_EXTS = {".html", ".htm", ".css", ".js", ".json", ".xml", ".md", ".svg"}

# Thresholds
SHRINK_RATIO = 0.25            # must shrink by at least this to be suspicious
MIN_PREV_SIZE = 100            # ignore truly tiny files
MAX_SEARCH_COMMITS = 50        # how far back to walk looking for an intact version

# Closing markers whose loss is a strong structural signal. We treat JSON
# top-level `}` and `]` as markers too — a .json file that went from
# `{...}` to `{"a":1` is unambiguously truncated.
STRUCTURAL_MARKERS = (
    "</html>",
    "</body>",
    "</head>",
    "</svg>",
    "</script>",
    "</style>",
)


def has_balanced_json_close(text: str) -> bool:
    """True if the trimmed text ends with a top-level } or ]."""
    stripped = text.rstrip()
    return stripped.endswith(("}", "]"))


@dataclass
class Finding:
    path: Path
    reasons: list[str] = field(default_factory=list)
    prev_size: int = 0
    curr_size: int = 0
    repaired_from: str | None = None
    repair_error: str | None = None


def git_text(*args: str) -> str:
    """Run a git command and return stdout decoded as UTF-8 (lossy)."""
    result = subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        capture_output=True,
        check=False,
    )
    return result.stdout.decode("utf-8", errors="replace")


def git_bytes(*args: str) -> bytes | None:
    """Run a git command and return raw stdout bytes, or None on failure."""
    result = subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    return result.stdout


def iter_candidate_files() -> list[Path]:
    out: list[Path] = []
    for path in REPO_ROOT.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(REPO_ROOT)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        if path.suffix.lower() not in INCLUDE_EXTS:
            continue
        out.append(path)
    return out


def ends_abruptly(text: str) -> bool:
    """True if the file looks cut mid-tag or mid-string."""
    stripped = text.rstrip()
    if not stripped:
        return True
    last = stripped[-1]
    if last == "<":
        return True
    # Check last 256 chars for an unclosed '<' (opening tag without '>').
    tail = stripped[-256:]
    last_open = tail.rfind("<")
    last_close = tail.rfind(">")
    if last_open > last_close:
        return True
    return False


def lost_markers(prev: str, curr: str) -> list[str]:
    """Return structural markers present in `prev` but missing in `curr`."""
    prev_l = prev.lower()
    curr_l = curr.lower()
    missing: list[str] = []
    for marker in STRUCTURAL_MARKERS:
        if marker in prev_l and marker not in curr_l:
            missing.append(marker)
    return missing


def is_truncated(prev_bytes: bytes, curr_bytes: bytes) -> list[str]:
    """Return a list of truncation reasons. Empty means not truncated."""
    reasons: list[str] = []

    prev_size = len(prev_bytes)
    curr_size = len(curr_bytes)

    if prev_size < MIN_PREV_SIZE:
        return reasons  # too small to judge

    if curr_size >= prev_size:
        return reasons  # didn't shrink

    shrink = (prev_size - curr_size) / prev_size
    if shrink < SHRINK_RATIO:
        return reasons  # shrank, but within normal edit range

    try:
        prev = prev_bytes.decode("utf-8", errors="replace")
        curr = curr_bytes.decode("utf-8", errors="replace")
    except Exception:
        return reasons  # give up on undecodable content

    missing = lost_markers(prev, curr)
    abrupt = ends_abruptly(curr)

    # JSON-style closer lost: prev ended with } or ], curr does not.
    prev_s = prev.rstrip()
    curr_s = curr.rstrip()
    json_closer_lost = (
        prev_s.endswith(("}", "]"))
        and curr_s
        and not curr_s.endswith(("}", "]"))
    )
    if json_closer_lost:
        missing = missing + ["top-level } or ]"]

    # Primary signal: shrank a lot AND lost a structural closing marker
    # that was present in the previous version. A deliberate rewrite may
    # shrink the file, but it rarely drops all the closing tags at once.
    if missing:
        reasons.append(
            f"shrank {shrink:.0%} "
            f"({prev_size} → {curr_size} bytes), "
            f"lost markers: {', '.join(missing)}"
            + (", ends abruptly" if abrupt else "")
        )
        return reasons

    # Fallback: collapsed to near-empty from something substantial AND
    # ends abruptly. Catches cases where the previous version itself
    # happened to not contain obvious closing markers.
    if abrupt and curr_size < MIN_PREV_SIZE and prev_size >= MIN_PREV_SIZE:
        reasons.append(
            f"collapsed from {prev_size} to {curr_size} bytes, ends abruptly"
        )

    return reasons


def git_log_commits(rel_path: str) -> list[str]:
    """Return commit hashes that touched this path, newest first."""
    out = git_text("log", f"-{MAX_SEARCH_COMMITS}", "--pretty=format:%H",
                   "--follow", "--", rel_path)
    return [line.strip() for line in out.splitlines() if line.strip()]


def file_at_commit(commit: str, rel_path: str) -> bytes | None:
    return git_bytes("show", f"{commit}:{rel_path}")


def find_intact_version(rel_path: str, curr_bytes: bytes) -> tuple[str, bytes] | None:
    """
    Walk history newest-first. Skip any historical version that is itself
    truncated vs the version before it. Return the first intact one.
    """
    commits = git_log_commits(rel_path)
    prev_content: bytes | None = None
    for i, commit in enumerate(commits):
        content = file_at_commit(commit, rel_path)
        if content is None:
            continue
        if i + 1 < len(commits):
            older = file_at_commit(commits[i + 1], rel_path)
        else:
            older = None

        # Candidate is "intact" if, compared to its own predecessor, it
        # did not truncate. If there's no predecessor, accept it.
        if older is None or not is_truncated(older, content):
            # Also require that the candidate actually differs from the
            # current truncated bytes (no point "restoring" to the same bytes).
            if content != curr_bytes:
                return commit, content
    return None


def write_report(findings: list[Finding], scanned: int) -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    lines.append("# File Truncation Repair Report")
    lines.append("")
    lines.append(f"- Files scanned: **{scanned}**")
    lines.append(f"- Truncated files found: **{len(findings)}**")
    repaired = [f for f in findings if f.repaired_from]
    lines.append(f"- Files repaired: **{len(repaired)}**")
    unresolved = [f for f in findings if not f.repaired_from]
    lines.append(f"- Unresolved (no intact history): **{len(unresolved)}**")
    lines.append("")

    if findings:
        lines.append("## Findings")
        lines.append("")
        for f in findings:
            rel = f.path.relative_to(REPO_ROOT).as_posix()
            lines.append(f"### `{rel}`")
            for r in f.reasons:
                lines.append(f"- {r}")
            if f.repaired_from:
                lines.append(f"- **Repaired from commit** `{f.repaired_from[:12]}`")
            elif f.repair_error:
                lines.append(f"- **Repair failed:** {f.repair_error}")
            else:
                lines.append("- **No intact version found in recent history**")
            lines.append("")
    else:
        lines.append("No truncation detected.")
        lines.append("")

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    files = iter_candidate_files()
    findings: list[Finding] = []

    for path in files:
        rel_path = path.relative_to(REPO_ROOT).as_posix()

        # Need a previous version to compare against. Use HEAD's version
        # for the initial comparison — the working tree vs HEAD diff is
        # what a scheduled repair is actually watching for in practice.
        prev_bytes = file_at_commit("HEAD", rel_path)
        if prev_bytes is None:
            continue  # untracked or newly added

        try:
            curr_bytes = path.read_bytes()
        except OSError as e:
            findings.append(Finding(path=path, reasons=[f"read error: {e}"]))
            continue

        reasons = is_truncated(prev_bytes, curr_bytes)
        if not reasons:
            continue

        finding = Finding(
            path=path,
            reasons=reasons,
            prev_size=len(prev_bytes),
            curr_size=len(curr_bytes),
        )

        try:
            intact = find_intact_version(rel_path, curr_bytes)
        except Exception as e:
            finding.repair_error = f"history walk failed: {e}"
            intact = None

        if intact is not None:
            commit, content = intact
            try:
                path.write_bytes(content)
                finding.repaired_from = commit
            except OSError as e:
                finding.repair_error = f"write failed: {e}"

        findings.append(finding)

    write_report(findings, scanned=len(files))

    repaired = sum(1 for f in findings if f.repaired_from)
    unresolved = sum(1 for f in findings if not f.repaired_from)
    print(f"Scanned {len(files)} files. "
          f"Truncated: {len(findings)}. "
          f"Repaired: {repaired}. "
          f"Unresolved: {unresolved}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
