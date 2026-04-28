# /new-course — Aesop AI Academy Course Creator

Create a complete, properly structured new course with all required entries so it appears in ModGen, has every required field, and is ready to build.

## Trigger

Run when the user wants to add a new course to the academy and needs all data structures created automatically.

---

## Step 1 — Gather Course Info

Ask the user (or use what they've already provided) for the following. Fill gaps with smart defaults when intent is clear; only ask what you don't know.

| Field | Required | Notes |
|-------|----------|-------|
| **Title** | yes | Human display name, e.g. "AI for Nurses" |
| **Slug** | auto | Derived from title: lowercase, hyphens, no special chars. E.g. `ai-for-nurses`. Confirm before writing. |
| **Category** | yes | See category list below |
| **Age Group** | yes | `youth` \| `young_adult` \| `professional` |
| **Tier** | yes | `Beginner` \| `Intermediate` \| `Advanced` |
| **Module count** | yes | `4` (short/public), `6` (Youth), `8` (standard) |
| **Description** | yes | 1–2 sentence course description for the catalog |
| **Source tag** | auto | `aip` if public-audience, `ya` if young adult, omit otherwise |

### Valid Categories

| Category | Use for |
|----------|---------|
| `Cybersecurity` | Security, privacy, pen testing, red teaming, code auditing |
| `Development` | Coding, APIs, building AI apps, deployment, agents |
| `Business` | Strategy, operations, marketing, finance, entrepreneurship |
| `Arts & Creative` | Design, music, writing, video, photography, game design |
| `AI Foundations` | How AI works, models, alignment, history |
| `Applied AI` | Cutting-edge: agents, multimodal, reasoning, hardware |
| `Young Adult` | Teen-focused AI literacy (set ageGroup=young_adult too) |
| `Youth` | Ages 8–15 (set ageGroup=youth too) |

---

## Step 2 — Generate Module Titles

For each module (1 through N), generate:
- `title` — the module topic heading
- `sub` — one sentence describing what this module covers and why it matters

Module progression must follow this arc:
1. **Context / Why it matters** — orient the learner, establish stakes
2. **Core concept A** — foundational knowledge
3. **Core concept B** — next layer
4. (Additional concepts as needed)
5. **Practical application** — hands-on or case study
6. **Advanced / Edge cases** — nuance, failure modes
7. **Ethics / Implications** — real-world consequences
8. **Synthesis / What's next** — pull it all together, future outlook

For Youth courses (6 modules): compress to Context → 3 Core concepts → Application → Synthesis.
For 4-module courses: Context → 2 Core concepts → Application/Synthesis.

Show the user the module outline and ask for approval or changes before writing to files.

---

## Step 3 — Validate Slug is Unique

Before writing anything, check:
- `ai-academy/modules/courses-data.json` — search for an `id` field matching the slug
- `ai-academy/modules/course-registry.json` — search for a top-level key matching the slug

If a duplicate is found, show the conflict and ask the user to confirm update or choose a new slug.

---

## Step 4 — Write courses-data.json Entry

Load `ai-academy/modules/courses-data.json`. Insert the new course object into the `courses` array. Required structure:

```json
{
  "id": "{slug}",
  "name": "{Title}",
  "description": "{description}",
  "tier": "{Beginner|Intermediate|Advanced}",
  "ageGroup": "{youth|young_adult|professional}",
  "category": "{Category}",
  "live": false,
  "modules": [
    { "n": 1, "title": "Module 1 Title", "sub": "What the learner gets from this module" },
    { "n": 2, "title": "Module 2 Title", "sub": "What the learner gets from this module" }
  ]
}
```

Rules:
- `live` is always `false` for new courses — activation through ModGen sets it to `true`
- `modules` array must be non-empty or the course will not appear in the ModGen dropdown
- Include `"source": "aip"` only for public-audience courses; omit the field entirely for standard courses
- All field names must match exactly — no variations like `courseId` or `age_group`

---

## Step 5 — Write course-registry.json Entry

Load `ai-academy/modules/course-registry.json`. Add a new top-level key using the slug. Required structure:

```json
"{slug}": {
  "title": "{Title}",
  "status": "coming-soon",
  "category": "{Category}",
  "ageGroup": "{youth|young_adult|professional}",
  "tier": "{Beginner|Intermediate|Advanced}",
  "url": "/ai-academy/modules/{slug}/{slug}-m1.html",
  "modules": [
    "{slug}-m1",
    "{slug}-m2"
  ]
}
```

Rules:
- `status` is always `"coming-soon"` for new courses — never `"live"`
- `modules` array lists module IDs in order (filename without `.html`)
- `url` points to module 1 at the standard path
- Module count in this array must match the count in courses-data.json

---

## Step 6 — Create Module Directory and Stub Files

Create the directory: `ai-academy/modules/{slug}/`

For each module N, create `{slug}-m{N}.html` as a minimal stub:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{Title} — Module {N}</title>
</head>
<body>
  <!-- STUB: Use ModGen to build this module -->
  <p>Module {N} — {Module N Title} — not yet built.</p>
</body>
</html>
```

These stubs let CI and the activation workflow detect that the course folder exists.

---

## Step 7 — Commit and Push

Stage only these files:
- `ai-academy/modules/courses-data.json`
- `ai-academy/modules/course-registry.json`
- `ai-academy/modules/{slug}/` (all stub files)

Commit message format:
```
feat: scaffold {Title} course ({N} modules, {Category})

Category: {Category} | AgeGroup: {ageGroup} | Tier: {Tier}
Status: coming-soon — ready to build in ModGen
```

Push to `main` immediately (standing authorization per CLAUDE.md).

---

## Step 8 — Completion Report

Print this summary after pushing:

```
Course Created: {Title}
   Slug:      {slug}
   Category:  {Category}
   Age Group: {ageGroup} ([Youth] / [Young Adult] / [Professional] in ModGen)
   Tier:      {Tier}
   Modules:   {N} modules scaffolded

Files written:
   courses-data.json     — new entry added (live: false)
   course-registry.json  — new entry added (status: coming-soon)
   ai-academy/modules/{slug}/ — {N} stub HTML files

Next step: Open ModGen, select "{Title}", set your repo folder, and build each module.
```

---

## Validation Checklist

Verify every item before committing:

- [ ] `id` in courses-data matches the slug key in course-registry
- [ ] `modules` array in courses-data is non-empty (required for ModGen dropdown)
- [ ] `modules` array in registry has the correct count and follows `{slug}-mN` format
- [ ] `category` exactly matches one of the valid values (no typos, no invented values)
- [ ] `ageGroup` is exactly `youth`, `young_adult`, or `professional`
- [ ] `live: false` in courses-data
- [ ] `status: "coming-soon"` in registry
- [ ] Slug is URL-safe: lowercase, hyphens only, no spaces, no special characters
- [ ] Module directory exists at `ai-academy/modules/{slug}/`
- [ ] No duplicate slug in either file

---

## Common Mistakes to Prevent

| Wrong | Right |
|-------|-------|
| `"modules": []` — empty array | Always populate modules before writing — empty = invisible in ModGen |
| No `category` field | Always set — prevents the uncategorized drift we've been fixing |
| No `ageGroup` field | Always set — ModGen labels `[Youth]` / `[Young Adult]` depend on it |
| `"status": "live"` on a new course | Always `"coming-soon"` — ModGen activation handles promotion to live |
| `"live": true` on a new course | Always `false` — activation sets this |
| Slug with uppercase or spaces | Lowercase, hyphens only |
| Forgetting the module directory | Always create `ai-academy/modules/{slug}/` with stubs |
| Module count mismatch between files | courses-data modules array length must equal registry modules array length |
