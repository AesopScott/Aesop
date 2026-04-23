# AESOP Course Audit Report

**Generated:** 2026-04-23 14:11 UTC
**Status:** 🔴 ISSUES FOUND
**Errors:** 17 · **Warnings:** 35

---

## Course Registry (course-registry.json)

### Errors (7)
- 🔴 **MISSING_DIR**: Registry course `cp13` (status=live) has no `url` field — cannot locate directory
- 🔴 **MISSING_DIR**: Registry course `how_large_language_models_work` references `/ai-academy/modules/how_large_language_models_work/` which does not exist
- 🔴 **MISSING_DIR**: Registry course `ap-7` (status=live) has no `url` field — cannot locate directory
- 🔴 **MISSING_DIR**: Registry course `ar-8` (status=live) has no `url` field — cannot locate directory
- 🔴 **MISSING_DIR**: Registry course `bu-4` (status=live) has no `url` field — cannot locate directory
- 🔴 **MISSING_DIR**: Registry course `dv-14` (status=live) has no `url` field — cannot locate directory
- 🔴 **MISSING_DIR**: Registry course `foundations-advanced` (status=None) has no `url` field — cannot locate directory

### Warnings (7)
- 🟡 **EXTRA_MODULES**: `governance` (ai-governance) has 9 module files but registry defines 8 modules
- 🟡 **EXTRA_MODULES**: `society` (ai-in-society) has 9 module files but registry defines 8 modules
- 🟡 **EXTRA_MODULES**: `ethics` (ai-ethics) has 9 module files but registry defines 8 modules
- 🟡 **EXTRA_MODULES**: `building` (building-with-ai) has 9 module files but registry defines 8 modules
- 🟡 **EXTRA_MODULES**: `ai-and-education` (ai-and-education) has 7 module files but registry defines 6 modules
- 🟡 **EXTRA_MODULES**: `ai-leadership` (ai-leadership) has 7 module files but registry defines 6 modules
- 🟡 **EXTRA_MODULES**: `gpt-vs-claude-vs-gemini` (gpt-vs-claude-vs-gemini) has 9 module files but registry defines 8 modules

## courses.html

### Errors (10)
- 🔴 **ORPHAN_LINK**: courses.html links to course "ai-agents-in-the-wild" not in registry
- 🔴 **ORPHAN_LINK**: courses.html links to course "ai-for-graphic-design" not in registry
- 🔴 **ORPHAN_LINK**: courses.html links to course "ai-job-market-impact" not in registry
- 🔴 **ORPHAN_LINK**: courses.html links to course "applied-ai-development" not in registry
- 🔴 **ORPHAN_LINK**: courses.html links to course "code-audit-workflows-team-standards" not in registry
- 🔴 **ORPHAN_LINK**: courses.html links to course "conversational-ai-chatbots" not in registry
- 🔴 **ORPHAN_LINK**: courses.html links to course "evaluation-and-testing-for-ai" not in registry
- 🔴 **ORPHAN_LINK**: courses.html links to course "funding-and-pitching-ai-ventures" not in registry
- 🔴 **ORPHAN_LINK**: courses.html links to course "running-models-locally" not in registry
- 🔴 **ORPHAN_LINK**: courses.html links to course "synthetic-data-and-self-improvement" not in registry

## Electives Hub (electives-hub.html)

> Note: `electives-hub.html` is registry-only — it derives its course list at runtime from `course-registry.json` (filter: `!k.startsWith("_") && c.url && c.status === "live"`). There is no hardcoded `BASE_COURSES` array, so Checks H-1/H-2 operate on the derived course list.

✅ No issues found.

## Cross-References

