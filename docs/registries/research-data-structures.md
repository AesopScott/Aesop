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
      "existingCourses": ["course-id-1", "course-id-2"],
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
- `aesop-api/research-engine.js` (or skill module) — Task #1, Phase 2
  - Queries: Pinecone index (`aesop-academy`)
  - Queries: courses-v2.html and courses.html registries
  - Queries: Claude web search tool
  - Synthesizes findings into structured format

**Consumers** (who uses this)
- `aesop-api/recommendation-generator.js` — Task #1, Phase 3
  - Reads `researchFindings` object
  - Maps findings to planning questions
  - Generates recommendations with reasoning

**Purpose:** Decouple research collection from recommendation synthesis; allow research to be cached/logged independently

**Status:** ⚠ Planned (Task #1, Phase 2) — not yet in code

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
      "reasoning": "string (1-2 sentences explaining why)",
      "derivedFrom": {
        "researchSources": ["string"],
        "highConfidence": "boolean"
      }
    }
  ],
  "generatedAt": "ISO 8601 timestamp",
  "researchInputHash": "string (SHA256 of researchFindings for audit trail)"
}
```

**Producers** (who generates this)
- `aesop-api/recommendation-generator.js` — Task #1, Phase 3
  - Input: `researchFindings` object
  - Calls Claude (Sonnet) with synthesis prompt
  - Structures output into recommendations array

**Consumers** (who uses this)
- `.claude/skills/aesop-course-builder/` planning phase — Task #1, Phase 4
  - Displays recommendations to user
  - Collects approvals/modifications
  - Passes approved recommendations to course generator

**Adjacent constraint:** 
- Recommendation count must match planning question count (1:1 mapping)
- Each recommendation must answer a specific planning question (no orphaned recommendations)
- Reasoning must be concise (1-2 sentences) per design spec

**Status:** ⚠ Planned (Task #1, Phase 3) — not yet in code

---

## `planningInput` (Object)

Approved (or modified) recommendations, ready for course generation. User has approved/modified all recommendations.

**Schema:**
```json
{
  "courseConcept": "string (original user input)",
  "targetAudience": "string (approved recommendation or user modification)",
  "coreTopics": ["string"],
  "moduleStructure": "string (e.g., '8 modules: Intro, Scenario, Lesson, Context, Lab')",
  "prerequisites": ["string"],
  "assessmentApproach": "string",
  "approvedAt": "ISO 8601 timestamp",
  "approvalNotes": "string (user comments if any modifications made)",
  "derivedFromRecommendations": "boolean (true if all fields came from recommendations)"
}
```

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

**Status:** ⚠ Planned (Task #1, Phase 4) — not yet in code

---

## Summary

| Structure | Producer | Consumer | Status |
|-----------|----------|----------|--------|
| `researchFindings` | research-engine.js (Task #1) | recommendation-generator.js (Task #1) | ⚠ Planned |
| `recommendations` | recommendation-generator.js (Task #1) | planning phase (Task #1) | ⚠ Planned |
| `planningInput` | planning phase (Task #1) | course generator (Task #1) | ⚠ Planned |

---

## Audit Trail — Proof of Registry Verification

**Last audit:** 2026-05-20 19:45 UTC (by /cross-boundary-audit, Task #1 planning)

**Boundaries checked:** Research data structures (inter-module contracts)

**Evidence recorded:**
- 0 entries currently in code (all planned for Task #1)
- 3 new data structure contracts introduced by Task #1
- Schema defined and documented for each
- Producer/consumer mapping clear (research → recommendation → planning → generation)
- New identifiers introduced: `researchFindings`, `recommendations`, `planningInput` (all Task #1)
- Registries match current code diff: Yes (no code yet; spec-level audit)

**Gaps identified:** None — all structures designed to avoid orphaned producers/consumers and shape mismatches

**Status:** Audit complete (planning phase) — ready for implementation in Task #1 build phase
