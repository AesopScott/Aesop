#!/usr/bin/env python3
"""
self_heal.py — AI-powered workflow repair agent.

Fetches the logs from a failed GitHub Actions run, sends them to Claude
along with the relevant source files, applies any suggested fixes, commits
them, and re-triggers the failed workflow.

Usage (called by self-heal.yml):
    python .github/scripts/self_heal.py \
        --run-id <run_id> \
        --workflow-file <workflow_filename> \
        --attempt <attempt_number>

Requires:
    ANTHROPIC_API_KEY   Claude API key
    AIP_COMMIT_TOKEN    GitHub PAT with repo + actions write scope
    GITHUB_REPOSITORY   Set automatically by GitHub Actions (owner/repo)
"""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

REPO       = Path(__file__).resolve().parents[2]
SCRIPTS    = REPO / ".github" / "scripts"
WORKFLOWS  = REPO / ".github" / "workflows"
MAX_ATTEMPTS = 3

# Which script files are relevant to each workflow
WORKFLOW_SCRIPTS = {
    "register-courses.yml":       ["add_course.py", "notify_registration.py",
                                   "build_registry.py", "build_stats.py"],
    "auto-activate-courses.yml":  ["auto_activate_courses.py", "build_registry.py",
                                   "build_stats.py"],
    "update-stats.yml":           ["build_stats.py"],
    "aip-autopatch.yml":          ["aip_autopatch.py"],
    "aip-generate.yml":           ["aip_research_agent.py"],
    "k12-autopatch.yml":          ["aip_autopatch.py"],
    "k12-research.yml":           ["k12_research_agent.py"],
    "index-corpus.yml":           ["index_aesop.py"],
    "truncation-repair.yml":      ["repair_truncation.py"],
    "backup-firebase.yml":        ["backup_firebase.py"],
}


def run(cmd: str, check: bool = True) -> str:
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"Command failed: {cmd}")
        print(result.stderr[-1000:])
        sys.exit(1)
    return (result.stdout + result.stderr).strip()


def fetch_logs(run_id: str) -> str:
    """Get the failed step logs for a workflow run via gh CLI."""
    logs = run(f"gh run view {run_id} --log-failed", check=False)
    if not logs:
        logs = run(f"gh run view {run_id} --log", check=False)
    # Truncate to last 12k chars — most relevant errors are at the end
    return logs[-12000:] if len(logs) > 12000 else logs


def load_source_files(workflow_file: str) -> dict[str, str]:
    """Load the workflow file and its related scripts."""
    sources = {}

    # The workflow itself
    wf_path = WORKFLOWS / workflow_file
    if wf_path.exists():
        sources[f".github/workflows/{workflow_file}"] = wf_path.read_text(encoding="utf-8")

    # Related scripts
    for script_name in WORKFLOW_SCRIPTS.get(workflow_file, []):
        path = SCRIPTS / script_name
        if path.exists():
            sources[f".github/scripts/{script_name}"] = path.read_text(encoding="utf-8")

    return sources


def build_prompt(workflow_file: str, run_id: str, logs: str,
                 sources: dict[str, str]) -> str:
    source_block = ""
    for path, content in sources.items():
        source_block += f"\n### {path}\n```\n{content}\n```\n"

    return f"""A GitHub Actions workflow has failed and needs to be repaired.

Workflow: {workflow_file}
Run ID: {run_id}

## Failed step logs
```
{logs}
```

## Source files
{source_block}

Analyze the failure carefully. Common causes include: Python exceptions, missing
files, bad JSON, regex failures, import errors, subprocess failures, API errors.

Respond with a JSON object and nothing else:

If you can fix it:
{{
  "diagnosis": "one sentence describing the root cause",
  "fixable": true,
  "files": [
    {{
      "path": "relative/path/from/repo/root",
      "content": "complete new file content"
    }}
  ]
}}

If you cannot fix it automatically (e.g. missing secret, infra issue, data problem):
{{
  "diagnosis": "one sentence describing why it failed",
  "fixable": false,
  "reason": "why automatic repair isn't possible"
}}

Important: only include files you are actually changing. Preserve all existing
logic unless it is the direct cause of the failure."""


