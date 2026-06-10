# BUILD — The Ladder Redesign (morgan-dev)

**For:** CeCe (Claude Code)
**Branch:** `morgan-dev` (already created — do not branch again)
**Companion docs:** `AUDIT-LADDER-REDESIGN.md` (run after build), `design-handoff-ladder/` (design package)
**Prepared by:** Morgan + Fable, 2026-06-10

---

## 0. What this is

Apply the new Aesop AI Academy design system to The Ladder, and split the single overloaded
`/theladder/index.html` into separate pages. Two goals, equal priority:

1. **Re-skin** — implement the new brand (4 themes × light/dark, square corners, light
   editorial type) per `design-handoff-ladder/BRAND_GUIDE.md`.
2. **Restructure** — homepage becomes a **marketing landing page only** (Scott's explicit
   requirement). All product functionality moves to dedicated pages.

**Read first, in order:**
1. `design-handoff-ladder/README.md` — per-screen specs
2. `design-handoff-ladder/BRAND_GUIDE.md` — full token/component system
3. This file

The `design-handoff-ladder/references/*.dc.html` files are **interactive prototypes** — open
them in a browser to see exact look and behavior. They use a prototyping runtime
(`support.js`, `<x-dc>`, `{{ }}` holes) — **ignore the runtime entirely**; recreate the
screens in this repo's actual stack.

### Authority order (when sources disagree)
1. **Live functionality** — nothing that works today may be lost (see §2)
2. This BUILD doc
3. `design-handoff-ladder/` (BRAND_GUIDE.md + README.md + references)
4. Repo `DESIGN.md` / `PRODUCT.md` — **superseded for `/theladder/*` pages** (see §10)

### Hard constraints
- **Vanilla stack only.** Plain HTML + CSS + ES modules, exactly like the existing code. No
  React, no build tooling, no npm dependencies, no Tailwind.
- **Preserve all live functionality** (§2 inventory). The design prototypes were created
  from the public URL without project access — where a prototype shows a simplified fake
  (static quiz, hardcoded tier names), the **real implementation wins** and gets restyled.
- **Real data, not prototype data.** Tier names/rung counts come from `LADDER_TIERS` in
  `theladder/ladder-data.js` (see §6.2). The prototype's tier names (Foundations,
  Conversation, Prompting…) are placeholders — never render them.
- **Tokens only.** No hardcoded hex in components — every color via the CSS custom
  properties in BRAND_GUIDE.md §3–4. Square corners everywhere (`border-radius: 0`).
  Display headings weight 400, never 700+.
- **Don't touch:** `theladder-shared/` engines, `ai-academy/`, root-site pages, Firebase
  rules, `aesop-api/`. Exceptions only where §5/§7 explicitly says so.
- **Surgical changes.** Move code; don't rewrite logic. Every changed line traces to this doc.

---

## 1. Page architecture (target)

| URL | Purpose | Design reference | Status |
|---|---|---|---|
| `/theladder/index.html` | **Marketing landing only** — no app logic | `references/Home.dc.html` | Rebuild |
| `/theladder/ladder.html` | The climb hub — tier accordion, progress, resume | `references/The Ladder.dc.html` | New |
| `/theladder/assessment.html` | AI placement conversation (real engine, new skin) | `references/Assessment.dc.html` | New |
| `/theladder/climb.html` | Rung workspace — guided conversation, vocab, resources, certification | No prototype — build in brand language (§6.5) | New |
| `/theladder/transcript.html` | Transcript / verifiable record | `references/Transcript.dc.html` | New |
| `/theladder/authenticate.html` | Auth — keep working; restyle is a stretch goal (§9) | — | Keep |

**Navigation map** (top bar on every page, per Home spec):
- Logo/wordmark → `/theladder/` (marketing home)
- "The Ladder" → `/theladder/ladder.html`
- "Transcripts" → `/theladder/transcript.html`
- **"Training" and "Certification" nav items: omit for now** (no pages designed yet — per
  handoff README "hide the links until they exist"). Leave an HTML comment where they go.
- "Get started" / "Start climbing" / assessment CTAs → `/theladder/assessment.html`
- Hub "Resume rung N" → `/theladder/climb.html?tier={n}&rung={n}` (§6.5)
- Avatar (34px square, learner initials, only when a learner exists) → `/theladder/transcript.html`

