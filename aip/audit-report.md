# AESOP Course Audit Report

**Generated:** 2026-08-04 14:12 UTC
**Status:** 🔴 ISSUES FOUND
**Errors:** 12 · **Warnings:** 29

---

## Course Registry (course-registry.json)

### Errors (1)
- 🔴 **MISSING_DIR**: Registry course `eval-benchmark` references `/ai-academy/modules/eval-benchmark/` which does not exist

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

### Errors (11)
- 🔴 **DEAD_LINK**: courses.html links to `/ai-academy/modules/ai-misinformation/` but file does not exist
- 🔴 **DEAD_LINK**: courses.html links to `/ai-academy/modules/gpt-vs-claude-vs-gemini/` but file does not exist
- 🔴 **DEAD_LINK**: courses.html links to `/ai-academy/modules/ai-agents-in-the-wild/` but file does not exist
- 🔴 **DEAD_LINK**: courses.html links to `/ai-academy/modules/ai-autonomous-systems/` but file does not exist
- 🔴 **DEAD_LINK**: courses.html links to `/ai-academy/modules/ai-in-game-design-i/` but file does not exist
- 🔴 **DEAD_LINK**: courses.html links to `/ai-academy/modules/building-an-ai-first-business/` but file does not exist
- 🔴 **DEAD_LINK**: courses.html links to `/ai-academy/modules/building-ai-agents-v-optimization/` but file does not exist
- 🔴 **DEAD_LINK**: courses.html links to `/ai-academy/modules/working-with-the-anthropic-api/` but file does not exist
- 🔴 **DEAD_LINK**: courses.html links to `/ai-academy/modules/vertex-ai-data-agents/` but file does not exist
- 🔴 **DEAD_LINK**: courses.html links to `/ai-academy/modules/ai-side-hustle-money/` but file does not exist
- 🔴 **DEAD_LINK**: courses.html links to `/ai-academy/modules/ai-job-market-impact/` but file does not exist


## Electives Hub (electives-hub.html)

_Note: electives-hub.html loads courses dynamically from `course-registry.json` at runtime — no static `BASE_COURSES` array is defined. Checks H-1/H-2 are trivially satisfied; the runtime source is the registry itself, which Section 1 audits._

✅ No issues found.

## Cross-References

### Warnings (5)
- 🟡 **NOT_IN_COURSES_HTML**: registry course "society" has no link from courses.html
- 🟡 **NOT_IN_COURSES_HTML**: registry course "ar-11" has no link from courses.html
- 🟡 **NOT_IN_COURSES_HTML**: registry course "ar-8" has no link from courses.html
- 🟡 **NOT_IN_COURSES_HTML**: registry course "ap-7" has no link from courses.html
- 🟡 **NOT_IN_COURSES_HTML**: registry course "eval-benchmark" has no link from courses.html


---

## Summary

**12 error(s) require attention:**
1. **MISSING_DIR**: Registry course `eval-benchmark` references `/ai-academy/modules/eval-benchmark/` which does not exist
2. **DEAD_LINK**: courses.html links to `/ai-academy/modules/ai-misinformation/` but file does not exist
3. **DEAD_LINK**: courses.html links to `/ai-academy/modules/gpt-vs-claude-vs-gemini/` but file does not exist
4. **DEAD_LINK**: courses.html links to `/ai-academy/modules/ai-agents-in-the-wild/` but file does not exist
5. **DEAD_LINK**: courses.html links to `/ai-academy/modules/ai-autonomous-systems/` but file does not exist
6. **DEAD_LINK**: courses.html links to `/ai-academy/modules/ai-in-game-design-i/` but file does not exist
7. **DEAD_LINK**: courses.html links to `/ai-academy/modules/building-an-ai-first-business/` but file does not exist
8. **DEAD_LINK**: courses.html links to `/ai-academy/modules/building-ai-agents-v-optimization/` but file does not exist
9. **DEAD_LINK**: courses.html links to `/ai-academy/modules/working-with-the-anthropic-api/` but file does not exist
10. **DEAD_LINK**: courses.html links to `/ai-academy/modules/vertex-ai-data-agents/` but file does not exist
... and 2 more.

### Stats
- Registry courses: 131 (126 live, 3 coming soon, 2 retired)
- courses.html internal links checked: 143
- courses.html `?course=` IDs referenced: 123
- Electives hub BASE_COURSES: 0 (dynamic — sourced from registry at runtime)
- Module files verified: 780
