# aesopacademy.org — File Map
<!-- Last updated: v1.0.0 — built from known structure, browser parse pending -->

---

## Root

| Server Path | Local File | Notes |
|---|---|---|
| `/index.html` | `aesop-academy-index-v[version].html` | Site root — age group cards, AI Academy CTA links to `/ai-academy/` |

---

## AI Academy

| Server Path | Local File | Notes |
|---|---|---|
| `/ai-academy/index.html` | `ai-academy-index-v[version].html` | Academy hub — age selector, 10-module cumulative nav, 3-col layout |

### Module Files
Naming convention: `/ai-academy/modules/module-N/age-X.html`

Each module folder contains one file per age group that has access to that module.
Modules unlock cumulatively: M1–M5 at Ages 5–6, +1 per age group, all 10 at Ages 16+.

| Server Path | Age Group | Lessons |
|---|---|---|
| `/ai-academy/modules/module-1/age-5-6.html` | Ages 5–6 | L1–L3 |
| `/ai-academy/modules/module-1/age-7-8.html` | Ages 7–8 | L1–L4 |
| `/ai-academy/modules/module-1/age-9-10.html` | Ages 9–10 | L1–L5 |
| `/ai-academy/modules/module-1/age-11-12.html` | Ages 11–12 | L1–L6 |
| `/ai-academy/modules/module-1/age-13-15.html` | Ages 13–15 | L1–L7 |
| `/ai-academy/modules/module-1/age-16plus.html` | Ages 16+ | L1–L8 |
| `/ai-academy/modules/module-2/age-5-6.html` | Ages 5–6 | L1–L3 |
| `/ai-academy/modules/module-2/age-7-8.html` | Ages 7–8 | L1–L4 |
| `/ai-academy/modules/module-2/age-9-10.html` | Ages 9–10 | L1–L5 |
| `/ai-academy/modules/module-2/age-11-12.html` | Ages 11–12 | L1–L6 |
| `/ai-academy/modules/module-2/age-13-15.html` | Ages 13–15 | L1–L7 |
| `/ai-academy/modules/module-2/age-16plus.html` | Ages 16+ | L1–L8 |
| `/ai-academy/modules/module-3/age-5-6.html` | Ages 5–6 | L1–L3 |
| `/ai-academy/modules/module-3/age-7-8.html` | Ages 7–8 | L1–L4 |
| `/ai-academy/modules/module-3/age-9-10.html` | Ages 9–10 | L1–L5 |
| `/ai-academy/modules/module-3/age-11-12.html` | Ages 11–12 | L1–L6 |
| `/ai-academy/modules/module-3/age-13-15.html` | Ages 13–15 | L1–L7 |
| `/ai-academy/modules/module-3/age-16plus.html` | Ages 16+ | L1–L8 |
| `/ai-academy/modules/module-4/age-5-6.html` | Ages 5–6 | L1–L3 |
| `/ai-academy/modules/module-4/age-7-8.html` | Ages 7–8 | L1–L4 |
| `/ai-academy/modules/module-4/age-9-10.html` | Ages 9–10 | L1–L5 |
| `/ai-academy/modules/module-4/age-11-12.html` | Ages 11–12 | L1–L6 |
| `/ai-academy/modules/module-4/age-13-15.html` | Ages 13–15 | L1–L7 |
| `/ai-academy/modules/module-4/age-16plus.html` | Ages 16+ | L1–L8 |
| `/ai-academy/modules/module-5/age-5-6.html` | Ages 5–6 | L1–L3 |
| `/ai-academy/modules/module-5/age-7-8.html` | Ages 7–8 | L1–L4 |
| `/ai-academy/modules/module-5/age-9-10.html` | Ages 9–10 | L1–L5 |
| `/ai-academy/modules/module-5/age-11-12.html` | Ages 11–12 | L1–L6 |
| `/ai-academy/modules/module-5/age-13-15.html` | Ages 13–15 | L1–L7 |
| `/ai-academy/modules/module-5/age-16plus.html` | Ages 16+ | L1–L8 |
| `/ai-academy/modules/module-6/age-7-8.html` | Ages 7–8 | L1–L4 · **Unlocks at 7–8** |
| `/ai-academy/modules/module-6/age-9-10.html` | Ages 9–10 | L1–L5 |
| `/ai-academy/modules/module-6/age-11-12.html` | Ages 11–12 | L1–L6 |
| `/ai-academy/modules/module-6/age-13-15.html` | Ages 13–15 | L1–L7 |
| `/ai-academy/modules/module-6/age-16plus.html` | Ages 16+ | L1–L8 |
| `/ai-academy/modules/module-7/age-9-10.html` | Ages 9–10 | L1–L5 · **Unlocks at 9–10** |
| `/ai-academy/modules/module-7/age-11-12.html` | Ages 11–12 | L1–L6 |
| `/ai-academy/modules/module-7/age-13-15.html` | Ages 13–15 | L1–L7 |
| `/ai-academy/modules/module-7/age-16plus.html` | Ages 16+ | L1–L8 |
| `/ai-academy/modules/module-8/age-11-12.html` | Ages 11–12 | L1–L6 · **Unlocks at 11–12** |
| `/ai-academy/modules/module-8/age-13-15.html` | Ages 13–15 | L1–L7 |
| `/ai-academy/modules/module-8/age-16plus.html` | Ages 16+ | L1–L8 |
| `/ai-academy/modules/module-9/age-13-15.html` | Ages 13–15 | L1–L7 · **Unlocks at 13–15** |
| `/ai-academy/modules/module-9/age-16plus.html` | Ages 16+ | L1–L8 |
| `/ai-academy/modules/module-10/age-16plus.html` | Ages 16+ | L1–L8 · **Unlocks at 16+** |

**Total module files: 47**

---

## Forums

| Server Path | Notes |
|---|---|
| `/forums/index.html` | Forums landing page |

---

## Assets

| Server Path | Notes |
|---|---|
| `/og-image.jpg` | Open Graph / Twitter card image |

---

## Notes

- **Completion tracking:** In-session only until Firebase auth is live. Lesson files signal completion to nav via `window.parent.postMessage({ type:'lessonComplete', lessonId:'m1-l1' }, '*')`
- **Firebase project:** `playagame-f733d` — auth will gate module access and persist progress
- **Browser parse:** Filemap built from known structure. Run browser parse from aesopacademy.org root to fill in any missing files (forums, assets, additional pages)
