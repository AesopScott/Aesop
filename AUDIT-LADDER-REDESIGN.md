# AUDIT — The Ladder Redesign (morgan-dev)

**Run after completing `BUILD-LADDER-REDESIGN.md`.** Record every item in
`AUDIT-RESULTS-LADDER-REDESIGN.md` as **PASS / FAIL / N-T** (not testable, with reason).
FAIL on any item in sections A, C, D, or E blocks handoff — fix and re-run.

## Setup

- Serve the repo root locally. Prefer `php -S localhost:8080` from repo root (enables
  `/aesop-api/proxy.php` if PHP + keys are configured). If PHP/keys unavailable, use any
  static server and mark AI round-trip items **N-T** with reason — do not fake them.
- Test pages: `/theladder/`, `/theladder/ladder.html`, `/theladder/assessment.html`,
  `/theladder/climb.html`, `/theladder/transcript.html`.
- Two browser profiles: one **fresh** (no localStorage), one **returning learner**
  (seed by completing/simulating placement + some progress, or import an existing
  `aesop-ladder-state`).
- Screenshots required (desktop ~1440px and ~390px width): every page in
  indigo-light and indigo-dark; plus the home page in all 8 theme×mode combos.

---

## A. Functionality preservation (the contract — BUILD §2 table)

Verify each row F1–F21 on its destination page:

- [ ] **A1 (F1)** Language select present on all functional pages; switching to Spanish
      re-labels UI strings; switching back works. Spot-check one RTL (Arabic) renders.
- [ ] **A2 (F2/§4)** Theme switcher on every page incl. marketing home: 4 themes listed,
      each name in its own display font, Light/Dark segmented control, active dot.
- [ ] **A3 (F3)** Dead `updateNavCertCount()` script not carried forward; certification
      counts (certified + expert + mastered) appear correctly in the hub summary (A5).
- [ ] **A4 (F4)** Education focus select routes to `/theladder-products/` and
      `/theladder-use-cases/`.
- [ ] **A5 (F5/F9)** Hub summary card: progress %, rungs done/total, tier counts, and cert
      ribbon all match the seeded state — and are **computed** (change state in
      localStorage, reload, numbers change).
- [ ] **A6 (F6)** Topic search returns results and navigates to the right rung in climb.html.
- [ ] **A7 (F7)** Certification launcher: education-tier vs professional-role dropdown
      populated per `LADDER-ARCHITECTURE-UPDATE-2026-06-10.md` (roles show O*NET/WEF tags),
      depth select shows CORE/Certification/Expert/Master, start button gates correctly,
      cooldown notice logic intact.
- [ ] **A8 (F8)** Placement: full conversational flow on assessment.html — begin, exchange
      turns, completion signal renders the result phase with the **real** placed tier (real
      name from `LADDER_TIERS`), rungs granted, placed-out tiers. (N-T allowed without
      proxy; then verify at minimum: conversation UI renders, send/turn-counter/Top/Latest
      work against a stubbed response, reset/retake clears state.)
- [ ] **A9 (F8)** Returning placed learner landing on assessment.html sees the result
      phase ("View results" behavior); Retake resets.
- [ ] **A10 (F10)** Hub accordion: 15 rows, single-open, current tier open by default,
      badge/progress states correct from state, rung-square counts match each tier's
      topic count in `ladder-data.js` (no hardcoded 18).
- [ ] **A11 (F11)** climb.html: deep link `?tier=&rung=` opens the right topic; education
      tier select works; "Mark self-reported" updates state + hub progress.
- [ ] **A12 (F12)** Certification workspace panel: target line, start, links to
      certification record + transcript pages work.
- [ ] **A13 (F13)** Vocab: list populates per topic, definitions display, "ask about this
      term" round-trips (N-T without proxy).
- [ ] **A14 (F14/F15)** Guided conversation: start, chat round-trip (N-T without proxy),
      exam mode bar appears during certification, finalize + return-to-training buttons
      behave, exam-in-progress banner shows when applicable.
- [ ] **A15 (F16)** Resources list renders; "Find more videos" triggers research flow
      (N-T without proxy).
- [ ] **A16 (F17)** transcript.html: records list matches state; Download PDF/export
      produces the same artifact as the old export; link to
      `/student-transcript-live.html` present and working.
- [ ] **A17 (F18)** Certification guide dialog opens, content loads, closes.
- [ ] **A18 (F19)** Auth: authenticate.html sign-in/out works; signed-in learner identity
      reflected (avatar initials, transcript meta); adult attestation gate unchanged.
- [ ] **A19 (F20)** localStorage keys unchanged: `aesop-learner-id`, `aesop-ladder-state`,
      `aesop-ladder-adult-attested`. An existing pre-redesign state blob loads cleanly
      (no migration required, nothing dropped). Firestore sync still reads/writes.
- [ ] **A20** Marketing home loads **zero** app JS: no Firebase requests, no proxy calls,
      no auth — network tab shows only page assets + fonts (+ theme.js).

## B. Design fidelity (BRAND_GUIDE.md)

