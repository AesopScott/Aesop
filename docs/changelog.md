# Changelog

## [2026-07-04] - Desktop & Mobile Layout Overhaul (Header + Hero)

### Changed
- **Desktop header** (`assets/top-banner-v2.js`):
  - Switched from `padding: 0 12.5%` to `padding: 0 3rem` with `justify-content: space-between`
  - Nav links wrapped in `.tb-nav-center` for clean centering
  - Language selector replaced from button group to native `<select>` with custom styling (pill shape, SVG caret, flag-icon)
  - Removed stats-bar spacing dependency
- **Mobile header** (`assets/top-banner-v2.js`):
  - Header becomes `position: static` (no sticky on mobile)
  - All desktop nav/controls hidden via `display: none` under 760px
  - Hamburger button opens right-side drawer with full nav, mobile Start Learning button, and flag-button language selector
  - Drawer closes on overlay click, close button, Escape key, or nav-link click
- **Hero section** (`academy-theme.css`):
  - Reduced vertical padding: `5rem 2rem 4.5rem` → `3.75rem 2rem 3rem`
  - Reduced title: `clamp(2.6rem, 6vw, 4.2rem)` → `clamp(2.2rem, 5.5vw, 3.5rem)`
  - Reduced subtitle margin: `1.75rem` → `1.25rem`
  - Reduced desc margin & font-size: `2.25rem` / `1rem` → `1.5rem` / `0.95rem`
  - Reduced line-heights throughout for tighter vertical fit
  - Updated responsive breakpoints (900px, 600px) to match new sizing
- CTA buttons now fit above the fold on standard 1366×768 laptop screens (674px hero vs 640px available viewport)

## [2026-07-02] - Cross-Device Learner ID Resolution

### Added
- **Cross-device learner ID resolution**: When a signed-in user visits any page on a new device, the system now queries Firestore by `accountUid` to find their existing `learnerId`. This prevents orphaned learner records when users sign in across multiple browsers or devices.
- **Files modified**: `assets/auth-modal.js`, `account.html`, `theladder/ladder-core.js`, `theladder/ladder-app.js`
- **Mechanism**: Each file's `onAuthStateChanged` handler now calls `resolveLearnerIdByAccount()` — a Firestore query on `learners` where `accountUid == user.uid` — and overwrites `localStorage` with the found `learnerId` before any account-profile save or UI render.

## [2026-07-02] - Deployment Regression & Fix

### Fixed
- Restored `.github/workflows/deploy.yml` to the live repository (`AesopScott/Aesop`) after it was accidentally deleted during a cleanup of the redesign repository. This restored Cloudflare Pages auto-deployment functionality.

### Lessons Learned
- **Risk of Dual-Remote Pushing**: Pushing to multiple remotes simultaneously during cleanup can lead to destructive changes in the production environment if the cleanup is not carefully scoped.
- **Mitigation**: Established `directives/repo_management.md` to mandate explicit remote targeting (`origin` vs `redesign`) and mandatory verification before pushing to production.
