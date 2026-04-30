# AESOP AI Academy — Claude Code Guidelines

## Session Startup (READ FIRST)

**At the start of every session, read the complete memory system from disk:**

1. Read the memory index:
   ```
   Read: C:\Users\scott\.claude\projects\C--Users-Scott-Code-Aesop\memory\MEMORY.md
   ```

2. For each memory file referenced in the index, read it to load the actual content (MEMORY.md is just an index pointing to the real memory files):
   ```
   Read: C:\Users\scott\.claude\projects\C--Users-Scott-Code-Aesop\memory\[filename].md
   ```

3. Load all memory files at startup—each contains standing instructions, feedback, and project context that must be active for the session

- Must use the Read tool explicitly (not rely on system context)
- Follow all "always," "proactive," and standing behavioral rules from all memory files
- This ensures every session loads the latest memory state before beginning work

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
