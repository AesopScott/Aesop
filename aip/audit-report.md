# AESOP Course Audit Report

**Generated:** 2026-06-06 14:07 UTC
**Status:** 🔴 ISSUES FOUND
**Errors:** 2 · **Warnings:** 31

---

## Course Registry (course-registry.json)

### Errors (1)
- 🔴 **MISSING_DIR**: Registry course `eval-benchmark` references `/ai-academy/modules/eval-benchmark/` which does not exist

### Warnings (24)
- 🟡 **EXTRA_MODULES**: `society` has 9 files but registry defines 8 modules
- 🟡 **EXTRA_MODULES**: `ai-and-education` has 7 files but registry defines 6 modules
- 🟡 **EXTRA_MODULES**: `ai-leadership` has 7 files but registry defines 6 modules
- 🟡 **EXTRA_MODULES**: `gpt-vs-claude-vs-gemini` has 9 files but registry defines 8 modules
- 🟡 **EXTRA_MODULES**: `ai-side-hustle-money` has 8 files but registry defines 6 modules
- 🟡 **EXTRA_MODULES**: `deploying-and-monitoring-ai` has 8 files but registry defines 3 modules
- 🟡 **EXTRA_MODULES**: `truth-detectives-ai-and-fake-info` has 6 files but registry defines 2 modules
- 🟡 **EXTRA_MODULES**: `voice-and-real-time-ai` has 8 files but registry defines 3 modules
- 🟡 **EXTRA_MODULES**: `ai-network-pentesting` has 8 files but registry defines 1 modules
- 🟡 **EXTRA_MODULES**: `pentesting-ai-agents` has 8 files but registry defines 1 modules
- 🟡 **EXTRA_MODULES**: `what-s-coming-next` has 8 files but registry defines 1 modules
- 🟡 **EXTRA_MODULES**: `ai-in-science` has 8 files but registry defines 7 modules
- 🟡 **EXTRA_MODULES**: `ai-and-the-writer-s-voice` has 8 files but registry defines 1 modules
- 🟡 **EXTRA_MODULES**: `ap-7` has 8 files but registry defines 3 modules
- 🟡 **EXTRA_MODULES**: `ai-work-and-automation-deep-dive` has 8 files but registry defines 7 modules
- 🟡 **EXTRA_MODULES**: `ai-agent-risk-and-oversight` has 8 files but registry defines 3 modules
- 🟡 **EXTRA_MODULES**: `ai-hype-critical-thinking` has 8 files but registry defines 3 modules
- 🟡 **EXTRA_MODULES**: `deep-learning-for-builders` has 8 files but registry defines 5 modules
- 🟡 **EXTRA_MODULES**: `build-ai-workflows-no-code` has 6 files but registry defines 1 modules
- 🟡 **EXTRA_MODULES**: `gemini-for-college-life` has 5 files but registry defines 3 modules
- 🟡 **EXTRA_MODULES**: `agile-ai-side-projects` has 8 files but registry defines 1 modules
- 🟡 **EXTRA_MODULES**: `prompt-engineering-that-works` has 8 files but registry defines 1 modules
- 🟡 **EXTRA_MODULES**: `ai-in-gaming-and-interactive-media` has 6 files but registry defines 3 modules
- 🟡 **EXTRA_MODULES**: `is-the-robot-being-fair` has 4 files but registry defines 1 modules

## courses.html

✅ No issues found.

## Electives Hub (electives-hub.html) — dynamic registry mode

### Errors (1)
- 🔴 **MISSING_DIR**: electives-hub BASE_COURSE "eval-benchmark" references directory that does not exist


## Cross-References

### Warnings (7)
- 🟡 **NOT_IN_COURSES_HTML**: registry course "society" has no link from courses.html
- 🟡 **NOT_IN_ELECTIVES_HUB**: registry course "society" missing from electives-hub
- 🟡 **NOT_IN_COURSES_HTML**: registry course "ar-11" has no link from courses.html
- 🟡 **NOT_IN_ELECTIVES_HUB**: registry course "ar-11" missing from electives-hub
- 🟡 **NOT_IN_COURSES_HTML**: registry course "ar-8" has no link from courses.html
- 🟡 **NOT_IN_COURSES_HTML**: registry course "ap-7" has no link from courses.html
- 🟡 **NOT_IN_COURSES_HTML**: registry course "eval-benchmark" has no link from courses.html

---

## Summary

**2 error(s) require attention:**
1. MISSING_DIR: Registry course `eval-benchmark` references `/ai-academy/modules/eval-benchmark/` which does not exist
2. MISSING_DIR: electives-hub BASE_COURSE "eval-benchmark" references directory that does not exist

### Stats
- Registry courses: 131 (126 live, 3 coming soon, 2 other)
- courses.html internal links checked: 143
- Electives hub BASE_COURSES: 126 (sourced from registry at runtime)
- Module files verified: 780
