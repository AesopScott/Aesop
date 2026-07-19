# AESOP Live Link Check Report

**Generated:** 2026-07-19 10:11 UTC
**Status:** 🟡 WARNINGS — live fetch blocked at sandbox egress (6th week running); local proxy check still flags the same 1 candidate broken module URL
**URLs checked:** 911 · **404s:** 0 confirmed · **Errors:** 911 (all fetch errors) · **Redirects:** 0

---

## 404 Not Found

None **confirmed** — see fetch-error notice below. Per the routine guardrail, infrastructure failures are not reported as 404s.

The **local repo proxy check** (see "Local proxy check" further down) again flagged the same URL it flagged the previous five weeks as a strong candidate for a live 404 — its backing file is still missing from the deployed source tree:

- `https://aesopacademy.org/ai-academy/modules/eval-benchmark/eval-benchmark-m1.html` — registry lists `eval-benchmark` as `status: "live"` with `modCount: 1`, but the directory `ai-academy/modules/eval-benchmark/` still does not exist in the repo. The course tile likely links to a page that was never built. No change vs. 2026-07-05 / 2026-06-28 / 2026-06-21 / 2026-06-14 — the underlying fix has not landed. The daily `aip/audit-report.md` has independently been flagging the same `MISSING_DIR` error every day this week, so the finding is corroborated by a second signal.

## Other Errors (5xx / Timeout / SSL)

All 911 URLs in the check list returned **fetch errors** this run, identical signature to the previous five weeks. Both `curl` and `web_fetch` from the routine container fail at the egress proxy with `HTTP/1.1 403 Forbidden` against `aesopacademy.org:443` — the proxy's own status endpoint (`$HTTPS_PROXY/__agentproxy/status`) reports `connect_rejected · "gateway answered 403 to CONNECT (policy denial or upstream failure)"` for the host. The block is at the network policy layer, not at the live origin. Today's control probes:

| Host | Status |
| --- | --- |
| `https://aesopacademy.org/` | 403 `host_not_allowed` (proxy CONNECT rejected) |

The proxy's `noProxy` list still only exempts anthropic.com, npmjs, jsr, pypi, crates, and go-proxy hosts — every non-GitHub upstream is denied. This is the **sixth consecutive weekly run** blocked the same way (see 2026-06-07, 2026-06-14, 2026-06-21, 2026-06-28, and 2026-07-05 reports). The site itself is deployed via **Cloudflare Pages** (see `.github/workflows/deploy.yml`), so the block is not the origin — it's the sandbox's egress allow-list. Recommended fix: switch this routine's environment to a more permissive network policy, or add `aesopacademy.org` (and ideally `discord.gg`) to the egress allow-list for the current one. Reference: https://code.claude.com/docs/en/claude-code-on-the-web (network policies / environments).

Representative fetch-error entries (pattern is identical for all 911):

- `https://aesopacademy.org/` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/ai-academy/courses.html` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/ai-academy/modules/electives-hub.html` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/ai-news/` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/about/mission.html` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/review/aesop-sitemap.html` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/ai-academy/modules/ar/courses.html` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/ai-academy/modules/ai-and-creativity/ai-and-creativity-m1.html` — fetch error: HTTP 403 `host_not_allowed`
- …and 903 further course / module URLs with the same fetch-error signature.

## Redirects (informational)

None observed (no request reached the live server).

## External Links Spot-Check

Attempted via local extraction of `<a href="…">` and `<link href="…">` from `index.html` and `ai-academy/courses.html` since the live homepage couldn't be fetched. **One** unique external host referenced from those two pages (unchanged vs. 2026-07-05):

- `https://discord.gg/pKDa5ryX` — fetch error: HTTP 403 `host_not_allowed` (sandbox-blocked, not site-blocked)

Not reachable from this container. Cannot confirm or deny liveness from this run.

---

## Local proxy check (substitute for live fetch)

