# Handoff: Aesop — The Ladder (redesign)

## Overview
This package contains the redesigned UI for **Aesop AI Academy / The Ladder** — a guided
AI‑literacy platform (15 tiers, 270 rungs). It covers four screens — **marketing Home**,
**The Ladder hub**, **Assessment (placement)**, and **Transcript** — plus a runtime
**theme system** (4 themes × light/dark) that persists across pages.

The goal of this handoff is to **work this design into the existing Aesop — The Ladder
project**. The old site crammed assessment, the ladder, and transcripts onto one page; the
new design separates them into distinct pages and gives the product a real, cohesive brand.

## About the design files
The files in `references/` are **design references created as HTML prototypes** — they show
the intended look, layout, and behavior. **They are not production code to copy directly.**

> ⚠️ The `.dc.html` files use an internal prototyping runtime (`support.js`, `<x-dc>`,
> `{{ }}` template holes, a `Component`/`renderVals()` logic class). **Ignore that runtime.**
> It is a prototyping harness, not part of the design. Recreate the screens in the Aesop
> project's actual stack (e.g. React + your existing CSS/styling approach), using the
> **BRAND_GUIDE.md** tokens and the per‑screen specs below. Treat the HTML as a precise
> visual + behavioral reference you re‑implement idiomatically.

Open any `references/*.dc.html` file in a browser to interact with the real prototype
(theme switcher, assessment flow, tier accordion all work).

## Fidelity
**High‑fidelity.** Final colors, typography, spacing, components, and interactions are all
specified. Recreate pixel‑accurately using the values in `BRAND_GUIDE.md`. The one area to
adapt rather than copy: the **scroll‑reveal animation** (the prototype uses CSS
`animation-timeline: view()`; prefer an IntersectionObserver `is-in` class in the app — see
Brand Guide §8). Never leave content invisible if the effect can't run.

## Read first
**`BRAND_GUIDE.md`** holds the entire design system — all 8 color palettes (exact hex),
typography scale, layout rules, every component spec, and motion. The per‑screen notes below
reference it rather than repeat it.

---

## Screens / Views

### 1. Home (`references/Home.dc.html`) — marketing landing
**Purpose:** market the product and route to the five destinations. **Not a dashboard.**

**Layout (top → bottom), each section full‑width with a `--hair` bottom border, content
capped at 1280px / 40px gutter:**
1. **Top bar** — sticky, blurred. Mark + "Aesop"; nav: *The Ladder, Training, Certification,
   Transcripts*; right: **Theme** switcher + **Get started** (primary → Assessment).
2. **Hero** — eyebrow ("Aesop AI Academy", with accent square + rule); huge **The Ladder**
   (172px, display 400); subline "How high can *you* climb?" (italic "you", `--primary`);
   paragraph; flush **Start climbing** (primary) + **Take the assessment** (ghost) → Assessment;
   "Built for" chips (Grades 3–12 / Engineers / Data Scientists). Right column: a 340px
   **"Your climb"** panel (1px border + 3px accent top border) listing Tiers 15, 04, then a
   highlighted **Tier 03 · Prompting 62%** row with a mini progress bar, then Tiers 02, 01.
3. **Stats strip** — 4‑col, hairline dividers: **15** Tiers · **270** Rungs · **1:1** Mentor · **∞** Self‑paced.
4. **What is The Ladder** — 2‑col: left H2 "One climb. Fifteen tiers. Two hundred seventy
   rungs." / right 3 paragraphs.
5. **Pathways** — H2 "Five parts, one journey upward" + an **editorial numbered list** (01–05):
   The Ladder (featured, index in `--primary`), Training, Assessment, Certification, Transcript.
   Each row links to its page; hover slides the `→` and tints the row (Brand Guide §7).
6. **How it works** — 3 borderless columns w/ `--hair` dividers: **Assess → Climb → Certify**.
7. **Who it's for** — 2 columns split by a `--hair` divider: *In the classroom* (Elementary…
   Educators chips) and *In your career* (Engineers… Team Leads chips). Chips share borders
   (negative‑margin grid, square).
8. **Final CTA** — full‑bleed `--ink` band, big light `--bg` heading "How high can you climb?",
   flush primary + ghost buttons.
