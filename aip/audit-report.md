# AESOP Course Audit Report

**Generated:** 2026-04-24 14:17 UTC
**Status:** 🔴 ISSUES FOUND
**Errors:** 19 · **Warnings:** 11

---

## Course Registry (course-registry.json)

### Errors (5)
- 🔴 BAD_URL: Registry course `cp19` has missing/invalid url field: ``
- 🔴 MISSING_DIR: Registry course `how_large_language_models_work` references `/ai-academy/modules/how_large_language_models_work/` which does not exist
- 🔴 BAD_URL: Registry course `am-8` has missing/invalid url field: ``
- 🔴 BAD_URL: Registry course `bu-11` has missing/invalid url field: ``
- 🔴 BAD_URL: Registry course `bu-12` has missing/invalid url field: ``

### Warnings (7)
- 🟡 EXTRA_MODULES: `governance` has 9 module files but registry defines 8 modules
- 🟡 EXTRA_MODULES: `society` has 9 module files but registry defines 8 modules
- 🟡 EXTRA_MODULES: `ethics` has 9 module files but registry defines 8 modules
- 🟡 EXTRA_MODULES: `building` has 9 module files but registry defines 8 modules
- 🟡 EXTRA_MODULES: `ai-and-education` has 7 module files but registry defines 6 modules
- 🟡 EXTRA_MODULES: `ai-leadership` has 7 module files but registry defines 6 modules
- 🟡 EXTRA_MODULES: `gpt-vs-claude-vs-gemini` has 9 module files but registry defines 8 modules

## courses.html

### Errors (14)
- 🔴 ORPHAN_LINK: courses.html links to course "ai-and-climate" not in registry
- 🔴 ORPHAN_LINK: courses.html links to course "ai-and-fake-information" not in registry
- 🔴 ORPHAN_LINK: courses.html links to course "ai-bias-and-fairness" not in registry
- 🔴 ORPHAN_LINK: courses.html links to course "ai-for-small-business-managers" not in registry
- 🔴 ORPHAN_LINK: courses.html links to course "building-agents-vertex-ai" not in registry
- 🔴 ORPHAN_LINK: courses.html links to course "coded-unfair-ai-bias-exposed" not in registry
- 🔴 ORPHAN_LINK: courses.html links to course "creating-with-ai-tools" not in registry
- 🔴 ORPHAN_LINK: courses.html links to course "how-large-language-models-work" not in registry
- 🔴 ORPHAN_LINK: courses.html links to course "make-it-yours-creating-with-ai" not in registry
- 🔴 ORPHAN_LINK: courses.html links to course "the-alignment-problem" not in registry
- 🔴 ORPHAN_LINK: courses.html links to course "the-context-window-race" not in registry
- 🔴 ORPHAN_LINK: courses.html links to course "the-future-of-intelligence" not in registry
- 🔴 ORPHAN_LINK: courses.html links to course "vertex-ai-data-agents" not in registry
- 🔴 ORPHAN_LINK: courses.html links to course "whats-really-inside-ai" not in registry

## Electives Hub (electives-hub.html)

_Note: `electives-hub.html` is registry-only (no hardcoded `BASE_COURSES` array); course data is fetched from `course-registry.json` at runtime. Checks H-1, H-2, X-2, X-3 have no entries to evaluate._

✅ No issues found.

## Cross-References

### Warnings (4)
- 🟡 NOT_IN_COURSES_HTML: registry course "cp19" (slug `cp19`) has no link from courses.html
- 🟡 NOT_IN_COURSES_HTML: registry course "am-8" (slug `am-8`) has no link from courses.html
- 🟡 NOT_IN_COURSES_HTML: registry course "bu-11" (slug `bu-11`) has no link from courses.html
- 🟡 NOT_IN_COURSES_HTML: registry course "bu-12" (slug `bu-12`) has no link from courses.html

---

## Summary

**19 error(s) require attention:**
1. MISSING_DIR: Registry course `how_large_language_models_work` references `/ai-academy/modules/how_large_language_models_work/` which does not exist
2. ORPHAN_LINK: courses.html links to course "ai-and-climate" not in registry
3. ORPHAN_LINK: courses.html links to course "ai-and-fake-information" not in registry
4. ORPHAN_LINK: courses.html links to course "ai-bias-and-fairness" not in registry
5. ORPHAN_LINK: courses.html links to course "ai-for-small-business-managers" not in registry
6. ORPHAN_LINK: courses.html links to course "building-agents-vertex-ai" not in registry
7. ORPHAN_LINK: courses.html links to course "coded-unfair-ai-bias-exposed" not in registry
8. ORPHAN_LINK: courses.html links to course "creating-with-ai-tools" not in registry
9. ORPHAN_LINK: courses.html links to course "how-large-language-models-work" not in registry
10. ORPHAN_LINK: courses.html links to course "make-it-yours-creating-with-ai" not in registry
…and 9 more (see sections above).

**11 warning(s):** see sections above for details.

### Stats
- Registry courses: 133 (54 live, 79 coming soon)
- courses.html internal `/ai-academy/` links checked: 7
- courses.html `?course=` parameters: 68
- Electives hub BASE_COURSES: 0 _(registry-only hub)_
- Module files verified: 351
