# AESOP Course Audit Report

**Generated:** 2026-07-24 14:09 UTC
**Status:** 🔴 ISSUES FOUND
**Errors:** 3 · **Warnings:** 28

---

## Course Registry (course-registry.json)

### Errors (3)
- 🔴 **MISSING_DIR**: Registry course `society` references `/ai-academy/modules/society/` which does not exist or is empty
- 🔴 **MISSING_DIR**: Registry course `ar-11` references `/ai-academy/modules/ar-11/` which does not exist or is empty
- 🔴 **MISSING_DIR**: Registry course `eval-benchmark` references `/ai-academy/modules/eval-benchmark/` which does not exist or is empty

### Warnings (23)
- 🟡 **EXTRA_MODULES**: `ai-and-education` has 7 module files on disk but registry defines 6 modules
- 🟡 **EXTRA_MODULES**: `ai-leadership` has 7 module files on disk but registry defines 6 modules
- 🟡 **EXTRA_MODULES**: `gpt-vs-claude-vs-gemini` has 9 module files on disk but registry defines 8 modules
- 🟡 **EXTRA_MODULES**: `ai-side-hustle-money` has 8 module files on disk but registry defines 6 modules
- 🟡 **EXTRA_MODULES**: `deploying-and-monitoring-ai` has 8 module files on disk but registry defines 3 modules
- 🟡 **EXTRA_MODULES**: `truth-detectives-ai-and-fake-info` has 6 module files on disk but registry defines 2 modules
- 🟡 **EXTRA_MODULES**: `voice-and-real-time-ai` has 8 module files on disk but registry defines 3 modules
- 🟡 **EXTRA_MODULES**: `ai-network-pentesting` has 8 module files on disk but registry defines 1 modules
- 🟡 **EXTRA_MODULES**: `pentesting-ai-agents` has 8 module files on disk but registry defines 1 modules
- 🟡 **EXTRA_MODULES**: `what-s-coming-next` has 8 module files on disk but registry defines 1 modules
- 🟡 **EXTRA_MODULES**: `ai-in-science` has 8 module files on disk but registry defines 7 modules
- 🟡 **EXTRA_MODULES**: `ai-and-the-writer-s-voice` has 8 module files on disk but registry defines 1 modules
- 🟡 **EXTRA_MODULES**: `ap-7` has 8 module files on disk but registry defines 3 modules
- 🟡 **EXTRA_MODULES**: `ai-work-and-automation-deep-dive` has 8 module files on disk but registry defines 7 modules
- 🟡 **EXTRA_MODULES**: `ai-agent-risk-and-oversight` has 8 module files on disk but registry defines 3 modules
- 🟡 **EXTRA_MODULES**: `ai-hype-critical-thinking` has 8 module files on disk but registry defines 3 modules
- 🟡 **EXTRA_MODULES**: `deep-learning-for-builders` has 8 module files on disk but registry defines 5 modules
- 🟡 **EXTRA_MODULES**: `build-ai-workflows-no-code` has 6 module files on disk but registry defines 1 modules
- 🟡 **EXTRA_MODULES**: `gemini-for-college-life` has 5 module files on disk but registry defines 3 modules
- 🟡 **EXTRA_MODULES**: `agile-ai-side-projects` has 8 module files on disk but registry defines 1 modules
- 🟡 **EXTRA_MODULES**: `prompt-engineering-that-works` has 8 module files on disk but registry defines 1 modules
- 🟡 **EXTRA_MODULES**: `ai-in-gaming-and-interactive-media` has 6 module files on disk but registry defines 3 modules
- 🟡 **EXTRA_MODULES**: `is-the-robot-being-fair` has 4 module files on disk but registry defines 1 modules

## courses.html

✅ No issues found.

## Electives Hub (electives-hub.html)

✅ No issues found. `electives-hub.html` is registry-only (v1.1.0+) — all course data is loaded at runtime from `course-registry.json`, so H-1/H-2 checks are inherently satisfied.

## Cross-References

### Warnings (5)
- 🟡 **NOT_IN_COURSES_HTML**: registry course `society` has no `?course=society` link from courses.html
- 🟡 **NOT_IN_COURSES_HTML**: registry course `ar-11` has no `?course=ar-11` link from courses.html
- 🟡 **NOT_IN_COURSES_HTML**: registry course `ar-8` has no `?course=ar-8` link from courses.html
- 🟡 **NOT_IN_COURSES_HTML**: registry course `ap-7` has no `?course=ap-7` link from courses.html
- 🟡 **NOT_IN_COURSES_HTML**: registry course `eval-benchmark` has no `?course=eval-benchmark` link from courses.html

---

## Summary

**3 error(s) require attention:**
1. **MISSING_DIR** — Registry course `society` references `/ai-academy/modules/society/` which does not exist or is empty
2. **MISSING_DIR** — Registry course `ar-11` references `/ai-academy/modules/ar-11/` which does not exist or is empty
3. **MISSING_DIR** — Registry course `eval-benchmark` references `/ai-academy/modules/eval-benchmark/` which does not exist or is empty

### Stats
- Registry courses: 131 (128 live, 3 coming soon)
- courses.html internal links checked: 21
- Electives hub BASE_COURSES: n/a (registry-only)
- Module files verified: 764
