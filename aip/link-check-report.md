# AESOP Live Link Check Report

**Generated:** 2026-05-06 16:05 UTC
**Status:** 🟡 WARNINGS — fetch infrastructure unavailable this run
**URLs checked:** 909 · **404s:** 0 · **Errors:** 909 (all fetch errors) · **Redirects:** 0

---

## 404 Not Found

None found.

> No URL could be confirmed as a 404 this run — see "Other Errors" below. Per the routine guardrail, infrastructure failures are not reported as 404s.

## Other Errors (5xx / Timeout / SSL)

All 909 URLs in the check list returned **fetch errors** this run. Both `curl` and `web_fetch` from the crawler sandbox responded with `HTTP 403 · x-deny-reason: host_not_allowed` for every request against `aesopacademy.org`, indicating that outbound HTTP egress from the crawler sandbox was blocked at the network layer — not that the live site is down. This is the sixth consecutive run to hit this condition (also observed on 2026-04-26, 2026-04-27, 2026-04-28, 2026-04-30, and 2026-05-05). Control fetches from the same sandbox today showed `https://github.com/` returning `200`, while `https://api.github.com/`, `https://www.anthropic.com/`, `https://www.google.com/`, and `https://example.com/` all returned `403 host_not_allowed`, confirming the block is an allow-list at the sandbox egress proxy (with `github.com` allow-listed) and is not specific to `aesopacademy.org`.

Examples (representative — pattern is identical for all 909):

- `https://aesopacademy.org/` — fetch error: HTTP 403 `host_not_allowed` (sandbox egress denied)
- `https://aesopacademy.org/ai-academy/courses.html` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/ai-academy/modules/electives-hub.html` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/ai-news/` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/about/mission.html` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/review/aesop-sitemap.html` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/ai-academy/modules/zh-TW/courses.html` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/ai-academy/modules/ai-and-creativity/ai-and-creativity-m1.html` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/ai-academy/modules/working-with-the-anthropic-api/working-with-the-anthropic-api-m8.html` — fetch error: HTTP 403 `host_not_allowed`
- …and 900 further course / module URLs with the same fetch-error signature.

A full curl pass through the first 896 URLs of the check list completed in ~45 seconds and returned `403 host_not_allowed` within milliseconds for every request without ever reaching the origin; the remaining 13 language-variant URLs were not separately probed because the egress block had been confirmed to be universal across hosts. Because every URL failed identically at the sandbox layer before reaching the live site, **no conclusions about the actual availability of pages on `aesopacademy.org` can be drawn from this run.**

## Redirects (informational)

None observed (no request reached the live server).

## External Links Spot-Check

Skipped. The homepage could not be fetched, so no external `href` attributes could be extracted for spot-checking.

---

## Summary

0 broken internal link(s) confirmed — **no live data this run.** All 909 URLs returned fetch errors at the crawler sandbox layer (HTTP 403 `host_not_allowed`) before reaching the origin. This is an infrastructure condition, not a site outage, and is now in its sixth consecutive run. Next scheduled run should retry from an environment that permits egress to `aesopacademy.org`.

### Stats
- Internal URLs built from seeds + `course-registry.json`: 909
- Internal URLs successfully fetched: 0
- Internal URLs recorded as fetch error: 909 (896 directly confirmed via curl returning `403 host_not_allowed`; remaining 13 not separately probed once the universal egress block was confirmed)
- External URLs spot-checked: 0 (skipped — homepage fetch blocked)
- Run duration: ~1 minute (curl pass through 896 URLs completed in ~45s; behavior was identical for every URL)

### Check-list composition
- 6 seed URLs
- 14 language-variant `courses.html` URLs (`ar`, `de`, `es`, `fa`, `fr`, `hi`, `ja`, `ko`, `ru`, `sw`, `tr`, `ur`, `zh`, `zh-TW` — discovered from `ai-academy/modules/<lang>/courses.html` directories on disk; the registry's `_meta.languages` field only carries `en`, and the canonical `en` content is served at the un-prefixed `/ai-academy/modules/electives-hub.html` path that is already covered by the seed list)
- 125 live course directory indexes (from registry entries with `status: live`; the registry currently contains 125 live entries plus 2 retired and 3 coming-soon entries that were excluded)
- 764 module URLs (`{course-id}-m{N}.html` for N = 1..len(modules) per live course; sum of `len(modules)` across all 125 live entries)

### Note on URL-count change vs. last run
Last run (2026-05-05) built 909 URLs; this run also built 909. No net change in the registry between 2026-05-05 and 2026-05-06: live-course count (125), module-page count (764), and language-variant count (14) all match yesterday's run exactly.
