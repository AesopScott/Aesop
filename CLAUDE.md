# AESOP AI Academy — Claude Code Guidelines

## Layout & Page Width

- All page content areas must use **75% of the viewport width** (`width: 75%; margin: 0 auto`).
- Set `max-width` to a large cap (e.g. `1800px`) to prevent runaway expansion on ultra-wide monitors.
- `body` minimum width: `900px`.
- Never constrain content to narrow fixed widths (760–800px range is explicitly off-limits).
- Full-bleed sections (hero banners, nav bars, footers) may span 100% width, but their *inner* content wrappers must follow the 75% rule.

## Design System

- Colors: `--navy: #0d1b2a`, `--gold: #c9a05a`, `--cream: #faf8f4`
- Fonts: Playfair Display (display/headings), DM Sans (body)
- Reference `academy-theme.css` and `academy-dark-mode.css` for shared tokens.

## Git & Deployment

- Commits to `main` deploy automatically to Mocahost via FTP (`deploy.yml`).
- Standing authorization to commit and push every change to `main` immediately — no need to ask.
- Use `git -C "/path"` instead of `cd` — `cd` triggers permission prompts.