Since live HTTP fetch is unavailable, this run again ran a **best-effort proxy check** against the deployed source tree on `main`: for each URL in the check list, map to its filesystem path (`https://aesopacademy.org/foo/bar.html` → `<repo>/foo/bar.html`; trailing `/` → `index.html`) and verify the file exists. This catches *static* link rot (the file isn't built / deployed in the repo) but not server-side issues, MIME problems, or content errors.

### Result

- **784** of 911 URL targets resolved to a file present in the repo.
- **125** course-directory URLs lack an `index.html` in the repo — see "Systemic course-directory pattern" below.
- **2** URL targets have no backing path: `ai-academy/modules/eval-benchmark/` and `ai-academy/modules/eval-benchmark/eval-benchmark-m1.html` (both stem from the same missing course directory — already listed under 404 candidates above).

### Systemic course-directory pattern

125 of the 126 live course-directory URLs (e.g. `/ai-academy/modules/ai-and-creativity/`) map to a directory that exists but does not contain an `index.html` — this is true for **all 125 non-missing live courses**, not a per-course bug. Live behavior of these URLs cannot be determined from the repo alone; on Cloudflare Pages these typically resolve via directory-index conventions or a rewrite rule, so many may serve 200 in production. Once the egress block is resolved, the next run should clarify by fetching these URLs.

---

## Summary

0 broken internal link(s) confirmed live — **no live data this run** (6th week in a row). All 911 URLs returned fetch errors at the routine container's egress layer (HTTP 403 `host_not_allowed`) before reaching the origin. This is the routine's environment, not a site outage.

**Local proxy check** (run as a fallback) surfaced the same **1 likely broken course (2 URLs)** that has been pending since 2026-06-14: `eval-benchmark` (registry entry exists with `status: live`, directory does not). The daily course audit (`aip/audit-report.md`, latest 2026-07-18) independently flags the same `MISSING_DIR` error, and the same course is missing from `courses.html` — so the tile is likely orphaned in the registry rather than actively linked from the site. 125 course-directory URLs without local `index.html` remain flagged as systemic — confirmation requires live fetch.

**Action required:** widen this routine's egress allow-list to include `aesopacademy.org` (and ideally the external hosts it references). Until then the live crawl portion of this routine is non-functional and the proxy-check fallback is the only signal.

### Stats
- Internal URLs built from seeds + `course-registry.json`: 911
- Internal URLs successfully fetched live: 0
- Internal URLs recorded as fetch error: 911 (confirmed via parallel `curl` returning `000` after proxy `403 host_not_allowed` and via `WebFetch` returning `HTTP 403 Forbidden`)
- Internal URLs cross-checked against repo filesystem: 911 (784 OK · 125 systemic dir-no-index · 2 missing-path stemming from 1 missing course)
- External URLs spot-checked live: 0 (sandbox-blocked); 1 unique external host identified from local homepage + courses page
- Run duration: ~1 minute (curl probes + registry parse + filesystem cross-check)

### Check-list composition
- 6 seed URLs
- 14 language-variant `courses.html` URLs (`ar`, `de`, `es`, `fa`, `fr`, `hi`, `ja`, `ko`, `ru`, `sw`, `tr`, `ur`, `zh`, `zh-TW` — discovered from `ai-academy/modules/<lang>/courses.html` directories on disk; the registry still carries no `_meta.languages` field)
- 126 live course directory URLs (`status: "live"` only; 2 `retired` and 3 `coming-soon` entries excluded)
- 765 module URLs (`{course-id}-m{N}.html` for N = 1..`modCount` per live course)

### Change vs. last run (2026-07-05)
- URL count unchanged at 911 (registry: 126 live courses, 765 live modules — same as last five weeks)
- Network block unchanged for `aesopacademy.org` (still `host_not_allowed`)
- Candidate broken link unchanged — `eval-benchmark-m1.html` still missing; no fix landed in the past two weeks; the daily audit report has been flagging the same `MISSING_DIR` continuously
- External link surface unchanged — same one host (`discord.gg`) as last week
- Methodology unchanged — same seed list, same language-variant discovery, same proxy-check logic
- Site plumbing note added — the deploy target is Cloudflare Pages (`.github/workflows/deploy.yml`), which explains how directory URLs without local `index.html` can still serve 200 in production
