# AESOP Live Link Check Report

**Generated:** 2026-09-06 10:11 UTC
**Status:** 🟡 WARNINGS — live fetch blocked at sandbox egress (10th week running); local proxy check flags the same 1 candidate broken module URL and surfaces 2 retired courses whose registry module URLs no longer resolve
**URLs checked:** 913 · **404s:** 0 confirmed · **Errors:** 913 (all fetch errors) · **Redirects:** 0

---

## 404 Not Found

None **confirmed** — see fetch-error notice below. Per the routine guardrail, infrastructure failures are not reported as 404s.

The **local repo proxy check** (see "Local proxy check" further down) again flagged the same URL it flagged the previous nine weeks as a strong candidate for a live 404 — its backing file is still missing from the deployed source tree:

- `https://aesopacademy.org/ai-academy/modules/eval-benchmark/eval-benchmark-m1.html` — registry lists `eval-benchmark` as `status: "live"` with `modCount: 1`, but the directory `ai-academy/modules/eval-benchmark/` still does not exist in the repo. The course tile likely links to a page that was never built. No change vs. 2026-08-30 / 2026-08-23 / 2026-08-02 / 2026-07-19 / 2026-07-05 / 2026-06-28 / 2026-06-21 / 2026-06-14 — the underlying fix has not landed. The daily `aip/audit-report.md` (latest 2026-09-05) independently flags the same `MISSING_DIR` error, so the finding is corroborated by a second signal. Same audit also confirms the course has no incoming link from `courses.html` (a separate `NOT_IN_COURSES_HTML` warning), so the tile appears to be orphaned in the registry rather than actively linked from the live site — likely a low-severity user-visible break (a stale registry entry) rather than a broken visitor path.

**New this week (registry hygiene, not necessarily live 404s):** the two retired courses `society` (title *AI in Society*) and `ar-11` (title *Performing Arts and AI*) each list 8 modules in the registry (`modCount: 8`, `modules[]` length 8), but their `id` no longer matches their `url` slug — `society.url = /ai-academy/modules/ai-in-society/` and `ar-11.url = /ai-academy/modules/performing-arts-and-ai/`. The routine's URL-construction rule (`{course-id}/{course-id}-m{N}.html`) therefore builds paths that do not exist in the repo (`ai-academy/modules/society/society-m*.html` × 8 and `ai-academy/modules/ar-11/ar-11-m*.html` × 8). The actual retired-course files still exist at the renamed paths (`ai-academy/modules/ai-in-society/ai-in-society-m1..m9.html` and `ai-academy/modules/performing-arts-and-ai/performing-arts-and-ai-m1..m8.html`), so these are unlikely to be user-visible 404s (retired courses aren't linked from `courses.html` by definition). Two remediations either fix it: (a) drop the `modules[]` array or set `modCount: 0` on retired entries; or (b) rewrite the routine's URL rule to derive from `c.url` rather than `c.id` (the URL field is authoritative). Option (a) is safer — it also stops the tile from advertising module content that isn't reachable via the tile's own directory URL.

## Other Errors (5xx / Timeout / SSL)

All 913 URLs in the check list returned **fetch errors** this run, identical signature to the previous nine weeks. Both `curl` and `web_fetch` from the routine container fail at the egress proxy with `HTTP/1.1 403 Forbidden` against `aesopacademy.org:443` — the proxy's own status endpoint (`$HTTPS_PROXY/__agentproxy/status`) reports `connect_rejected · "gateway answered 403 to CONNECT (policy denial or upstream failure)"` for the host. The block is at the network policy layer, not at the live origin. Today's control probes:

| Host | Status |
| --- | --- |
| `https://aesopacademy.org/` | 403 (proxy CONNECT rejected, `curl` exit 56; `web_fetch` returns `EGRESS_BLOCKED`) |
| `https://aesopacademy.org/ai-academy/courses.html` | 403 (proxy CONNECT rejected via `web_fetch`, `EGRESS_BLOCKED`) |
| `https://discord.gg/` | 403 (proxy CONNECT rejected, `curl` exit 56) |

The proxy's `noProxy` list still only exempts anthropic.com, npmjs, jsr, pypi, crates, and go-proxy hosts — every non-GitHub upstream is denied. This is the **tenth consecutive weekly run** blocked the same way (see 2026-06-07, 2026-06-14, 2026-06-21, 2026-06-28, 2026-07-05, 2026-07-19, 2026-08-02, 2026-08-23, and 2026-08-30 reports). The site itself is deployed via **Cloudflare Pages** (see `.github/workflows/deploy.yml`), so the block is not the origin — it's the sandbox's egress allow-list. Recommended fix: switch this routine's environment to a more permissive network policy, or add `aesopacademy.org` (and ideally `discord.gg`) to the egress allow-list for the current one. Reference: https://code.claude.com/docs/en/claude-code-on-the-web (network policies / environments).

Representative fetch-error entries (pattern is identical for all 913):

- `https://aesopacademy.org/` — fetch error: HTTP 403 (egress-blocked)
- `https://aesopacademy.org/ai-academy/courses.html` — fetch error: HTTP 403 (egress-blocked)
- `https://aesopacademy.org/ai-academy/modules/electives-hub.html` — fetch error: HTTP 403 (egress-blocked)
- `https://aesopacademy.org/ai-news/` — fetch error: HTTP 403 (egress-blocked)
- `https://aesopacademy.org/about/mission.html` — fetch error: HTTP 403 (egress-blocked)
- `https://aesopacademy.org/review/aesop-sitemap.html` — fetch error: HTTP 403 (egress-blocked)
- `https://aesopacademy.org/ai-academy/modules/ai-and-creativity/ai-and-creativity-m1.html` — fetch error: HTTP 403 (egress-blocked)
- …and 906 further course / module URLs with the same fetch-error signature.