**Old-link compatibility:** other site pages link to `/theladder/` expecting the app. That
link now lands on marketing — acceptable (one click to "The Ladder" in nav). Do **not** add
redirects. The existing deep links `/ladder-certifications.html` and
`/student-transcript-live.html` (root site) keep working and stay untouched.

---

## 2. Functionality inventory — nothing on this list may break

Everything below currently lives in `/theladder/index.html` (1,034 lines) bound by
`/theladder/ladder-app.js` (3,886 lines). Each item moves to a destination page and must
work after the move. This table is the **contract** — the audit checks every row.

| # | Feature (current DOM ids) | Current location | Destination |
|---|---|---|---|
| F1 | Language switcher, 11 languages (`languageSelect`, `data-i18n` bindings) | nav | All functional pages (not marketing home — see §8) |
| F2 | Dark mode toggle (`darkToggle`, `aesop-theme` key) | nav | Replaced by new theme switcher, all pages (§4) |
| F3 | Cert count badge (`navCertCount`) — **dead code today**: the inline `updateNavCertCount()` script targets an element that exists nowhere in the repo | nav | Drop the dead script with the old index.html; certification counts live on in F5 |
| F4 | Education focus selector (`educationFocusSelect` — routes between Concepts/Products/Use-Cases pathways) | hero | ladder.html header area |
| F5 | Hero progress stats (`heroCertCount`, `heroCoursesComplete`, `heroTiersComplete`, `heroTiersCertified`, `heroTiersExpert`, `heroTiersMastered`, `heroRibbonTrack`) | hero | ladder.html summary card + stats (§6.2) |
| F6 | Topic search "Find a Rung" (`topicSearchInput`, `topicSearchResults`) | hero panel | ladder.html (below climb header) |
| F7 | Certification launcher (`certificationTierSelect`, `testDepthSelect`, `startEvaluationBtn`, `activeEvaluationTarget`, `evaluationCooldownNotice`) — incl. education-tier vs professional-role dropdown (O*NET/WEF) per `LADDER-ARCHITECTURE-UPDATE-2026-06-10.md` | hero panel | climb.html certification panel |
| F8 | **AI placement assessment** — full conversational flow (`placementSection`, `placementStatus`, `placementSummary`, `startPlacementBtn`, `togglePlacementBtn`, `resetPlacementBtn`, `placementProfilePrompt`, `applyPlacementProfileBtn`, `dismissProfilePromptBtn`, `assessmentTurnCount`, `assessmentTopBtn`, `assessmentLatestBtn`, `assessmentLog`, `assessmentForm`, `assessmentInput`, `assessmentSend`, `placementMetrics`) | placement section | assessment.html (§6.4) |
| F9 | Overall progress meter (`progressBar`, `progressText` — "N of 270 rungs") | placement section | ladder.html summary card |
| F10 | Tier rail (`tierList`, `tierCompletionStatus`) | workspace | ladder.html accordion (§6.2) |
| F11 | Active topic workspace (`activeTierLabel`, `activeTopicTitle`, `educationTierSelect`, `completeTopicBtn` "Mark self-reported") | workspace | climb.html |
| F12 | Certification workspace panel (`certificationWorkspaceTarget`, `certificationWorkspaceCooldown`, `startWorkspaceCertificationBtn`, `ladderCertificationsLink`, `studentTranscriptLink`) | workspace | climb.html |
| F13 | Vocab panels (`vocabCount`, `vocabList`, `vocabDefinitionTerm`, `vocabDefinitionBox`, `vocabPromptForm`, `vocabPromptInput`) | workspace | climb.html |
| F14 | Exam-in-progress banner (`examInProgressBanner`) | workspace | climb.html |
| F15 | **Guided conversation** — core learning loop (`conversationTitle`, `conversationSummary`, `startConversationBtn`, `chatLog`, `chatForm`, `chatInput`) + certification exam mode (`certificationModeBar`, `certificationModeTitle`, `certificationModeDetail`, `finalizeCertificationBtn`, `endCertificationBtn`) | workspace | climb.html |
| F16 | Resources panel (`resourceList`, `researchBtn` "Find more videos") | workspace | climb.html |
| F17 | Transcript panel (`transcriptList`, `transcriptPageLink`, `exportTranscriptBtn`) | workspace | transcript.html (full page now; §6.6) |
| F18 | Certification guide dialog (`architectureDialog`, `architectureDialogTitle`, `architectureDialogContent`) | dialog | climb.html |
| F19 | Firebase auth + learner identity (`ladder-auth.js`, `authenticate.html`, identity-assurance levels, adult attestation `aesop-ladder-adult-attested`) | app-wide | unchanged, loaded on all functional pages |
| F20 | State persistence — localStorage `aesop-learner-id`, `aesop-ladder-state` + Firestore sync | app-wide | unchanged keys, loaded on all functional pages |
| F21 | AI proxy calls via `/aesop-api/proxy.php` (placement, conversation, certification, vocab, research) | app-wide | unchanged |

