# AUDIT RESULTS — Ladder Redesign — 2026-06-10

Build commits: `3cf3f73c..ed508eee` (P0–P6 + DESIGN.md note + audit fixes, on `morgan-dev`)
JS strategy used: **extraction** (`ladder-core.js` + four page entry modules), not whole-app gating.
Why: `ladder-app.js` already routed every DOM touch through one `el` lookup table, so the
extraction was mechanical — `bindDom()` moved into `initCore()` (module is DOM-light at top
level), every element use null-guarded, the old `renderTiers` tier rail replaced by a
`tierProgress()` helper consumed by `hub-page.js`, dark-toggle code removed (owned by
`theme.js`), and a `registerPageRenderer()` hook lets each page render its own new UI inside
the core render cycle. Engine logic (placement, certification, validation, transcript,
persistence, i18n) moved verbatim — the four schema-bearing functions
(`buildCertificationResult`, `saveCertificationResult`, `recordCertificationResult`,
`normalizeCertificationValidation`) are byte-identical between `ladder-app.js` and
`ladder-core.js` (md5-verified).

**Test setup:** served from repo root with the repo's existing `npx serve` launch config
(static — PHP/keys unavailable, so `/aesop-api/proxy.php` AI round-trips are **N-T** per the
AUDIT setup rules; the app's graceful-fallback paths were exercised instead). Two profiles
tested: fresh (cleared localStorage) and returning learner (seeded pre-redesign-shaped
`aesop-ladder-state` blob: 3 placed-out tiers, completed/self-reported topics, one `ai_exam`
credential, placement payload, assessment messages). Firebase/Firestore ran live against the
real project (Write channels returned 200 for the generated learner `AESOP-5GZE`).

**Test-server artifact (not an app bug):** `npx serve` 301-redirects `*.html` URLs to clean
URLs and **drops query strings** in the redirect, so `.html?tier=&rung=` deep links were
tested via the extensionless form. Production serves `.html` directly; no redirect occurs.

| Item | Result | Notes |
|------|--------|-------|
| A1   | PASS   | Language select on all 4 functional pages; Spanish re-labels (`Niveles certificados`, `Tu ID de estudiante:`) and reverts; Arabic renders (`مستويات معتمدة`). Marketing home English-only by design (known-acceptable #3). |
| A2   | PASS   | Switcher on all 5 pages incl. marketing home: 4 themes, each name in its own display font, Light/Dark segmented control, active dot. Found+fixed during audit: popover closed itself after theme selection (re-render detached the clicked button; close handler now ignores detached targets) — commit `ed508eee`. |
| A3   | PASS   | `grep updateNavCertCount\|navCertCount` → zero hits outside retired `ladder-app.js`. Cert counts render in the hub stat strip (certified 1/15 with seed). |
| A4   | PASS   | Changing the select navigated to `/theladder-products/` (verified live); `/theladder-use-cases/` option present and that page loads. |
| A5   | PASS   | Seeded state → 56/270 rungs, 21%, 3 tiers complete, `Resume rung 3` → `climb.html?tier=4&rung=3`, ribbon shows the 1 exam-certified tier (assessment certs correctly excluded from ribbons). Numbers recomputed after every localStorage change (fresh profile showed zeros; D3 probe changed totals). |
| A6   | PASS   | "prompt injection" returned ranked results; **Start** navigated to climb.html at T12-L02 with the right topic active. |
| A7   | PASS (note) | Selector populated: 3 education tiers + 14 professional roles with O*NET/WEF tags. Depth select shows **three** levels (Core/Expert/Master Certification) — the standalone "Certification" depth was intentionally removed in commit `51331637` after the AUDIT doc was written; real implementation wins. Start-button gating and cooldown notice intact (cooldown is 0 ms today via the pre-existing `CERTIFICATION_COOLDOWN_MS` TODO — unchanged). |
| A8   | N-T (AI) / PASS (shell) | No proxy on static server. Verified: Begin starts the real engine (actual opener message), send appends the user turn and renders the engine's fallback reply, turn counter increments, Top/Latest scroll, restart/reset clear state. Result phase rendering verified via seeded placement payload (Tier 04 · Business Process Design, real stats 3 tiers placed out / 54 rungs granted / 3 assigned). |
| A9   | PASS   | Returning placed learner lands directly on the result phase; **Retake** resets to intro, clears placement grants + assessment-source certs, keeps earned/self-reported topics. |
| A10  | PASS   | 15 rows, single-open, current tier open by default, badge/progress/meta from state (3 done badges, placed-out meta), rung-square counts from data — D3 probe rendered 19 squares for tier-01. "Locked" is visual-only; rows stay browsable with an enabled "Start tier" action (BUILD §6.2 — no new gating invented; meta reads "not started" rather than "locked" to stay honest). |
| A11  | PASS   | `?tier=4&rung=3` opened T04-L03 ("AI-assisted action item extraction"); education tier select renders/persists; **Mark self-reported** wrote `self_reported` to state and updated hub progress. Deep link wins over both local and remote loads; prev/next keep the URL shareable. |
| A12  | PASS (note) | Certification surface is the F7+F12 **merge** prescribed by BUILD §6.5: one target line, one start button, cooldown notice, links to certification record + student transcript (with `?id=` learner param) all work. The redundant F12 duplicate ids (`certificationWorkspaceTarget/-Cooldown`, `startWorkspaceCertificationBtn`) were retired with the merge; core still guards them. |
| A13  | PASS (UI) / N-T (AI) | 14 terms render for the tier, definitions display on click and mark reviewed, ask-form present and wired; round-trip needs proxy. |
| A14  | PASS (shell) / N-T (AI) | Start conversation works (real first message + fallback reply); starting certification raised exam mode: banner visible, mode bar with depth title/detail, Examiner labels and exam styling on messages; **Return to training** restored the training conversation. Finalize appears after 2 learner turns per existing logic. |
| A15  | PASS (render) / N-T (AI) | Resources list renders for the active topic. "Find more videos" is the unchanged `findVideos` (YouTube search in a new tab) — not click-tested in the headless preview to avoid popup handling; code identical to pre-redesign. |
| A16  | PASS (note) | `transcriptList` evidence entries match state; export button runs the **unchanged** JSON export builder (byte-identical function) — the download artifact itself isn't inspectable in the headless preview. `/student-transcript-live.html?id=AESOP-5GZE` link present and page loads. Button labeled "Export transcript" (it produces the existing JSON, not a PDF — labeling it "Download PDF" would misdescribe the artifact; BUILD §6.6 keeps the existing export). |
| A17  | PASS   | Dialog opens with the full certification guide (current target rendered), scrolls, closes. |
| A18  | N-T (sign-in) / PASS (preserved) | `authenticate.html` + `ladder-auth.js` are untouched (git-clean) and the page loads. No test credentials exist for a live Firebase sign-in from the audit session. Learner identity is reflected where it exists (avatar initials "5G", transcript meta `AESOP-5GZE`); adult-attestation gate code unchanged. |
| A19  | PASS   | Keys unchanged (`aesop-learner-id`, `aesop-ladder-state`, `aesop-ladder-adult-attested`). A pre-redesign-shaped state blob loaded cleanly — no migration, nothing dropped (placed-out topics, certs, placement, assessment messages, transcript events all surfaced). Firestore sync live: learner doc created and Write channels 200 on persist. |
| A20  | PASS   | Final fresh load of `/theladder/`: network shows page assets + Google Fonts + `theme.js` only — no Firebase, no Firestore, no proxy, no auth. |
| B1   | PASS   | Grep clean across new HTML, `*-page.js`, `theme.js`. Also clean in `ladder-core.js` (the celebration modal's hardcoded hex was re-skinned to tokens). Theme-switcher swatches use `--swatch-*` tokens defined in `ladder-brand.css`. |
| B2   | PASS   | Only `border-radius: 0` (global reset); none elsewhere. |
| B3   | PASS   | No 700+ weights in `ladder-brand.css`; display styles are weight 400 (500 for wordmark per spec). |
| B4   | PASS   | All 8 palettes computed-verified against BRAND_GUIDE §4 (6 tokens per palette spot-checked) including volt-light inverted primary `#171D14`/on-primary `#AEF24E` with `--fill` staying `#5F9C0A`. |
| B5   | PASS   | Schibsted Grotesk / Bricolage Grotesque / Space Grotesk woff2s load with the specified weights; `--font-display` switches per theme (computed); body stack is Helvetica Neue. |
| B6   | PASS (note) | Side-by-side vs prototypes: top bar, eyebrow + 7×7 accent square (+hero rule), paired flush buttons (shared seam, no gap), editorial pathway rows (bg tint + arrow slide on hover), tier rows + rung squares, verified seal, status pills all match. **Quiz/option rows don't appear** — the prototype's static quiz was replaced by the real conversational assessment per BUILD §6.4 (the `.opt-row` component exists in the CSS for future use). |
| B7   | PASS   | IntersectionObserver adds one-shot `is-in` (30px rise, .9s ease-out-expo); `prefers-reduced-motion` rule disables; hidden initial state only applies under `html.js`, so content is visible whenever JS fails. |
| B8   | PASS   | At 1440px: hero 172px / weight 400 / Schibsted (computed), "Your climb" panel 1px border + 3px `#E8843C` accent top border, stats strip hairline dividers, ink CTA band. |
| C1   | PASS   | volt+dark set on home persisted across ladder → climb → assessment → transcript; `aesop_theme` JSON correct; legacy `aesop-theme` mirrors mode; inline pre-paint head snippet on every page → no theme flash on reload. |
| C2   | PASS   | Fresh profile with only `aesop-theme: 'dark'` opened indigo-dark (`#121022` body background). |
| C3   | PASS   | All hrefs enumerated and resolve; Training/Certification absent from nav/footer with HTML comment placeholders; pathway rows 02/04 render unlinked. Found+fixed during audit: footer "About"/"For schools" pointed at `/about/` and `/for-schools/` which have no index pages → now `/pedagogy.html` and `/institutional-procurement.html` (the root site's real For Schools target) — commit `ed508eee`. |
| C4   | PASS   | Zero console errors across every page, fresh AND seeded profiles, through all interactions (theme switching, search, deep links, exam mode, placement begin/send/retake, export, dialog, language switching). |
| C5   | PASS   | `/ladder-certifications.html`, `/student-transcript-live.html`, `/theladder/authenticate.html`, `/ladder-credential.html` all load unchanged (the 301s observed locally are the test server's clean-URL redirect, not a repo change). |
| D1   | PASS   | Grep for `Foundations|Context & Memory|Images & Vision|Code with AI` → zero matches in `theladder/*.html` + `*.js`. All rendered names come from `LADDER_TIERS` (or, on the no-app marketing panel, an inline copy of the same 15 real names). |
| D2   | PASS   | Grep for `Avery|AES-2026-04471|47 / 270|Tier 03` → zero matches in shipped pages. |
| D3   | PASS   | Temporarily added a 19th topic to tier-01 in `ladder-data.js`: hub total became **271**, tier-01 meta "0 / 19 rungs", rung grid rendered 19 squares; reverted (file restored byte-identical via git). |
| D4   | PASS (by inspection) / N-T (live) | A full stubbed certification needs the proxy. Schema preservation proven instead: the four functions that build/store certification results and validations are **byte-identical** (md5) between `ladder-app.js` and `ladder-core.js`; `LADDER-ARCHITECTURE-UPDATE-2026-06-10.md` field set untouched. |
| E1   | PASS   | `/theladder-products/` (500-product catalog, category rail, course panel, certification tests) and `/theladder-use-cases/` load and run with zero console errors; shared-engine imports resolve; their old academy styling unchanged; nav links incl. `/theladder/` work. |
| E2   | PASS   | `/index.html` and `/ai-academy/students.html` render as before and still respect the legacy `aesop-theme` key (mirrored by theme.js). |
| E3   | PASS   | `git diff main --stat` contains exactly: `BUILD-LADDER-REDESIGN.md`, `AUDIT-LADDER-REDESIGN.md`, this file, `DESIGN.md` (+2 lines, the note only), `design-handoff-ladder/*`, `theladder/*`. No edits to `theladder-shared/`, `aesop-api/`, `ai-academy/`, `firestore.rules`, or `.claude/launch.json`. |
| F1   | PASS   | Conventional commits, one+ per phase (P0 `3cf3f73c`, P1 `56ec74b1`, P2 `6749f4ec`, P3 `2767fae5`, P4 `e3cbe082`, P5 `1e738aa1`, P6 `730ed71e`, docs `1ce9f8df`, audit fixes `ed508eee`); working tree clean. |
| F2   | PASS   | All new CSS/JS referenced with `?v=1`; `ladder-data.js` keeps `?v=2` (file unchanged). Old `ladder.css?v=51` / `ladder-app.js?v=50` no longer referenced by any page. |
| F3   | PASS   | All five pages open with `<!-- theladder-v0.2.0 | 2026-06-10 -->`. |
| F4   | PASS   | `DESIGN.md` diff is exactly the one supersession note (2 lines incl. blank), nothing else. |

Screenshots: captured live in the preview browser during this audit (desktop ~1440px and
~390px mobile): marketing home in indigo-light, indigo-dark, volt-dark + theme popover, and
all 8 theme×mode token sets computed-verified; hub (volt-dark, fresh + seeded), climb
workspace with exam mode, assessment result phase, transcript with credential card. The
preview harness does not persist screenshot files into the repo — re-capture with
`scripts/impeccable-ladder-audit.ps1` or a manual pass if archival copies are needed.

Open issues / follow-ups:
1. **i18n pass** — new redesign strings (summary card, accordion meta, result-phase copy,
   record table, marketing home) render in English in all 11 languages; existing
   `data-i18n` keys reattached where they exist (known-acceptable #2). Marketing home is
   English-only this build (known-acceptable #3).
2. **Training and Certification pages** — nav/footer placeholders in HTML comments; pathway
   rows 02/04 unlinked until designed (per handoff README).
3. **AI round-trips untested locally** (placement completion signal, guided-conversation
   completion, certification result + validator, vocab ask, standards review) — engine code
   moved verbatim and all fallback paths exercised; verify once against a PHP host with
   keys before merging to main.
4. **authenticate.html restyle** — stretch goal not taken; page works unchanged in the old
   academy theme.
5. Pre-existing (not introduced, left untouched per the surgical rule):
   `CERTIFICATION_COOLDOWN_MS = 0` TODO; `state.educationTierId` defaults to `'college'`
   which is not in `EDUCATION_TIERS`, so the climb "Teach at" select starts blank until the
   learner picks a value.
6. **Emerald/spring palettes are green/teal** — intentional, DESIGN.md superseded for
   /theladder pages (known-acceptable #1); Scott's impeccable-audit scripts may flag.
7. **Responsive** — clean single-column collapse verified at 390px; dedicated mobile design
   remains a later pass (known-acceptable #4).