## Redirects (informational)

None observed (no request reached the live server).

## External Links Spot-Check

Attempted via local extraction of `<a href="…">` attributes from `index.html` and `ai-academy/courses.html` since the live homepage couldn't be fetched. **One** unique external host referenced from those two pages (unchanged vs. 2026-08-30):

- `https://discord.gg/pKDa5ryX` — fetch error: HTTP 403 (egress-blocked, not site-blocked; control probe against `https://discord.gg/` also 403 from this container)

Not reachable from this container. Cannot confirm or deny liveness from this run.

---

## Local proxy check (substitute for live fetch)

Since live HTTP fetch is unavailable, this run again ran a **best-effort proxy check** against the deployed source tree on `main`: for each URL in the check list, map to its filesystem path (`https://aesopacademy.org/foo/bar.html` → `<repo>/foo/bar.html`; trailing `/` → `index.html`) and verify the file exists. This catches *static* link rot (the file isn't built / deployed in the repo) but not server-side issues, MIME problems, or content errors.

### Result

- **770** of 913 URL targets resolved to a file present in the repo (unchanged from 2026-08-30 in absolute terms — the 16-URL registry growth this week is entirely new retired-course module URLs that have no backing file).
- **125** course-directory URLs lack an `index.html` in the repo — see "Systemic course-directory pattern" below (unchanged).
- **18** URL targets have no backing path (up from 2 last week). Breakdown:
  - **2** under `eval-benchmark/` (unchanged, 10th week): `ai-academy/modules/eval-benchmark/` (directory absent) and `ai-academy/modules/eval-benchmark/eval-benchmark-m1.html`.
  - **8** under `society/` (new this week — retired course id/url mismatch): `ai-academy/modules/society/society-m1.html` through `-m8.html`. Retired course, files live at `ai-in-society/ai-in-society-m1..m9.html` per the entry's `url` field.
  - **8** under `ar-11/` (new this week — retired course id/url mismatch): `ai-academy/modules/ar-11/ar-11-m1.html` through `-m8.html`. Retired course, files live at `performing-arts-and-ai/performing-arts-and-ai-m1..m8.html` per the entry's `url` field.

### Systemic course-directory pattern

All 125 live course-directory URLs (e.g. `/ai-academy/modules/ai-and-creativity/`) map to a directory that exists but does not contain an `index.html` — this is systemic across the whole live catalog, not a per-course bug. Live behavior of these URLs cannot be determined from the repo alone; on Cloudflare Pages these typically resolve via directory-index conventions or a rewrite rule, so many may serve 200 in production. Once the egress block is resolved, the next run should clarify by fetching these URLs.

### Registry state vs. previous run

- **Total URL count 913** (up from 897 last week, +16). The 16 new URLs are all retired-course module pages (`society` +8, `ar-11` +8) added since 2026-08-30. Registry `_meta` block is still absent, so 0 language-variant `courses.html` URLs were built this week (same as 2026-08-30). Live-course count unchanged at 126; retired-course count unchanged at 2 (but both retired courses' `modules[]` arrays now enumerate their 8 modules under stale `{id}-m{N}` slugs — see "New this week" note under 404 section).

---

## Summary

0 broken internal link(s) confirmed live — **no live data this run** (10th week in a row). All 913 URLs returned fetch errors at the routine container's egress layer (HTTP 403 `host_not_allowed`) before reaching the origin. This is the routine's environment, not a site outage.

**Local proxy check** (run as a fallback) surfaced:
- **1 unchanged likely-broken course (2 URL targets)** pending since 2026-06-14: `eval-benchmark` (registry entry exists with `status: live`, directory does not). The daily course audit (`aip/audit-report.md`, latest 2026-09-05) independently flags the same `MISSING_DIR` error, and the same course is missing from `courses.html` — so the tile is likely orphaned in the registry rather than actively linked from the site.
- **1 new registry-hygiene finding** (16 URL targets): retired courses `society` and `ar-11` have `modules[]` arrays enumerating 8 modules each under stale `{id}-m{N}` slugs, but their `url` fields point to renamed directories (`ai-in-society/`, `performing-arts-and-ai/`) where the actual files live. Retired courses aren't typically linked from `courses.html`, so this is likely not a user-visible 404 — but the registry is now internally inconsistent. Cleanest fix: drop `modules[]` from retired entries.
- **125 course-directory URLs** without local `index.html` remain flagged as systemic — confirmation requires live fetch.

**Action required:** widen this routine's egress allow-list to include `aesopacademy.org` (and ideally the external hosts it references). Until then the live crawl portion of this routine is non-functional and the proxy-check fallback is the only signal.

### Stats
- Internal URLs checked: 913 (all fetch errors)
- External URLs spot-checked: 1 (fetch error — egress-blocked)
- Local proxy check: 770 present · 125 dir-without-index (systemic) · 18 fully missing (2 `eval-benchmark`, 8 `society`, 8 `ar-11`)
- Run duration: ~1 minute
