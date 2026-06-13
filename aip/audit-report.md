# AESOP Course Audit Report

**Generated:** 2026-06-13 14:08 UTC
**Status:** 🔴 ISSUES FOUND
**Errors:** 1 · **Warnings:** 64

---

## Course Registry (course-registry.json)

### Errors (1)
- 🔴 **MISSING_DIR**: `eval-benchmark` (expected directory `ai-academy/modules/eval-benchmark`)

### Warnings (24)
- 🟡 **EXTRA_MODULES**: `society` has 9 module files but registry defines 8
- 🟡 **EXTRA_MODULES**: `ai-and-education` has 7 module files but registry defines 6
- 🟡 **EXTRA_MODULES**: `ai-leadership` has 7 module files but registry defines 6
- 🟡 **EXTRA_MODULES**: `gpt-vs-claude-vs-gemini` has 9 module files but registry defines 8
- 🟡 **EXTRA_MODULES**: `ai-side-hustle-money` has 8 module files but registry defines 6
- 🟡 **EXTRA_MODULES**: `deploying-and-monitoring-ai` has 8 module files but registry defines 3
- 🟡 **EXTRA_MODULES**: `truth-detectives-ai-and-fake-info` has 6 module files but registry defines 2
- 🟡 **EXTRA_MODULES**: `voice-and-real-time-ai` has 8 module files but registry defines 3
- 🟡 **EXTRA_MODULES**: `ai-network-pentesting` has 8 module files but registry defines 1
- 🟡 **EXTRA_MODULES**: `pentesting-ai-agents` has 8 module files but registry defines 1
- 🟡 **EXTRA_MODULES**: `what-s-coming-next` has 8 module files but registry defines 1
- 🟡 **EXTRA_MODULES**: `ai-in-science` has 8 module files but registry defines 7
- 🟡 **EXTRA_MODULES**: `ai-and-the-writer-s-voice` has 8 module files but registry defines 1
- 🟡 **EXTRA_MODULES**: `ap-7` has 8 module files but registry defines 3
- 🟡 **EXTRA_MODULES**: `ai-work-and-automation-deep-dive` has 8 module files but registry defines 7
- 🟡 **EXTRA_MODULES**: `ai-agent-risk-and-oversight` has 8 module files but registry defines 3
- 🟡 **EXTRA_MODULES**: `ai-hype-critical-thinking` has 8 module files but registry defines 3
- 🟡 **EXTRA_MODULES**: `deep-learning-for-builders` has 8 module files but registry defines 5
- 🟡 **EXTRA_MODULES**: `build-ai-workflows-no-code` has 6 module files but registry defines 1
- 🟡 **EXTRA_MODULES**: `gemini-for-college-life` has 5 module files but registry defines 3
- 🟡 **EXTRA_MODULES**: `agile-ai-side-projects` has 8 module files but registry defines 1
- 🟡 **EXTRA_MODULES**: `prompt-engineering-that-works` has 8 module files but registry defines 1
- 🟡 **EXTRA_MODULES**: `ai-in-gaming-and-interactive-media` has 6 module files but registry defines 3
- 🟡 **EXTRA_MODULES**: `is-the-robot-being-fair` has 4 module files but registry defines 1

## courses.html

✅ No issues found.

## Electives Hub (electives-hub.html)

> **Note:** As of `electives-hub-v1.1.0`, the hub is fully registry-driven — the legacy `BASE_COURSES` array was removed (the comment in the source says: "Registry-only: all course data from course-registry.json"). The hub now reads `course-registry.json` at runtime, so any live registry course is rendered automatically. The checks below use the JSON-LD SEO block (`?course=…` self-references) as the static reference set instead.

✅ No issues found.

## Cross-References