**Marketing home gets NONE of these.** It loads zero app JS (theme switcher only).

---

## 3. Build order

Work phase by phase; commit at the end of each phase (conventional commits, see §11).

| Phase | Deliverable |
|---|---|
| P0 | Foundation: `ladder-brand.css` + `theme.js` (token system, components, switcher) |
| P1 | `index.html` — marketing landing |
| P2 | JS split: extract `ladder-core.js` from `ladder-app.js` (§7) |
| P3 | `ladder.html` — climb hub |
| P4 | `assessment.html` — placement |
| P5 | `climb.html` — rung workspace |
| P6 | `transcript.html` — record |
| P7 | Cleanup: retire dead code, cache-busters, version headers, run AUDIT |

P1 can ship before P2–P6 exist by temporarily pointing nav links at `/theladder/index.html#`
placeholders — but **do not merge to main** until all phases pass audit. Old `index.html`
functionality must never be unreachable on a deployed build.

---

## 4. P0 — Foundation: theme system & component CSS

Create **`/theladder/ladder-brand.css`**:
- The full token contract from BRAND_GUIDE.md §3, with all **8 palettes** (§4) — exact hex,
  scoped by `[data-theme="..."][data-mode="..."]` on `<html>` or `#app` root.
- Themes: `indigo` (Focus, default), `emerald` (Scholar), `spring` (Explorer), `volt`
  (Arcade). Note volt-light's inverted primary (ink button, neon text) — copy hex exactly.
- Base styles + components per §5–7: type scale (display font per theme via
  `--font-display`), buttons (primary/ghost/paired-flush), top bar, eyebrow + 7×7 accent
  square, stat tiles, editorial list rows, tier accordion rows, rung squares, progress bars,
  quiz/option rows, verified seal, status pills, footer.
- Google Fonts: Schibsted Grotesk, Bricolage Grotesque, Space Grotesk (weights per §5).
  Body stays Helvetica Neue stack.
- Motion per §8 — **use IntersectionObserver** adding an `is-in` class (not
  `animation-timeline: view()`); respect `prefers-reduced-motion`; content must default to
  visible if JS fails.

Create **`/theladder/theme.js`** (ES module, no app dependencies):
- Theme switcher popover per handoff README "Interactions" (4 theme swatches, each named in
  its own display font, + Light/Dark segmented control).
- Persist to `localStorage["aesop_theme"]` as `{"theme":"indigo","mode":"light"}`; read on
  load before first paint (inline head snippet to avoid flash).
- **Back-compat:** on first load, if `aesop_theme` absent but legacy `aesop-theme` === `'dark'`,
  seed mode=dark. On every mode change, also write legacy `aesop-theme` = `'light'|'dark'`
  so the rest of aesopacademy.org keeps respecting the user's mode.
- Loaded by **every** /theladder page including marketing home.

New ladder pages **stop loading** `/academy-theme.css` and `/academy-dark-mode.css` — the
brand CSS is self-contained. `theladder/ladder.css` (2,923 lines) survives only as a source
to port needed rules from; by P7 the new pages must not link it (leave the file in place —
other pathways may reference patterns from it; deletion is out of scope).

---

## 5. P1 — Marketing home (`/theladder/index.html`)

Rebuild per `references/Home.dc.html` + handoff README §"Home". Sections top-to-bottom:
top bar (Theme + "Get started"), hero ("The Ladder" 172px + "Your climb" panel), stats strip,
"What is The Ladder", Pathways editorial list (01–05), How it works (Assess → Climb →
Certify), Who it's for, final CTA band, footer.

