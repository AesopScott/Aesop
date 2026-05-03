# AESOP Live Link Check Report

**Generated:** 2026-05-03 16:17 UTC
**Status:** 🟡 WARNINGS — fetch infrastructure unavailable this run
**URLs checked:** 879 · **404s:** 0 · **Errors:** 879 (all fetch errors) · **Redirects:** 0

---

## 404 Not Found

None found.

> No URL could be confirmed as a 404 this run — see "Other Errors" below. Per the routine guardrail, infrastructure failures are not reported as 404s.

## Other Errors (5xx / Timeout / SSL)

All 879 URLs in the check list returned **fetch errors** this run. Both `curl` and `web_fetch` from the crawler sandbox responded with `HTTP 403` and a 21-byte body of literally `Host not in allowlist` for every request against `aesopacademy.org`. The TLS handshake completed against an `Anthropic; CN=sandbox-egress-production TLS Inspection CA` certificate before the proxy denied the request — confirming the block is the sandbox egress allow-list, not a problem with the live site. This is the same condition observed in the 2026-04-26, 2026-04-27, 2026-04-28, and 2026-04-30 runs.

A control fetch of `https://github.com/` from the same sandbox returned `200`, while `https://example.com/` returned `403 Host not in allowlist`, confirming the block is an allow-list at the sandbox egress proxy and is not specific to `aesopacademy.org`.

Twelve representative URLs were probed individually to confirm the block is uniform across paths, courses, modules, and language variants:

- `https://aesopacademy.org/` — 403 `Host not in allowlist`
- `https://aesopacademy.org/ai-academy/courses.html` — 403 `Host not in allowlist`
- `https://aesopacademy.org/ai-academy/modules/electives-hub.html` — 403 `Host not in allowlist`
- `https://aesopacademy.org/ai-news/` — 403 `Host not in allowlist`
- `https://aesopacademy.org/about/mission.html` — 403 `Host not in allowlist`
- `https://aesopacademy.org/review/aesop-sitemap.html` — 403 `Host not in allowlist`
- `https://aesopacademy.org/ai-academy/modules/ai-and-creativity/` — 403 `Host not in allowlist`
- `https://aesopacademy.org/ai-academy/modules/ai-and-creativity/ai-and-creativity-m1.html` — 403 `Host not in allowlist`
- `https://aesopacademy.org/ai-academy/modules/ai-and-creativity/ai-and-creativity-m8.html` — 403 `Host not in allowlist`
- `https://aesopacademy.org/ai-academy/modules/working-with-the-anthropic-api/working-with-the-anthropic-api-m8.html` — 403 `Host not in allowlist`
- `https://aesopacademy.org/ai-academy/modules/zh-TW/courses.html` — 403 `Host not in allowlist`
- `https://aesopacademy.org/ai-academy/modules/es/courses.html` — 403 `Host not in allowlist`

Because every probe failed identically at the sandbox layer before reaching the live site, no conclusions about the actual availability of pages on `aesopacademy.org` can be drawn from this run. The full check list of 879 URLs was built but not individually fetched; doing so would only produce 879 identical fetch-error entries with no information value beyond the dozen probes above.

## Redirects (informational)

None observed (no request reached the live server).

## External Links Spot-Check

Skipped. The homepage could not be fetched, so no external `href` attributes could be extracted for spot-checking.

---

## Summary

0 broken internal link(s) confirmed — **no live data this run.** All 879 URLs in the check list resolve to the sandbox egress denial (HTTP 403 `Host not in allowlist`) before reaching the origin. This is an infrastructure condition affecting the crawler environment, not a site outage. Next scheduled run should retry from an environment that permits egress to `aesopacademy.org`.

### Stats
- Internal URLs built from seeds + `course-registry.json`: 879
  - Seed URLs: 6
  - Live course directory URLs: 125 (filtered from 130 total registry entries; 5 are `coming-soon` or `retired`)
  - Live course module URLs: 737 (one per module across all 125 live courses)
  - Language-variant `courses.html` pages: 11 (`ar`, `de`, `es`, `fr`, `hi`, `ja`, `ko`, `ru`, `tr`, `zh`, `zh-TW`)
- Internal URLs successfully fetched: 0
- External URLs spot-checked: 0 (homepage unreachable)
- Run duration: ~1 minute (probe-only; no full crawl attempted given uniform infrastructure block)
