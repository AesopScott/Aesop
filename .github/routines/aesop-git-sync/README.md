# Aesop Git Sync — Claude Routine

## What it does
Produces a daily Markdown health report on the state of the
`AesopScott/Aesop` remote. Read-only. Runs on Anthropic's
infrastructure.

## What it reports
- **Last 10 commits on `main`** — SHA, author, timestamp, subject.
- **Anomalies:**
  - Auto-sync noise (drift-commit loop thrashing)
  - Merge-conflict markers accidentally pushed (`<<<<<<<` / `=======` / `>>>>>>>`)
  - Possible force-push rewrites (duplicate subjects within 1 min)
  - Commits by unexpected authors
  - Truncation-repair events
- **Long-lived branches** — anything non-main, with staleness flags
  (idle > 30 days while ahead of main; `claude/*` branches idle > 7 days).
- **Deploy surface freshness** — checks that `stats.json`,
  `ai-news/articles-index.json`, `course-registry.json`, and
  `eval-index.json` are being updated on schedule.

## Inputs
- **Connectors:** `github` (read-only on AesopScott/Aesop).
- **Schedule:** daily, 13:00 UTC (adjust in the Routine UI).
- **Repo:** AesopScott/Aesop.
- **Secrets needed:** none. This routine doesn't use GitHub Actions.

## Outputs
- A single Markdown report in the routine's run log.
- No commits. No pushes. No issues filed. No files written anywhere.

## Replaces
The Cowork-scheduled skill `aesop-git-sync-v2` at
`.github/scheduled/aesop-git-sync-v2/`. The current skill clones the
repo to `/tmp` and runs git commands in a sandbox shell. The Claude
Routine version uses the GitHub API directly (no clone, no shell).

**Migration:**
1. Configure this routine in Claude Code with the daily schedule.
2. Verify the first 3–5 daily reports look reasonable.
3. Delete `.github/scheduled/aesop-git-sync-v2/`.
4. **Important:** `aesop-git-sync-v2/SKILL.md` currently has a
   hardcoded GitHub PAT on line 14 (`ghp_RW2RCjPWg4...`). When you
   retire the skill, **revoke that PAT on GitHub**. The Claude
   Routine uses the connector's own auth and does not need it.

## How to test manually
In the Claude Routine UI, click "Run now." You should see the
Markdown report in the run output within 10–30 seconds (depending on
how many commits and branches are queried).

## Guardrails the prompt enforces
- **Read-only.** The prompt explicitly forbids any write calls
  through the GitHub connector: no commits, no branches, no issues,
  no PRs.
- **No shell.** The routine uses the connector's API surface only —
  no clone, no bash, no filesystem writes.
- **No retries.** If the connector fails, the routine reports the
  failure and stops.
- **Secrets are never echoed.** If the routine discovers a PAT-like
  string in commit history, it notes the presence but quotes nothing.

## The prompt itself
See [`ROUTINE.md`](./ROUTINE.md) — paste its contents into the
Instructions field of the Claude Routine.