### Warnings (28)
- 🟡 **NOT_IN_COURSES_HTML**: registry course "ai-and-climate" has no link from courses.html
- 🟡 **NOT_IN_COURSES_HTML**: registry course "ap-7" has no link from courses.html
- 🟡 **NOT_IN_COURSES_HTML**: registry course "ar-8" has no link from courses.html
- 🟡 **NOT_IN_COURSES_HTML**: registry course "bu-4" has no link from courses.html
- 🟡 **NOT_IN_COURSES_HTML**: registry course "cp13" has no link from courses.html
- 🟡 **NOT_IN_COURSES_HTML**: registry course "dv-14" has no link from courses.html
- 🟡 **NOT_IN_COURSES_HTML**: registry course "dv-15" has no link from courses.html
- 🟡 **NOT_IN_COURSES_HTML**: registry course "dv-16" has no link from courses.html
- 🟡 **NOT_IN_COURSES_HTML**: registry course "dv-17" has no link from courses.html
- 🟡 **NOT_IN_COURSES_HTML**: registry course "foundations-advanced" has no link from courses.html
- 🟡 **NOT_IN_ELECTIVES_HUB**: registry course "ap-7" missing from electives-hub
- 🟡 **NOT_IN_ELECTIVES_HUB**: registry course "ar-8" missing from electives-hub
- 🟡 **NOT_IN_ELECTIVES_HUB**: registry course "bu-4" missing from electives-hub
- 🟡 **NOT_IN_ELECTIVES_HUB**: registry course "cp13" missing from electives-hub
- 🟡 **NOT_IN_ELECTIVES_HUB**: registry course "dv-14" missing from electives-hub
- 🟡 **NOT_IN_ELECTIVES_HUB**: registry course "foundations-advanced" missing from electives-hub
- 🟡 **COURSES_HUB_MISMATCH**: courses.html links to "ai-agents-in-the-wild" but electives-hub does not define it
- 🟡 **COURSES_HUB_MISMATCH**: courses.html links to "ai-code-review-fundamentals" but electives-hub does not define it
- 🟡 **COURSES_HUB_MISMATCH**: courses.html links to "ai-for-graphic-design" but electives-hub does not define it
- 🟡 **COURSES_HUB_MISMATCH**: courses.html links to "ai-job-market-impact" but electives-hub does not define it
- 🟡 **COURSES_HUB_MISMATCH**: courses.html links to "applied-ai-development" but electives-hub does not define it
- 🟡 **COURSES_HUB_MISMATCH**: courses.html links to "code-audit-workflows-team-standards" but electives-hub does not define it
- 🟡 **COURSES_HUB_MISMATCH**: courses.html links to "conversational-ai-chatbots" but electives-hub does not define it
- 🟡 **COURSES_HUB_MISMATCH**: courses.html links to "evaluation-and-testing-for-ai" but electives-hub does not define it
- 🟡 **COURSES_HUB_MISMATCH**: courses.html links to "funding-and-pitching-ai-ventures" but electives-hub does not define it
- 🟡 **COURSES_HUB_MISMATCH**: courses.html links to "running-models-locally" but electives-hub does not define it
- 🟡 **COURSES_HUB_MISMATCH**: courses.html links to "security-auditing-ai-generated-code" but electives-hub does not define it
- 🟡 **COURSES_HUB_MISMATCH**: courses.html links to "synthetic-data-and-self-improvement" but electives-hub does not define it

---

## Summary

**17 error(s) require attention:**
1. **MISSING_DIR** — Registry course `cp13` (status=live) has no `url` field — cannot locate directory
2. **MISSING_DIR** — Registry course `how_large_language_models_work` references `/ai-academy/modules/how_large_language_models_work/` which does not exist
3. **MISSING_DIR** — Registry course `ap-7` (status=live) has no `url` field — cannot locate directory
4. **MISSING_DIR** — Registry course `ar-8` (status=live) has no `url` field — cannot locate directory
5. **MISSING_DIR** — Registry course `bu-4` (status=live) has no `url` field — cannot locate directory
6. **MISSING_DIR** — Registry course `dv-14` (status=live) has no `url` field — cannot locate directory
7. **MISSING_DIR** — Registry course `foundations-advanced` (status=None) has no `url` field — cannot locate directory
8. **ORPHAN_LINK** — courses.html links to course "ai-agents-in-the-wild" not in registry
9. **ORPHAN_LINK** — courses.html links to course "ai-for-graphic-design" not in registry
10. **ORPHAN_LINK** — courses.html links to course "ai-job-market-impact" not in registry
... and 7 more (see sections above).

### Stats
- Registry courses: 85 (43 live, 42 coming soon)
- courses.html internal links checked: 52
- courses.html `?course=` parameters: 45
- Electives hub courses (derived from registry): 37
- Module files verified: 269
