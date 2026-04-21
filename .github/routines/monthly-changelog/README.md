# Monthly "What Changed" Digest — Claude Routine

## What it does
On the 1st of each month at 09:00 UTC, reads the last 30 days of `main`
commits, filters out bot/heartbeat noise, groups signal commits by theme,
and publishes a plain-English changelog article to the AI news feed.

## Flow
1. Fetch git log for the previous calendar month from `main`.
2. Strip noise commits (auto-sync, stats refresh, truncation repair,
   audit heartbeats, daily news digests).
3. Group signal commits: new courses, new content, language expansion,
   UI/site improvements, review & scoring, infrastructure.
4. Write `ai-news/articles/YYYY-MM-changelog.json` — four-paragraph
   format (summary / major changes / smaller improvements / what's coming).
5. Prepend to `ai-news/articles-index.json`, bump `lastUpdated`.
6. Commit + push to `main`. The `build-news-html` GitHub Action auto-
   generates the matching HTML page within ~1–2 minutes.

## Inputs
- **Connectors:** `github` (read + write on `AesopScott/Aesop`).
  No `web_search` or `web_fetch` needed.
- **Schedule:** 1st of each month, 09:00 UTC.
- **Repo:** `AesopScott/Aesop`, branch `main`.

## Outputs
- One JSON article at `ai-news/articles/YYYY-MM-changelog.json`.
- Updated `ai-news/articles-index.json`.
- One commit on `main`, pushed.
- (Indirect) HTML article page from `build-news-html` Action.

## Article format
Same four-paragraph schema as daily AI news:
1. Opening summary — commit volume, month's biggest theme, direction.
2. Significant changes in detail — course activations, major features.
3. Smaller improvements — UI, infra, language additions, bug fixes.
4. What's coming — `coming_soon` courses in registry, visible WIP.

Tone: honest, specific, first-person plural. Not marketing copy.

## Net-new capability
This routine has no predecessor. There is no GitHub Actions workflow or
Cowork skill to delete — this is a new monthly article type in the
existing AI news feed.

## How to test
In the Claude Routine UI, click "Run now." Verify:
- One commit lands on `main`.
- `ai-news/articles-index.json` has the changelog path prepended.
- Within ~2 minutes, the HTML article page exists at
  `https://aesopacademy.org/ai-news/articles/YYYY-MM-changelog.html`.

## Failure modes
- **No signal commits** → routine writes a brief "quiet month" article
  rather than skipping; cadence is maintained.
- **Push rejected (main moved)** → rebase once, retry; never force-pushes.
- **build-news-html Action fails** → JSON lands but HTML doesn't; rerun
  the Action or re-push the JSON file to re-trigger it.
