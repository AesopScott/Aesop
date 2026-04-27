# AESOP Course Audit Report

**Generated:** 2026-04-27 14:21 UTC  
**Status:** 🔴 ISSUES FOUND  
**Errors:** 1 · **Warnings:** 27

---

## Course Registry (course-registry.json)

### Warnings (18)

- 🟡 DUPLICATE_URL: `/ai-academy/modules/ai-governance/` is referenced by 2 registry entries: `governance`, `ai-governance`
- 🟡 DUPLICATE_URL: `/ai-academy/modules/ai-in-society/` is referenced by 2 registry entries: `society`, `ai-in-society`
- 🟡 DUPLICATE_URL: `/ai-academy/modules/ai-ethics/` is referenced by 2 registry entries: `ethics`, `ai-ethics`
- 🟡 DUPLICATE_URL: `/ai-academy/modules/building-with-ai/` is referenced by 2 registry entries: `building`, `building-with-ai`
- 🟡 DUPLICATE_URL: `/ai-academy/modules/performing-arts-and-ai/` is referenced by 2 registry entries: `ar-11`, `performing-arts-and-ai`
- 🟡 EXTRA_MODULES: `ai-and-education` (ai-and-education) has 7 module files but registry defines 6 modules
- 🟡 EXTRA_MODULES: `ai-leadership` (ai-leadership) has 7 module files but registry defines 6 modules
- 🟡 EXTRA_MODULES: `gpt-vs-claude-vs-gemini` (gpt-vs-claude-vs-gemini) has 9 module files but registry defines 8 modules
- 🟡 LIVE_WITHOUT_MODULES: registry course `ai-ethics` is `status=live` but has empty `modules` array (url=`/ai-academy/modules/ai-ethics/`)
- 🟡 LIVE_WITHOUT_MODULES: registry course `ai-governance` is `status=live` but has empty `modules` array (url=`/ai-academy/modules/ai-governance/`)
- 🟡 LIVE_WITHOUT_MODULES: registry course `ai-in-society` is `status=live` but has empty `modules` array (url=`/ai-academy/modules/ai-in-society/`)
- 🟡 LIVE_WITHOUT_MODULES: registry course `building-with-ai` is `status=live` but has empty `modules` array (url=`/ai-academy/modules/building-with-ai/`)
- 🟡 EXTRA_MODULES: `ai-side-hustle-money` (ai-side-hustle-money) has 8 module files but registry defines 6 modules
- 🟡 EXTRA_MODULES: `deploying-and-monitoring-ai` (deploying-and-monitoring-ai) has 8 module files but registry defines 3 modules
- 🟡 EXTRA_MODULES: `truth-detectives-ai-and-fake-info` (truth-detectives-ai-and-fake-info) has 6 module files but registry defines 2 modules
- 🟡 EXTRA_MODULES: `voice-and-real-time-ai` (voice-and-real-time-ai) has 8 module files but registry defines 3 modules
- 🟡 EXTRA_MODULES: `ai-network-pentesting` (ai-network-pentesting) has 2 module files but registry defines 1 modules
- 🟡 EXTRA_MODULES: `pentesting-ai-agents` (pentesting-ai-agents) has 2 module files but registry defines 1 modules

## courses.html

### Errors (1)

- 🔴 ORPHAN_LINK: courses.html links to course `how_large_language_models_work` not in registry

## Electives Hub (electives-hub.html)

_The hub is registry-driven: it loads `course-registry.json` at runtime (filtered to live courses with a url). No hardcoded `BASE_COURSES` array exists, so registry/hub consistency is enforced by construction._

✅ No issues found.

## Cross-References

### Warnings (9)

- 🟡 NOT_IN_COURSES_HTML: registry course `ar-11` has no link from courses.html
- 🟡 NOT_IN_COURSES_HTML: registry course `truth-detectives-ai-and-fake-info` has no link from courses.html
- 🟡 NOT_IN_COURSES_HTML: registry course `storytelling-with-ai` has no link from courses.html
- 🟡 NOT_IN_COURSES_HTML: registry course `model-evaluation-and-benchmarks` has no link from courses.html
- 🟡 NOT_IN_COURSES_HTML: registry course `ai-augmented-reconnaissance` has no link from courses.html
- 🟡 NOT_IN_COURSES_HTML: registry course `ai-network-pentesting` has no link from courses.html
- 🟡 NOT_IN_COURSES_HTML: registry course `image-generation-models` has no link from courses.html
- 🟡 NOT_IN_COURSES_HTML: registry course `pentesting-ai-agents` has no link from courses.html
- 🟡 NOT_IN_COURSES_HTML: registry course `pentesting-llm-applications` has no link from courses.html

---

## Summary

**1 error(s) require attention:**

1. ORPHAN_LINK: courses.html links to course `how_large_language_models_work` not in registry

### Stats

- Registry courses: 167 (81 live, 86 coming soon)
- courses.html internal links checked: 9
- courses.html `?course=` references: 77
- Electives hub mode: registry-driven
- Module files verified: 521
