# AESOP Live Link Check Report

**Generated:** 2026-08-30 10:10 UTC
**Status:** 🟡 WARNINGS — live fetch blocked at sandbox egress (9th week running); local proxy check still flags the same 1 candidate broken module URL
**URLs checked:** 897 · **404s:** 0 confirmed · **Errors:** 897 (all fetch errors) · **Redirects:** 0

---

## 404 Not Found

None **confirmed** — see fetch-error notice below. Per the routine guardrail, infrastructure failures are not reported as 404s.

The **local repo proxy check** (see "Local proxy check" further down) again flagged the same URL it flagged the previous eight weeks as a strong candidate for a live 404 — its backing file is still missing from the deployed source tree:

- `https://aesopacademy.org/ai-academy/modules/eval-benchmark/eval-benchmark-m1.html` — registry lists `eval-benchmark` as `status: "live"` with `modCount: 1`, but the directory `ai-academy/modules/eval-benchmark/` still does not exist in the repo. The course tile likely links to a page that was never built. No change vs. 2026-08-23 / 2026-08-02 / 2026-07-19 / 2026-07-05 / 2026-06-28 / 2026-06-21 / 2026-06-14 — the underlying fix has not landed. The daily `aip/audit-report.md` (latest 2026-08-28) independently flags the same `MISSING_DIR` error, so the finding is corroborated by a second signal. Same audit also confirms the course has no incoming link from `courses.html` (a separate `NOT_IN_COURSES_HTML` warning), so the tile appears to be orphaned in the registry rather than actively linked from the live site — likely a low-severity user-visible break (a stale registry entry) rather than a broken visitor path.

## Other Errors (5xx / Timeout / SSL)

All 897 URLs in the check list returned **fetch errors** this run, identical signature to the previous eight weeks. Both `curl` and `web_fetch` from the routine container fail at the egress proxy with `HTTP/1.1 403 Forbidden` against `aesopacademy.org:443` — the proxy's own status endpoint (`$HTTPS_PROXY/__agentproxy/status`) reports `connect_rejected · "gateway answered 403 to CONNECT (policy denial or upstream failure)"` for the host. The block is at the network policy layer, not at the live origin. Today's control probes:

| Host | Status |
| --- | --- |
| `https://aesopacademy.org/` | 403 (proxy CONNECT rejected, `curl` exit 56; `web_fetch` returns `EGRESS_BLOCKED`) |
| `https://aesopacademy.org/ai-academy/courses.html` | 403 (proxy CONNECT rejected) |
| `https://aesopacademy.org/ai-academy/modules/eval-benchmark/eval-benchmark-m1.html` | 403 (proxy CONNECT rejected) |

The proxy's `noProxy` list still only exempts anthropic.com, npmjs, jsr, pypi, crates, and go-proxy hosts — every non-GitHub upstream is denied. This is the **ninth consecutive weekly run** blocked the same way (see 2026-06-07, 2026-06-14, 2026-06-21, 2026-06-28, 2026-07-05, 2026-07-19, 2026-08-02, and 2026-08-23 reports). The site itself is deployed via **Cloudflare Pages** (see `.github/workflows/deploy.yml`), so the block is not the origin — it's the sandbox's egress allow-list. Recommended fix: switch this routine's environment to a more permissive network policy, or add `aesopacademy.org` (and ideally `discord.gg`) to the egress allow-list for the current one. Reference: https://code.claude.com/docs/en/claude-code-on-the-web (network policies / environments).

Representative fetch-error entries (pattern is identical for all 897):

- `https://aesopacademy.org/` — fetch error: HTTP 403 (egress-blocked)
- `https://aesopacademy.org/ai-academy/courses.html` — fetch error: HTTP 403 (egress-blocked)
- `https://aesopacademy.org/ai-academy/modules/electives-hub.html` — fetch error: HTTP 403 (egress-blocked)
- `https://aesopacademy.org/ai-news/` — fetch error: HTTP 403 (egress-blocked)
- `https://aesopacademy.org/about/mission.html` — fetch error: HTTP 403 (egress-blocked)
- `https://aesopacademy.org/review/aesop-sitemap.html` — fetch error: HTTP 403 (egress-blocked)
- `https://aesopacademy.org/ai-academy/modules/ai-and-creativity/ai-and-creativity-m1.html` — fetch error: HTTP 403 (egress-blocked)
- …and 890 further course / module URLs with the same fetch-error signature.

