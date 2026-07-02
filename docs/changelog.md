# AESOP Academy — Change Log

> All changes made to the AesopScott/Aesop repository are logged here for traceability.
> If anything breaks, follow this log to identify and revert changes.

---

## 2026-07-02 — Homepage Redesign + Nav Update

### Summary
Replaced the live homepage (`index.html`) with a redesigned version based on the mock at `hassan-x2a.github.io/aesop-academy-redesign/`, updated the shared top banner nav to include richer navigation links, and preserved a backup of the original.

### Files Changed

| File | Action | Reason |
|------|--------|--------|
| `index.html` | **Replaced** | New homepage with modern hero, featured courses, value props, stats, secondary audiences. Old version backed up to `docs/backup/`. |
| `assets/top-banner-v2.js` | **Modified** | Added nav links (Courses, Find Your Path, How It Works) and "Start Learning" CTA button to the shared site-wide banner. |
| `docs/backup/index-legacy-v2.3.8.html` | **Created** | Backup of the original `index.html` (v2.3.8, 2026-06-03) for recovery. |
| `docs/changelog.md` | **Created** | This file — action log for traceability. |

### What Changed in Detail

#### `index.html`
- **Replaced** the old hero section with the mock's cleaner hero (eyebrow, title, subtitle, desc, CTA buttons)
- **Added** featured courses section ("Start in 30 seconds" with 3 course cards)
- **Added** value proposition section ("Why AESOP — Designed differently")
- **Added** stats strip with live counts (pulled from `stats.json`)
- **Added** secondary audiences section (Educators & Parents, Schools & Districts)
- **Kept** pedagogy insight strip and footer from original
- **Kept** `top-banner-v2.js` as the nav/banner system (no custom nav HTML)
- **Kept** `academy-theme.css` + `academy-dark-mode.css` for consistent design tokens
- **Kept** dark mode toggle integrated with `aesop-theme` localStorage key
- Used the same Design System tokens (navy/gold/violet) as the live site
- All links use relative paths matching existing site structure

#### `assets/top-banner-v2.js`
- Added "Courses" link (points to `/ai-academy/courses-v2.html`)
- Added "Find Your Path" link (points to `/ai-academy/assessment.html`)
- Added "How It Works" link (points to `/pedagogy.html`)
- Added "Start Learning" CTA button in the stats bar area
- Kept existing brand (logo + "AESOP AI Academy"), "About", "For Schools", stats, language selector, dark mode toggle, and report link

### Recovery Instructions
To revert the homepage:
```bash
git checkout HEAD~1 -- index.html
```
Or manually copy `docs/backup/index-legacy-v2.3.8.html` to `index.html`.

To revert the nav:
```bash
git checkout HEAD~1 -- assets/top-banner-v2.js
```

### Next Steps (Not Yet Implemented)
- **"Save your progress — create an account" prompt**: Post-module auth prompt. Should appear when starting a lesson session. If dismissed, reappears. Eventually expand to other pages.
- **Dedicated auth page (`/account.html`)**: Email + password + Google OAuth sign-up/sign-in flow. Triggered by "Start Learning" button.
- **Auth modal in `top-banner-v2.js`**: Reusable sign-in/sign-up modal injectable on any page.

---

*For questions, contact the build agent that made these changes.*
