# Daily Usage Cost Report — Claude Routine

## What it does
Runs every morning at 07:00 UTC. Pulls yesterday's token consumption
from the Anthropic usage API, calculates estimated USD costs per model,
carries a month-to-date running total, and commits `aip/usage-report.md`.

## Flow
1. GET Anthropic usage API for yesterday's date — input tokens, output
   tokens, request count, broken down by model.
2. Calculate estimated cost using list prices (Haiku $0.80/$4.00,
   Sonnet $3.00/$15.00, Opus $15.00/$75.00 per MTok in/out).
3. Read previous report to carry forward the MTD running total table.
4. Overwrite `aip/usage-report.md` with yesterday's breakdown + MTD
   cumulative table.
5. Commit `[skip ci]` + push to `main`.

## Inputs
- **Connectors:** `github` (read + write), `web_fetch`.
- **Secret:** `ANTHROPIC_API_KEY` — API key with usage-read access,
  stored in the Routine's secret store (not in the repo).
- **Schedule:** daily, 07:00 UTC.
- **Model:** claude-haiku (latest) — reporting task, no heavy reasoning needed.

## Outputs
- `aip/usage-report.md` — yesterday's per-model breakdown, estimated
  cost by routine, and MTD running total table.
- One `[skip ci]` commit on `main`, pushed.

## Setting up the API key
1. In the Anthropic Console → Settings → API Keys, create a key scoped
   to usage-read (or use your existing key if it has that permission).
2. Add it as `ANTHROPIC_API_KEY` in the Routine's secret configuration
   (not in GitHub Secrets — this is an Anthropic Routine secret).

## Limitations
- **Per-routine cost breakdown is estimated**, not exact. Anthropic's
  usage API reports by model, not by which routine made the call. The
  per-routine numbers are proportional estimates based on known cadence
  and typical token counts.
- **Prices may drift.** The routine uses hardcoded list prices — update
  the ROUTINE.md pricing table if Anthropic changes rates.
- **API availability.** If the usage API is unreachable, the report
  records $0.00 with a note; it does not skip the commit.

## Net-new capability
No predecessor. First time AESOP has automated cost visibility.
