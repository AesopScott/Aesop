# Changelog

## [2026-07-02] - Deployment Regression & Fix

### Fixed
- Restored `.github/workflows/deploy.yml` to the live repository (`AesopScott/Aesop`) after it was accidentally deleted during a cleanup of the redesign repository. This restored Cloudflare Pages auto-deployment functionality.

### Lessons Learned
- **Risk of Dual-Remote Pushing**: Pushing to multiple remotes simultaneously during cleanup can lead to destructive changes in the production environment if the cleanup is not carefully scoped.
- **Mitigation**: Established `directives/repo_management.md` to mandate explicit remote targeting (`origin` vs `redesign`) and mandatory verification before pushing to production.
