# Registry & Filesystem Audit — Claude Routine

## What it does
Runs daily at 08:00 UTC. Verifies that the three course sources of truth —
`course-registry.json`, `courses.html`, and `electives-hub.html` — are
internally consistent and that every referenced file actually exists in
the repo. Writes `aip/audit-report.md` on every run and commits it.

## Flow
1. Read + validate `course-registry.json`: check all course directories
   and module HTML files exist; flag extra or missing files.
2. Audit `courses.html`: check all internal `/ai-academy/` links resolve;
   flag any `?course=` IDs not in the registry.
3. Audit `electives-hub.html`: check all BASE_COURSES directories exist;
   flag any not in registry.
4. Cross-reference all three: flag courses in registry not linked from
   courses.html, courses missing from electives-hub, and mismatches
   between courses.html and electives-hub.
5. Write `aip/audit-report.md` with full findings (errors / warnings /
   stats) and a run timestamp.
6. Commit `[skip ci]` + push to `main`.

## Inputs
- **Connectors:** `github` (read + write on `AesopScott/Aesop`).
  No `web_search` or `web_fetch` needed.
- **Schedule:** daily, 08:00 UTC (matching the old GitHub Actions cadence).
- **Repo:** `AesopScott/Aesop`, branch `main`.

## Outputs
- `aip/audit-report.md` — markdown report with timestamp, status badge,
  error/warning list, and stats row.
- One `[skip ci]` commit on `main`, pushed.

## Severity levels
| Level | Meaning |
|-------|---------|
| 🔴 ERROR | Broken reference that will cause a user-visible failure (dead link, missing file, invalid JSON). Requires fix. |
| 🟡 WARNING | Inconsistency that could cause confusion but doesn't break navigation (course in registry but not linked from courses.html, extra module files, etc.). Review when convenient. |
| 🟢 CLEAR | All checks passed. |

## Replaces
The GitHub Actions workflow `.github/workflows/audit-courses.yml` (Checks
1–4 and the module file integrity bonus check). The live-URL HTTP check
(Check 5 of the Python script) is handled separately by **Routine #5:
Broken Link / 404 Crawler**.

**Migration:** once this routine has run cleanly for 5 days, delete
`.github/workflows/audit-courses.yml`. The Python script at
`.github/scripts/audit_courses.py` can remain as a manual/local fallback
or be removed at the same time.

## How to test
In the Claude Routine UI, click "Run now." Verify:
- One commit lands on `main` with the `[skip ci]` tag.
- `aip/audit-report.md` has today's timestamp.
- Any known broken links or missing files appear in the report.

## Failure modes
- **course-registry.json missing or invalid** → routine records
  `CRITICAL` in the report and still commits; does not attempt
  subsequent checks that depend on the registry.
- **Push rejected (main moved)** → rebase once, retry; stops if still
  failing; never force-pushes.
- **courses.html or electives-hub.html missing** → recorded as ERROR
  in their respective sections; remaining checks that don't need those
  files still run.

## Guardrails
- Read-and-report only — never modifies HTML, JSON, or any asset files.
- Only write target is `aip/audit-report.md`.
- Always commits (heartbeat), even on a clean run.
