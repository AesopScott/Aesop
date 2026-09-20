# AESOP Live Link Check Report

**Generated:** 2026-09-20 10:10 UTC
**Status:** 🟡 WARNINGS — live fetch blocked at sandbox egress (10th week running); local proxy check still flags the same 1 candidate broken module URL
**URLs checked:** 897 · **404s:** 0 confirmed · **Errors:** 897 (all fetch errors) · **Redirects:** 0

---

## 404 Not Found

None **confirmed** — see fetch-error notice below. Per the routine guardrail, infrastructure failures are not reported as 404s.

The **local repo proxy check** (see "Local proxy check" further down) again flagged the same URL it flagged the previous nine weeks as a strong candidate for a live 404 — its backing file is still missing from the deployed source tree:

- `https://aesopacademy.org/ai-academy/modules/eval-benchmark/eval-benchmark-m1.html` — registry lists `eval-benchmark` as `status: "live"` with `modCount: 1`, but the directory `ai-academy/modules/eval-benchmark/` still does not exist in the repo. The course tile likely links to a page that was never built. No change vs. 2026-08-30 / 2026-08-23 / 2026-08-02 / 2026-07-19 / 2026-07-05 / 2026-06-28 / 2026-06-21 / 2026-06-14 — the underlying fix has not landed. The daily `aip/audit-report.md` (latest 2026-09-19) independently flags the same `MISSING_DIR` error, so the finding is corroborated by a second signal. Same audit also confirms the course has no incoming link from `courses.html` (a separate `NOT_IN_COURSES_HTML` warning), so the tile appears to be orphaned in the registry rather than actively linked from the live site — likely a low-severity user-visible break (a stale registry entry) rather than a broken visitor path.

## Other Errors (5xx / Timeout / SSL)

All 897 URLs in the check list returned **fetch errors** this run, identical signature to the previous nine weeks. Both `curl` and `web_fetch` from the routine container fail at the egress proxy with `HTTP/1.1 403 Forbidden` against `aesopacademy.org:443` — the proxy's own status endpoint (`$HTTPS_PROXY/__agentproxy/status`) reports `connect_rejected · "gateway answered 403 to CONNECT (policy denial or upstream failure)"` for the host. The block is at the network policy layer, not at the live origin. Today's control probes:

| Host | Status |
| --- | --- |
| `https://aesopacademy.org/` | 403 (proxy CONNECT rejected, `curl` exit 56) |
| `https://aesopacademy.org/ai-academy/courses.html` | 403 (proxy CONNECT rejected) |
| `https://discord.gg/pKDa5ryX` | 403 (proxy CONNECT rejected, external control) |

The proxy's `noProxy` list still only exempts anthropic.com, npmjs, jsr, pypi, crates, and go-proxy hosts — every non-GitHub upstream is denied. This is the **tenth consecutive weekly run** blocked the same way (see 2026-06-07, 2026-06-14, 2026-06-21, 2026-06-28, 2026-07-05, 2026-07-19, 2026-08-02, 2026-08-23, and 2026-08-30 reports). The site itself is deployed via **Cloudflare Pages** (see `.github/workflows/deploy.yml`), so the block is not the origin — it's the sandbox's egress allow-list. Recommended fix: switch this routine's environment to a more permissive network policy, or add `aesopacademy.org` (and ideally `discord.gg`) to the egress allow-list for the current one. Reference: https://code.claude.com/docs/en/claude-code-on-the-web (network policies / environments).

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

Attempted via local extraction of `<a href="…">` attributes from `index.html` and `ai-academy/courses.html` since the live homepage couldn't be fetched. **One** unique external host referenced from those two pages (unchanged vs. 2026-08-30):

- `https://discord.gg/pKDa5ryX` — fetch error: HTTP 403 (egress-blocked, not site-blocked; control probe against `https://discord.gg/` also 403 from this container)

Not reachable from this container. Cannot confirm or deny liveness from this run.

## Local proxy check (repo-side heuristic)

Because live fetches keep being blocked, this run again walked the registry against the local filesystem to flag URLs whose backing files are missing from the source tree — a strong indicator that they would 404 on the live site.

- **Registry entries scanned:** 131 total (126 `live`, 3 `coming-soon`, 2 `retired` — same distribution as 2026-08-30)
- **`_meta.languages` block:** still absent from `course-registry.json`; the routine's Step 1 language-variant URLs (`/ai-academy/modules/{lang}/courses.html`) yielded 0 additions.
- **Live courses whose directory is missing on disk:** 1 (unchanged)
  - `eval-benchmark` → `ai-academy/modules/eval-benchmark/` — directory does not exist; registry lists it as `live` with `modCount: 1`. Corroborated by `aip/audit-report.md` (2026-09-19) `MISSING_DIR` finding.
- **Live courses whose per-module HTML file is missing on disk (`{cid}-m{N}.html`):** only the eval-benchmark case above; no other new gaps.

This is a heuristic — the deployed site may include files not in the source tree (unlikely for Cloudflare Pages, which builds from `main`) — but the audit report's independent `MISSING_DIR` finding on the same course means both signals now agree for the tenth consecutive week.

---

## Summary

0 confirmed broken internal links (no requests reached the live origin — egress blocked for the tenth consecutive week). **1 candidate 404** flagged by local repo cross-check: `ai-academy/modules/eval-benchmark/eval-benchmark-m1.html` — no change since 2026-06-14, and corroborated by today's `aip/audit-report.md`.

**Action needed:** either (a) grant the routine's egress allow-list `aesopacademy.org` so future runs can distinguish real 404s from block errors, or (b) fix the stale `eval-benchmark` registry entry (create the missing directory + module page, or set its status to `coming-soon`/`retired`).

### Stats
- Internal URLs planned: 897 (6 seeds + 126 live-course dir URLs + 765 per-module URLs; 0 language-variant URLs — no `_meta.languages` in registry)
- Internal URLs successfully checked against the live origin: 0 (all 897 blocked at egress)
- External URLs planned for spot-check: 1 unique host (from local HTML extraction)
- External URLs successfully checked: 0 (blocked at egress)
- Local repo heuristic candidates flagged: 1 (unchanged, 10 consecutive weeks)
- Run duration: <1 minute (fast-fail on egress rejection)
