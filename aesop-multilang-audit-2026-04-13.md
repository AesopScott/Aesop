# Aesop Academy — Multilingual (/es/, /hi/) Audit

**Date:** 2026-04-13
**Scope:** EN ↔ ES ↔ HI parity, language switcher behavior, Foundations course routing.

## Fixes applied in this session

1. **`/ai-academy/index.html`** — replaced the in-page-only `setLang()` button bindings with a URL-based `switchSiteLang()` handler. Buttons now navigate `/ai-academy/` ↔ `/es/ai-academy/` ↔ `/hi/ai-academy/`. A Hindi (हि) button was added. On `/es/` and `/hi/` URLs, `setLang()` is auto-invoked on load so the Advanced-tier filter and Spanish notice still apply.
2. **`/ai-academy/courses.html`** — removed the stray duplicate `<a data-lang="es">ES</a></div>` block sitting after the proper `#siteLangSwitch` close. Same cleanup applied to `/es/ai-academy/courses.html` and `/hi/ai-academy/courses.html` (the Hindi copy also had the wrong title attribute).
3. **`/es/ai-academy/courses.html`** — Foundations card link `/ai-academy/` → `/es/ai-academy/` (was dumping users into the English hub).
4. **`/hi/ai-academy/courses.html`** — Foundations card link `/ai-academy/` → `/hi/ai-academy/`.
5. **`/es/ai-academy/index.html`** and **`/hi/ai-academy/index.html`** — created (copies of the English hub) so the Foundations link no longer 403s. The hub's URL-aware code marks ES/HI as active when loaded from these paths.

## Content state

### Top-level pages

| File | EN | ES | HI | Notes |
|---|---|---|---|---|
| `/index.html` | ✅ | ⚠️ body text still English | ⚠️ body text still English | `<html lang="es">` / `<html lang="hi">` but body strings ("Learning through Adventure", "WE ARE IN DEVELOPMENT", etc.) match the EN file. |
| `/ai-academy/index.html` | ✅ | ⚠️ stub (just created, English shell) | ⚠️ stub (just created, English shell) | Hub chrome is English; module data is bilingual through `setLang()` for ES, no HI equivalent yet. |
| `/ai-academy/courses.html` | ✅ | ⚠️ English copy + ES nav fix | ⚠️ English copy + HI nav fix | Course catalog body text is still English in the translated trees. |

### Module coverage

Per Scott: **10 modules per language IS the complete curriculum** for ES and HI — Intro/Basic tiers and the elective library are English-only by design and are not a gap.

- EN: `ai-academy/modules/module-{n}/` has three tier files each (Intro/Basic/Advanced) plus the electives library.
- ES: `es/ai-academy/modules/module-{n}/advanced-m{n}.html` — 10 files, complete.
- HI: `hi/ai-academy/modules/module-{n}/advanced-m{n}.html` — 10 files, complete.

Spot-check: `es/ai-academy/modules/module-1/advanced-m1.html` is genuinely translated (94 hits on Spanish keywords like `lección`, `módulo`, `bienvenid…`). Translations are real.

### Site shell on EN pages

The EN `/index.html` already serves all three buttons (EN/ES/हि). The deployed copy of `aesopacademy.org/index.html` only has EN/ES — local repo is ahead, deploy is stale (likely pending push or a deploy pipeline lag).

## Recommended next moves (in priority order)

1. **Translate `/es/index.html` and `/hi/index.html` body content** — they're currently English masquerading as localized.
2. **Translate `/es/ai-academy/courses.html` and `/hi/ai-academy/courses.html` catalog copy** — only nav was fixed; body text still English.
3. **Confirm deploy pipeline is firing** — the live site at `aesopacademy.org/` is missing the third (हि) button that the repo has, so a deploy is overdue.
4. **Generalize `setLang()`** in the hub — currently `lang === 'es'` is hardcoded for the Advanced-tier filter and the Spanish notice; Hindi gets no special handling. Add a `'hi'` branch so Hindi users land on the Advanced tier and see an equivalent notice.

## Files touched this session

- `ai-academy/index.html`
- `ai-academy/courses.html`
- `es/ai-academy/courses.html`
- `hi/ai-academy/courses.html`
- `es/ai-academy/index.html` (new)
- `hi/ai-academy/index.html` (new)

## Git status note

The local clone's `.git/index` was being repeatedly locked by a Windows-side process (likely an auto-sync agent — commit history shows recurring "Auto-sync: local changes ..." commits). Edits are in place on disk; commit/push was deferred. Once the lock contention clears, run from `C:\Users\scott\Documents\Aesop`:

```
git add ai-academy/index.html ai-academy/courses.html es/ai-academy/ hi/ai-academy/
git commit -m "Multilang: fix lang switch on hub + courses, repair /es/ /hi/ Foundations route"
git push
```
