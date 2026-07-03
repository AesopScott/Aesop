# Changelog

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
