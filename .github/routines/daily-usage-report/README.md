# Daily Usage Cost Report — Claude Routine

## What it does
Runs every morning at 07:00 UTC. Estimates yesterday's API costs from
known routine cadence and typical token budgets — no API key required.
Carries a month-to-date running total and commits `aip/usage-report.md`.

## Flow
1. Determine yesterday's date and day of week.
2. Calculate estimated cost per routine from schedule × token budget × price.
3. Read previous report to carry forward the MTD running total.
4. Overwrite `aip/usage-report.md` with yesterday's breakdown + MTD table.
5. Commit `[skip ci]` + push to `main`.

## Inputs
- **Connectors:** `github` (read + write).
- **Schedule:** daily, 07:00 UTC.
- **Model:** claude-haiku (latest).

## Outputs
- `aip/usage-report.md` — per-routine cost breakdown and MTD running total.
- One `[skip ci]` commit on `main`, pushed.

## How costs are calculated
No live API call is made. Instead, each routine's cost is estimated as:

`runs_yesterday × ((input_tokens / 1M × input_rate) + (output_tokens / 1M × output_rate))`

Token budgets and prices are hardcoded in the routine instructions.
Weekly routines (Broken Link Crawler, Weekly Changelog) count 1 run
only on their scheduled day, 0 runs on other days.

## Limitations
- **Estimates only.** Actual token counts vary run-to-run; these are
  typical-case budgets. Actual billing may differ.
- **No live data.** Switching to real Anthropic usage API data requires
  secrets support in the Routines UI — update the ROUTINE.md when that
  becomes available.
- **Prices may drift.** Update the pricing table in ROUTINE.md if
  Anthropic changes rates.
