# Truncation Sweep — Claude Routine

## What it does
Runs twice daily (06:00 and 18:00 UTC) to detect and repair files in
the `AesopScott/Aesop` repository that were accidentally truncated by
a mid-write interruption. Updates `aip/truncation-report.md` on every
run — even clean ones — so the commit log proves the routine is alive.

## Flow
1. Collect files changed in the last 20 minutes from `main` commits
   (15-min interval + 5-min overlap = no gaps).
2. For each candidate, compare current content vs. the prior version.
3. Flag files that shrank ≥25% and lost structural closing markers
   (`</body>`, `</html>`, etc.) or end abruptly — or JSON that was
   valid and no longer parses.
4. Walk git history (up to 50 commits back) to find the last intact
   version of each flagged file.
5. Restore truncated files; record unresolvable ones without touching them.
6. Update `aip/truncation-report.md` with the run timestamp and findings.
7. Commit only when repairs are made, or at 06:00 UTC daily heartbeat.
   Clean non-heartbeat runs do not commit (no log noise at 96 runs/day).

## Inputs
- **Connectors:** `github` (read + write on `AesopScott/Aesop`).
  No `web_search` or `web_fetch` needed.
- **Schedule:** every 15 minutes.
- **Repo:** `AesopScott/Aesop`, branch `main`.

## Outputs
- Repaired file(s) overwritten with last intact content (if any).
- `aip/truncation-report.md` updated with run stats and findings.
- One commit on `main`, pushed.

## Replaces
The GitHub Actions workflow `.github/workflows/truncation-repair.yml`,
which ran the Python script `.github/scripts/repair_truncation.py` on a
GitHub-hosted runner.

**Migration:** once this routine has run cleanly at both UTC windows for
1 week, delete `.github/workflows/truncation-repair.yml`.
The Python script at `.github/scripts/repair_truncation.py` can be kept
as a local/manual fallback or deleted at the same time — it has no
ongoing scheduled role once this routine is active.

## How to test
In the Claude Routine UI, click "Run now." Verify:
- One commit lands on `main` with the `[skip ci]` tag.
- `aip/truncation-report.md` has today's timestamp.
- Any known-truncated files are restored (or listed as unresolved).

## Failure modes
- **No recent commits** → routine scans zero candidates, writes a
  clean heartbeat report, commits, and exits normally.
- **Push rejected (main moved)** → routine rebases once and retries;
  stops if it still fails. Will never force-push.
- **File unresolvable** → listed in the report as "No intact version
  found in recent history." No change written to that file.

## Guardrails the prompt enforces
- Only repairs files with confirmed structural truncation signals.
- Only restores content from a prior git commit — never synthesizes
  replacement content.
- Never touches `.github/`, secrets, or config files.
- Never force-pushes.
- Always appends `[skip ci]` to commit messages.
