# AESOP Course Audit Report

**Generated:** 2026-04-30 14:32 UTC  
**Status:** 🟡 WARNINGS ONLY  
**Errors:** 0 · **Warnings:** 30

---

## Course Registry (course-registry.json)

### Warnings (26)
- 🟡 **EXTRA_MODULES**: `society` has 9 files but registry defines 8 modules
- 🟡 **EXTRA_MODULES**: `ai-and-education` has 7 files but registry defines 6 modules
- 🟡 **EXTRA_MODULES**: `ai-leadership` has 7 files but registry defines 6 modules
- 🟡 **EXTRA_MODULES**: `gpt-vs-claude-vs-gemini` has 9 files but registry defines 8 modules
- 🟡 **EXTRA_MODULES**: `ai-ethics` has 9 files but registry defines 0 modules
- 🟡 **EXTRA_MODULES**: `ai-governance` has 9 files but registry defines 0 modules
- 🟡 **EXTRA_MODULES**: `ai-in-society` has 9 files but registry defines 0 modules
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

## courses.html

✅ No issues found.

## Electives Hub (electives-hub.html)

✅ No issues found.

_Note: `electives-hub.html` is now registry-driven (v1.1.0 — no hardcoded `BASE_COURSES`). All course data is fetched from `course-registry.json` at runtime, so checks H-1/H-2 are not applicable._

## Cross-References

### Warnings (4)
- 🟡 **NOT_IN_COURSES_HTML**: registry course "society" has no link from courses.html
- 🟡 **NOT_IN_COURSES_HTML**: registry course "ar-11" has no link from courses.html
- 🟡 **NOT_IN_COURSES_HTML**: registry course "ar-8" has no link from courses.html
- 🟡 **NOT_IN_COURSES_HTML**: registry course "ap-7" has no link from courses.html

_Note: Cross-references X-2 and X-3 (registry vs. `BASE_COURSES`) are not applicable — `electives-hub.html` reads directly from the registry._

---

## Summary

No errors. 30 warning(s) noted below for review.

### Stats
- Registry courses: 125 (122 live, 3 coming soon)
- courses.html internal links checked: 20
- courses.html `?course=` IDs referenced: 118
- Electives hub BASE_COURSES: 0 _(registry-driven)_
- Module files verified: 730
