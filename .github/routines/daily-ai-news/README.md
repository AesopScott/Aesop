# Daily AI News — Claude Routine

## What it does
Publishes a daily digest of significant AI news to `/ai-news/` on
aesopacademy.org. Runs on Anthropic's infrastructure (no local
machine required).

## Flow
1. Survey the last 24h of AI news via `web_search`.
2. Deduplicate against `ai-news/articles-index.json` (14-day window).
3. Write each story as a JSON article at `ai-news/articles/YYYY-MM-DD-slug.json`.
4. Prepend to `articles-index.json`, bump `lastUpdated`.
5. Commit + push to `main` in one commit.
6. The `build-news-html.yml` GitHub Action runs on JSON push and
   auto-generates the matching shareable HTML page for each new
   article.

## Inputs
- **Connectors:** `github` (read+write on AesopScott/Aesop),
  `web_search`, `web_fetch`.
- **Schedule:** daily, 14:00 UTC (adjust in the Routine UI).
- **Repo:** AesopScott/Aesop, branch `main`.

## Outputs
- 3–8 new JSON article files per run.
- Updated `ai-news/articles-index.json`.
- Commit on `main`, pushed.
- (Indirect, via GitHub Action) HTML pages at
  `ai-news/articles/YYYY-MM-DD-slug.html`.

## Replaces
The Cowork-scheduled skill `daily-ai-news-v2` at
`.github/scheduled/daily-ai-news-v2/`. That skill is clone-based and
requires Scott's local repo to be online to push. The Claude Routine
version removes that dependency — runs entirely on Anthropic's infra
and pushes via the GitHub connector.

**Migration:** once this routine has run cleanly for ~5 days, delete
`.github/scheduled/daily-ai-news-v2/`.

## How to test manually (without waiting for the schedule)
In the Claude Routine UI, click "Run now." The routine will execute
the same steps as a scheduled run. Verify:
- One commit lands on `main`.
- `articles-index.json` has the new paths at the top.
- Within 1–2 minutes, `build-news-html.yml` completes and the HTML
  pages exist alongside the JSON.
- `https://aesopacademy.org/ai-news/` shows the new stories at the
  top (after GitHub Pages deploys, typically ~1 minute after the
  HTML commit).

## Failure modes
- **Web search empty** → routine writes a "No items today" JSON (see
  ROUTINE.md Step 6) and still pushes.
- **Commit rejected (main moved)** → routine rebases once, retries,
  gives up if still failing. It will never force-push.
- **HTML-build Action fails** → JSON lands but HTML doesn't.
  Articles visible in the JSON feed but not as standalone pages.
  Fix the workflow and re-push any JSON to re-trigger.

## Guardrails the prompt enforces
- Never edits existing articles.
- Never touches paths outside `ai-news/articles/` + `articles-index.json`.
- Never force-pushes.
- Four-paragraph house voice: what / why it matters / context /
  takeaway for learners.

## The prompt itself
See [`ROUTINE.md`](./ROUTINE.md) — paste its contents into the
Instructions field of the Claude Routine.
