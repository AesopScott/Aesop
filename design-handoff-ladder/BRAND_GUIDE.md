# Aesop AI Academy — Brand & Design System

> The visual system behind **The Ladder**. This guide is the single source of truth for
> colors, typography, layout, components, and motion. Everything here is expressed as
> framework‑agnostic tokens + rules so it can be implemented in React, Vue, Svelte,
> SwiftUI, or plain CSS.

---

## 1. Brand essence

**Aesop AI Academy** teaches AI literacy as a climb — *The Ladder* — 15 tiers, 270 rungs,
one rung at a time. The brand is the meeting point of three traits:

- **Warm & encouraging** — never intimidating; a 4th grader and a staff engineer both belong.
- **Smart & credible** — calm, precise, grown‑up. It looks like it knows AI.
- **Modern & editorial** — Swiss/editorial restraint, not "dashboard slop."

**Design north star:** the reference site aesthetic — *sharp square corners, big LIGHT
editorial headings, generous whitespace, hairline rules, and quiet scroll motion.* Avoid
rounded‑corner card soup, heavy bold headings, gradients-everywhere, and emoji.

**Tagline:** "How high can you climb?"
**Eyebrow / parent brand:** "Aesop AI Academy presents"

---

## 2. Logo / wordmark

No external logo asset — the wordmark is type + a built mark.

- **Wordmark:** the word **Aesop** set in the active theme's *display* font, weight **500**,
  letter‑spacing `.01em`. (The big hero word **The Ladder** is the same display font at
  weight **400**.)
- **Mark (the "ladder" glyph):** a square (no border radius) filled with `--primary`,
  containing three horizontal bars stacked with `gap:3px`. The top & bottom bars are
  `--on-primary` (full width); the middle bar is `--accent` at 60% width. Built in markup:

  ```html
  <span style="width:24px;height:24px;background:var(--primary);display:flex;
               flex-direction:column;justify-content:center;gap:3px;padding:5px">
    <span style="height:2px;background:var(--on-primary)"></span>
    <span style="height:2px;background:var(--accent);width:60%"></span>
    <span style="height:2px;background:var(--on-primary)"></span>
  </span>
  ```

- **Accent‑square motif:** a tiny **7×7px square** of `--accent` precedes every section
  eyebrow (the uppercase label). This is a recurring brand tell — reuse it.

---

## 3. The theme system (core architecture)

The product ships **4 themes × 2 modes = 8 palettes**, switchable at runtime and persisted.
Everything is driven by **CSS custom properties** scoped to a root element via
`data-theme` + `data-mode` attributes. **No color is ever hardcoded in a component** — only
token references (`var(--primary)` etc.).

```html
<div id="app" data-theme="indigo" data-mode="light"> … </div>
```

### Themes

| id        | Name (UI) | Personality            | Display font          | Use                              |
|-----------|-----------|------------------------|-----------------------|----------------------------------|
| `indigo`  | Focus     | Professional (default) | Schibsted Grotesk     | Default — credible, all‑ages     |
| `emerald` | Scholar   | Classic green, grown‑up| Schibsted Grotesk     | Green‑lovers, still professional |
| `spring`  | Explorer  | Playful                | **Bricolage Grotesque** | Younger learners (bubbly type) |
| `volt`    | Arcade    | High‑energy            | Space Grotesk         | Older students / technical, dark‑leaning |

Body font is the **same across all themes** (see §4). Only the **display** font + colors change.

### Persistence