def call_claude(prompt: str) -> dict:
    import anthropic
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=8096,
        messages=[{"role": "user", "content": prompt}],
    )

    text = response.content[0].text.strip()

    # Strip markdown code fences if Claude wrapped the JSON
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)

    return json.loads(text)


def apply_fixes(files: list[dict]) -> list[str]:
    """Write fixed file contents to disk. Returns list of changed paths."""
    changed = []
    for f in files:
        path = REPO / f["path"]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f["content"], encoding="utf-8")
        changed.append(f["path"])
        print(f"  ✓ Fixed: {f['path']}")
    return changed


def commit_and_push(changed: list[str], diagnosis: str, attempt: int) -> None:
    run("git config user.name 'Self-Heal Bot'")
    run("git config user.email 'bot@aesopacademy.org'")
    for path in changed:
        run(f"git add {path}")
    run(f'git commit -m "self-heal(attempt {attempt}): {diagnosis}"')
    run("git pull --rebase origin main")
    run("git push")


def rerun_workflow(run_id: str) -> None:
    result = run(f"gh run rerun {run_id} --failed", check=False)
    print(f"  Re-run triggered: {result or 'ok'}")


def notify_unfixable(workflow_file: str, run_id: str, diagnosis: str,
                     reason: str, attempt: int) -> None:
    """Print a clear summary — the notify script handles email separately."""
    print("\n" + "=" * 60)
    print("SELF-HEAL: Could not auto-repair")
    print(f"  Workflow:  {workflow_file}")
    print(f"  Run ID:    {run_id}")
    print(f"  Attempt:   {attempt}/{MAX_ATTEMPTS}")
    print(f"  Diagnosis: {diagnosis}")
    print(f"  Reason:    {reason}")
    print("=" * 60)

    # Write a report for the notification script to pick up
    report_path = REPO / "aip" / "self-heal-report.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps({
        "status":    "unfixable",
        "workflow":  workflow_file,
        "run_id":    run_id,
        "attempt":   attempt,
        "diagnosis": diagnosis,
        "reason":    reason,
    }, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id",        required=True)
    parser.add_argument("--workflow-file", required=True)
    parser.add_argument("--attempt",       type=int, default=1)
    args = parser.parse_args()

    if args.attempt > MAX_ATTEMPTS:
        print(f"Max repair attempts ({MAX_ATTEMPTS}) reached — giving up.")
        notify_unfixable(args.workflow_file, args.run_id,
                         "Max attempts exceeded", "Too many consecutive failures",
                         args.attempt)
        sys.exit(0)

    print(f"\n── Self-Heal: {args.workflow_file} (attempt {args.attempt}/{MAX_ATTEMPTS}) ──\n")

    logs    = fetch_logs(args.run_id)
    sources = load_source_files(args.workflow_file)
    prompt  = build_prompt(args.workflow_file, args.run_id, logs, sources)

    print("Sending logs to Claude for diagnosis…")
    result = call_claude(prompt)

    print(f"\nDiagnosis: {result['diagnosis']}")

    if not result.get("fixable"):
        notify_unfixable(args.workflow_file, args.run_id,
                         result["diagnosis"], result.get("reason", "unknown"),
                         args.attempt)
        sys.exit(0)

    print("\nApplying fixes…")
    changed = apply_fixes(result["files"])

    if not changed:
        print("No files changed — nothing to commit.")
        sys.exit(0)

    print("\nCommitting and pushing…")
    commit_and_push(changed, result["diagnosis"], args.attempt)

    print("\nRe-running failed workflow…")
    rerun_workflow(args.run_id)

    print(f"\n✓ Self-heal complete. Attempt {args.attempt} — re-run triggered.")


if __name__ == "__main__":
    main()
