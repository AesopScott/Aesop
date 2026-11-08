# AESOP Live Link Check Report

**Generated:** 2026-11-08 10:04 UTC
**Status:** 🟡 WARNINGS — live fetch blocked at sandbox egress (16th consecutive run blocked); local proxy check still flags the same 1 candidate broken module URL
**URLs checked:** 911 · **404s:** 0 confirmed · **Errors:** 911 (all fetch errors) · **Redirects:** 0

---

## 404 Not Found

None **confirmed** — see fetch-error notice below. Per the routine guardrail, infrastructure failures are not reported as 404s.

The **local repo proxy check** (see "Local proxy check" further down) again flagged the same URL it has flagged every prior week as a strong candidate for a live 404 — its backing file is still missing from the deployed source tree:

- `https://aesopacademy.org/ai-academy/modules/eval-benchmark/eval-benchmark-m1.html` — registry lists `eval-benchmark` as `status: "live"` with `modCount: 1`, but the directory `ai-academy/modules/eval-benchmark/` still does not exist in the repo. The course tile likely links to a page that was never built. No change vs. 2026-11-01 / 2026-10-25 / 2026-10-18 / 2026-10-11 / 2026-10-04 / 2026-09-20 / 2026-08-30 / 2026-08-23 / 2026-08-02 / 2026-07-19 / 2026-07-05 / 2026-06-28 / 2026-06-21 / 2026-06-14 — the underlying fix has not landed. Today's `aip/audit-report.md` (2026-11-07 14:09 UTC) independently flags the same `MISSING_DIR` error for `eval-benchmark`, so the finding is corroborated by a second signal. The audit also records `NOT_IN_COURSES_HTML` and `NOT_IN_ELECTIVES_HUB` warnings for `eval-benchmark`, meaning the registry entry is not actually linked from the main navigation — the tile is a stale registry entry rather than an active visitor path, so this remains a low-severity user-visible break.

## Other Errors (5xx / Timeout / SSL)

All 911 URLs in the check list returned **fetch errors** this run, identical signature to the previous fifteen blocked runs. `web_fetch` from the routine container returns `getaddrinfo ENOTFOUND aesopacademy.org` for every request against the host — the block is at the network policy layer (DNS not resolvable from this sandbox), not at the live origin. Today's control probes:

| Host | Status |
| --- | --- |
| `https://aesopacademy.org/` | fetch error: ENOTFOUND (web_fetch) |
| `https://aesopacademy.org/` via `curl --proxy` | CONNECT rejected (`connect_rejected` — host not allowed for this session) |
| `https://www.aesopacademy.org/` via `curl --proxy` | CONNECT rejected (same policy denial) |
| `https://aesopscott.github.io/` via `curl --proxy` | CONNECT rejected (same policy denial) |

Every non-GitHub upstream remains denied by this routine's network policy. This is the **sixteenth consecutive run** blocked the same way (see 2026-06-07, 2026-06-14, 2026-06-21, 2026-06-28, 2026-07-05, 2026-07-19, 2026-08-02, 2026-08-23, 2026-08-30, 2026-09-20, 2026-10-04, 2026-10-11, 2026-10-18, 2026-10-25, and 2026-11-01 reports). The site itself is deployed via **Cloudflare Pages** (see `.github/workflows/deploy.yml`), so the block is not the origin — it's the sandbox's egress allow-list. Recommended fix: switch this routine's environment to a more permissive network policy, or add `aesopacademy.org` (and ideally `discord.gg`) to the egress allow-list for the current one. Reference: https://code.claude.com/docs/en/claude-code-on-the-web (network policies / environments).

Representative fetch-error entries (pattern is identical for all 911):

