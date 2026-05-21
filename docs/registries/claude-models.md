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
- `aesop-api/lib/research-engine.js:88` — web search synthesis via Claude
- `aesop-api/lib/research-engine.js:147` — findings synthesis via Claude
- `aesop-api/lib/recommendation-generator.js:26` — prescriptive recommendation generation

**Consumers** (model invocations)
- `aesop-api/lib/research-engine.js` — Anthropic Messages API calls for web search and synthesis
- `aesop-api/lib/recommendation-generator.js` — Anthropic Messages API calls for recommendations
- `aesop-api/test-claude-sonnet.js:22` — connectivity test

**Purpose:** Higher-quality reasoning for research synthesis and course recommendations.

**Status:** ✓ In code (Task #1 complete)

---

## Summary

| Model | Context | Producers | Consumers | Status |
|-------|---------|-----------|-----------|--------|
| `claude-haiku-4-5-20251001` | Lab chat | proxy.php:16 | proxy.php + labs | ✓ |
| `claude-sonnet-4-6` | Research & recommendations | research-engine.js, recommendation-generator.js (Task #1) | research module, recommendation generator | ✓ |

---

## Audit Trail — Proof of Registry Verification

**Last audit:** 2026-05-20 22:00 UTC (by /cross-boundary-audit, Task #1 build complete)

**Boundaries checked:** Claude model versions and usage sites

**Evidence recorded:**
- 2 entries with complete producer/consumer pairs ✓ (Haiku in proxy.php, Sonnet in lib/)
- New identifiers introduced on this task: `claude-sonnet-4-6` (added to research-engine.js, recommendation-generator.js, test-claude-sonnet.js)
- Note: original plan used `claude-sonnet-4-20250514` (deprecated); updated to `claude-sonnet-4-6` in same task
- Registries match current code diff: Yes

**Gaps identified:** None — all models have producers and consumers paired

**Status:** Audit complete
