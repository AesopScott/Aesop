# Weekly Dev Log Update — Claude Routine

## What it does
Every Monday at 09:00 UTC, reads last week's signal commits from `main`,
groups them by date, and inserts new date entries directly into the
`DEV_LOG` JavaScript object inside `development.html`.

## Flow
1. Fetch git log for the last 7 days on `main`.
2. Filter out noise commits (auto-sync, stats refresh, truncation repair,
   audit heartbeats, daily news digests, usage reports).
3. Group signal commits by UTC date.
4. Read `development.html`, find `const DEV_LOG = {`.
5. Insert new date keys (newest first) before existing entries.
   Skip any date that already exists in the object.
6. Commit `Dev log: week of YYYY-MM-DD [skip ci]` + push to `main`.

## Inputs
- **Connectors:** `github` (read + write on `AesopScott/Aesop`).
- **Schedule:** Mondays at 09:00 UTC (`0 9 * * 1`).
- **Model:** claude-haiku (latest).
- **Repo:** `AesopScott/Aesop`, branch `main`.

## Outputs
- Updated `development.html` with new `DEV_LOG` date entries.
- One `[skip ci]` commit on `main`, pushed.

## development.html format
The `DEV_LOG` object uses `"YYYY-MM-DD"` keys mapping to arrays of
commit message strings. The page auto-categorizes each entry using
regex patterns (FIX, FEAT, INFRA, CONTENT, MARKETING, OPS) and renders
a collapsible timeline behind a Firebase admin auth gate.

## Failure modes
- **No signal commits** → routine does nothing; no commit, no file change.
- **Date already exists** → skipped; existing entries are never modified.
- **Push rejected (main moved)** → rebase once, retry; never force-pushes.

## How to test
In the Claude Routine UI, click "Run now." Verify:
- `development.html` has new date entries at the top of `DEV_LOG`.
- One commit lands on `main` with message `Dev log: week of ...`.
- The entries appear in the timeline at `https://aesopacademy.org/development.html`
  (after signing in with admin credentials).
