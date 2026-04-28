# AESOP Course Audit Report

**Generated:** 2026-04-28 14:11 UTC
**Status:** 🔴 ISSUES FOUND
**Errors:** 1 · **Warnings:** 36

---

## Course Registry (course-registry.json)

### Warnings (17)
- 🟡 **EXTRA_MODULES**: `ai-and-education` has 7 module files but registry defines 6 modules
- 🟡 **EXTRA_MODULES**: `ai-leadership` has 7 module files but registry defines 6 modules
- 🟡 **EXTRA_MODULES**: `gpt-vs-claude-vs-gemini` has 9 module files but registry defines 8 modules
- 🟡 **EMPTY_MODULES_ARRAY**: registry course `ai-ethics` has empty `modules` array but 9 module files exist in `/ai-academy/modules/ai-ethics/`
- 🟡 **EMPTY_MODULES_ARRAY**: registry course `ai-governance` has empty `modules` array but 9 module files exist in `/ai-academy/modules/ai-governance/`
- 🟡 **EMPTY_MODULES_ARRAY**: registry course `ai-in-society` has empty `modules` array but 9 module files exist in `/ai-academy/modules/ai-in-society/`
- 🟡 **EMPTY_MODULES_ARRAY**: registry course `building-with-ai` has empty `modules` array but 9 module files exist in `/ai-academy/modules/building-with-ai/`
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


## courses.html

### Errors (1)
- 🔴 **ORPHAN_LINK**: courses.html links to course `how_large_language_models_work` not in registry


## Electives Hub (electives-hub.html)

> ℹ️ electives-hub.html is registry-driven (loads `course-registry.json` at runtime); no `BASE_COURSES` array to audit. By construction, all live registry courses appear in the hub.

✅ No issues found.

## Cross-References

### Warnings (19)
- 🟡 **NOT_IN_COURSES_HTML**: registry course `truth-detectives-ai-and-fake-info` (dir `truth-detectives-ai-and-fake-info`) has no link from courses.html
- 🟡 **NOT_IN_COURSES_HTML**: registry course `storytelling-with-ai` (dir `storytelling-with-ai`) has no link from courses.html
- 🟡 **NOT_IN_COURSES_HTML**: registry course `model-evaluation-and-benchmarks` (dir `model-evaluation-and-benchmarks`) has no link from courses.html
- 🟡 **NOT_IN_COURSES_HTML**: registry course `ai-augmented-reconnaissance` (dir `ai-augmented-reconnaissance`) has no link from courses.html
- 🟡 **NOT_IN_COURSES_HTML**: registry course `ai-network-pentesting` (dir `ai-network-pentesting`) has no link from courses.html
- 🟡 **NOT_IN_COURSES_HTML**: registry course `image-generation-models` (dir `image-generation-models`) has no link from courses.html
- 🟡 **NOT_IN_COURSES_HTML**: registry course `pentesting-ai-agents` (dir `pentesting-ai-agents`) has no link from courses.html
- 🟡 **NOT_IN_COURSES_HTML**: registry course `pentesting-llm-applications` (dir `pentesting-llm-applications`) has no link from courses.html
- 🟡 **NOT_IN_COURSES_HTML**: registry course `what-s-coming-next` (dir `what-s-coming-next`) has no link from courses.html
- 🟡 **NOT_IN_COURSES_HTML**: registry course `robot-speak-talk-to-ai` (dir `robot-speak-talk-to-ai`) has no link from courses.html
- 🟡 **NOT_IN_COURSES_HTML**: registry course `what-ai-knows-about-you` (dir `what-ai-knows-about-you`) has no link from courses.html
- 🟡 **NOT_IN_COURSES_HTML**: registry course `ai-in-science` (dir `ai-in-science`) has no link from courses.html
- 🟡 **NOT_IN_COURSES_HTML**: registry course `ai-safety-and-alignment-basics` (dir `ai-safety-and-alignment-basics`) has no link from courses.html
- 🟡 **NOT_IN_COURSES_HTML**: registry course `ar-8` (dir `ar-8`) has no link from courses.html
- 🟡 **NOT_IN_COURSES_HTML**: registry course `deepfakes-and-synthetic-media` (dir `deepfakes-and-synthetic-media`) has no link from courses.html
- 🟡 **NOT_IN_COURSES_HTML**: registry course `human-ai-interaction` (dir `human-ai-interaction`) has no link from courses.html
- 🟡 **NOT_IN_COURSES_HTML**: registry course `future-of-work-ai` (dir `future-of-work-ai`) has no link from courses.html
- 🟡 **NOT_IN_COURSES_HTML**: registry course `ai-and-the-writer-s-voice` (dir `ai-and-the-writer-s-voice`) has no link from courses.html
- 🟡 **NOT_IN_COURSES_HTML**: registry course `ap-7` (dir `ap-7`) has no link from courses.html


---

## Summary

**1 error(s) require attention:**
1. ORPHAN_LINK: courses.html links to course `how_large_language_models_work` not in registry

Plus 36 warning(s) — see sections above.

### Stats
- Registry courses: 96 (92 live, 4 coming soon)
- courses.html internal links checked: 40
- Electives hub courses surfaced: 92 (registry-driven)
- Module files verified: 575