- [ ] **B1** Tokens only: `grep -rn "#[0-9a-fA-F]\{3,8\}" theladder/*.html theladder/*-page.js theladder/theme.js`
      — hex appears **only** in `ladder-brand.css` token definitions (and legacy untouched
      files). No inline hex in new components.
- [ ] **B2** Square corners: `grep -rn "border-radius" theladder/ladder-brand.css theladder/*.html`
      → only `border-radius: 0` or absent (legacy files exempt).
- [ ] **B3** Light headings: no `font-weight: 700`+ on display-font elements in new CSS.
- [ ] **B4** All 8 palettes present; spot-check 3 exact hex values per theme against
      BRAND_GUIDE §4 (incl. volt-light inverted primary `#171D14`/`#AEF24E`).
- [ ] **B5** Fonts: 3 Google display fonts loaded with specified weights; body stack is
      Helvetica Neue; display font switches with theme.
- [ ] **B6** Component spot-checks vs. prototypes side-by-side: top bar, eyebrow + 7×7
      accent square, paired flush buttons (no gap, shared seam), editorial pathway rows
      (hover: bg tint + arrow slide), tier row + rung squares, quiz/option rows on
      assessment, verified seal, status pills.
- [ ] **B7** Motion: scroll reveals via IntersectionObserver, one-shot, ~30px rise;
      `prefers-reduced-motion` disables; **JS disabled → all content still visible**.
- [ ] **B8** Home hero matches prototype at 1280px: 172px display heading, "Your climb"
      panel with 3px accent top border, stats strip with hairline dividers, ink CTA band.

## C. Cross-page behavior

- [ ] **C1** Theme persistence: set Explorer+dark on home → navigate all pages → persists;
      `localStorage["aesop_theme"]` JSON correct; legacy `aesop-theme` mirrors mode;
      reload → no flash of wrong theme.
- [ ] **C2** Legacy seed: fresh profile with only `aesop-theme: 'dark'` → new pages open
      in dark mode.
- [ ] **C3** Navigation map: every nav/footer/CTA link on every page lands correctly;
      Training/Certification absent (HTML comment placeholder only); no dead links
      (`grep -rn 'href="' theladder/*.html` and click through).
- [ ] **C4** Zero console errors on load + primary interactions, every page, fresh AND
      returning profiles.
- [ ] **C5** Old URLs intact: `/ladder-certifications.html`, `/student-transcript-live.html`,
      `/theladder/authenticate.html` load unchanged.

## D. Data integrity

- [ ] **D1** Tier names rendered anywhere = the 15 real names from `ladder-data.js`
      (General AI Literacy … Strategic Planning & Adoption). **Zero** occurrences of
      prototype names: `grep -rn -E "Foundations|Context & Memory|Images & Vision|Code with AI" theladder/*.html theladder/*.js`
      (excluding design-handoff-ladder/) → no matches in shipped pages.
- [ ] **D2** No fake learner data: `grep -rn -E "Avery|AES-2026-04471|47 / 270|Tier 03" theladder/` (excluding handoff folder) → no matches.
- [ ] **D3** Totals computed: temporarily edit a tier's topics array length locally →
      hub totals/rung grids update accordingly (then revert).
- [ ] **D4** Certification result schema untouched (`LADDER-ARCHITECTURE-UPDATE-2026-06-10.md`
      §Data Storage): complete a (stubbed) certification → stored object has all fields.

## E. Regression — rest of the repo

- [ ] **E1** `/theladder-products/` and `/theladder-use-cases/` load and run: shared-engine
      imports resolve, their nav links (including to `/theladder/`) work, styling unchanged.
- [ ] **E2** Root site unaffected: `/index.html`, `/ai-academy/students.html`,
      `/ai-academy/transcript.html` render as before (they still use `aesop-theme`).
- [ ] **E3** Scope check: `git diff main --stat` contains only the files allowed by
      BUILD §11. No edits to `theladder-shared/`, `aesop-api/`, `ai-academy/`,
      `firestore.rules`.

## F. Hygiene

- [ ] **F1** Conventional commits, one+ per phase, nothing uncommitted.
- [ ] **F2** Cache-busters bumped on all changed/added CSS/JS references.
- [ ] **F3** Page version comments present (`theladder-v0.2.0`).
- [ ] **F4** `DESIGN.md` supersession note added (one line, per BUILD §10.1) — and nothing
      else in that file changed.

## Known acceptable findings (pre-approved — report as PASS-WITH-NOTE)

1. Emerald/spring palettes contain green/teal — conflicts with DESIGN.md banned colors;
   intentional, supersession agreed (BUILD §10.1). Scott's impeccable-audit scripts may flag.
2. New marketing/redesign strings in English across all 11 languages (BUILD §8) — warning,
   queued for an i18n pass.
3. Marketing home is English-only (no language select) this build.
4. Responsive behavior = clean single-column collapse only; dedicated mobile design is a
   later pass (handoff README "Open items").

## AUDIT-RESULTS format

```markdown
# AUDIT RESULTS — Ladder Redesign — {date}
Build commits: {range}  ·  JS strategy used: {extraction | whole-app gating} + why
| Item | Result | Notes |
|------|--------|-------|
| A1   | PASS   |       |
| ...  |        |       |
Screenshots: {paths}
Open issues / follow-ups: {list}
```
