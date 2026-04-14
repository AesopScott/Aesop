---
name: weekly-site-audit-v2
description: Weekly filename/ID audit of the Aesop site (mounts C:\Users\scott\Code\Aesop)
---

Weekly site audit — scan all active HTML pages in the live Aesop repo for filename/ID/title mismatches and append a dated section to the Obsidian note AESOP/Filenames & IDs.md.

Setup (required every run):
1. Mount the canonical repo via request_cowork_directory with path: C:\Users\scott\Code\Aesop
2. Configure git identity (in case any follow-up commit is needed):
   `git -C /sessions/$SESSION_ID/mnt/Aesop config user.email "ravenshroud@gmail.com" && git -C /sessions/$SESSION_ID/mnt/Aesop config user.name "Scott"` (adjust mount path to match what request_cowork_directory returned)

Audit steps:
1. Run `python3 audit_modules.py` (it lives at the repo root) OR re-run the same scan from the previous version of this task — whichever is still present in the repo.
2. Extract the mismatch list from its output.
3. Load the previous audit's mismatch list from AESOP/Filenames & IDs.md (via obsidian MCP). Diff current vs previous: what's new, what's resolved.
4. Append a dated section to AESOP/Filenames & IDs.md with:
   - Date header
   - Total pages scanned
   - Mismatch count
   - Newly-introduced mismatches (flagged NEW)
   - Resolved-since-last-run (flagged RESOLVED)
   - Full current mismatch list

If the audit script is missing, report that and stop. Do NOT modify HTML files from this task — it's read-only audit + Obsidian write only.