Selection is stored in `localStorage` under key **`aesop_theme`** as
`{"theme":"indigo","mode":"light"}`, read on load, written on change. It must persist
**across pages** (set Explorer on Home → it's Explorer everywhere).

### Token contract (every theme defines all of these)

| Token            | Meaning                                                            |
|------------------|--------------------------------------------------------------------|
| `--bg`           | Page background                                                    |
| `--bg2`          | Secondary background (footer, subtle bands)                        |
| `--surface`      | Card / panel surface                                               |
| `--surface2`     | Inset / hover surface, progress track                             |
| `--ink`          | Primary text                                                       |
| `--muted`        | Secondary text                                                     |
| `--faint`        | Tertiary text / disabled / locked                                 |
| `--primary`      | Primary brand color (buttons, active)                             |
| `--primary2`     | Primary hover/darker                                               |
| `--on-primary`   | Text/icon on `--primary`                                          |
| `--accent`       | Secondary accent (the square motif, panel top‑borders)            |
| `--accent-ink`   | Accent used as text (needs contrast on `--bg`)                    |
| `--fill`         | Brand fill for bars/dots/rungs (≈ `--primary`, but green in volt‑light) |
| `--border`       | Standard 1px borders                                              |
| `--hair`         | Hairline rules / dividers (lighter than border)                  |
| `--ring`         | Translucent brand tint (glows, selection, eyebrow pills)         |
| `--font-display` | Theme display font family                                        |

---

## 4. Color tokens — all 8 palettes (exact hex)

> Light row first, dark row second, for each theme.

### indigo — "Focus" (default)
**Light:** `--bg:#F6F5F1` `--bg2:#EFEDE6` `--surface:#FFFFFF` `--surface2:#F1EFEA` `--ink:#1A1830` `--muted:#6A6880` `--faint:#A8A6B6` `--primary:#4B40C9` `--primary2:#3A30A8` `--on-primary:#FFFFFF` `--accent:#E8843C` `--accent-ink:#9A5012` `--fill:#4B40C9` `--border:#E0DDD2` `--hair:#D8D5C9` `--ring:rgba(75,64,201,.12)`
**Dark:** `--bg:#121022` `--bg2:#0C0B18` `--surface:#1A1830` `--surface2:#221F3C` `--ink:#EEEDF7` `--muted:#A6A3C0` `--faint:#615E80` `--primary:#8579F2` `--primary2:#9A90F5` `--on-primary:#121022` `--accent:#E8843C` `--accent-ink:#E8843C` `--fill:#8579F2` `--border:#2A2748` `--hair:#262343` `--ring:rgba(133,121,242,.18)`

### emerald — "Scholar"
**Light:** `--bg:#F2F5F1` `--bg2:#E7EEE8` `--surface:#FFFFFF` `--surface2:#EDF2EC` `--ink:#0F1F1A` `--muted:#516259` `--faint:#9AAAA0` `--primary:#0E9E6E` `--primary2:#0B855D` `--on-primary:#FFFFFF` `--accent:#E0A129` `--accent-ink:#6F5300` `--fill:#0E9E6E` `--border:#DBE4DC` `--hair:#D2DDD3` `--ring:rgba(14,158,110,.12)`
**Dark:** `--bg:#0B1613` `--bg2:#08110E` `--surface:#11201A` `--surface2:#16281F` `--ink:#E8F2EC` `--muted:#9BB3A9` `--faint:#5E7770` `--primary:#2BD49A` `--primary2:#37E0A6` `--on-primary:#08130F` `--accent:#E0A129` `--accent-ink:#E0A129` `--fill:#2BD49A` `--border:#1F332B` `--hair:#1B2D26` `--ring:rgba(43,212,154,.18)`

### spring — "Explorer"
**Light:** `--bg:#F1F6F4` `--bg2:#E4EFEA` `--surface:#FFFFFF` `--surface2:#E9F3EF` `--ink:#0E211D` `--muted:#4D635C` `--faint:#92A39B` `--primary:#0A9E7C` `--primary2:#088068` `--on-primary:#FFFFFF` `--accent:#E6B92F` `--accent-ink:#6F5600` `--fill:#0A9E7C` `--border:#D6E4DF` `--hair:#CDDCD6` `--ring:rgba(10,158,124,.12)`
**Dark:** `--bg:#091613` `--bg2:#06110E` `--surface:#0F201C` `--surface2:#153029` `--ink:#E6F4EF` `--muted:#9EC2B8` `--faint:#5D7C72` `--primary:#1FD6A6` `--primary2:#2EE0B2` `--on-primary:#06140F` `--accent:#E6B92F` `--accent-ink:#E6B92F` `--fill:#1FD6A6` `--border:#1B322C` `--hair:#172B26` `--ring:rgba(31,214,166,.18)`

### volt — "Arcade"
> Note: in **light** mode `--primary` is near‑black ink and `--on-primary` is the neon —
> i.e. solid buttons are *ink with neon text*. `--fill` stays a readable green so progress
> bars/dots remain legible. In **dark** mode `--primary` is the neon itself.

**Light:** `--bg:#F4F6F0` `--bg2:#E9EEDF` `--surface:#FFFFFF` `--surface2:#EEF3E6` `--ink:#131A11` `--muted:#5B6B54` `--faint:#97A38C` `--primary:#171D14` `--primary2:#000000` `--on-primary:#AEF24E` `--accent:#5F9C0A` `--accent-ink:#3F6B00` `--fill:#5F9C0A` `--border:#DCE3D2` `--hair:#D3DCC8` `--ring:rgba(120,180,40,.16)`
**Dark:** `--bg:#0D130E` `--bg2:#090D0A` `--surface:#131A13` `--surface2:#19211A` `--ink:#E9F2E7` `--muted:#9AAB97` `--faint:#67755F` `--primary:#AEF24E` `--primary2:#BCF563` `--on-primary:#0D130E` `--accent:#AEF24E` `--accent-ink:#AEF24E` `--fill:#AEF24E` `--border:#222C22` `--hair:#1D261D` `--ring:rgba(174,242,78,.18)`

---

## 5. Typography

### Families (Google Fonts)
- **Body (all themes):** `'Helvetica Neue', Helvetica, Arial, sans-serif` — a neo‑grotesque
  (Nimbus Sans / Helvetica). Intentional Swiss feel; **do not** substitute Inter/Roboto.
- **Display:** per theme — **Schibsted Grotesk** (indigo, emerald), **Bricolage Grotesque**
  (spring), **Space Grotesk** (volt). Exposed as `--font-display`.
- Load weights: Schibsted `400 500 600 700`, Bricolage `400 500 600 700`, Space `400 500 600`.

### The single most important type rule
**Headings are LIGHT, not bold.** Display headings use weight **400** (occasionally 500),
never 700/800. The size carries the emphasis; the weight stays thin and editorial.

### Scale (display = `--font-display`, weight 400 unless noted)
| Role                     | Size        | Line‑height | Letter‑spacing | Notes                         |
|--------------------------|-------------|-------------|----------------|-------------------------------|
| Hero wordmark (Home)     | 172px       | .84         | -.04em         | "The Ladder"                  |
| Page H1 (sub‑pages)      | 88–96px     | .86–.9      | -.04em         |                               |
| Hero subline             | 26–30px     | 1.04        | -.015em        | color `--primary`; italicize one word for flair |
| Section H2               | 34–54px     | 1.0–1.05    | -.025/-.03em   |                               |
| Card / tier title        | 23–30px     | 1.0         | -.02em         |                               |
| Big stat number          | 54–64px     | 1           | -.03em         |                               |
| Quiz question            | 46px        | 1.04        | -.03em         |                               |
| **Eyebrow / label**      | 11px        | —           | **.2em**       | UPPERCASE, weight 600, `--muted`, preceded by accent square |
| Body                     | 15–18px     | 1.6–1.75    | normal         | `--muted` for secondary copy  |
| Small meta               | 12–13px     | —           | .02–.04em      |                               |

**Italic accent:** italicize a single word in a subline for personality
(e.g. "How high can *you* climb?"). Used sparingly.

---

## 6. Layout & spacing

- **Corners are SQUARE.** `border-radius: 0` everywhere — buttons, cards, inputs, chips,
  swatches, badges. This is non‑negotiable to the aesthetic.
- **Content width:** `max-width: 1280px`, centered, **40px** horizontal gutter.
- **Section rhythm:** generous vertical padding — **60–120px** top/bottom. Hero ~88px.
  Sections separated by a **1px `--hair` bottom border**, not gaps.
- **Hairlines over boxes:** prefer thin `--hair` / `--border` rules and whitespace to
  separate content; avoid stacks of filled, shadowed cards. Where a card is used it is a
  flat `--surface` block with a **1px `--border`** (optionally a **3px `--accent` top
  border** for emphasis — see Verified seal / summary cards).
- **Shadows:** almost none. The one place a soft shadow appears is the open theme dropdown
  (`0 30px 60px -28px rgba(0,0,0,.3)`).
- **Spacing scale (px):** 4, 6, 8, 10, 14, 18, 22, 26, 32, 40, 48, 60, 80, 110.
- **Grids:** stat strips are 4‑col grids with `--hair` vertical dividers (`border-right`),
  inner columns padded left 36–40px. The Full‑record table is a CSS grid
  `64px 1fr 90px 150px 130px`.

---

## 7. Components

All examples use tokens. Sizes/paddings are exact.

### Button — primary
`padding:16px 30px; background:var(--primary); color:var(--on-primary); font-weight:500;
font-size:15px; letter-spacing:.02em; border:none;` · **square** · hover → `background:
var(--primary2)`. Disabled → `opacity:.4; pointer-events:none`.

### Button — ghost
`padding:16px 30px; background:transparent; border:1px solid var(--ink); color:var(--ink);
font-weight:500; letter-spacing:.02em;` · hover → `background:var(--ink); color:var(--bg)`.

### Paired buttons
When two buttons sit together they **butt up flush** (no gap) and the second drops its
left border (`border-left:none`) — a single seamed control, not two pills.

### Top bar / nav
Sticky, `background: color-mix(in srgb, var(--bg) 86%, transparent)`, `backdrop-filter:
blur(10px)`, `border-bottom:1px solid var(--hair)`, inner padded `17px 40px`. Left: mark +
"Aesop" wordmark. Center/!: nav links (13px, weight 500, `--muted`; **active** link is
weight 600, `--primary`). Right: Theme button + a 34×34 square avatar (or "Get started"
primary on marketing).

### Eyebrow label
`display:inline-flex; gap:9px; align-items:center; font-size:11px; letter-spacing:.2em;
text-transform:uppercase; font-weight:600; color:var(--muted)` — **prefixed with a 7×7px
`--accent` square**. (On the hero, the square is followed by a 20×1px `--ink` rule at 35% opacity.)

### Stat tile
Big number in `--font-display` 400 (`--ink`) + a 12–13px `--muted` caption. Arranged in a
4‑col grid with `--hair` `border-right` dividers; no card.

### Editorial list row (marketing "pathways")
Grid `90px 1fr auto`, `align-items:baseline`, `padding:34px 0`, `border-bottom:1px solid
var(--hair)`, top of list capped with a `1px solid var(--ink)` rule. Columns: index (`01`
in `--font-display`, `--primary` for the featured row else `--muted`), title (42px display
400) + sub (15px `--muted`), and a `→` arrow. **Hover:** row bg → `--surface2`; arrow
`translateX(7px)` and recolors to `--primary`.

### Tier row (The Ladder accordion)
A full‑width button, grid‑like flex: **40×40 badge** + (title 23px display + meta 12.5px) +
**110px progress bar** + chevron `↓`. Badge states:
- *done* → `background:var(--fill); color:var(--on-primary)`
- *current* → `border:2px solid var(--accent); color:var(--ink)`
- *locked* → `border:1px solid var(--faint); color:var(--faint)` (title also `--faint`)
Chevron rotates 180° when open (`transform:rotate(180deg)`, `transition .25s`). Expanded
panel sits on `--surface2`.

### Rung square
14×14px, **square**. *done* → `background:var(--fill)`; *current* → `border:2px solid
var(--accent)`; *locked* → `border:1px solid var(--faint); opacity:.5`. Rendered as a
wrapping flex grid with `gap:6px` (18 per tier).

### Progress bar
Track: `height:3–4px; background:var(--surface2)`. Fill: `background:var(--fill)`, width =
percent, `transition: width .5s cubic-bezier(.16,1,.3,1)`.

### Quiz option row
Full‑width button, `padding:19px 20px`, `border-bottom:1px solid var(--border)`, a 16×16
square indicator + label (16px). *Unselected* indicator → `border:1.5px solid var(--faint)`;
*selected* → `border:5px solid var(--fill)` (reads as a filled square) and row bg →
`--surface2`. Hover → `border-color:var(--ink)`.

### Verified seal / emphasis card
Flat `--surface` block, `1px solid var(--border)` **plus `border-top:3px solid var(--accent)`**.
Seal contains a 26–30px `--fill` square with `--on-primary` "✓" + label.

### Status pill (transcript)
*Certified* → `background:var(--fill); color:var(--on-primary); padding:5px 11px; font-size:12px;
font-weight:600`. *In progress* → `border:1px solid var(--accent); color:var(--accent-ink)`.
Square corners.

---

## 8. Motion

- **Scroll reveals:** primary entrance effect. Elements tagged `[data-reveal]` translate up
  + fade in **as they enter the viewport** using CSS scroll‑driven animation:
  ```css
  @keyframes revealUp { from { opacity:0; transform:translateY(36px); } to { opacity:1; transform:none; } }
  [data-reveal] { animation: revealUp both linear; animation-timeline: view(); animation-range: entry 2% cover 24%; }
  @media (prefers-reduced-motion: reduce) { [data-reveal] { animation: none; } }
  ```
  In a real app you may instead use **IntersectionObserver** to add an `is-in` class — just
  keep the *feel*: ~30px rise, fade, ~0.9s `cubic-bezier(.16,1,.3,1)`, one‑shot per element,
  and **never leave content stuck invisible** if the effect can't run (default to visible).
- **Hover transitions:** `transition: background-color .22s, color .22s, border-color .22s,
  transform .22s, opacity .22s` on links/buttons. Arrow slides `translateX(7px)`.
- **Theme change:** `#app { transition: background-color .4s ease, color .4s ease; }` for a
  soft cross‑fade between palettes.
- **Easing:** standard `cubic-bezier(.16,1,.3,1)` (an "ease‑out‑expo" feel).

---

## 9. Voice & copy

Warm, plain, confident. Short sentences. "Climb / rung / tier / summit" metaphor throughout.
Encouraging, never condescending. Examples in use: "How high can you climb?", "Find your
rung", "Start where you belong — not bored, not overwhelmed.", "AI literacy, rung by rung."

---

## 10. Don'ts

- ❌ Rounded corners. ❌ Bold (700+) display headings. ❌ Inter/Roboto/Arial as the *display*
  face. ❌ Gradient‑heavy backgrounds or drop‑shadow card stacks. ❌ Emoji as UI
  (except the deliberate playful flourishes already in the spring theme, if desired).
- ✅ Square edges, light big type, hairlines, whitespace, one accent square, calm motion.
