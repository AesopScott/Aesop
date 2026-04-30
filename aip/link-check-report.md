# AESOP Live Link Check Report

**Generated:** 2026-04-30 16:23 UTC
**Status:** 🟡 WARNINGS — fetch infrastructure unavailable this run
**URLs checked:** 853 · **404s:** 0 · **Errors:** 853 (all fetch errors) · **Redirects:** 0

---

## 404 Not Found

None found.

> No URL could be confirmed as a 404 this run — see "Other Errors" below. Per the routine guardrail, infrastructure failures are not reported as 404s.

## Other Errors (5xx / Timeout / SSL)

All 853 URLs in the check list returned **fetch errors** this run. Both `curl` and `web_fetch` from the crawler sandbox responded with `HTTP 403 · x-deny-reason: host_not_allowed` for every request against `aesopacademy.org`, indicating that outbound HTTP egress from the crawler sandbox was blocked at the network layer — not that the live site is down. This is the same infrastructure condition observed in the 2026-04-26, 2026-04-27, and 2026-04-28 runs. A control fetch of `https://github.com/` from the same sandbox returned `200`, while `https://example.com/` returned `403 host_not_allowed`, confirming the block is an allow-list at the sandbox egress proxy and is not specific to `aesopacademy.org`.

Examples (representative — pattern is identical for all 853):

- `https://aesopacademy.org/` — fetch error: HTTP 403 `host_not_allowed` (sandbox egress denied)
- `https://aesopacademy.org/ai-academy/courses.html` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/ai-academy/modules/electives-hub.html` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/ai-news/` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/about/mission.html` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/review/aesop-sitemap.html` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/ai-academy/modules/zh-TW/courses.html` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/ai-academy/modules/ai-and-creativity/ai-and-creativity-m1.html` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/ai-academy/modules/working-with-the-anthropic-api/working-with-the-anthropic-api-m8.html` — fetch error: HTTP 403 `host_not_allowed`
- …and 844 further course / module URLs with the same fetch-error signature.

Because every URL failed identically at the sandbox layer before reaching the live site, no conclusions about the actual availability of pages on `aesopacademy.org` can be drawn from this run. The full check list of 853 URLs was attempted via curl with five concurrent workers; every request returned `403 host_not_allowed` within milliseconds without ever reaching the origin.

## Redirects (informational)

None observed (no request reached the live server).

## External Links Spot-Check

Skipped. The homepage could not be fetched, so no external `href` attributes could be extracted for spot-checking.

---

## Summary

0 broken internal link(s) confirmed — **no live data this run.** All 853 URLs returned fetch errors at the crawler sandbox layer (HTTP 403 `host_not_allowed`) before reaching the origin. This is an infrastructure condition, not a site outage. Next scheduled run should retry from an environment that permits egress to `aesopacademy.org`.

### Stats
- Internal URLs built from seeds + `course-registry.json`: 853
- Internal URLs successfully fetched: 0
- Internal URLs recorded as fetch error: 853 (all directly confirmed via curl returning `403 host_not_allowed`)
- External URLs spot-checked: 0 (skipped — homepage fetch blocked)
- Run duration: ~1 minute (full curl pass completed in 43 seconds; every request denied at egress)

### Check-list composition
- 6 seed URLs
- 13 language-variant `courses.html` URLs (`ar`, `de`, `es`, `fa`, `fr`, `hi`, `ja`, `ko`, `ru`, `sw`, `ur`, `zh`, `zh-TW` — discovered from `ai-academy/modules/<lang>/courses.html` directories, since the registry does not carry a `_meta.languages` array)
- 120 live course directory indexes (from registry entries with `status: live` and no `comingSoon` flag — all 120 dedupe to 120 unique directory URLs; no shared directories this week)
- 714 module URLs (`{course-id}-m{N}.html` for N = 1..len(modules) per live course)

### Note on URL-count change vs. last week
Last week's run (2026-04-28) built 684 URLs; this week's run built 853. The +169 delta breaks down as:
- **+1 language-variant URL** — `zh-TW` is now picked up alongside the previously-tracked 12 locales (`ar`, `de`, `es`, `fa`, `fr`, `hi`, `ja`, `ko`, `ru`, `sw`, `ur`, `zh`); a `zh-TW/courses.html` is now present in the filesystem.
- **+29 live course directory URLs** — 120 unique live course directories this week vs. 91 last week, reflecting newly-promoted courses in the registry. The registry now contains 120 live entries (plus 3 coming-soon and 2 retired), and there are no shared directories among the 120 live entries.
- **+139 module URLs** — 714 module pages this week vs. 575 last week, reflecting both the 29 newly-live courses and additional modules added to existing live courses between 2026-04-28 and 2026-04-30.
