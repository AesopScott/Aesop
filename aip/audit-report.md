# AESOP Course Audit Report

**Generated:** 2026-05-10 14:13 UTC
**Status:** 🔴 ISSUES FOUND
**Errors:** 1 · **Warnings:** 0

---

## Course Registry (course-registry.json)

### Errors (1)

- 🔴 **CRITICAL: course-registry.json missing or invalid** — `ai-academy/modules/course-registry.json` is present but is not valid JSON. `json.load` fails at line 1039, column 1 (`Expecting value`). The offending line begins with a stray `n` character before the lesson string in `applied-ai-development` → module `cp1-m6` → lessons array:

  ```
  1038:           "Continuous Evaluation Pipelines",
  1039: n          "Cost Management & Optimization"
  1040:         ]
  ```

  Manual inspection of the file shows additional structural corruption further down (e.g., near lines 1140, 1232, 1445, 1453, 1469, 1478, 1539, 1600 — including a malformed `"id` key, a stray `n` prefix in `ai-and-media` lessons, an out-of-place `"languages"` block, an embedded `"resources"` array, a truncated `"title"` field in `building-ai-agents-i---use-cases`, and a malformed `_benchmark` key). The registry must be repaired before downstream checks can run.

## courses.html

⏭️ Skipped — registry invalid (per Check R-1, the routine skips to Step 5 when `course-registry.json` is unparseable).

## Electives Hub (electives-hub.html)

⏭️ Skipped — registry invalid.

## Cross-References

⏭️ Skipped — registry invalid.

---

## Summary

**1 error requires attention:**
1. `course-registry.json` is corrupted and cannot be parsed. The first parse failure is a stray `n` at line 1039:1 inside `applied-ai-development` → `cp1-m6.lessons`. Several additional corruption sites are visible in the same file. Until this file is restored to valid JSON, the registry, courses.html, electives-hub, and cross-reference checks cannot run.

**Recommended next action:** Restore `ai-academy/modules/course-registry.json` from a known-good commit (last clean parse evidenced by yesterday's audit report at 2026-05-09 21:55 UTC), or hand-repair the corrupted regions.

### Stats
- Registry courses: unknown (file unparseable)
- courses.html internal links checked: 0 (skipped)
- Electives hub BASE_COURSES: 0 (skipped)
- Module files verified: 0 (skipped)