Adaptations from prototype (the real-data rule):
- **Hero "Your climb" panel:** if learner state exists in localStorage, show their real
  current tier/progress (read via a tiny inline module that only reads `aesop-ladder-state`
  — no full app load); otherwise show the prototype's illustrative static panel content with
  real tier names from §6.2.
- **Stats strip:** "15 Tiers · 270 Rungs · 1:1 Mentor · ∞ Self-paced" — fine as marketing
  copy (matches real totals today).
- **Pathways list (01–05):** The Ladder → `ladder.html`; Assessment → `assessment.html`;
  Transcript → `transcript.html`; Training and Certification rows render **without links**
  (cursor default, no arrow hover) until those pages exist.
- Keep the existing `<head>` SEO/OG meta block (lines 1–31 of current index.html) — update
  description wording if needed, keep all og: / twitter: tags and favicons.
- Preserve the page version comment convention (`<!-- theladder-vX.Y.Z | date -->`) — bump
  to `v0.2.0`.

**No app JS on this page.** No auth, no Firebase, no i18n select (marketing is English-only
for now — see §8), no learner panels beyond the read-only hero climb panel.

---

## 6. P2–P6 — Functional pages

### 6.1 Shared chrome (all functional pages)
Top bar per BRAND_GUIDE §7 (sticky, blurred, hairline bottom): mark + "Aesop" wordmark, nav
(The Ladder / Transcripts, active state = weight 600 `--primary`), right side: language
select (F1, restyled as a quiet select), Theme button, avatar.
Slim footer variant. All pages `data-reveal` sections per §8 motion rules.

### 6.2 `ladder.html` — the climb hub (per `references/The Ladder.dc.html`)
- Climb header: eyebrow "Your climb · Welcome back, {learner}" (fall back to "Your climb"
  when anonymous); H1 "The Ladder" (96px); subline with current tier name italicized.
- Summary card (3px accent top border): overall % (F9), big rungs-done / rungs-total
  (computed from state — **never hardcode 47/270**), progress bar, **Resume rung** primary
  button → climb.html deep link, meta line "{n} tiers complete · Tier {m} of 15".
- Hero stats F5 fold into this card area as a 4–5 col stat strip; cert ribbon
  (`heroRibbonTrack`) renders under it.
- Topic search F6 as a panel below the header.
- Education focus selector F4 near the header (routes to `/theladder-products/`,
  `/theladder-use-cases/` — labels unchanged).
- **Tier accordion** (F10): 15 rows from `LADDER_TIERS` — **real names**:
  1 General AI Literacy · 2 Chat Mastery · 3 Information Fluency · 4 Business Process
  Design · 5 Visual & Audio Creation · 6 Business Function Mastery · 7 Workflow Automation
  & Integration · 8 Application Development · 9 Knowledge Systems & Retrieval · 10 Agentic
  Systems & Orchestration · 11 System Reliability & Operations · 12 Security & Threat
  Mitigation · 13 Legal, Ethics & Compliance · 14 Model Science & Advanced Techniques ·
  15 Strategic Planning & Adoption.
  Row spec per BRAND_GUIDE §7 "Tier row" (badge states done/current/locked, 110px progress
  bar, chevron). Expanded panel: rung-square grid (one square per topic in that tier,
  **count from data**), "Next — Rung N · {topic}" line, action button (Resume / Review /
  Locked) → climb.html deep link. Single-open accordion, current tier open by default.
  Status legend above the list.
- **Locked-tier semantics:** follow the app's real unlock logic from state (placed-out
  tiers count as done). If the current app treats all tiers as browsable, "locked" is
  visual-only — do not invent new gating logic.

### 6.3 State/data wiring
All real data comes through the extracted core (§7): learner state, per-tier/per-rung
progress, certifications, placement status. No page hardcodes progress numbers.

