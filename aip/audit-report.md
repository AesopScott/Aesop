# AESOP Course Audit Report

**Generated:** 2026-04-26 14:04 UTC
**Status:** 🔴 ISSUES FOUND
**Errors:** 1 · **Warnings:** 14

---

## Course Registry (course-registry.json)

### Warnings (11)

- 🟡 **EXTRA_MODULES**: `ai-and-education` has 7 module files but registry defines 6 modules
- 🟡 **EXTRA_MODULES**: `ai-leadership` has 7 module files but registry defines 6 modules
- 🟡 **EXTRA_MODULES**: `gpt-vs-claude-vs-gemini` has 9 module files but registry defines 8 modules
- 🟡 **EXTRA_MODULES**: `ai-ethics` has 9 module files but registry defines 0 modules
- 🟡 **EXTRA_MODULES**: `ai-governance` has 9 module files but registry defines 0 modules
- 🟡 **EXTRA_MODULES**: `ai-in-society` has 9 module files but registry defines 0 modules
- 🟡 **EXTRA_MODULES**: `building-with-ai` has 9 module files but registry defines 0 modules
- 🟡 **EXTRA_MODULES**: `ai-side-hustle-money` has 8 module files but registry defines 6 modules
- 🟡 **EXTRA_MODULES**: `deploying-and-monitoring-ai` has 8 module files but registry defines 3 modules
- 🟡 **EXTRA_MODULES**: `truth-detectives-ai-and-fake-info` has 6 module files but registry defines 2 modules
- 🟡 **EXTRA_MODULES**: `voice-and-real-time-ai` has 8 module files but registry defines 3 modules

## courses.html

### Errors (1)

- 🔴 **ORPHAN_LINK**: courses.html links to course `how_large_language_models_work` not in registry

## Electives Hub (electives-hub.html)

✅ No issues found. _Note: hub is registry-only — no hardcoded `BASE_COURSES`. Courses load directly from `course-registry.json`._

## Cross-References

### Warnings (3)

- 🟡 **NOT_IN_COURSES_HTML**: registry course `truth-detectives-ai-and-fake-info` has no `?course=` link from courses.html
- 🟡 **NOT_IN_COURSES_HTML**: registry course `storytelling-with-ai` has no `?course=` link from courses.html
- 🟡 **NOT_IN_COURSES_HTML**: registry course `model-evaluation-and-benchmarks` has no `?course=` link from courses.html

---

## Summary

**1 error(s) require attention:**

1. 🔴 **ORPHAN_LINK**: courses.html links to course `how_large_language_models_work` not in registry

### Stats
- Registry courses: 161 (74 live, 87 coming soon)
- courses.html internal links checked: 81
- courses.html `?course=` ids referenced: 76
- Electives hub BASE_COURSES: 0 (registry-only)
- Module files verified: 479
