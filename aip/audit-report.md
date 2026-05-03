# AESOP Course Audit Report

**Generated:** 2026-05-03 14:13 UTC
**Status:** 🟡 WARNINGS ONLY
**Errors:** 0 · **Warnings:** 36

---

## Course Registry (course-registry.json)

### Warnings (34)
- 🟡 **DUPLICATE_SLUG**: directory `/ai-academy/modules/ai-ethics/` is referenced by multiple registry keys ("ethics", "ai-ethics"); using `ai-ethics` as canonical
- 🟡 **DUPLICATE_SLUG**: directory `/ai-academy/modules/ai-governance/` is referenced by multiple registry keys ("governance", "ai-governance"); using `ai-governance` as canonical
- 🟡 **DUPLICATE_SLUG**: directory `/ai-academy/modules/ai-in-society/` is referenced by multiple registry keys ("society", "ai-in-society"); using `ai-in-society` as canonical
- 🟡 **DUPLICATE_SLUG**: directory `/ai-academy/modules/building-with-ai/` is referenced by multiple registry keys ("building", "building-with-ai"); using `building-with-ai` as canonical
- 🟡 **DUPLICATE_SLUG**: directory `/ai-academy/modules/performing-arts-and-ai/` is referenced by multiple registry keys ("ar-11", "performing-arts-and-ai"); using `performing-arts-and-ai` as canonical
- 🟡 **EXTRA_MODULES**: `ai-and-education` has 7 module files but registry defines 6 modules
- 🟡 **EXTRA_MODULES**: `ai-leadership` has 7 module files but registry defines 6 modules
- 🟡 **EXTRA_MODULES**: `gpt-vs-claude-vs-gemini` has 9 module files but registry defines 8 modules
- 🟡 **EXTRA_MODULES**: `ai-ethics` has 9 module files but registry defines 0 modules
- 🟡 **LIVE_NO_MODULES**: registry course `ai-ethics` is live but defines 0 modules
- 🟡 **EXTRA_MODULES**: `ai-governance` has 9 module files but registry defines 0 modules
- 🟡 **LIVE_NO_MODULES**: registry course `ai-governance` is live but defines 0 modules
- 🟡 **EXTRA_MODULES**: `ai-in-society` has 9 module files but registry defines 0 modules
- 🟡 **LIVE_NO_MODULES**: registry course `ai-in-society` is live but defines 0 modules
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

> ℹ️ `electives-hub.html` is registry-driven (no hardcoded `BASE_COURSES` block). Hub checks H-1, H-2 and cross-checks X-2, X-3 are not applicable in this configuration and were skipped.

## Cross-References

### Warnings (2)
- 🟡 **NOT_IN_COURSES_HTML**: registry course "ar-8" (slug `ar-8`) has no link from courses.html
- 🟡 **NOT_IN_COURSES_HTML**: registry course "ap-7" (slug `ap-7`) has no link from courses.html

---

## Summary

No errors. 36 warning(s) flagged — registry, courses.html, and electives-hub are internally consistent and every referenced file exists, but the items below are worth a look:

1. DUPLICATE_SLUG: directory `/ai-academy/modules/ai-ethics/` is referenced by multiple registry keys ("ethics", "ai-ethics"); using `ai-ethics` as canonical
2. DUPLICATE_SLUG: directory `/ai-academy/modules/ai-governance/` is referenced by multiple registry keys ("governance", "ai-governance"); using `ai-governance` as canonical
3. DUPLICATE_SLUG: directory `/ai-academy/modules/ai-in-society/` is referenced by multiple registry keys ("society", "ai-in-society"); using `ai-in-society` as canonical
4. DUPLICATE_SLUG: directory `/ai-academy/modules/building-with-ai/` is referenced by multiple registry keys ("building", "building-with-ai"); using `building-with-ai` as canonical
5. DUPLICATE_SLUG: directory `/ai-academy/modules/performing-arts-and-ai/` is referenced by multiple registry keys ("ar-11", "performing-arts-and-ai"); using `performing-arts-and-ai` as canonical
…and 31 more (see sections above).

### Stats
- Registry courses: 130 (125 live, 3 coming soon, 2 retired)
- courses.html internal links checked: 20
- courses.html `?course=` references: 123
- Electives hub BASE_COURSES: 0 (registry-driven, none expected)
- Module files verified: 737
