# AESOP Live Link Check Report

**Generated:** 2026-05-10 16:15 UTC
**Status:** 🟡 WARNINGS — fetch infrastructure unavailable this run
**URLs checked:** 110 · **404s:** 0 · **Errors:** 110 (all fetch errors) · **Redirects:** 0

---

## 404 Not Found

None found.

> No URL could be confirmed as a 404 this run — see "Other Errors" below. Per the routine guardrail, infrastructure failures are not reported as 404s.

## Other Errors (5xx / Timeout / SSL)

All 110 URLs in the check list returned **fetch errors** this run. Both `curl` and `web_fetch` from the crawler sandbox responded with `HTTP 403 · x-deny-reason: host_not_allowed` for every request against `aesopacademy.org`, indicating that outbound HTTP egress from the crawler sandbox was blocked at the network layer — not that the live site is down. This is the eighth consecutive run to hit this condition (also observed on 2026-04-26, 2026-04-27, 2026-04-28, 2026-04-30, 2026-05-05, 2026-05-06, and 2026-05-07). Control fetches from the same sandbox today showed `https://github.com/` returning `200`, while `https://www.anthropic.com/`, `https://www.google.com/`, `https://example.com/`, `https://api.github.com/`, and `https://aesopacademy.org/` all returned `403 host_not_allowed`, confirming the block is an allow-list at the sandbox egress proxy (with `github.com` allow-listed) and is not specific to `aesopacademy.org`.

Examples (representative — pattern is identical for all 110):

- `https://aesopacademy.org/` — fetch error: HTTP 403 `host_not_allowed` (sandbox egress denied)
- `https://aesopacademy.org/ai-academy/courses.html` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/ai-academy/modules/electives-hub.html` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/ai-news/` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/about/mission.html` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/review/aesop-sitemap.html` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/ai-academy/modules/zh-TW/courses.html` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/ai-academy/modules/ai-and-creativity/ai-and-creativity-m1.html` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/ai-academy/modules/applied-ai-development/applied-ai-development-m8.html` — fetch error: HTTP 403 `host_not_allowed`
- `https://aesopacademy.org/ai-academy/modules/eval-benchmark/eval-benchmark-m1.html` — fetch error: HTTP 403 `host_not_allowed`
- …and 100 further course / module URLs with the same fetch-error signature.

Every URL failed identically at the sandbox layer before reaching the live site, so **no conclusions about the actual availability of pages on `aesopacademy.org` can be drawn from this run.**

## Redirects (informational)

None observed (no request reached the live server).

## External Links Spot-Check

Skipped. The homepage could not be fetched, so no external `href` attributes could be extracted for spot-checking.

---

## Summary

0 broken internal link(s) confirmed — **no live data this run.** All 110 URLs returned fetch errors at the crawler sandbox layer (HTTP 403 `host_not_allowed`) before reaching the origin. This is an infrastructure condition, not a site outage, and is now in its eighth consecutive run. Next scheduled run should retry from an environment that permits egress to `aesopacademy.org`.

### Stats
- Internal URLs built from seeds + `course-registry.json`: 110
- Internal URLs successfully fetched: 0
- Internal URLs recorded as fetch error: 110 (all 110 directly confirmed via `urllib`/`curl` returning `403 host_not_allowed`)
- External URLs spot-checked: 0 (skipped — homepage fetch blocked)
- Run duration: ~33 seconds

### Check-list composition
- 6 seed URLs
- 14 language-variant `courses.html` URLs (`ar`, `de`, `es`, `fa`, `fr`, `hi`, `ja`, `ko`, `ru`, `sw`, `tr`, `ur`, `zh`, `zh-TW` — discovered from `ai-academy/modules/<lang>/courses.html` directories on disk; the registry no longer carries a `_meta.languages` field after the recent rewrite, so the language code list was sourced from the filesystem)
- 13 live course directory indexes (from registry entries with `status: live`; the registry currently contains 13 live entries plus 1 retired and 5 coming-soon entries that were excluded)
- 77 module URLs (`{course-id}-m{N}.html` for N = 1..modCount per live course; sum across the 13 live entries: 8+6+6+6+6+6+8+6+6+6+6+6+1)

### Note on URL-count change vs. last run
Last run (2026-05-07) built 909 URLs; this run built 110. The drop reflects a registry rewrite committed on 2026-05-09 (`feat: build by AI Factory`) that reduced `course-registry.json` from ~7,500 lines to ~1,600 lines and left the file with several JSON-syntax artifacts (a stray `n` token, a duplicated `"id"` key, mid-string corruption inside `the-future-of-intelligence`, and a trailing `};` instead of `}`). The current registry parses only with a tolerant regex pass; strict `json.load` raises `JSONDecodeError`. This crawler's URL build worked around the corruption by extracting course keys, `status`, `modCount`, and `url` fields with regex, so the 110-URL list reflects everything the registry currently *declares* as live — but the underlying registry health is degraded and may need a separate fix outside this routine's scope.

### Control-host change vs. last run
Yesterday's run noted `https://api.github.com/` returning `200`; today the same probe returns `403 host_not_allowed`, so the egress allow-list has tightened back: only `github.com` itself appears on the allow-list today. The block on `aesopacademy.org` and on the other control hosts (`anthropic.com`, `google.com`, `example.com`) is unchanged.
