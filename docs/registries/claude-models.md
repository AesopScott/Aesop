# Claude Model Registry

Every Claude model version referenced in this project. For each: where it's used, what it does, and when it was introduced.

---

## `claude-haiku-4-5-20251001`

Lab chat endpoint for student interactions. Lightweight, cost-efficient model for conversational exchanges in course labs.

**Usage context:** Lab modules — student AI conversations in /aesop-api/proxy.php

**Producers** (model selection)
- `aesop-api/proxy.php:16` — hardcoded model constant `$MODEL = 'claude-haiku-4-5-20251001'`

**Consumers** (model invocations)
- `aesop-api/proxy.php:90+` — POST to Anthropic API with this model
- Lab HTML pages — implicit (call proxy.php, which uses Haiku)

**Purpose:** Cost-effective student chat responses in course labs.

**Status:** ✓ Currently in production

---

## `claude-sonnet-4-6`

Research and recommendation synthesis for course development planning phase. Higher quality reasoning for analyzing course corpus and generating recommendations.

**Usage context:** Course builder planning phase (Task #1) — research engine and recommendation generator

**Producers** (model selection)
- `.claude/skills/aesop-course-builder/research-engine.js` — planned for Task #1 (TBD exact line)
- `.claude/skills/aesop-course-builder/recommendation-generator.js` — planned for Task #1 (TBD exact line)

**Consumers** (model invocations)
- Research module — calls Anthropic Messages API with Sonnet for synthesis
- Recommendation generator — calls Anthropic Messages API with Sonnet for prescriptive recommendations

**Purpose:** Higher-quality reasoning for research synthesis and course recommendations.

**Status:** ⚠ Planned (Task #1) — not yet in code

---

## Summary

| Model | Context | Producers | Consumers | Status |
|-------|---------|-----------|-----------|--------|
| `claude-haiku-4-5-20251001` | Lab chat | proxy.php:16 | proxy.php + labs | ✓ |
| `claude-sonnet-4-6` | Research & recommendations | research-engine.js, recommendation-generator.js (Task #1) | research module, recommendation generator | ⚠ Planned |

---

## Audit Trail — Proof of Registry Verification

**Last audit:** 2026-05-20 19:45 UTC (by /cross-boundary-audit, Task #1 planning)

**Boundaries checked:** Claude model versions and usage sites

**Evidence recorded:**
- 1 entry with current producer/consumer pairs ✓ (Haiku in proxy.php)
- 1 entry with planned usage ⚠ (Sonnet for Task #1)
- New identifiers introduced: `claude-sonnet-4-6` (Task #1 planning introduces this)
- Registries match current code diff: Yes

**Gaps identified:**
- Sonnet model not yet in code (expected — Task #1 not started yet)

**Status:** Audit complete (planning phase) — Sonnet producer location TBD in Task #1 build phase
