---
name: daily-ai-news-v2
description: Daily AI news digest (writes to ai-news/ in C:\Users\scott\Code\Aesop)
---

Daily AI news digest — compile a short daily AI news summary and save it into the Aesop repo's ai-news/ directory.

This task supports on-demand "Run Now" execution. When triggered manually, it runs the same steps as the scheduled daily run.

Setup (required every run):
1. Mount the canonical repo via request_cowork_directory with path: C:\Users\scott\Code\Aesop
2. Configure git: credential.helper store + the PAT line + user.email and user.name (same as aesop-git-sync-v2).

Steps:
1. Use WebSearch to gather 5-8 significant AI news items from the last 24 hours (prefer: major model releases, notable research, regulation, industry/business moves, incidents). Skip low-signal items.
2. For each item write a JSON article file at ai-news/articles/YYYY-MM-DD-slug.json matching the existing schema:
   ```json
   {
     "id": "YYYY-MM-DD-slug",
     "title": "...",
     "subtitle": "...",
     "date": "YYYY-MM-DD",
     "author": "AESOP AI Engine",
     "category": "Industry|Healthcare|Policy|Safety|Research|Creative AI|...",
     "tags": ["..."],
     "readTime": "3 min read",
     "heroEmoji": "...",
     "body": ["paragraph 1", "paragraph 2", "paragraph 3", "paragraph 4"],
     "sources": [{"title": "...", "url": "..."}],
     "status": "published"
   }
   ```
   Body should be 4 paragraphs written for a student audience: what happened, why it matters, broader context, and a takeaway for learners.
3. Update ai-news/articles-index.json: prepend the new article paths to the existing "articles" array and set "lastUpdated" to today.
4. Run `python3 ai-news/build-articles.py` to generate shareable HTML pages for all articles (including new ones).
5. Git add all new/changed files under ai-news/ and commit with message "daily AI news digest YYYY-MM-DD". Do NOT push — Scott pushes manually via GitHub Desktop.
6. Report: file paths, commit hash, number of items, and the shareable URLs (https://aesopacademy.org/ai-news/articles/{id}.html).

If WebSearch is blocked or returns nothing useful, write a file with a clear "No items today" note rather than skipping — keeps the daily cadence intact.
