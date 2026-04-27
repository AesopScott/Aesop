# AESOP Live Link Check Report

**Generated:** 2026-04-27 16:12 UTC
**Status:** 🟡 WARNINGS — fetch infrastructure unavailable this run
**URLs checked:** 608 · **404s:** 0 · **Errors:** 608 (all fetch errors) · **Redirects:** 0

---

## 404 Not Found

None found.

> No URL could be confirmed as a 404 this run — see "Other Errors" below. Per the routine guardrail, infrastructure failures are not reported as 404s.

## Other Errors (5xx / Timeout / SSL)

All 608 URLs in the check list returned **fetch errors** this run. Both `curl` and `web_fetch` from the crawler sandbox responded with `HTTP 403 · x-deny-reason: host_not_allowed` for every request against `aesopacademy.org` (and against `www.aesopacademy.org`), indicating that outbound HTTP egress from the crawler sandbox was blocked at the network layer — not that the live site is down. This is the same infrastructure condition observed in the 2026-04-26 run.

Examples (representative — pattern is identical for all 608):

- `https://aesopacademy.org/` — fetch error: HTTP 403 `host_not_allowed` (sandbox egress denied)
- `https://aesopacademy.org/ai-academy/courses.html` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/ai-academy/modules/electives-hub.html` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/ai-news/` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/about/mission.html` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/review/aesop-sitemap.html` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/ai-academy/modules/en/courses.html` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/ai-academy/modules/ai-and-creativity/ai-and-creativity-m1.html` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/ai-academy/modules/working-with-the-anthropic-api/working-with-the-anthropic-api-m8.html` — fetch error: HTTP 403 `host_not_allowed`
- …and 599 further course / module URLs with the same fetch-error signature.

Because every URL failed identically at the sandbox layer before reaching the live site, no conclusions about the actual availability of pages on `aesopacademy.org` can be drawn from this run.

## Redirects (informational)

None observed (no request reached the live server).

## External Links Spot-Check

Skipped. The homepage could not be fetched, so no external `href` attributes could be extracted for spot-checking.

---

## Summary

0 broken internal link(s) confirmed — **no live data this run.** All 608 URLs returned fetch errors at the crawler sandbox layer (HTTP 403 `host_not_allowed`) before reaching the origin. This is an infrastructure condition, not a site outage. Next scheduled run should retry from an environment that permits egress to `aesopacademy.org`.

### Stats
- Internal URLs built from seeds + `course-registry.json`: 608
- Internal URLs successfully fetched: 0
- Internal URLs recorded as fetch error: 608
- External URLs spot-checked: 0 (skipped — homepage fetch blocked)
- Run duration: ~3 minutes (curl pass completed; all responses were `403 host_not_allowed`)

### Check-list composition
- 6 seed URLs
- 1 language-variant `courses.html` URL (`en`; the registry currently lists only `en` under `_meta.languages`)
- 81 live course directory indexes (from registry `status: live` entries)
- 521 module URLs (`{course-id}-m{N}.html` for N = 1..len(modules) per live course)

### Note on URL-count change vs. last week
Last week's run built 572 URLs; this week's run built 608. The +36 delta reflects new live courses and additional modules added to existing live courses in the registry between 2026-04-26 and 2026-04-27. The language-variant count dropped from 13 to 1 because the registry's per-course `_meta.languages` arrays currently only declare `en`; if other locales return to the registry, those URLs will reappear in the check list automatically.