- `https://aesopacademy.org/` — fetch error: ENOTFOUND
- `https://aesopacademy.org/ai-academy/courses.html` — fetch error: ENOTFOUND
- `https://aesopacademy.org/ai-academy/modules/electives-hub.html` — fetch error: ENOTFOUND
- `https://aesopacademy.org/ai-news/` — fetch error: ENOTFOUND
- `https://aesopacademy.org/about/mission.html` — fetch error: ENOTFOUND
- `https://aesopacademy.org/review/aesop-sitemap.html` — fetch error: ENOTFOUND
- `https://aesopacademy.org/ai-academy/modules/ai-and-creativity/ai-and-creativity-m1.html` — fetch error: ENOTFOUND
- …and 904 further course / module URLs with the same fetch-error signature.

## Redirects (informational)

None observed — no requests completed TLS, so no response headers were available to inspect for redirects.

## External Links Spot-Check

Skipped this run. The external-link spot-check depends on first loading `https://aesopacademy.org/` and the courses page to extract `href` attributes; both are fetch-blocked, so there is no live DOM to parse. No external request was issued from this routine. (When egress is restored, the spot check will resume on the first 20 unique external URLs found on the homepage and courses page, per the routine spec.)

---

## Local proxy check (repo-side substitute while egress is blocked)

To keep the routine's heartbeat useful while the sandbox cannot reach the live origin, we cross-check the planned URL list against the committed source tree. For every URL of shape `/ai-academy/modules/{course-id}/{course-id}-m{N}.html`, we verify that `ai-academy/modules/{course-id}/{course-id}-m{N}.html` exists on `main`. A missing file on `main` is a **candidate** live 404 (Cloudflare Pages deploys directly from `main`), subject to confirmation once egress is restored.

**Live courses in registry:** 126
**Module URLs in list:** 765
**Candidate broken module URLs (file missing from `main`):** **1**

- `ai-academy/modules/eval-benchmark/eval-benchmark-m1.html` — directory `ai-academy/modules/eval-benchmark/` not present in repo (registry says `status: "live"`, `modCount: 1`). Status unchanged vs. prior 15 reports. Corroborated by `aip/audit-report.md` (2026-11-07) `MISSING_DIR` error.

All 125 other live courses have at least a directory and the expected `-m1.html`…`-mN.html` files committed.

**Language-variant courses pages** (`/ai-academy/modules/{lang}/courses.html`): 14 language directories detected on disk (`ar`, `de`, `es`, `fa`, `fr`, `hi`, `ja`, `ko`, `ru`, `sw`, `tr`, `ur`, `zh`, `zh-TW`) — the registry has no `_meta.languages` block, so the routine falls back to the filesystem layout to enumerate language variants. All 14 variant pages are present on `main`. (The URL list grew from 897 last week to 911 this week — +4 new language dirs: `fa`, `sw`, `tr`, `ur`, plus a handful of additional live-course modules.)

---

## Summary

🟡 Egress to `aesopacademy.org` blocked by routine network policy for the **16th consecutive run** — live 404s cannot be confirmed from this sandbox. The local repo proxy check (which does not depend on egress) continues to flag **1 candidate live 404**: `eval-benchmark/eval-benchmark-m1.html`, whose directory is still missing from the deployed source tree. This finding is corroborated by `aip/audit-report.md` from 2026-11-07, which flags the same `MISSING_DIR` error.

**Action for Scott:** either add `aesopacademy.org` to this routine's egress allow-list (so the checker can confirm live-site 404s directly), or decide what to do about the `eval-benchmark` registry entry — build the module, mark it `coming-soon`, or remove it. The audit report confirms the tile is not linked from `courses.html` or `electives-hub.html`, so user-facing impact is minimal.

### Stats
- Internal URLs checked: 911 (0 confirmed 200, 0 confirmed 404, 911 fetch errors, 0 redirects)
- External URLs spot-checked: 0 (skipped — no DOM available while egress is blocked)
- Local proxy check: 765 module URLs cross-checked, 1 candidate broken
- Live courses in registry: 126 · Coming-soon: 3 · Retired: 2 · Total registry entries: 131
- Language variants detected: 14 (`ar`, `de`, `es`, `fa`, `fr`, `hi`, `ja`, `ko`, `ru`, `sw`, `tr`, `ur`, `zh`, `zh-TW`)
- Run duration: ~1 minute (no live network work — all fetches failed fast at DNS/CONNECT)