9. **Footer** — 4‑col link columns on `--bg2`.

**Links:** The Ladder → `The Ladder`; Training/Certification → (no page yet — see Open items);
Transcripts → `Transcript`; Get started / Start climbing / assessment CTAs → `Assessment`.

### 2. The Ladder (`references/The Ladder.dc.html`) — the climb hub
**Purpose:** the logged‑in learning home; see progress and resume.

**Layout:**
- **Top bar** (The Ladder nav link active) + 34px avatar ("AK") → Transcript.
- **Climb header** — eyebrow "Your climb · Welcome back, Avery"; 2‑col: left H1 **The Ladder**
  (96px) + subline "You're on Tier 3 — *Prompting*. Eleven rungs in."; right a summary card
  (3px accent top border): "Overall progress 17%", big **47** / 270 rungs, progress bar,
  **Resume rung 12** primary, footer meta "2 tiers complete · Tier 3 of 15".
- **Tier list** — H2 "All fifteen tiers" + a legend (Completed / In progress / Locked squares).
  An **accordion** of 15 rows (Brand Guide §7 "Tier row"), list capped with a `1px --ink` top
  rule, rows divided by `--hair`. Clicking a row toggles its expanded panel
  (`--surface2`): an 18‑square **rung grid** (done/current/locked) + a "Next — Rung N · …" line
  + an action button (*current* → primary "Resume rung N"; *done* → ghost "Review tier";
  *locked* → disabled "Locked"). Default open tier = the current one (Tier 03).
- **Footer** (slim variant).

**Tier data (n, name, status, rungsDone/total):** 1 Foundations done 18/18 · 2 Conversation
done 18/18 · 3 Prompting **current** 11/18 · 4 Context & Memory · 5 Reasoning · 6 Tools &
Search · 7 Data & Analysis · 8 Images & Vision · 9 Code with AI · 10 Workflows · 11 Agents ·
12 Evaluation · 13 Safety & Ethics · 14 Building Apps · 15 Mastery (4–15 locked, 0/18).

### 3. Assessment (`references/Assessment.dc.html`) — placement flow
**Purpose:** place a new learner on the right rung. Standalone, focused (no full nav).

**Layout:** top bar (mark + "Placement Assessment" centered + Theme + **Exit** → Home), a
**3px progress bar** under the header (width = phase progress), and a centered `max-width:760px`
stage with three phases (state machine):
- **Intro** — eyebrow "~5 minutes · no wrong answers"; H1 **Find your rung** (88px); paragraph;
  **Begin assessment** primary; a 3‑stat row (5 questions / 15 tiers / ∞ retakes).
- **Quiz** — "Question N / 5" + **← Back**; big question (46px display 400); a vertical list of
  **option rows** (square indicator fills when selected; Brand Guide §7); **Next** (disabled
  until an option is chosen) → last question becomes **See my result**.
- **Result** — eyebrow "Your placement"; "You belong on" → **Tier 03** (80px) → **Prompting**
  (`--primary`); descriptive paragraph; a 3‑stat emphasis card (2 tiers skipped / 18 rungs /
  13 tiers above); flush **Start climbing from Tier 3** (→ The Ladder) + **Retake** (ghost).

**Questions (label + options):**
1. "How often do you use AI chat assistants?" — Never tried one / A few times / I use them most weeks / I build things with them
2. "A "prompt" is best described as…" — A kind of AI model / The instruction you give an AI / A programming language / A subscription plan
3. "Your AI answer comes back too vague. What helps most?" — Ask the same thing again / Add context and an example / Type in all capitals / Nothing — it's random
4. "Which sounds most like you right now?" — A student (grades 3–12) / An educator / An engineer or developer / A data scientist or analyst
5. "How comfortable are you giving an AI step‑by‑step instructions?" — Not at all yet / Somewhat / Pretty comfortable / Very — I do it daily

> The prototype result is **fixed to Tier 03** (not scored). If you want it adaptive, map an
> answer score → tier; otherwise keep the fixed placement for now.

### 4. Transcript (`references/Transcript.dc.html`) — verifiable record
**Purpose:** a portable, official record of progress & credentials.

