# AESOP AI Academy — Claude Code Guidelines

## Session Startup (READ FIRST) — MANDATORY VERIFICATION CHECKLIST

**⚠️ BLOCKING REQUIREMENT: Verify these four items BEFORE answering any user question.**

### 1. Load All Memory Files
Read `C:\Users\scott\.claude\projects\C--Users-Scott-Code-Aesop\memory\MEMORY.md` and every `.md` file it references. Confirm at least 14+ memory files loaded (feedback_*, project_*).

### 2. Verify Obsidian Connection
Test connection to Obsidian REST API:
```bash
curl -s -H "Authorization: Bearer 6391d0528f05cc0fa09bef6519476d2b7a4974633f047c02e7d84418aee71530" http://127.0.0.1:27123/vault/
```
Must return `"files"` array with `"Northstar/"` and `"Sessions/"` folders.

### 3. Read Previous Session Logs
Fetch list of previous Northstar sessions from Obsidian:
```bash
curl -s -H "Authorization: Bearer 6391d0528f05cc0fa09bef6519476d2b7a4974633f047c02e7d84418aee71530" http://127.0.0.1:27123/vault/Northstar/ | grep session_
```
Read the most recent session file to understand what was done last.

### 4. Confirm Session Logging Enabled
Verify you can write to Obsidian. After this session ends, you will POST the session log to:
```
POST http://127.0.0.1:27123/vault/northstar/session_[ISO-datetime].md
```
Include: what you did, what worked, what didn't work, links & references.

**Then confirm all four items in your response to the user** before proceeding with any work.

## Layout & Page Width

- Content sections use `padding: 0 12.5%` on left and right — not a fixed width or max-width constraint.
- `body` minimum width: `900px`.
- Never constrain content to narrow fixed widths (760–800px range is explicitly off-limits).
- Full-bleed sections (hero banners, nav bars, footers) span 100% width; their inner content uses the 12.5% padding rule.

## Design System

- Colors: `--navy: #0d1b2a`, `--gold: #c9a05a`, `--cream: #faf8f4`
- Fonts: Playfair Display (display/headings), DM Sans (body)
- Reference `academy-theme.css` and `academy-dark-mode.css` for shared tokens.

## Git & Deployment

- Commits to `main` deploy automatically to Mocahost via FTP (`deploy.yml`).
- Standing authorization to commit and push every change to `main` immediately — no need to ask.
- Use `git -C "/path"` instead of `cd` — `cd` triggers permission prompts.

## Northstar Server

- **NEVER kill, stop, or restart the Northstar server** — restarting creates a restart loop.
- If server.js changes require a restart, **REQUEST it from the user** — do not execute the restart yourself.
- mockup.html changes take effect on next browser reload (no server restart needed).

## Northstar Files — Local Only

**Northstar source files are maintained locally ONLY. They are NOT in GitHub and NOT synced to any remote server.**

- **Location:** `C:\Users\Scott\Code\Northstar`
- Files: `server.js`, `mockup.html`, and dependencies
- These files are local development files that you may edit directly
- Do not look for them elsewhere; this is the authoritative location
- Changes made here do not auto-sync anywhere — they are local-only until user manually commits/pushes
