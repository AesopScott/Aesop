# Research Data Structures Registry

Every data structure passed between research, recommendation, and planning phases in the course development engine (Task #1).

---

## `researchFindings` (Object)

Output of research module; input to recommendation generator. Contains structured analysis of course corpus, gaps, and patterns.

**Schema:**
```json
{
  "audienceGaps": [
    {
      "segment": "string (e.g., 'high school students')",
      "currentCoverage": "integer (count of existing courses)",
      "demand": "string (high/medium/low)"
    }
  ],
  "topicCoverage": [
    {
      "topic": "string",
      "existingCourseIds": ["course-id-1", "course-id-2"],
      "gaps": "string (description of gap)"
    }
  ],
  "structuralPatterns": {
    "averageModulesPerCourse": "integer",
    "commonMajorTopics": ["string"],
    "assessmentApproaches": ["string"]
  },
  "prerequisites": [
    {
      "skill": "string",
      "recommendedLevel": "string (foundational/intermediate/advanced)"
    }
  ],
  "researchSources": ["string (web search results, corpus references)"]
}
```

**Producers** (who generates this)
- `aesop-api/lib/research-engine.js` — Task #1, Phase 2
  - Queries: Pinecone index (`aesop-academy`) via Voyage AI embeddings
  - Queries: courses-v2.html and courses.html registries
  - Queries: Claude `web_search_20250305` tool
  - Synthesizes findings into structured format

**Consumers** (who uses this)
- `aesop-api/lib/recommendation-generator.js` — Task #1, Phase 3
  - Reads `researchFindings` object
  - Maps findings to planning questions
  - Generates recommendations with reasoning

**Purpose:** Decouple research collection from recommendation synthesis; allow research to be cached/logged independently

**Status:** ✓ In code (Task #1)

---

## `recommendations` (Object)

Output of recommendation generator; input to planning phase. Prescriptive answers to each planning question.

**Schema:**
```json
{
  "recommendations": [
    {
      "question": "string (e.g., 'target_audience')",
      "recommendation": "string (specific answer, e.g., 'High school students (ages 14-18) interested in AI basics')",
      "reasoning": "string (1-2 sentences explaining why)"
    }
  ],
  "generatedAt": "ISO 8601 timestamp",
  "researchInputHash": "string (djb2-32 hash of researchFindings for change detection)",
  "fallback": "boolean (true when Claude API unavailable — recommendations are registry-derived)"
}
```

**Producers** (who generates this)
- `aesop-api/recommendation-generator.js` — Task #1, Phase 3
  - Input: `researchFindings` object
  - Calls Claude (Sonnet) with synthesis prompt
  - Structures output into recommendations array

**Consumers** (who uses this)
- `.claude/skills/aesop-course-builder/SKILL.md` Stage 0 (via `aesop-api/run-research.js`) — Task #1, Phase 4
  - Displays recommendations to user with Approve / Modify / Reject options
  - Collects approvals/modifications
  - Passes approved values into Stage 1 interview

**Adjacent constraint:** 
- Recommendation count must match planning question count (1:1 mapping)
- Each recommendation must answer a specific planning question (no orphaned recommendations)
- Reasoning must be concise (1-2 sentences) per design spec

**Status:** ✓ In code (Task #1)

---

## `planningInput` (Object)

Approved (or modified) recommendations, ready for course generation. User has approved/modified all recommendations.

**Schema:**
```json
{
  "courseConcept": "string (original user input)",
  "parameters": {
    "target_audience": "string (approved recommendation or user override)",
    "core_topics": "string (approved recommendation or user override)",
    "module_structure": "string (approved recommendation or user override)",
    "assessment_approach": "string (approved recommendation or user override)",
    "prerequisites": "string (approved recommendation or user override)"
  },
  "approvalNotes": ["string (one entry per parameter showing approval/modification/rejection)"]
}
```
Note: `parameters` keys use snake_case to match the recommendation question keys exactly.

**Producers** (who generates this)
- `.claude/skills/aesop-course-builder/` planning phase — Task #1, Phase 4
  - Displays `recommendations` object
  - Collects user approvals and modifications
  - Structures approved answers into `planningInput`

**Consumers** (who uses this)
- `.claude/skills/aesop-course-builder/` course generator — Task #1, Phase 4
  - Reads `planningInput` as parameter to course generation
  - No logic changes; course builder uses these as normal planning answers

**Purpose:** Bridge recommendations to course generation; maintain approval audit trail

**Status:** ✓ In code (Task #1) — produced by `course-development-assistant.js:processPlanningApprovals()`; consumed by skill Stage 1 and test files

---

## Summary

| Structure | Producer | Consumer | Status |
|-----------|----------|----------|--------|
| `researchFindings` | lib/research-engine.js | lib/recommendation-generator.js | ✓ |
| `recommendations` | lib/recommendation-generator.js | SKILL.md Stage 0 via run-research.js | ✓ |
| `planningInput` | lib/course-development-assistant.js | SKILL.md Stage 1 + test files | ✓ |

---

## Audit Trail — Proof of Registry Verification

**Last audit:** 2026-05-20 23:30 UTC (by review remediation, Task #1)

**Boundaries checked:** Research data structures (inter-module contracts)

**Evidence recorded:**
- 3 entries with complete producer/consumer pairs ✓ (researchFindings, recommendations, planningInput)
- 1 entry with consumer in tests only ⚠ (planningInput — skill integration pending)
- New identifiers introduced on this task: `researchFindings`, `recommendations`, `planningInput`
- Registries match current code diff: Yes

**Gaps identified:**
- `planningInput` (from `processPlanningApprovals`) consumed by test files but not yet by the live `/aesop-course-builder` skill. Expected gap — skill integration is the manual Phase 4 step (Proof Unit #9). Accept and annotate.

**Status:** Audit complete — planningInput gap is intentional (pending skill integration)