**Layout:**
- **Top bar** (Transcripts active) + avatar.
- **Document header** — eyebrow "Official record"; H1 **Transcript** (92px); learner meta row
  (Learner: Avery Kim · Learner ID: AES‑2026‑04471 · Issued: 10 June 2026); right: a
  **Verified** seal (3px accent top border, `--fill` square ✓) + flush **Download PDF**
  (primary) / **Share link** (ghost).
- **Summary strip** — 4‑col hairline grid: **2** Tiers certified · **47** Rungs completed ·
  **2** Credentials earned · **31h** Time invested.
- **Credentials earned** — 2 cards (3px accent top border): **Foundations** (Tier 01) &
  **Conversation** (Tier 02), each with a ✓ square, description, credential ID + date, and a
  **Verify →** link.
- **Full record** — H2 + a table (grid `64px 1fr 90px 150px 130px`): header row over a `--ink`
  rule, then tier rows with **Certified** (filled pill) / **In progress** (outlined pill) /
  **Not started** (faint, dimmed) statuses; closing "+ 10 more tiers ahead" line.
- **Footer** (slim).

---

## Interactions & behavior
- **Theme switcher** (every page): a popover from the **Theme** button lists the 4 themes
  (swatch pair + name in that theme's display font + active dot) and a **Light/Dark** segmented
  control. Selecting either updates `data-theme`/`data-mode` on the root and writes
  `localStorage["aesop_theme"]`. Read it on load so the choice **persists across pages**.
- **Tier accordion:** click toggles one open tier (single‑open). Chevron rotates 180°.
- **Assessment:** Begin → quiz; selecting an option enables Next; Next advances / final →
  Result; Back steps back (first question → Intro); Retake → Intro and clears answers.
- **Hover:** buttons darken/invert; editorial rows tint + arrow slides; quiz options border‑ink.
- **Scroll reveals:** sections rise+fade on entry (Brand Guide §8).
- **Navigation map:** Home ⇄ The Ladder ⇄ Assessment ⇄ Transcript via header/footer/CTAs.

## State management
- **Global/persisted:** `theme` ('indigo'|'emerald'|'spring'|'volt'), `mode` ('light'|'dark')
  — persisted to `localStorage["aesop_theme"]`, shared app‑wide.
- **Local UI:** `switcherOpen` (popover); The Ladder `expanded` (tier id | null);
  Assessment `phase` ('intro'|'quiz'|'result'), `qIndex`, `answers{}`.
- **Real‑app data to wire up:** learner profile, per‑tier/per‑rung progress, credentials, and
  transcript records currently hardcoded in the prototypes — replace with the project's data
  layer. Field shapes are implied by the specs above.

## Design tokens
See **`BRAND_GUIDE.md` §3–§4** for the full token contract and all 8 palettes (exact hex), and
§5–§8 for type, spacing, components, and motion. Implement colors as CSS variables scoped by
`data-theme` + `data-mode` (or your framework's theming equivalent) — **do not hardcode hex in
components.**

## Assets
- **No image/icon assets.** All glyphs (the ladder mark, ✓ seals, arrows, chevrons, rung
  squares) are built from CSS/markup or Unicode. Keep it that way, or swap to the project's
  existing icon set if preferred.
- **Fonts (Google Fonts):** Schibsted Grotesk, Bricolage Grotesque, Space Grotesk; body =
  Helvetica Neue/Helvetica/Arial system stack.

## Files
```
design_handoff_aesop_ladder/
├── README.md            ← this file
├── BRAND_GUIDE.md       ← full design system (read this)
└── references/
    ├── Home.dc.html         ← marketing landing
    ├── The Ladder.dc.html   ← climb hub (accordion)
    ├── Assessment.dc.html   ← placement flow
    ├── Transcript.dc.html   ← verifiable record
    └── support.js           ← prototyping runtime (IGNORE — not part of the design)
```

## Open items / not yet designed
- **Training** and **Certification** are referenced in nav and the pathways list but have
  **no dedicated page** yet (currently linked to placeholders). Build them in this system when
  ready, or hide the links until they exist.
- **Assessment scoring** is not implemented (result fixed to Tier 03).
- Designs are specified at desktop width (1280px). **Responsive/mobile** breakpoints are not
  yet defined — apply the project's responsive conventions (the layouts are flex/grid‑based and
  collapse cleanly to single‑column).
