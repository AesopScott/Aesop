# AESOP Course Audit Report

**Generated:** 2026-10-03 14:21 UTC
**Status:** ISSUES FOUND
**Errors:** 1 - **Warnings:** 26

---

## Course Registry (course-registry.json)

### Errors (1)
- ERROR: MISSING_DIR: eval-benchmark (expected directory `ai-academy/modules/eval-benchmark/`)

### Warnings (23)
- WARNING: EXTRA_MODULES: ai-and-education has 7 files but registry defines 6 modules
- WARNING: EXTRA_MODULES: ai-leadership has 7 files but registry defines 6 modules
- WARNING: EXTRA_MODULES: gpt-vs-claude-vs-gemini has 9 files but registry defines 8 modules
- WARNING: EXTRA_MODULES: ai-side-hustle-money has 8 files but registry defines 6 modules
- WARNING: EXTRA_MODULES: deploying-and-monitoring-ai has 8 files but registry defines 3 modules
- WARNING: EXTRA_MODULES: truth-detectives-ai-and-fake-info has 6 files but registry defines 2 modules
- WARNING: EXTRA_MODULES: voice-and-real-time-ai has 8 files but registry defines 3 modules
- WARNING: EXTRA_MODULES: ai-network-pentesting has 8 files but registry defines 1 modules
- WARNING: EXTRA_MODULES: pentesting-ai-agents has 8 files but registry defines 1 modules
- WARNING: EXTRA_MODULES: what-s-coming-next has 8 files but registry defines 1 modules
- WARNING: EXTRA_MODULES: ai-in-science has 8 files but registry defines 7 modules
- WARNING: EXTRA_MODULES: ai-and-the-writer-s-voice has 8 files but registry defines 1 modules
- WARNING: EXTRA_MODULES: ap-7 has 8 files but registry defines 3 modules
- WARNING: EXTRA_MODULES: ai-work-and-automation-deep-dive has 8 files but registry defines 7 modules
- WARNING: EXTRA_MODULES: ai-agent-risk-and-oversight has 8 files but registry defines 3 modules
- WARNING: EXTRA_MODULES: ai-hype-critical-thinking has 8 files but registry defines 3 modules
- WARNING: EXTRA_MODULES: deep-learning-for-builders has 8 files but registry defines 5 modules
- WARNING: EXTRA_MODULES: build-ai-workflows-no-code has 6 files but registry defines 1 modules
- WARNING: EXTRA_MODULES: gemini-for-college-life has 5 files but registry defines 3 modules
- WARNING: EXTRA_MODULES: agile-ai-side-projects has 8 files but registry defines 1 modules
- WARNING: EXTRA_MODULES: prompt-engineering-that-works has 8 files but registry defines 1 modules
- WARNING: EXTRA_MODULES: ai-in-gaming-and-interactive-media has 6 files but registry defines 3 modules
- WARNING: EXTRA_MODULES: is-the-robot-being-fair has 4 files but registry defines 1 modules

## courses.html

OK No issues found.

## Electives Hub (electives-hub.html)

Note: `electives-hub.html` has no hardcoded `BASE_COURSES` array — it builds its course list from `course-registry.json` at runtime (see v1.1.0 header comment). Checks H-1, H-2, X-2, and X-3 are therefore not applicable; the hub stays in sync with the registry by construction.

## Cross-References

### Warnings (3)
- WARNING: NOT_IN_COURSES_HTML: registry course "ar-8" has no link from courses.html
- WARNING: NOT_IN_COURSES_HTML: registry course "ap-7" has no link from courses.html
- WARNING: NOT_IN_COURSES_HTML: registry course "eval-benchmark" has no link from courses.html

---

## Summary

**1 error(s) require attention:**
1. MISSING_DIR: eval-benchmark (expected directory `ai-academy/modules/eval-benchmark/`)

### Stats
- Registry courses: 131 (126 live, 3 coming soon, 2 retired)
- courses.html internal links checked: 21
- Electives hub BASE_COURSES: n/a (registry-driven)
- Module files verified: 764
