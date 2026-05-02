# AESOP Course Audit Report

**Generated:** 2026-05-02 14:23 UTC
**Status:** 🟡 WARNINGS ONLY
**Errors:** 0 · **Warnings:** 34

---

## Course Registry (course-registry.json)

### Warnings (32)
- 🟡 **EXTRA_MODULES**: `ai-and-education` (slug `ai-and-education`) has 7 module files but registry defines 6 modules
- 🟡 **EXTRA_MODULES**: `ai-leadership` (slug `ai-leadership`) has 7 module files but registry defines 6 modules
- 🟡 **EXTRA_MODULES**: `gpt-vs-claude-vs-gemini` (slug `gpt-vs-claude-vs-gemini`) has 9 module files but registry defines 8 modules
- 🟡 **EXTRA_MODULES**: `ai-ethics` (slug `ai-ethics`) has 9 module files but registry defines 0 modules
- 🟡 **EXTRA_MODULES**: `ai-governance` (slug `ai-governance`) has 9 module files but registry defines 0 modules
- 🟡 **EXTRA_MODULES**: `ai-in-society` (slug `ai-in-society`) has 9 module files but registry defines 0 modules
- 🟡 **EXTRA_MODULES**: `ai-side-hustle-money` (slug `ai-side-hustle-money`) has 8 module files but registry defines 6 modules
- 🟡 **EXTRA_MODULES**: `deploying-and-monitoring-ai` (slug `deploying-and-monitoring-ai`) has 8 module files but registry defines 3 modules
- 🟡 **EXTRA_MODULES**: `truth-detectives-ai-and-fake-info` (slug `truth-detectives-ai-and-fake-info`) has 6 module files but registry defines 2 modules
- 🟡 **EXTRA_MODULES**: `voice-and-real-time-ai` (slug `voice-and-real-time-ai`) has 8 module files but registry defines 3 modules
- 🟡 **EXTRA_MODULES**: `ai-network-pentesting` (slug `ai-network-pentesting`) has 8 module files but registry defines 1 modules
- 🟡 **EXTRA_MODULES**: `pentesting-ai-agents` (slug `pentesting-ai-agents`) has 8 module files but registry defines 1 modules
- 🟡 **EXTRA_MODULES**: `what-s-coming-next` (slug `what-s-coming-next`) has 8 module files but registry defines 1 modules
- 🟡 **EXTRA_MODULES**: `ai-in-science` (slug `ai-in-science`) has 8 module files but registry defines 7 modules
- 🟡 **EXTRA_MODULES**: `ai-and-the-writer-s-voice` (slug `ai-and-the-writer-s-voice`) has 8 module files but registry defines 1 modules
- 🟡 **EXTRA_MODULES**: `ap-7` (slug `ap-7`) has 8 module files but registry defines 3 modules
- 🟡 **EXTRA_MODULES**: `ai-work-and-automation-deep-dive` (slug `ai-work-and-automation-deep-dive`) has 8 module files but registry defines 7 modules
- 🟡 **EXTRA_MODULES**: `ai-agent-risk-and-oversight` (slug `ai-agent-risk-and-oversight`) has 8 module files but registry defines 3 modules
- 🟡 **EXTRA_MODULES**: `ai-hype-critical-thinking` (slug `ai-hype-critical-thinking`) has 8 module files but registry defines 3 modules
- 🟡 **EXTRA_MODULES**: `deep-learning-for-builders` (slug `deep-learning-for-builders`) has 8 module files but registry defines 5 modules
- 🟡 **EXTRA_MODULES**: `build-ai-workflows-no-code` (slug `build-ai-workflows-no-code`) has 6 module files but registry defines 1 modules
- 🟡 **EXTRA_MODULES**: `gemini-for-college-life` (slug `gemini-for-college-life`) has 5 module files but registry defines 3 modules
- 🟡 **EXTRA_MODULES**: `agile-ai-side-projects` (slug `agile-ai-side-projects`) has 8 module files but registry defines 1 modules
- 🟡 **EXTRA_MODULES**: `prompt-engineering-that-works` (slug `prompt-engineering-that-works`) has 8 module files but registry defines 1 modules
- 🟡 **EXTRA_MODULES**: `ai-in-gaming-and-interactive-media` (slug `ai-in-gaming-and-interactive-media`) has 6 module files but registry defines 3 modules
- 🟡 **EXTRA_MODULES**: `is-the-robot-being-fair` (slug `is-the-robot-being-fair`) has 4 module files but registry defines 1 modules
- 🟡 **DUPLICATE_URL**: `/ai-academy/modules/ai-ethics/` is referenced by 2 registry entries: `ethics`, `ai-ethics`
- 🟡 **DUPLICATE_URL**: `/ai-academy/modules/ai-governance/` is referenced by 2 registry entries: `governance`, `ai-governance`
- 🟡 **DUPLICATE_URL**: `/ai-academy/modules/ai-in-society/` is referenced by 2 registry entries: `society`, `ai-in-society`
- 🟡 **DUPLICATE_URL**: `/ai-academy/modules/building-with-ai/` is referenced by 2 registry entries: `building`, `building-with-ai`
- 🟡 **DUPLICATE_URL**: `/ai-academy/modules/performing-arts-and-ai/` is referenced by 2 registry entries: `ar-11`, `performing-arts-and-ai`
- 🟡 **MISSING_ID_FIELD**: Registry entry `building-with-ai` has no `id` field

## courses.html

✅ No issues found.

## Electives Hub (electives-hub.html)

### Notes (1)
- ℹ️ **REGISTRY_DRIVEN**: electives-hub.html no longer defines a `BASE_COURSES` array; it loads all `status: "live"` courses from `course-registry.json` at runtime (see `loadCourseRegistry()` near line 2148). Checks H-1, H-2 are therefore N/A.

✅ No errors or warnings.

## Cross-References

### Warnings (2)
- 🟡 **NOT_IN_COURSES_HTML**: registry course "ap-7" (slug `ap-7`) has no `?course=` link from courses.html
- 🟡 **NOT_IN_COURSES_HTML**: registry course "ar-8" (slug `ar-8`) has no `?course=` link from courses.html

### Notes (1)
- ℹ️ **HUB_REGISTRY_DRIVEN**: Cross-references X-2 and X-3 are N/A: the electives hub renders every `status: "live"` registry course automatically, so there is no separate BASE_COURSES list to compare against.

---

## Summary

No errors. 34 warning(s) recorded for review:

1. **EXTRA_MODULES** — `ai-and-education` (slug `ai-and-education`) has 7 module files but registry defines 6 modules
2. **EXTRA_MODULES** — `ai-leadership` (slug `ai-leadership`) has 7 module files but registry defines 6 modules
3. **EXTRA_MODULES** — `gpt-vs-claude-vs-gemini` (slug `gpt-vs-claude-vs-gemini`) has 9 module files but registry defines 8 modules
4. **EXTRA_MODULES** — `ai-ethics` (slug `ai-ethics`) has 9 module files but registry defines 0 modules
5. **EXTRA_MODULES** — `ai-governance` (slug `ai-governance`) has 9 module files but registry defines 0 modules
…and 29 more (see sections above).

### Stats
- Registry courses: 130 (125 live, 3 coming soon, 2 retired)
- courses.html internal `/ai-academy/` links checked: 20
- courses.html `?course=` parameters: 123
- Electives hub BASE_COURSES: N/A (registry-driven)
- Module files verified: 737
