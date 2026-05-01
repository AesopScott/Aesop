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
Content-Type: text/markdown
```
Write the session log as **raw markdown text** (not JSON). Use `-H "Content-Type: text/markdown"` and `--data-binary` in curl.

Include: what you did, what worked, what didn't work, links & references.

**Then confirm all four items in your response to the user** before proceeding with any work.

### 5. Reassess Session Name After Context Load
After loading all memory files and reading the startup checklist items, **reassess the session name** based on what the rules and context reveal. The initial extraction from the user's prompt is a first pass; reading the Obsidian vault and memory files may clarify what the session is *actually* about.

**How to apply:**
- Initial name: Extract 5 words from the user's first message before loading context
- Announce it: "This session: **[Initial Name]**" with the startup verification
- After loading all four startup items, pause and ask: "Does the context I just read suggest a clearer framing of what this session is about?"
- If yes: Announce an updated name: "**Updated session name: [Better Name]**"
- If no: Keep the initial name and proceed
- Use the reassessed name in the Obsidian session log at end-of-session

**Why:** The first message doesn't always make the session's intent fully clear. Rules, previous session logs, and the current state (git, Obsidian, Northstar) provide context that refines the name. A session named "Learn from new session perspective" reads the mandatory startup checklist; after reading it, the session is more accurately "Discover what fresh session perspective reveals."

## Session Naming (Northstar)

Every session must be named with a 5-word phrase extracted from the user's initial prompt. The five words should be the **most meaningful words that describe what the session is about**, not a mechanical extraction of the first five words.

**Example:**
- Prompt: "Tell me everything you learn from a new session perspective"
- Session name: "Learn from new session perspective" ← describes the actual work
- NOT: "Tell me everything you learn from" ← mechanical but meaningless

**How to apply:**
- Extract 5 meaningful words from the first user message
- Announce the session name in your first response: "This session: **[Name]**"
- Include it in Obsidian session logs as the title
- If you can't extract a meaningful 5-word phrase, ask the user for clarification on session intent before proceeding

## Rule Enforcement (Non-Negotiable)

**ALL rules in CLAUDE.md and memory files MUST be followed without exception.** Rules are not suggestions, preferences, or "nice-to-have" guidelines. If a rule exists, it is binding.

**Critical enforcement points:**
- Session naming: ALWAYS do it, NEVER skip
- Memory file rules: READ and FOLLOW every rule in `~/.claude/projects/*/memory/*.md`
- Git workflow: Standing authorizations in CLAUDE.md override default behavior
- Page width: 12.5% padding rule applies to every page, no exceptions
- Northstar server: NEVER restart without user request

If you are not following the rules, you are failing the job. Rules are how you remain useful and predictable.

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

## Northstar is Electron, NOT a Browser

**CRITICAL:** Northstar runs as an Electron-wrapped desktop application at `C:\Users\Scott\AppData\Local\Programs\Northstar\resources\`. It is NOT a web browser window.

Implications for debugging and troubleshooting:
- **No F12 DevTools access** — do not suggest opening DevTools, inspecting elements, or using browser console
- **No browser refresh (Ctrl+R/Cmd+R)** — Electron app reloads via file watcher or app restart, not browser reload
- **No browser cache** — mockup.html changes apply when the app next reads the file, not on reload
- **Diagnostics only via code inspection** — analyze source files (server.js, mockup.html) and suggest code changes, not browser debugging steps

When mockup.html needs testing, suggest: "I've changed mockup.html. Close and restart the Northstar app to pick up the change."

When diagnosing display freezes or crashes, analyze the code paths directly—don't ask for browser console output.

## Northstar Files — Local Only with Git

**Northstar source files are maintained locally ONLY. They are NOT in GitHub and NOT synced to any remote server.**

- **Location:** `C:\Users\Scott\Code\Northstar`
- Files: `server.js`, `mockup.html`, and dependencies
- **Local git repo:** Yes — uses git locally for version history and revert capability, but does NOT push to any remote
- These files are local development files that you may edit directly
- Do not look for them elsewhere; this is the authoritative location
- Use `git -C "C:\Users\Scott\Code\Northstar"` to check history, revert changes, or see what broke
- Changes are tracked locally; never push to a remote server
