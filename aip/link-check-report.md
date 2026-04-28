# AESOP Live Link Check Report

**Generated:** 2026-04-28 16:15 UTC
**Status:** 🟡 WARNINGS — fetch infrastructure unavailable this run
**URLs checked:** 684 · **404s:** 0 · **Errors:** 684 (all fetch errors) · **Redirects:** 0

---

## 404 Not Found

None found.

> No URL could be confirmed as a 404 this run — see "Other Errors" below. Per the routine guardrail, infrastructure failures are not reported as 404s.

## Other Errors (5xx / Timeout / SSL)

All 684 URLs in the check list returned **fetch errors** this run. Both `curl` and `web_fetch` from the crawler sandbox responded with `HTTP 403 · x-deny-reason: host_not_allowed` for every request against `aesopacademy.org` (and against `www.aesopacademy.org`), indicating that outbound HTTP egress from the crawler sandbox was blocked at the network layer — not that the live site is down. This is the same infrastructure condition observed in the 2026-04-26 and 2026-04-27 runs. A control fetch of `https://example.com/` from the same sandbox also returned `403 host_not_allowed`, while `https://github.com/` returned `200`, confirming the block is an allow-list at the sandbox egress proxy and is not specific to `aesopacademy.org`.

Examples (representative — pattern is identical for all 684):

- `https://aesopacademy.org/` — fetch error: HTTP 403 `host_not_allowed` (sandbox egress denied)
- `https://aesopacademy.org/ai-academy/courses.html` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/ai-academy/modules/electives-hub.html` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/ai-news/` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/about/mission.html` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/review/aesop-sitemap.html` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/ai-academy/modules/es/courses.html` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/ai-academy/modules/ai-and-creativity/ai-and-creativity-m1.html` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/ai-academy/modules/working-with-the-anthropic-api/working-with-the-anthropic-api-m8.html` — fetch error: HTTP 403 `host_not_allowed`
- …and 675 further course / module URLs with the same fetch-error signature.

Because every URL failed identically at the sandbox layer before reaching the live site, no conclusions about the actual availability of pages on `aesopacademy.org` can be drawn from this run. The crawler loop was halted after 140 confirming requests (all `403 host_not_allowed`) to avoid wasting cycles on a uniformly blocked host; the remaining 544 URLs in the check list are recorded as fetch errors by inference from the identical sandbox response.

## Redirects (informational)

None observed (no request reached the live server).

## External Links Spot-Check

Skipped. The homepage could not be fetched, so no external `href` attributes could be extracted for spot-checking.

---

## Summary

0 broken internal link(s) confirmed — **no live data this run.** All 684 URLs returned fetch errors at the crawler sandbox layer (HTTP 403 `host_not_allowed`) before reaching the origin. This is an infrastructure condition, not a site outage. Next scheduled run should retry from an environment that permits egress to `aesopacademy.org`.

### Stats
- Internal URLs built from seeds + `course-registry.json`: 684
- Internal URLs successfully fetched: 0
- Internal URLs recorded as fetch error: 684 (140 directly confirmed via curl; 544 inferred from the identical sandbox response)
- External URLs spot-checked: 0 (skipped — homepage fetch blocked)
- Run duration: ~1 minute (curl pass halted after uniform `403 host_not_allowed` response was confirmed)

### Check-list composition
- 6 seed URLs
- 12 language-variant `courses.html` URLs (`ar`, `de`, `es`, `fa`, `fr`, `hi`, `ja`, `ko`, `ru`, `sw`, `ur`, `zh` — discovered from `ai-academy/modules/<lang>/courses.html` directories, since the registry no longer carries a `_meta.languages` array)
- 91 live course directory indexes (from registry `status != coming-soon` entries — 92 live entries dedupe to 91 unique directory URLs because two course IDs share the `performing-arts-and-ai/` directory)
- 575 module URLs (`{course-id}-m{N}.html` for N = 1..len(modules) per live course)

### Note on URL-count change vs. last week
Last week's run built 608 URLs; this week's run built 684. The +76 delta breaks down as:
- **+11 language-variant URLs** — language variants are now sourced from filesystem `ai-academy/modules/<lang>/` directories (12 locales: `ar`, `de`, `es`, `fa`, `fr`, `hi`, `ja`, `ko`, `ru`, `sw`, `ur`, `zh`) instead of from a registry `_meta.languages` array, which was last seen with only `en` and is no longer present in the registry.
- **+10 live course directory URLs** — 91 unique live course directories this week vs. 81 last week, reflecting newly-promoted courses in the registry.
- **+54 module URLs** — 575 module pages this week vs. 521 last week, reflecting both newly-live courses and additional modules added to existing live courses between 2026-04-27 and 2026-04-28.
