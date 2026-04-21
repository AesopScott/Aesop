# Panel Review Rotation — Claude Routine

## What it does
Each Monday at 09:00 UTC, selects the highest-priority unreviewed (or
longest-since-reviewed) live course, reads all of its module HTML files,
and scores each module against the full five-dimension AESOP curriculum
rubric. Writes the eval-report.json and updates the eval-index. Commits
directly to `main`.

## Flow
1. Read `eval-index.json` + `course-registry.json` to identify the
   next course to review (never reviewed → oldest review date → lowest
   moduleCount vs. files present).
2. List `ai-academy/modules/{course-id}/` to find all `*-m{N}.html` files.
3. Read each module file in full.
4. Score every module across all five rubric dimensions (D1–D5) with
   per-criterion scores 0–5 (weighted criteria counted ×2 toward total).
   Acting as the **Claude reviewer**: primary focus Narrative & Curriculum
   Integrity, but all dimensions scored.
5. Write `ai-academy/modules/{course-id}/{course-id}-eval-report.json`.
6. Update `ai-academy/modules/eval-index.json` (date, reviewers, moduleCount,
   panelAverage).
7. Commit + push to `main`.

## Inputs
- **Connectors:** `github` (read + write on `AesopScott/Aesop`).
  No `web_search` or `web_fetch` needed.
- **Schedule:** Mondays, 09:00 UTC.
- **Repo:** `AesopScott/Aesop`, branch `main`.

## Outputs per run
- One eval-report.json written (or overwritten).
- `eval-index.json` updated.
- One commit on `main`, pushed.

## Rubric summary (quick reference)
| Dim | Name                  | Max  | Primary Role |
|-----|-----------------------|------|--------------|
| D1  | Narrative Integrity   | 25   | Claude       |
| D2  | Concept Accuracy      | 20   | Gemini       |
| D3  | Level Appropriateness | 20   | ChatGPT      |
| D4  | Delivery Architecture | 15   | All equal    |
| D5  | Applied Outcome       | 20   | All (override: <8 = auto-FAIL) |

**Verdicts:**
- PASS: ≥80 total, D5≥8
- PASS W/ NOTES: 70–79 total, D5≥8
- NEEDS REVISION: 55–69 total, D5≥8
- FAIL: <55 total, or D5<8

## Replaces
Manual panel reviews currently triggered from the review admin pages
(`review/AESOP-Panel-Scoring-Dashboard.html`,
`review/AESOP-Safety-Scheduler-v1.3.html`). Those pages remain
usable for on-demand / human-override reviews; this routine
automates the weekly Claude-reviewer pass so the backlog of
unreviewed courses gets covered systematically.

No GitHub Actions workflow to delete — this is net-new automation.

## How to test
In the Claude Routine UI, click "Run now." Verify:
- One commit lands on `main`.
- The commit touches exactly one eval-report.json + eval-index.json.
- `eval-index.json` has today's date and `"reviewers": ["Claude"]` for
  the reviewed course.
- The eval-report.json is valid JSON with one entry per module.

## Failure modes
- **Module files not found** → module recorded with scores 0 and a
  "file missing" note; run still commits and updates the index.
- **Push rejected (main moved)** → rebase once, retry; stops if still
  failing; never force-pushes.
- **All courses already reviewed recently** → selects the oldest
  review date; every course gets refreshed on a rolling basis.

## What the routine does NOT do
- Does not score the Gemini, ChatGPT, or Perplexity reviewer columns.
  Those panels require those models to run their own evaluations.
- Does not modify any module HTML files.
- Does not trigger any UI rebuild or cache invalidation.
