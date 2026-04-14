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
2. For each item: headline, 2-3 sentence summary, source link.
3. Write a markdown file at ai-academy/ai-news/YYYY-MM-DD.md (adjust path if ai-news is at repo root — check first with `ls`). Frontmatter should include `date`, `generated_by: daily-ai-news-v2`.
4. Git add + commit the new file with message "daily AI news digest YYYY-MM-DD". Do NOT push — Scott pushes manually via GitHub Desktop.
5. Report: file path, commit hash, number of items.

If WebSearch is blocked or returns nothing useful, write a file with a clear "No items today" note rather than skipping — keeps the daily cadence intact.
