# `.githooks/` — local Git hooks for the AESOP repo

Tracked, opt-in. Hooks here are not active until you tell Git to use this directory.

## Install (one time per clone)

```bash
git config core.hooksPath .githooks
```

That's it. Hooks then run automatically on the relevant Git events. To disable, run `git config --unset core.hooksPath`.

## What's in here

| File | Trigger | What it does |
|------|---------|--------------|
| `pre-commit` | before `git commit` | Runs `.github/scripts/check_courses_html_sanity.py` against any staged change to `ai-academy/courses.html`, comparing the staged version against `origin/main`. Aborts the commit if the file looks like a stale-working-tree clobber (e.g., section count drops sharply, file shrinks >25%, a section heading goes missing). |

## Bypassing the guard

When a change is intentionally large or a real restructure (rare):

```bash
git commit -m "your message [skip-courses-guard]"
# or
COURSES_GUARD_SKIP=1 git commit ...
# nuclear option (skips ALL hooks)
git commit --no-verify
```

## Why this matters

On 2026-04-29, a 1,048-file commit (`feat(enforcement): medium gate`) shipped a stale local `courses.html` alongside an unrelated mass retrofit. The stale file silently destroyed all 6 Youth sub-sections, the live-typeahead search bar, and ~100 nav buttons. The diff was buried in the commit and only got noticed after deploy. This pre-commit hook plus the matching CI workflow `.github/workflows/guard-courses-html.yml` exist to catch that pattern before it can land again.
