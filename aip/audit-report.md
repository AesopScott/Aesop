# AESOP Course Audit Report

**Generated:** 2026-05-26 14:11 UTC
**Status:** 🔴 ISSUES FOUND
**Errors:** 1 · **Warnings:** 31

---

## Course Registry (course-registry.json)

### Errors (1)
- 🔴 **MISSING_DIR**: Registry course `eval-benchmark` references `/ai-academy/modules/eval-benchmark/` which does not exist or is empty

### Warnings (28)
- 🟡 **DUPLICATE_URL**: `/ai-academy/modules/ai-ethics/` is referenced by 2 registry keys: `ethics` (coming-soon), `ai-ethics` (live)
- 🟡 **DUPLICATE_URL**: `/ai-academy/modules/ai-governance/` is referenced by 2 registry keys: `governance` (coming-soon), `ai-governance` (live)
- 🟡 **DUPLICATE_URL**: `/ai-academy/modules/ai-in-society/` is referenced by 2 registry keys: `society` (retired), `ai-in-society` (live)
- 🟡 **DUPLICATE_URL**: `/ai-academy/modules/building-with-ai/` is referenced by 2 registry keys: `building` (coming-soon), `building-with-ai` (live)
- 🟡 **DUPLICATE_URL**: `/ai-academy/modules/performing-arts-and-ai/` is referenced by 2 registry keys: `ar-11` (retired), `performing-arts-and-ai` (live)
- 🟡 **EXTRA_MODULES**: `agile-ai-side-projects` has 8 module files but registry defines 1 modules
- 🟡 **EXTRA_MODULES**: `ai-agent-risk-and-oversight` has 8 module files but registry defines 3 modules
- 🟡 **EXTRA_MODULES**: `ai-and-education` has 7 module files but registry defines 6 modules
- 🟡 **EXTRA_MODULES**: `ai-and-the-writer-s-voice` has 8 module files but registry defines 1 modules
- 🟡 **EXTRA_MODULES**: `ai-hype-critical-thinking` has 8 module files but registry defines 3 modules
- 🟡 **EXTRA_MODULES**: `ai-in-gaming-and-interactive-media` has 6 module files but registry defines 3 modules
- 🟡 **EXTRA_MODULES**: `ai-in-science` has 8 module files but registry defines 7 modules
- 🟡 **EXTRA_MODULES**: `ai-leadership` has 7 module files but registry defines 6 modules
- 🟡 **EXTRA_MODULES**: `ai-network-pentesting` has 8 module files but registry defines 1 modules
- 🟡 **EXTRA_MODULES**: `ai-side-hustle-money` has 8 module files but registry defines 6 modules
- 🟡 **EXTRA_MODULES**: `ai-work-and-automation-deep-dive` has 8 module files but registry defines 7 modules
- 🟡 **EXTRA_MODULES**: `ap-7` has 8 module files but registry defines 3 modules
- 🟡 **EXTRA_MODULES**: `build-ai-workflows-no-code` has 6 module files but registry defines 1 modules
- 🟡 **EXTRA_MODULES**: `deep-learning-for-builders` has 8 module files but registry defines 5 modules
- 🟡 **EXTRA_MODULES**: `deploying-and-monitoring-ai` has 8 module files but registry defines 3 modules
- 🟡 **EXTRA_MODULES**: `gemini-for-college-life` has 5 module files but registry defines 3 modules
- 🟡 **EXTRA_MODULES**: `gpt-vs-claude-vs-gemini` has 9 module files but registry defines 8 modules
- 🟡 **EXTRA_MODULES**: `is-the-robot-being-fair` has 4 module files but registry defines 1 modules
- 🟡 **EXTRA_MODULES**: `pentesting-ai-agents` has 8 module files but registry defines 1 modules
- 🟡 **EXTRA_MODULES**: `prompt-engineering-that-works` has 8 module files but registry defines 1 modules
- 🟡 **EXTRA_MODULES**: `truth-detectives-ai-and-fake-info` has 6 module files but registry defines 2 modules
- 🟡 **EXTRA_MODULES**: `voice-and-real-time-ai` has 8 module files but registry defines 3 modules
- 🟡 **EXTRA_MODULES**: `what-s-coming-next` has 8 module files but registry defines 1 modules

## courses.html

✅ No issues found.

## Electives Hub (electives-hub.html)

ℹ️ **Not applicable — registry-driven.** `electives-hub.html` is version `v1.1.0` ("Registry-only: all course data from course-registry.json"). It contains no hardcoded `BASE_COURSES` array; course data is fetched at runtime from `course-registry.json` via `loadCourseRegistry()`. Checks **H-1**, **H-2**, **X-2** and **X-3** depend on a static `BASE_COURSES` list and are therefore not applicable. Because the hub renders directly from the registry, its course set is the registry by construction.

## Cross-References

### Warnings (3)
- 🟡 **NOT_IN_COURSES_HTML**: registry course "ap-7" has no link from courses.html
- 🟡 **NOT_IN_COURSES_HTML**: registry course "ar-8" has no link from courses.html
- 🟡 **NOT_IN_COURSES_HTML**: registry course "eval-benchmark" has no link from courses.html

> **X-2 / X-3 not evaluated:** these compare the registry and `courses.html` against the electives-hub `BASE_COURSES` list, which no longer exists (the hub is registry-driven — see above).

---

## Summary

**1 error(s) require attention:**
1. **MISSING_DIR** — Registry course `eval-benchmark` references `/ai-academy/modules/eval-benchmark/` which does not exist or is empty

Plus **31 warning(s)** — chiefly registry `modules` arrays that under-report the module files actually present on disk, and five directories referenced by two registry keys each (a live full-slug entry alongside a legacy short-key entry).

### Stats
- Registry entries: 131 keys → 126 unique course directories (126 live, 3 coming-soon, 2 retired; 5 duplicate-URL pairs)
- courses.html absolute `/ai-academy/` links checked: 21
- courses.html `?course=` references: 123 (all resolve to registry courses)
- Electives hub BASE_COURSES: 0 (registry-driven — none hardcoded)
- Module files verified present: 764
