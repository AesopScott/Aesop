#!/usr/bin/env python3
"""Repository health tripwire for Aesop."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OBSIDIAN_BUILD = Path("G:/My Drive/Aesop Academy/Obsidian/Aesop_Build")

JSON_TARGETS = [
    ROOT / "ai-academy/modules/course-registry.json",
    ROOT / "ai-academy/modules/courses-data.json",
    ROOT / "stats.json",
    ROOT / "file-versions.json",
]

SECRET_PATTERNS = [
    re.compile(r"sk-ant-[A-Za-z0-9_-]+"),
    re.compile(r"github_pat_[A-Za-z0-9_]+"),
    re.compile(r"ghp_[A-Za-z0-9_]+"),
    re.compile(r"define\(\s*['\"](?:AZURE_CLIENT_SECRET|DB_PASS)['\"]\s*,\s*['\"][^'\"]+['\"]"),
]

SECRET_CHECK_FILES = [
    ROOT / "scheduling/config.php",
    ROOT / "aesop-api/proxy.php",
    ROOT / "aesop-api/archive/proxy.php",
]

REQUIRED_DEPLOY_EXCLUDES = [
    "**/secrets.local.php",
    "**/config.local.php",
    "**/archive/**",
    "**/aesop-api/archive/**",
]


def git_tracked(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    result = subprocess.run(
        ["git", "ls-files", "--error-unmatch", rel],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.returncode == 0


def main() -> int:
    failures: list[str] = []

    for path in JSON_TARGETS:
        if not path.exists():
            failures.append(f"Missing JSON target: {path}")
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            failures.append(f"Invalid JSON in {path}: {exc}")

    for path in SECRET_CHECK_FILES:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                failures.append(f"Tracked secret-like value remains in {path}")
                break

    for local_secret in [ROOT / "secrets.local.php", ROOT / "scheduling/config.local.php"]:
        if git_tracked(local_secret):
            failures.append(f"Local secret file is tracked: {local_secret}")

    deploy = ROOT / ".github/workflows/deploy.yml"
    deploy_text = deploy.read_text(encoding="utf-8", errors="replace") if deploy.exists() else ""
    for item in REQUIRED_DEPLOY_EXCLUDES:
        if item not in deploy_text:
            failures.append(f"Deploy workflow is missing exclude: {item}")

    versions = json.loads((ROOT / "file-versions.json").read_text(encoding="utf-8"))
    version = versions.get("projectVersion")
    if not version:
        failures.append("file-versions.json is missing projectVersion.")
    else:
        changelog = OBSIDIAN_BUILD / "4-Changelog.md"
        build_plan = OBSIDIAN_BUILD / "3-Build-Plan.md"
        if not changelog.exists() or f"| {version} |" not in changelog.read_text(encoding="utf-8", errors="replace"):
            failures.append(f"Aesop changelog is missing version row {version}.")
        if not build_plan.exists() or f"v{version}" not in build_plan.read_text(encoding="utf-8", errors="replace"):
            failures.append(f"Aesop build plan is missing current phase v{version}.")

    if failures:
        print("FAIL aesop-sync")
        for item in failures:
            print(f"- {item}")
        return 1

    print(f"PASS aesop-sync v{version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
