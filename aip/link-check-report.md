# AESOP Live Link Check Report

**Generated:** 2026-04-29 16:13 UTC
**Status:** 🟡 WARNINGS — fetch infrastructure unavailable this run
**URLs checked:** 772 · **404s:** 0 · **Errors:** 772 (all fetch errors) · **Redirects:** 0

---

## 404 Not Found

None found.

> No URL could be confirmed as a 404 this run — see "Other Errors" below. Per the routine guardrail, infrastructure failures are not reported as 404s.

## Other Errors (5xx / Timeout / SSL)

All 772 URLs in the check list returned **fetch errors** this run. Both `curl` and `web_fetch` from the crawler sandbox responded with `HTTP 403 · x-deny-reason: host_not_allowed` for every request against `aesopacademy.org`, indicating that outbound HTTP egress from the crawler sandbox was blocked at the network layer — not that the live site is down. This is the same infrastructure condition observed in the 2026-04-26, 2026-04-27, and 2026-04-28 runs. Control fetches from the same sandbox confirmed the block is an allow-list at the egress proxy and is not specific to `aesopacademy.org`:

- `https://example.com/` → `HTTP 403 host_not_allowed` (also blocked)
- `https://github.com/` → `HTTP 200` (allowed)

The full check-list of 772 URLs was attempted via parallel rate-limited HEAD requests (5 workers, 5 req/s ceiling) and every single response carried the identical `x-deny-reason: host_not_allowed` header. The crawler ran to completion in 154 seconds; no request reached the origin web server.

Examples (representative — pattern is identical for all 772):

- `https://aesopacademy.org/` — fetch error: HTTP 403 `host_not_allowed` (sandbox egress denied)
- `https://aesopacademy.org/ai-academy/courses.html` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/ai-academy/modules/electives-hub.html` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/ai-news/` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/about/mission.html` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/review/aesop-sitemap.html` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/ai-academy/modules/en/courses.html` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/ai-academy/modules/ai-and-creativity/ai-and-creativity-m1.html` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/ai-academy/modules/working-with-the-anthropic-api/working-with-the-anthropic-api-m8.html` — fetch error: HTTP 403 `host_not_allowed`
- …and 763 further course / module URLs with the same fetch-error signature.

Because every URL failed identically at the sandbox layer before reaching the live site, no conclusions about the actual availability of pages on `aesopacademy.org` can be drawn from this run.

## Redirects (informational)

None observed (no request reached the live server).

## External Links Spot-Check

Skipped. The homepage could not be fetched, so no external `href` attributes could be extracted for spot-checking.

---

## Summary

0 broken internal link(s) confirmed — **no live data this run.** All 772 URLs returned fetch errors at the crawler sandbox layer (HTTP 403 `host_not_allowed`) before reaching the origin. This is an infrastructure condition, not a site outage, and now spans four consecutive scheduled runs (2026-04-26 → 2026-04-29). Suggest moving the crawl to an environment that permits egress to `aesopacademy.org`, or adding the host to the sandbox egress allow-list.

### Stats
- Internal URLs built from seeds + `course-registry.json`: 772
- Internal URLs successfully fetched: 0
- Internal URLs recorded as fetch error: 772 (all directly confirmed via 772 HEAD requests, each returning `403 host_not_allowed`)
- External URLs spot-checked: 0 (skipped — homepage fetch blocked)
- Run duration: ~3 minutes (154s of network attempts plus registry parse and report write)

### Check-list composition
- 6 seed URLs
- 1 language-variant `courses.html` URL (`en` — the only language code present in the registry under any course's `_meta.languages`, per the routine spec)
- 107 unique live course directory indexes (109 live registry entries dedupe to 107 unique directory URLs because two pairs of course IDs share a directory: `society` + `ai-in-society` both map to `/ai-academy/modules/ai-in-society/`, and `ar-11` + `performing-arts-and-ai` both map to `/ai-academy/modules/performing-arts-and-ai/`)
- 658 module URLs (`{course-id}-m{N}.html` for N = 1..len(modules) per live course; raw count is 666 but 8 collide with the shared `performing-arts-and-ai/` directory entries)

### Note on URL-count change vs. last week
Last week's run (2026-04-28) built 684 URLs; this week's run built 772. The +88 delta breaks down as:
- **−11 language-variant URLs** — language variants are now sourced from the registry's `_meta.languages` field (per the routine spec), which lists only `en` across the four courses that carry the field. Last week's run sourced language variants from filesystem `ai-academy/modules/<lang>/` directories (12 locales) as a fallback; this week's run reverted to the spec-defined source. Filesystem-based discovery is recorded here for next maintenance review — consider reconciling spec vs. filesystem.
- **+16 live course directory URLs** — 107 unique live course directories this week vs. 91 last week, reflecting newly-promoted courses in the registry (109 live entries this week vs. 92 last week; dedup adjusts to 107 vs. 91).
- **+83 module URLs** — 658 module pages this week vs. 575 last week, reflecting both newly-live courses and additional modules added to existing live courses between 2026-04-28 and 2026-04-29.
