# AESOP Live Link Check Report

**Generated:** 2026-05-09 16:09 UTC
**Status:** 🟡 WARNINGS — fetch infrastructure unavailable this run
**URLs checked:** 911 · **404s:** 0 · **Errors:** 911 (all fetch errors) · **Redirects:** 0

---

## 404 Not Found

None found.

> No URL could be confirmed as a 404 this run — see "Other Errors" below. Per the routine guardrail, infrastructure failures are not reported as 404s.

## Other Errors (5xx / Timeout / SSL)

All 911 URLs in the check list returned **fetch errors** this run. Both `curl` and `web_fetch` from the crawler sandbox responded with `HTTP 403 · x-deny-reason: host_not_allowed` for every request against `aesopacademy.org`, indicating that outbound HTTP egress from the crawler sandbox was blocked at the network layer — not that the live site is down. This is the eighth consecutive run to hit this condition (also observed on 2026-04-26, 2026-04-27, 2026-04-28, 2026-04-30, 2026-05-05, 2026-05-06, and 2026-05-07). Control fetches from the same sandbox today showed `https://github.com/` returning `200`, while `https://api.github.com/`, `https://www.anthropic.com/`, `https://www.google.com/`, `https://example.com/`, and `https://aesopacademy.org/` all returned `403 host_not_allowed`, confirming the block is an allow-list at the sandbox egress proxy (with only `github.com` allow-listed today) and is not specific to `aesopacademy.org`.

Examples (representative — pattern is identical for all 911):

- `https://aesopacademy.org/` — fetch error: HTTP 403 `host_not_allowed` (sandbox egress denied)
- `https://aesopacademy.org/ai-academy/courses.html` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/ai-academy/modules/electives-hub.html` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/ai-news/` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/about/mission.html` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/review/aesop-sitemap.html` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/ai-academy/modules/zh-TW/courses.html` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/ai-academy/modules/ai-and-creativity/ai-and-creativity-m1.html` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/ai-academy/modules/working-with-the-anthropic-api/working-with-the-anthropic-api-m8.html` — fetch error: HTTP 403 `host_not_allowed`
- …and 902 further course / module URLs with the same fetch-error signature.

A full curl pass through all 911 URLs of the check list completed in ~11 seconds (12-way parallel) and returned `403 host_not_allowed` within milliseconds for every request without ever reaching the origin. Because every URL failed identically at the sandbox layer before reaching the live site, **no conclusions about the actual availability of pages on `aesopacademy.org` can be drawn from this run.**

## Redirects (informational)

None observed (no request reached the live server).

## External Links Spot-Check

Skipped. The homepage could not be fetched, so no external `href` attributes could be extracted for spot-checking.

---

## Summary

0 broken internal link(s) confirmed — **no live data this run.** All 911 URLs returned fetch errors at the crawler sandbox layer (HTTP 403 `host_not_allowed`) before reaching the origin. This is an infrastructure condition, not a site outage, and is now in its eighth consecutive run. Next scheduled run should retry from an environment that permits egress to `aesopacademy.org`.

### Stats
- Internal URLs built from seeds + `course-registry.json`: 911
- Internal URLs successfully fetched: 0
- Internal URLs recorded as fetch error: 911 (all 911 directly confirmed via parallel curl returning `403 host_not_allowed`)
- External URLs spot-checked: 0 (skipped — homepage fetch blocked)
- Run duration: ~11 seconds (full 12-way parallel curl pass through all 911 URLs)

### Check-list composition
- 6 seed URLs
- 14 language-variant `courses.html` URLs (`ar`, `de`, `es`, `fa`, `fr`, `hi`, `ja`, `ko`, `ru`, `sw`, `tr`, `ur`, `zh`, `zh-TW` — discovered from `ai-academy/modules/<lang>/courses.html` directories on disk; the registry has no `_meta.languages` field, and the canonical `en` content is served at the un-prefixed `/ai-academy/modules/electives-hub.html` path that is already covered by the seed list)
- 128 non-coming-soon course directory indexes (from registry entries with `status: live` (126) plus `status: retired` (2 — `society` and `ar-11`, both of whose URLs alias live-course directories and dedupe out); 3 `coming-soon` entries (`governance`, `ethics`, `building`) excluded per the routine)
- 763 module URLs (`{slug}-m{N}.html` for N = 1..len(modules) per non-coming-soon course; sum of `len(modules)` across all 128 non-coming-soon entries minus 18 URLs that aliased and deduped against the two retired courses)

### Note on URL-count change vs. last successful run
Last run (2026-05-07) built 909 URLs; this run builds 911 — a net +2. The course-registry.json gained one new live course entry between 2026-05-07 and 2026-05-09 (live-course count 125 → 126); the additional URL count is the new directory index plus its module entries, partially offset by deduplication against the existing retired-course aliases.

### Control-host change vs. last run
Yesterday's run (2026-05-07) noted `https://api.github.com/` returning `200` from the crawler sandbox; today the same probe returns `403 host_not_allowed`, so the egress allow-list has tightened back to permit only `github.com` (the bare host). The block on `aesopacademy.org` and on the other control hosts (`anthropic.com`, `google.com`, `example.com`) is unchanged.