### 6.4 `assessment.html` — placement (per `references/Assessment.dc.html`, adapted)
The prototype shows a static 5-question quiz with a fixed Tier-3 result. **Discard the fake
quiz content; keep its three-phase shell and styling** and run the real AI placement (F8):
- **Intro phase:** prototype's intro styled as designed ("Find your rung", 88px) — copy
  adjusted to describe the conversational assessment honestly (e.g. stat row: "adaptive
  conversation / 15 tiers / ∞ retakes"). "Begin assessment" → starts the real placement
  conversation (current `startPlacementBtn` behavior, including profile prompt F8 and adult
  attestation if it currently gates here).
- **Conversation phase:** the existing assessment log + input form (`assessmentLog`,
  `assessmentForm`…) restyled into the centered 760px stage; turn counter + Top/Latest
  controls kept. The 3px progress bar under the header may advance per assistant turn
  (approximate is fine) — purely cosmetic.
- **Result phase:** when `LADDER_PLACEMENT_COMPLETE` fires, render the designed result
  screen ("You belong on / Tier {NN} / {Real tier name}") from the **real placement payload**,
  with the real stats (tiers placed out, rungs granted). "Start climbing from Tier {n}" →
  `climb.html` deep link; "Retake" → existing reset flow (`resetPlacementBtn`).
- Standalone chrome per design: minimal top bar (mark + "Placement Assessment" + Theme +
  **Exit** → `/theladder/`). Language select stays (the engine takes `languageLabel`).
- "View results" for returning placed users: landing here with a completed placement shows
  the result phase directly (current `togglePlacementBtn` behavior).

### 6.5 `climb.html` — rung workspace (no prototype; design it in the brand system)
The page learners actually work in. Layout, in brand language:
- Top bar (6.1) + a compact climb header: eyebrow "Tier {NN} · {Tier name}", H1 = active
  topic title (display 400, ~54px), meta (rung n of N, education tier select F11 restyled).
- Two-column workspace grid (collapse to single column < 1024px):
  - **Main column:** guided conversation panel (F15) — chat log, input, exam mode bar with
    its accent treatment (use `--accent` 3px top border + eyebrow "Certification exam in
    progress"); exam banner F14 above it.
  - **Side column:** certification panel (F7 + F12 merged — one certification surface:
    target line, tier/role select, depth select, start button, cooldown notice, links to
    certification record + transcript); vocab panels F13; resources F16; "Mark
    self-reported" F11 action.
- Tier/rung navigation: read `?tier=&rung=` on load → set active topic via existing
  state logic; a slim prev/next rung control. The full tier rail does NOT move here (it
  lives on ladder.html); a "← All tiers" link returns to the hub.
- Certification guide dialog F18 ports here unchanged (restyle the dialog frame only).
- Empty state (no placement, no state): friendly prompt → "Take the assessment" CTA.

### 6.6 `transcript.html` (per `references/Transcript.dc.html`, adapted)
- Document header: H1 "Transcript", learner meta from real identity (name/learner ID
  `aesop-learner-id`, issued = today). Verified seal per spec.
- **"Download PDF" button = existing export** (F17 `exportTranscriptBtn` logic — keep
  whatever it produces today; do not build new PDF generation). If the design's "Share
  link" has no backing feature, omit the button.
- Summary strip computed from real state: tiers certified, rungs completed, credentials
  earned (count of certification results), time invested **only if** the app tracks it —
  otherwise drop that tile (never fake a stat).
- Credentials cards from real certification results (name, depth label, credential
  id/date if stored). "Verify →" links only if a verification URL exists today (e.g.
  `/ladder-credential.html` flow) — else omit.
- Full record table: 15 rows from real tiers + status pills (Certified / In progress /
  Not started) per BRAND_GUIDE §7.
- Transcript list detail (F17 `transcriptList` evidence entries) renders below the table
  as "Record detail" — same data as today.
- Keep links to `/student-transcript-live.html` ("Full academy transcript") so the
  root-site record stays reachable.

---

## 7. P2 — JS split strategy (the risky part — read carefully)

`ladder-app.js` binds ~80 DOM ids assuming one page. Strategy: **extract, don't rewrite.**

1. Create `/theladder/ladder-core.js` — move (verbatim where possible): Firebase init +
   auth wiring, learner id + state load/save/merge (localStorage + Firestore), proxy-call
   helpers, placement orchestration + `PLACEMENT_REGEX` parsing, certification
   orchestration (+ result/validation regexes, cooldown), transcript record builders,
   i18n helpers (`LADDER_UI_TRANSLATIONS`, `applyTranslations`), topic/tier selection state.
   Export functions; module must be **DOM-light** (no top-level `getElementById`).
2. Page entry modules: `hub-page.js`, `assessment-page.js`, `climb-page.js`,
   `transcript-page.js` — each binds only its own ids (table §2) and imports from core.
   Guard every element lookup (`?.`) so shared code never throws on missing nodes.
3. Keep `ladder-data.js` untouched. Keep `ladder-auth.js` untouched (import per page).
4. **Fallback if extraction runs into deep coupling:** keep `ladder-app.js` loaded whole on
   every functional page with an early page-type flag that no-ops the sections whose DOM is
   absent. Less clean, acceptable. Document in commit message + AUDIT-RESULTS which path
   you took and why.
5. Cross-page invariants either way: localStorage keys **unchanged** (`aesop-learner-id`,
   `aesop-ladder-state`, `aesop-ladder-adult-attested`); Firestore document shapes
   unchanged; certification result schema per `LADDER-ARCHITECTURE-UPDATE-2026-06-10.md`
   unchanged.

---

## 8. i18n policy for this build

- Functional pages keep full i18n: existing `data-i18n` keys reattach to the moved
  elements; `languageSelect` present in the chrome.
- **New strings** introduced by the redesign: add keys to the translations table with
  English values for all languages where a translation isn't trivially available — English
  fallback is acceptable and is a **warning, not a blocker**, in the audit.
- Marketing home is English-only this build (no language select). Note it in
  AUDIT-RESULTS as a known gap for the phase-2/i18n pass.

---

## 9. Stretch (only if everything above is green)

- Restyle `authenticate.html` into the brand system (keep all auth logic + identity
  assurance levels intact).
- `mockups.html` is a scratch file — leave it.

## Out of scope (do NOT do in this build)

- `theladder-products/` and `theladder-use-cases/` restyle — **Phase 2, separate
  BUILD doc.** They keep working against the old academy theme meanwhile; their nav links
  to `/theladder/` and shared-engine imports must keep functioning (audit checks).
- Training and Certification marketing pages (not designed yet).
- Assessment auto-scoring quiz, "Share link", new PDF generation, responsive breakpoint
  *design* work beyond clean single-column collapse (per handoff README "Open items").
- Deleting `ladder.css` or old assets.

---

## 10. Known conflicts — flag, don't fix

1. **Repo `DESIGN.md`/`PRODUCT.md` ban teal/green-blue accents.** The new brand's
   `emerald` and `spring` themes are green/teal by design. The design handoff supersedes
   DESIGN.md **for /theladder pages only**. Do not "correct" the palettes. Add a short
   note at the top of `DESIGN.md`: *"/theladder/* pages follow
   `design-handoff-ladder/BRAND_GUIDE.md` (4-theme system), which supersedes this file for
   those pages — agreed Morgan/Scott 2026-06."* Scott's impeccable-audit scripts may flag
   these colors — that's expected; note it in AUDIT-RESULTS.
2. **Prototype content vs. real data** — covered in §2/§6; prototype always loses.
3. **Theme key migration** — covered in §4.

---

## 11. Hygiene & conventions

- **Commits:** conventional (`feat:`, `refactor:`, `docs:`…), one per phase minimum,
  never leave changes uncommitted. Work only on `morgan-dev`; no pushes to `main`.
- **Cache-busters:** bump `?v=` on every changed/added CSS/JS reference (current:
  `ladder.css?v=51`, `ladder-app.js?v=50`).
- **Version headers:** each page gets the `<!-- theladder-vX.Y.Z | date -->` comment;
  bump to `v0.2.0` for this redesign.
- **Scope check before finishing:** `git diff main --stat` should show only: `/theladder/*`,
  `BUILD-LADDER-REDESIGN.md`, `AUDIT-LADDER-REDESIGN.md`, `AUDIT-RESULTS-LADDER-REDESIGN.md`,
  `design-handoff-ladder/*`, and the one-line `DESIGN.md` note. Anything else is a bug.
- When done: run **`AUDIT-LADDER-REDESIGN.md`** top to bottom and write
  `AUDIT-RESULTS-LADDER-REDESIGN.md` (format defined there).
