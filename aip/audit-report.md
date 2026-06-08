# AESOP Course Audit Report

**Generated:** 2026-06-08 14:08 UTC
**Status:** 🔴 ISSUES FOUND
**Errors:** 1 · **Warnings:** 29

---

## Course Registry (course-registry.json)

### Errors (1)

- 🔴 **MISSING_DIR**: registry course `eval-benchmark` references `/ai-academy/modules/eval-benchmark/` which does not exist

### Warnings (24)

- 🟡 **EXTRA_MODULES**: `society` has 9 module files but registry defines 8 modules
- 🟡 **EXTRA_MODULES**: `ai-and-education` has 7 module files but registry defines 6 modules
- 🟡 **EXTRA_MODULES**: `ai-leadership` has 7 module files but registry defines 6 modules
- 🟡 **EXTRA_MODULES**: `gpt-vs-claude-vs-gemini` has 9 module files but registry defines 8 modules
- 🟡 **EXTRA_MODULES**: `ai-side-hustle-money` has 8 module files but registry defines 6 modules
- 🟡 **EXTRA_MODULES**: `deploying-and-monitoring-ai` has 8 module files but registry defines 3 modules
- 🟡 **EXTRA_MODULES**: `truth-detectives-ai-and-fake-info` has 6 module files but registry defines 2 modules
- 🟡 **EXTRA_MODULES**: `voice-and-real-time-ai` has 8 module files but registry defines 3 modules
- 🟡 **EXTRA_MODULES**: `ai-network-pentesting` has 8 module files but registry defines 1 modules
- 🟡 **EXTRA_MODULES**: `pentesting-ai-agents` has 8 module files but registry defines 1 modules
- 🟡 **EXTRA_MODULES**: `what-s-coming-next` has 8 module files but registry defines 1 modules
- 🟡 **EXTRA_MODULES**: `ai-in-science` has 8 module files but registry defines 7 modules
- 🟡 **EXTRA_MODULES**: `ai-and-the-writer-s-voice` has 8 module files but registry defines 1 modules
- 🟡 **EXTRA_MODULES**: `ap-7` has 8 module files but registry defines 3 modules
- 🟡 **EXTRA_MODULES**: `ai-work-and-automation-deep-dive` has 8 module files but registry defines 7 modules
- 🟡 **EXTRA_MODULES**: `ai-agent-risk-and-oversight` has 8 module files but registry defines 3 modules
- 🟡 **EXTRA_MODULES**: `ai-hype-critical-thinking` has 8 module files but registry defines 3 modules
- 🟡 **EXTRA_MODULES**: `deep-learning-for-builders` has 8 module files but registry defines 5 modules
- 🟡 **EXTRA_MODULES**: `build-ai-workflows-no-code` has 6 module files but registry defines 1 modules
- 🟡 **EXTRA_MODULES**: `gemini-for-college-life` has 5 module files but registry defines 3 modules
- 🟡 **EXTRA_MODULES**: `agile-ai-side-projects` has 8 module files but registry defines 1 modules
- 🟡 **EXTRA_MODULES**: `prompt-engineering-that-works` has 8 module files but registry defines 1 modules
- 🟡 **EXTRA_MODULES**: `ai-in-gaming-and-interactive-media` has 6 module files but registry defines 3 modules
- 🟡 **EXTRA_MODULES**: `is-the-robot-being-fair` has 4 module files but registry defines 1 modules

## courses.html

✅ No issues found.

## Electives Hub (electives-hub.html)

ℹ️ Electives hub is registry-driven — courses load directly from `course-registry.json` (no hardcoded `BASE_COURSES`). Checks H-1/H-2 are N/A.

✅ No issues found.

## Cross-References

### Warnings (5)

- 🟡 **NOT_IN_COURSES_HTML**: registry course `ap-7` has no link from courses.html
- 🟡 **NOT_IN_COURSES_HTML**: registry course `ar-11` has no link from courses.html
- 🟡 **NOT_IN_COURSES_HTML**: registry course `ar-8` has no link from courses.html
- 🟡 **NOT_IN_COURSES_HTML**: registry course `eval-benchmark` has no link from courses.html
- 🟡 **NOT_IN_COURSES_HTML**: registry course `society` has no link from courses.html

_Note: X-2 (NOT_IN_ELECTIVES_HUB) and X-3 (COURSES_HUB_MISMATCH) are N/A — electives-hub is registry-driven._

---

## Summary

**1 error(s) require attention:**

1. MISSING_DIR: registry course `eval-benchmark` references `/ai-academy/modules/eval-benchmark/` which does not exist

### Stats
- Registry courses: 131 (128 live, 3 coming soon)
- courses.html internal links checked: 21
- Electives hub BASE_COURSES: N/A (registry-driven)
- Module files verified: 780
