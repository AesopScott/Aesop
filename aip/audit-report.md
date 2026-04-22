# AESOP Course Audit Report

**Generated:** 2026-04-22 14:27 UTC
**Status:** 🔴 ISSUES FOUND
**Errors:** 13 · **Warnings:** 26

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

### Errors (6)
- 🔴 **ORPHAN_LINK**: courses.html links to course "ai-agents-in-the-wild" not in registry
- 🔴 **ORPHAN_LINK**: courses.html links to course "ai-for-graphic-design" not in registry
- 🔴 **ORPHAN_LINK**: courses.html links to course "applied-ai-development" not in registry
- 🔴 **ORPHAN_LINK**: courses.html links to course "evaluation-and-testing-for-ai" not in registry
- 🔴 **ORPHAN_LINK**: courses.html links to course "funding-and-pitching-ai-ventures" not in registry
- 🔴 **ORPHAN_LINK**: courses.html links to course "synthetic-data-and-self-improvement" not in registry

## Electives Hub (electives-hub.html)

> Note: `electives-hub.html` is registry-only — it derives its course list at runtime from `course-registry.json` (filter: `!k.startsWith("_") && c.url && c.status === "live"`). There is no hardcoded `BASE_COURSES` array, so Checks H-1/H-2 operate on the derived course list.

✅ No issues found.

## Cross-References

### Warnings (19)
- 🟡 **NOT_IN_COURSES_HTML**: registry course "ai-and-climate" has no link from courses.html
- 🟡 **NOT_IN_COURSES_HTML**: registry course "ai-security-and-red-teaming" has no link from courses.html
- 🟡 **NOT_IN_COURSES_HTML**: registry course "ap-7" has no link from courses.html
- 🟡 **NOT_IN_COURSES_HTML**: registry course "ar-8" has no link from courses.html
- 🟡 **NOT_IN_COURSES_HTML**: registry course "bu-4" has no link from courses.html
- 🟡 **NOT_IN_COURSES_HTML**: registry course "cp13" has no link from courses.html
- 🟡 **NOT_IN_COURSES_HTML**: registry course "dv-14" has no link from courses.html
- 🟡 **NOT_IN_COURSES_HTML**: registry course "dv-15" has no link from courses.html
- 🟡 **NOT_IN_ELECTIVES_HUB**: registry course "ap-7" missing from electives-hub
- 🟡 **NOT_IN_ELECTIVES_HUB**: registry course "ar-8" missing from electives-hub
- 🟡 **NOT_IN_ELECTIVES_HUB**: registry course "bu-4" missing from electives-hub
- 🟡 **NOT_IN_ELECTIVES_HUB**: registry course "cp13" missing from electives-hub
- 🟡 **NOT_IN_ELECTIVES_HUB**: registry course "dv-14" missing from electives-hub
- 🟡 **COURSES_HUB_MISMATCH**: courses.html links to "ai-agents-in-the-wild" but electives-hub does not define it
- 🟡 **COURSES_HUB_MISMATCH**: courses.html links to "ai-for-graphic-design" but electives-hub does not define it
- 🟡 **COURSES_HUB_MISMATCH**: courses.html links to "applied-ai-development" but electives-hub does not define it
- 🟡 **COURSES_HUB_MISMATCH**: courses.html links to "evaluation-and-testing-for-ai" but electives-hub does not define it
- 🟡 **COURSES_HUB_MISMATCH**: courses.html links to "funding-and-pitching-ai-ventures" but electives-hub does not define it
- 🟡 **COURSES_HUB_MISMATCH**: courses.html links to "synthetic-data-and-self-improvement" but electives-hub does not define it

---

## Summary

**13 error(s) require attention:**
1. **MISSING_DIR** — Registry course `cp13` (status=live) has no `url` field — cannot locate directory
2. **MISSING_DIR** — Registry course `how_large_language_models_work` references `/ai-academy/modules/how_large_language_models_work/` which does not exist
3. **MISSING_DIR** — Registry course `ap-7` (status=live) has no `url` field — cannot locate directory
4. **MISSING_DIR** — Registry course `ar-8` (status=live) has no `url` field — cannot locate directory
5. **MISSING_DIR** — Registry course `bu-4` (status=live) has no `url` field — cannot locate directory
6. **MISSING_DIR** — Registry course `dv-14` (status=live) has no `url` field — cannot locate directory
7. **MISSING_DIR** — Registry course `foundations-advanced` (status=None) has no `url` field — cannot locate directory
8. **ORPHAN_LINK** — courses.html links to course "ai-agents-in-the-wild" not in registry
9. **ORPHAN_LINK** — courses.html links to course "ai-for-graphic-design" not in registry
10. **ORPHAN_LINK** — courses.html links to course "applied-ai-development" not in registry
... and 3 more (see sections above).

### Stats
- Registry courses: 86 (40 live, 45 coming soon)
- courses.html internal links checked: 7
- courses.html `?course=` parameters: 38
- Electives hub courses (derived from registry): 35
- Module files verified: 253