## Redirects (informational)

None observed (no request reached the live server).

## External Links Spot-Check

Attempted via local extraction of `<a href="…">` attributes from `index.html` and `ai-academy/courses.html` since the live homepage couldn't be fetched. **One** unique external host referenced from those two pages (unchanged vs. 2026-08-23):

- `https://discord.gg/pKDa5ryX` — fetch error: HTTP 403 (egress-blocked, not site-blocked; control probe against `https://discord.gg/` also 403 from this container)

Not reachable from this container. Cannot confirm or deny liveness from this run.

---

## Local proxy check (substitute for live fetch)

Since live HTTP fetch is unavailable, this run again ran a **best-effort proxy check** against the deployed source tree on `main`: for each URL in the check list, map to its filesystem path (`https://aesopacademy.org/foo/bar.html` → `<repo>/foo/bar.html`; trailing `/` → `index.html`) and verify the file exists. This catches *static* link rot (the file isn't built / deployed in the repo) but not server-side issues, MIME problems, or content errors.

### Result

- **770** of 897 URL targets resolved to a file present in the repo (unchanged vs. 2026-08-23).
- **125** course-directory URLs lack an `index.html` in the repo — see "Systemic course-directory pattern" below.
- **2** URL targets have no backing path, both under `eval-benchmark/`: `ai-academy/modules/eval-benchmark/` and `ai-academy/modules/eval-benchmark/eval-benchmark-m1.html` (previously bucketed as 1 missing file + 126 missing dir-index — same underlying finding, split differently this run because the directory itself doesn't exist).

### Systemic course-directory pattern

All 125 live course-directory URLs (e.g. `/ai-academy/modules/ai-and-creativity/`) map to a directory that exists but does not contain an `index.html` — this is systemic across the whole live catalog, not a per-course bug. Live behavior of these URLs cannot be determined from the repo alone; on Cloudflare Pages these typically resolve via directory-index conventions or a rewrite rule, so many may serve 200 in production. Once the egress block is resolved, the next run should clarify by fetching these URLs.

### Registry state vs. previous run

- **Total URL count 897 (unchanged).** The registry's `_meta` block is still absent, so 0 language-variant `courses.html` URLs were built this week (same as 2026-08-23). Live-course count unchanged at 126. If language pages are still deployed but the registry no longer advertises them, they will continue to be silently skipped by this crawler until `_meta.languages` is restored — worth confirming on the next live-fetch-capable run.

---

## Summary

0 broken internal link(s) confirmed live — **no live data this run** (9th week in a row). All 897 URLs returned fetch errors at the routine container's egress layer (HTTP 403 `host_not_allowed`) before reaching the origin. This is the routine's environment, not a site outage.

**Local proxy check** (run as a fallback) surfaced the same **1 likely broken course (2 URL targets)** that has been pending since 2026-06-14: `eval-benchmark` (registry entry exists with `status: live`, directory does not). The daily course audit (`aip/audit-report.md`, latest 2026-08-28) independently flags the same `MISSING_DIR` error, and the same course is missing from `courses.html` — so the tile is likely orphaned in the registry rather than actively linked from the site. 125 course-directory URLs without local `index.html` remain flagged as systemic — confirmation requires live fetch.

**Action required:** widen this routine's egress allow-list to include `aesopacademy.org` (and ideally the external hosts it references). Until then the live crawl portion of this routine is non-functional and the proxy-check fallback is the only signal.

### Stats
- Internal URLs checked: 897 (all fetch errors)
- External URLs spot-checked: 1 (fetch error — egress-blocked)
- Local proxy check: 770 present · 125 dir-without-index (systemic) · 2 fully missing (both `eval-benchmark`)
- Run duration: ~1 minute
