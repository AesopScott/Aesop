# AESOP Course Audit Report

**Generated:** 2026-05-25 14:14 UTC  
**Status:** 🔴 ISSUES FOUND  
**Errors:** 1 · **Warnings:** 32

---

## Course Registry (course-registry.json)

### Errors (1)

- 🔴 **MISSING_DIR**: Registry course `eval-benchmark` references `/ai-academy/modules/eval-benchmark/` which does not exist

### Warnings (29)

- 🟡 **DUPLICATE_URL**: `/ai-academy/modules/ai-ethics/` is claimed by 2 registry entries: `ethics` (coming-soon), `ai-ethics` (live)
- 🟡 **DUPLICATE_URL**: `/ai-academy/modules/ai-governance/` is claimed by 2 registry entries: `governance` (coming-soon), `ai-governance` (live)
- 🟡 **DUPLICATE_URL**: `/ai-academy/modules/ai-in-society/` is claimed by 2 registry entries: `society` (retired), `ai-in-society` (live)
- 🟡 **DUPLICATE_URL**: `/ai-academy/modules/building-with-ai/` is claimed by 2 registry entries: `building` (coming-soon), `building-with-ai` (live)
- 🟡 **DUPLICATE_URL**: `/ai-academy/modules/performing-arts-and-ai/` is claimed by 2 registry entries: `ar-11` (retired), `performing-arts-and-ai` (live)
- 🟡 **EXTRA_MODULES**: `society` has 9 module files but registry defines 8 modules (status: retired)
- 🟡 **EXTRA_MODULES**: `ai-and-education` has 7 module files but registry defines 6 modules
- 🟡 **EXTRA_MODULES**: `ai-leadership` has 7 module files but registry defines 6 modules
- 🟡 **EXTRA_MODULES**: `gpt-vs-claude-vs-gemini` has 9 module files but registry defines 8 modules
- 🟡 **EXTRA_MODULES**: `ai-side-hustle-money` has 8 module files but registry defines 6 modules
- 🟡 **EXTRA_MODULES**: `deploying-and-monitoring-ai` has 8 module files but registry defines 3 modules
- 🟡 **EXTRA_MODULES**: `truth-detectives-ai-and-fake-info` has 6 module files but registry defines 2 modules
- 🟡 **EXTRA_MODULES**: `voice-and-real-time-ai` has 8 module files but registry defines 3 modules
- 🟡 **EXTRA_MODULES**: `ai-network-pentesting` has 8 module files but registry defines 1 module
- 🟡 **EXTRA_MODULES**: `pentesting-ai-agents` has 8 module files but registry defines 1 module
- 🟡 **EXTRA_MODULES**: `what-s-coming-next` has 8 module files but registry defines 1 module
- 🟡 **EXTRA_MODULES**: `ai-in-science` has 8 module files but registry defines 7 modules
- 🟡 **EXTRA_MODULES**: `ai-and-the-writer-s-voice` has 8 module files but registry defines 1 module
- 🟡 **EXTRA_MODULES**: `ap-7` has 8 module files but registry defines 3 modules
- 🟡 **EXTRA_MODULES**: `ai-work-and-automation-deep-dive` has 8 module files but registry defines 7 modules
- 🟡 **EXTRA_MODULES**: `ai-agent-risk-and-oversight` has 8 module files but registry defines 3 modules
- 🟡 **EXTRA_MODULES**: `ai-hype-critical-thinking` has 8 module files but registry defines 3 modules
- 🟡 **EXTRA_MODULES**: `deep-learning-for-builders` has 8 module files but registry defines 5 modules
- 🟡 **EXTRA_MODULES**: `build-ai-workflows-no-code` has 6 module files but registry defines 1 module
- 🟡 **EXTRA_MODULES**: `gemini-for-college-life` has 5 module files but registry defines 3 modules
- 🟡 **EXTRA_MODULES**: `agile-ai-side-projects` has 8 module files but registry defines 1 module
- 🟡 **EXTRA_MODULES**: `prompt-engineering-that-works` has 8 module files but registry defines 1 module
- 🟡 **EXTRA_MODULES**: `ai-in-gaming-and-interactive-media` has 6 module files but registry defines 3 modules
- 🟡 **EXTRA_MODULES**: `is-the-robot-being-fair` has 4 module files but registry defines 1 module


## courses.html

✅ No issues found.


## Electives Hub (electives-hub.html)

> **Note:** This build of `electives-hub.html` has no static `BASE_COURSES` array. `COURSES` is populated at runtime from `course-registry.json`, filtered to `status === 'live'` (see `loadCourseRegistry()`). Checks H-1/H-2 have no static list to validate, so the hub's effective course set is — by construction — the live registry courses. Inconsistencies that would otherwise be hub-only are surfaced under Cross-References instead.

✅ No issues found.


## Cross-References

> **Note (X-2):** Because the hub derives its list from the registry's live courses at runtime, every live course is present by construction — there are no hub-omission (`NOT_IN_ELECTIVES_HUB`) findings to report.

### Warnings (3)

- 🟡 **NOT_IN_COURSES_HTML**: registry course "ar-8" has no link from courses.html
- 🟡 **NOT_IN_COURSES_HTML**: registry course "ap-7" has no link from courses.html
- 🟡 **NOT_IN_COURSES_HTML**: registry course "eval-benchmark" has no link from courses.html


---

## Summary

**1 error(s) require attention:**
1. **MISSING_DIR** — Registry course `eval-benchmark` references `/ai-academy/modules/eval-benchmark/` which does not exist

### Stats
- Registry courses: 131 (126 live, 3 coming soon, 2 retired)
- courses.html internal links checked: 143
- courses.html `?course=` references: 123
- Electives hub BASE_COURSES: dynamic — derived from 126 live registry courses at runtime (no static list)
- Module files verified: 780