### Warnings (40)
- 🟡 **NOT_IN_COURSES_HTML**: registry course "ar-8" has no link from courses.html
- 🟡 **NOT_IN_COURSES_HTML**: registry course "ap-7" has no link from courses.html
- 🟡 **NOT_IN_ELECTIVES_HUB**: registry elective "claude-ai-chat" missing from electives-hub
- 🟡 **NOT_IN_ELECTIVES_HUB**: registry elective "claude-cowork" missing from electives-hub
- 🟡 **NOT_IN_ELECTIVES_HUB**: registry elective "claude-code" missing from electives-hub
- 🟡 **NOT_IN_ELECTIVES_HUB**: registry elective "ai-tutor-under-the-hood" missing from electives-hub
- 🟡 **NOT_IN_ELECTIVES_HUB**: registry elective "ai-lens-on-the-world" missing from electives-hub
- 🟡 **NOT_IN_ELECTIVES_HUB**: registry elective "how-ai-actually-works" missing from electives-hub
- 🟡 **NOT_IN_ELECTIVES_HUB**: registry elective "prompt-engineering-that-works" missing from electives-hub
- 🟡 **NOT_IN_ELECTIVES_HUB**: registry elective "ai-in-gaming-and-interactive-media" missing from electives-hub
- 🟡 **NOT_IN_ELECTIVES_HUB**: registry elective "ai-ethics-foundations" missing from electives-hub
- 🟡 **NOT_IN_ELECTIVES_HUB**: registry elective "ai-safety-for-everyone" missing from electives-hub
- 🟡 **NOT_IN_ELECTIVES_HUB**: registry elective "ai-tools-for-real-teaching" missing from electives-hub
- 🟡 **NOT_IN_ELECTIVES_HUB**: registry elective "is-the-robot-being-fair" missing from electives-hub
- 🟡 **NOT_IN_ELECTIVES_HUB**: registry elective "pick-the-right-ai-tool" missing from electives-hub
- 🟡 **NOT_IN_ELECTIVES_HUB**: registry elective "wispr-flow" missing from electives-hub
- 🟡 **NOT_IN_ELECTIVES_HUB**: registry elective "how-machines-learn" missing from electives-hub
- 🟡 **NOT_IN_ELECTIVES_HUB**: registry elective "ai-and-architecture" missing from electives-hub
- 🟡 **NOT_IN_ELECTIVES_HUB**: registry elective "ai-safety-and-alignment" missing from electives-hub
- 🟡 **NOT_IN_ELECTIVES_HUB**: registry elective "real-or-rendered" missing from electives-hub
- 🟡 **NOT_IN_COURSES_HTML**: registry course "eval-benchmark" has no link from courses.html
- 🟡 **NOT_IN_ELECTIVES_HUB**: registry elective "eval-benchmark" missing from electives-hub
- 🟡 **COURSES_HUB_MISMATCH**: courses.html links to "ai-and-architecture" but electives-hub does not reference it
- 🟡 **COURSES_HUB_MISMATCH**: courses.html links to "ai-in-gaming-and-interactive-media" but electives-hub does not reference it
- 🟡 **COURSES_HUB_MISMATCH**: courses.html links to "wispr-flow" but electives-hub does not reference it
- 🟡 **COURSES_HUB_MISMATCH**: courses.html links to "prompt-engineering-that-works" but electives-hub does not reference it
- 🟡 **COURSES_HUB_MISMATCH**: courses.html links to "how-ai-actually-works" but electives-hub does not reference it
- 🟡 **COURSES_HUB_MISMATCH**: courses.html links to "ai-lens-on-the-world" but electives-hub does not reference it
- 🟡 **COURSES_HUB_MISMATCH**: courses.html links to "ai-tools-for-real-teaching" but electives-hub does not reference it
- 🟡 **COURSES_HUB_MISMATCH**: courses.html links to "ai-tutor-under-the-hood" but electives-hub does not reference it
- 🟡 **COURSES_HUB_MISMATCH**: courses.html links to "how-machines-learn" but electives-hub does not reference it
- 🟡 **COURSES_HUB_MISMATCH**: courses.html links to "is-the-robot-being-fair" but electives-hub does not reference it
- 🟡 **COURSES_HUB_MISMATCH**: courses.html links to "pick-the-right-ai-tool" but electives-hub does not reference it
- 🟡 **COURSES_HUB_MISMATCH**: courses.html links to "real-or-rendered" but electives-hub does not reference it
- 🟡 **COURSES_HUB_MISMATCH**: courses.html links to "ai-ethics-foundations" but electives-hub does not reference it
- 🟡 **COURSES_HUB_MISMATCH**: courses.html links to "ai-safety-for-everyone" but electives-hub does not reference it
- 🟡 **COURSES_HUB_MISMATCH**: courses.html links to "ai-safety-and-alignment" but electives-hub does not reference it
- 🟡 **COURSES_HUB_MISMATCH**: courses.html links to "claude-ai-chat" but electives-hub does not reference it
- 🟡 **COURSES_HUB_MISMATCH**: courses.html links to "claude-cowork" but electives-hub does not reference it
- 🟡 **COURSES_HUB_MISMATCH**: courses.html links to "claude-code" but electives-hub does not reference it

---

## Summary

**1 error(s) require attention:**
1. MISSING_DIR: `eval-benchmark` (expected directory `ai-academy/modules/eval-benchmark`)

### Stats
- Registry courses: 131 (126 live, 3 coming soon, 2 retired)
- courses.html internal links checked: 143
- courses.html `?course=` IDs referenced: 123
- Electives hub static course IDs (JSON-LD): 109
- Electives hub version: `1.1.0` (BASE_COURSES present: no)
- Module files verified: 875
