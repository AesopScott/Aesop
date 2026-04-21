# Broken Link / 404 Crawler — Claude Routine

## What it does
Runs every Sunday at 10:00 UTC. Fetches all live course module URLs,
seed pages, and a spot-check of external links on `aesopacademy.org`.
Records 404s, server errors, and redirects in `aip/link-check-report.md`.
Commits on every run — clean or not — so the timestamp proves it ran.

## Flow
1. Build URL list from seed pages + every live course module URL from
   `course-registry.json` + language course pages from `_meta.languages`.
2. Fetch each URL via `web_fetch`; record status code and redirect chain.
3. Spot-check first 20 external links found on the homepage/courses page.
4. Classify results: 404 (hard error), other error (transient), redirect
   (informational), OK.
5. Write `aip/link-check-report.md` with full findings.
6. Commit `[skip ci]` + push to `main`.

## Inputs
- **Connectors:** `github` (read on `AesopScott/Aesop`), `web_fetch`.
- **Schedule:** Sundays, 10:00 UTC.
- **Repo:** `AesopScott/Aesop`, branch `main`.

## Outputs
- `aip/link-check-report.md` — status badge, 404 list, error list,
  redirect list, external spot-check, stats.
- One `[skip ci]` commit on `main`, pushed.

## Replaces
The live-site HTTP check (Check 5) from `.github/scripts/audit_courses.py`,
which runs inside `audit-courses.yml`. That check hits the live server
synchronously during the daily CI job. Moving it to this weekly routine:
- Removes network I/O from the daily CI job (faster, cheaper).
- Gives a dedicated weekly cadence appropriate for link rot (which accrues
  over days/weeks, not hours).
- Adds external link spot-checking — net-new capability.

**This is net-new automation** — no workflow to delete. Once this routine
is running, the live-URL block of `audit_courses.py` can optionally be
removed, but it's safe to leave it too (duplicate checking is harmless).

## How to test
In the Claude Routine UI, click "Run now." Verify:
- One commit lands on `main` with the `[skip ci]` tag.
- `aip/link-check-report.md` has today's timestamp and a URL count.
- Any known-missing pages appear in the 404 section.

## Failure modes
- **web_fetch unavailable** → URLs logged as "fetch error" not "404";
  routine still writes the report and commits.
- **Rate limiting from server** → routine slows down (≤5 req/s) and
  records any HTTP 429s in the errors section.
- **Push rejected (main moved)** → rebase once, retry; never force-pushes.
- **Large registry** → routine may check 200+ URLs; this is expected
  and within normal `web_fetch` capacity for a weekly run.

## Guardrails
- Never modifies site files — `aip/link-check-report.md` only.
- Never crawls external domains recursively.
- Always commits, even on a clean run (heartbeat).
