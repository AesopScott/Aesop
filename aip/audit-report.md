# AESOP Course Audit Report

**Generated:** 2026-06-01 14:09 UTC  
**Status:** 🔴 ISSUES FOUND  
**Errors:** 1 · **Warnings:** 26

---

## Course Registry (course-registry.json)

### Errors (1)
- 🔴 **MISSING_DIR**: `eval-benchmark` references `/ai-academy/modules/eval-benchmark/` which does not exist

### Warnings (23)
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

ℹ️ `electives-hub.html` is registry-only — no hardcoded `BASE_COURSES` array. Checks H-1, H-2 skipped (vacuously satisfied).

✅ No issues found.

## Cross-References

ℹ️ Checks X-2 and X-3 (electives-hub BASE_COURSES vs registry / courses.html) skipped — hub is registry-only.

### Warnings (3)
- 🟡 **NOT_IN_COURSES_HTML**: registry course `ar-8` has no link from courses.html
- 🟡 **NOT_IN_COURSES_HTML**: registry course `ap-7` has no link from courses.html
- 🟡 **NOT_IN_COURSES_HTML**: registry course `eval-benchmark` has no link from courses.html

---

## Summary

**1 error(s) require attention:**
1. MISSING_DIR: `eval-benchmark` references `/ai-academy/modules/eval-benchmark/` which does not exist

**26 warning(s):**
1. EXTRA_MODULES: `ai-and-education` has 7 module files but registry defines 6 modules
2. EXTRA_MODULES: `ai-leadership` has 7 module files but registry defines 6 modules
3. EXTRA_MODULES: `gpt-vs-claude-vs-gemini` has 9 module files but registry defines 8 modules
4. EXTRA_MODULES: `ai-side-hustle-money` has 8 module files but registry defines 6 modules
5. EXTRA_MODULES: `deploying-and-monitoring-ai` has 8 module files but registry defines 3 modules
6. EXTRA_MODULES: `truth-detectives-ai-and-fake-info` has 6 module files but registry defines 2 modules
7. EXTRA_MODULES: `voice-and-real-time-ai` has 8 module files but registry defines 3 modules
8. EXTRA_MODULES: `ai-network-pentesting` has 8 module files but registry defines 1 modules
9. EXTRA_MODULES: `pentesting-ai-agents` has 8 module files but registry defines 1 modules
10. EXTRA_MODULES: `what-s-coming-next` has 8 module files but registry defines 1 modules
…and 16 more — see sections above.

### Stats
- Registry courses: 131 (126 live, 3 coming soon, 2 retired)
- courses.html internal links checked: 143
- courses.html distinct `?course=` IDs: 123
- Electives hub BASE_COURSES: 0 (registry-only mode)
- Module files verified: 764
