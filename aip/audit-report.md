# AESOP Course Audit Report

**Generated:** 2026-05-08 14:11 UTC
**Status:** 🟡 WARNINGS ONLY
**Errors:** 0 · **Warnings:** 28

---

## Course Registry (course-registry.json)

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

✅ No issues found.

> **Note:** electives-hub.html v1.1.0 is registry-driven — it loads all course data directly from `course-registry.json` rather than maintaining a hardcoded `BASE_COURSES` constant. Checks H-1, H-2, X-2, and X-3 are therefore not applicable to this implementation; the registry itself (verified in Step 1 above) is the single source of truth for the hub.

## Cross-References

### Warnings (4)
- 🟡 **NOT_IN_COURSES_HTML**: registry course "society" has no link from courses.html
- 🟡 **NOT_IN_COURSES_HTML**: registry course "ar-11" has no link from courses.html
- 🟡 **NOT_IN_COURSES_HTML**: registry course "ar-8" has no link from courses.html
- 🟡 **NOT_IN_COURSES_HTML**: registry course "ap-7" has no link from courses.html


---

## Summary

No errors. 28 warning(s) for review:

- **24 `EXTRA_MODULES`** warnings — courses with more module files in the directory than the registry defines (likely stale/draft files or in-progress modules not yet wired into the registry).
- **4 `NOT_IN_COURSES_HTML`** warning(s) — registry courses with no link from `courses.html`.

### Stats
- Registry courses: 130 (127 live, 3 coming soon)
- courses.html internal links checked: 20
- Electives hub BASE_COURSES: n/a (registry-driven; data loaded from `course-registry.json`)
- Module files verified: 780
