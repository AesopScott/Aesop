# Repository Management SOP

This directive defines the standard operating procedure for managing the dual-remote repository setup to prevent accidental deployments to the live production environment.

## Repository Structure

- **Live Repository (`origin`)**: `AesopScott/Aesop`
    - Purpose: Production environment.
    - Target: Cloudflare Pages (via `.github/workflows/deploy.yml`).
    - **CRITICAL**: Any push to `origin` triggers an immediate deployment to `aesopacademy.org`.
- **Redesign Repository (`redesign`)**: `Hassan-x2a/aesop-academy-redesign`
    - Purpose: Experimental, feature development, and staging.
    - **CRITICAL**: This is a sandbox. Changes here do not affect the live site.

## Operating Rules

### 1. Explicit Remote Targeting
**NEVER** run `git push` without specifying a remote. Always use:
- `git push origin <branch>` for production.
- `git push redesign <branch>` for experimental work.

### 2. Verification Before Push
Before pushing to `origin`, always run:
- `git status` to see what is being staged.
- `git diff --cached` to inspect the changes.
- `git remote -v` to confirm you are targeting the correct remote.

### 3. Atomic Cleanup
When performing "cleanup" operations (removing files, workflows, or experimental code):
- Verify the commit content specifically to ensure no production-critical files (like `.github/workflows/deploy.yml`) are included in the deletion.
- Perform the cleanup on the `redesign` remote first.
- Only push to `origin` after verifying that the changes are strictly additive or safe for production.

### 4. Self-Annealing & Error Recovery
If a mistake occurs (e.g., accidental deletion from `origin`):
1. Immediately identify the lost commit/file.
2. Restore the file/commit in the local `.tmp` environment.
3. Push the restoration to `origin` immediately to restore service.
4. Update this directive and the `docs/changelog.md` to prevent recurrence.
