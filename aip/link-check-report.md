# AESOP Live Link Check Report

**Generated:** 2026-04-22 16:51 UTC
**Status:** 🟡 WARNINGS — fetch infrastructure unavailable this run
**URLs checked:** 305 · **404s:** 0 · **Errors:** 305 (all fetch errors) · **Redirects:** 0

---

## 404 Not Found

None found.

> No URL could be confirmed as a 404 this run — see "Other Errors" below. Per the routine guardrail, infrastructure failures are not reported as 404s.

## Other Errors (5xx / Timeout / SSL)

All 305 URLs in the check list returned **fetch errors** this run. The crawler environment responded with `HTTP 403 · x-deny-reason: host_not_allowed` for every request against `aesopacademy.org` (and also for control requests against `example.com`), indicating that outbound HTTP egress from the crawler sandbox was blocked at the network layer — not that the live site is down.

Examples (representative — pattern is identical for all 305):

- `https://aesopacademy.org/` — fetch error: HTTP 403 `host_not_allowed` (sandbox egress denied)
- `https://aesopacademy.org/ai-academy/courses.html` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/ai-academy/modules/electives-hub.html` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/ai-news/` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/about/mission.html` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/review/aesop-sitemap.html` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/ai-academy/modules/ko/courses.html` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/ai-academy/modules/zh-TW/courses.html` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/ai-academy/modules/ur/courses.html` — fetch error: HTTP 403 `host_not_allowed`
- …and 296 further module/course URLs with the same fetch-error signature.

Because every URL failed identically at the sandbox layer before reaching the live site, no conclusions about the actual availability of pages on `aesopacademy.org` can be drawn from this run.

## Redirects (informational)

None observed (no request reached the live server).

## External Links Spot-Check

Skipped. The homepage could not be fetched, so no external `href` attributes could be extracted for spot-checking.

---

## Summary

0 broken internal link(s) confirmed — **no live data this run.** All 305 URLs returned fetch errors at the crawler sandbox layer (HTTP 403 `host_not_allowed`) before reaching the origin. This is an infrastructure condition, not a site outage. Next scheduled run should retry from an environment that permits egress to `aesopacademy.org`.

### Stats
- Internal URLs built from seeds + `course-registry.json`: 305
- Internal URLs successfully fetched: 0
- Internal URLs recorded as fetch error: 305
- External URLs spot-checked: 0 (skipped — homepage fetch blocked)
- Run duration: ~2 minutes

### Check-list composition
- 6 seed URLs
- 3 language-variant `courses.html` URLs (`ko`, `zh-TW`, `ur`)
- 35 live course directory indexes (from registry `status: live` entries with non-empty `url`)
- 261 module URLs (`{course-id}-m{N}.html` for N = 1..len(modules) per live course)
