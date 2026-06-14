# AESOP Live Link Check Report

**Generated:** 2026-06-14 10:09 UTC
**Status:** 🟡 WARNINGS — live fetch blocked at sandbox egress (2nd week running); local proxy check surfaced 1 candidate broken module URL
**URLs checked:** 911 · **404s:** 0 confirmed · **Errors:** 911 (all fetch errors) · **Redirects:** 0

---

## 404 Not Found

None **confirmed** — see fetch-error notice below. Per the routine guardrail, infrastructure failures are not reported as 404s.

A **local repo proxy check** (see "Local proxy check" further down) flagged one URL whose backing file is missing from the deployed source tree, making it a strong candidate for a live 404:

- `https://aesopacademy.org/ai-academy/modules/eval-benchmark/eval-benchmark-m1.html` — registry lists `eval-benchmark` as `status: "live"` with `modCount: 1`, but the directory `ai-academy/modules/eval-benchmark/` does not exist in the repo. The course tile likely links to a page that was never built.

## Other Errors (5xx / Timeout / SSL)

All 911 URLs in the check list returned **fetch errors** this run, identical signature to last week. Both `curl` and `web_fetch` from the routine container responded with `HTTP 403 · x-deny-reason: host_not_allowed` for every request against `aesopacademy.org`, indicating that outbound HTTP egress from this container is blocked at the network policy layer — not that the live site is down. Today's control probes:

| Host | Status |
| --- | --- |
| `https://github.com/` | 200 |
| `https://raw.githubusercontent.com/` | 301 → 200 |
| `https://api.github.com/` | 429 (rate limited, reachable) |
| `https://aesopacademy.org/` | 403 `host_not_allowed` |
| `https://google.com/` | 403 `host_not_allowed` |
| `https://example.com/` | 403 `host_not_allowed` |
| `https://cdnjs.cloudflare.com/` | 403 `host_not_allowed` |
| `https://mojoaistudio.com/` | 403 `host_not_allowed` |
| `https://discord.gg/` | 403 `host_not_allowed` |

This is the second consecutive weekly run blocked the same way (see 2026-06-07 report). The block is by hostname allow-list — only GitHub-family hosts pass — so this routine will continue to fail until the environment's network policy is widened to include `aesopacademy.org` (and the external-link domains it references). Recommended fix: switch this routine's environment to a more permissive network policy, or add an `aesopacademy.org` egress allowance to the current one.

Representative fetch-error entries (pattern is identical for all 911):

- `https://aesopacademy.org/` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/ai-academy/courses.html` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/ai-academy/modules/electives-hub.html` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/ai-news/` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/about/mission.html` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/review/aesop-sitemap.html` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/ai-academy/modules/zh-TW/courses.html` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/ai-academy/modules/ai-and-creativity/ai-and-creativity-m1.html` — fetch error: HTTP 403 `host_not_allowed`
- …and 903 further course / module URLs with the same fetch-error signature.

## Redirects (informational)

None observed (no request reached the live server).

## External Links Spot-Check

Attempted via local extraction of `<a href="…">` from `index.html` and `ai-academy/courses.html` since the live homepage couldn't be fetched. Three unique external hosts referenced from those two pages:

- `https://cdnjs.cloudflare.com/ajax/libs/flag-icon-css/6.6.6/css/flag-icons.min.css` — fetch error: HTTP 403 `host_not_allowed` (sandbox-blocked, not site-blocked)
- `https://mojoaistudio.com/learn` — fetch error: HTTP 403 `host_not_allowed`
- `https://discord.gg/pKDa5ryX` — fetch error: HTTP 403 `host_not_allowed`

None reachable from this container. Cannot confirm or deny liveness from this run.

---

## Local proxy check (substitute for live fetch)

Since live HTTP fetch is unavailable, this run added a **best-effort proxy check** against the deployed source tree on `main`: for each URL in the check list, map to its filesystem path (`https://aesopacademy.org/foo/bar.html` → `<repo>/foo/bar.html`; trailing `/` → `index.html`) and verify the file exists. This catches *static* link rot (the file isn't built / deployed in the repo) but not server-side issues, MIME problems, or content errors.

### Result

- **784** of 911 URL targets resolved to a file present in the repo.
- **126** course-directory URLs lack an `index.html` in the repo — see "Systemic course-directory pattern" below.
- **1** module URL has no backing file: `ai-academy/modules/eval-benchmark/eval-benchmark-m1.html` (already listed under 404 candidates above).

### Systemic course-directory pattern

Every one of the 126 live course-directory URLs (e.g. `/ai-academy/modules/ai-and-creativity/`) maps to a directory that exists but does not contain an `index.html` — this is true for **all 126**, not a per-course bug. Live behavior of these URLs cannot be determined from the repo alone; the server may auto-index, redirect to the electives hub, or return 404. Once the egress block is resolved, the next run should clarify by fetching these URLs.

---

## Summary

0 broken internal link(s) confirmed live — **no live data this run** (2nd week in a row). All 911 URLs returned fetch errors at the routine container's egress layer (HTTP 403 `host_not_allowed`) before reaching the origin. This is the routine's environment, not a site outage.

**Local proxy check** (run as a fallback) surfaced **1 likely broken module URL** for follow-up: `eval-benchmark-m1.html` (registry entry exists, directory does not). 126 course-directory URLs without local `index.html` are flagged as systemic — confirmation requires live fetch.

### Stats
- Internal URLs built from seeds + `course-registry.json`: 911
- Internal URLs successfully fetched live: 0
- Internal URLs recorded as fetch error: 911 (all 911 directly confirmed via parallel curl returning `403 host_not_allowed`)
- Internal URLs cross-checked against repo filesystem: 911 (784 OK · 126 systemic dir-no-index · 1 missing module)
- External URLs spot-checked live: 0 (all 3 sandbox-blocked); 3 unique external hosts identified from local homepage + courses page
- Run duration: ~20 seconds (curl pass + filesystem cross-check)

### Check-list composition
- 6 seed URLs
- 14 language-variant `courses.html` URLs (`ar`, `de`, `es`, `fa`, `fr`, `hi`, `ja`, `ko`, `ru`, `sw`, `tr`, `ur`, `zh`, `zh-TW` — discovered from `ai-academy/modules/<lang>/courses.html` directories on disk; the registry still carries no `_meta.languages` field)
- 126 live course directory URLs (`status: "live"` only; 2 `retired` and 3 `coming-soon` entries excluded)
- 765 module URLs (`{course-id}-m{N}.html` for N = 1..len(modules) per live course)

### Change vs. last run (2026-06-07)
- URL count unchanged at 911 (registry: 126 live courses, 765 live modules — same as last week)
- Network block unchanged — `aesopacademy.org` still `host_not_allowed`
- New this run: local proxy check added as fallback, surfaced `eval-benchmark-m1.html` as candidate 404
- Control-host change: `api.github.com` now returns `429` (rate-limited but reachable) vs `403` last week — egress allow-list slightly widened to include `api.github.com`, still does not include `aesopacademy.org`
