# Task #1 Planning — Modify Course Development Engine to Do Research

## DESIGN DISCUSSION — Research & Recommendations for Course Planning

### User Problem

When building courses directly (without AIP), the `/aesop-course-builder` skill enters a planning phase that asks questions (target audience, core topics, module structure, assessment approach, prerequisites). Today, you must answer from intuition/memory with no data backing. With research + recommendations, the skill should research answers first, present backed-by-data suggestions with brief reasoning, and let you approve, reject, or modify them before proceeding to course generation.

### End-to-End Reachability

**Journey:**
1. Invoke `/aesop-course-builder` with a course concept
2. Skill researches answers to planning questions via Corpus Registry + global web search
3. Skill presents recommendations with reasoning (1-2 sentences per recommendation)
4. You approve, reject, or modify each recommendation
5. Skill generates course using approved parameters

**Gaps closed by this feature:**
- No current Corpus Registry access in the skill
- No research phase before planning questions
- No way to feed research data into recommendations
- All answers are manual/prose-based today

### System Components

**Data Sources:**
- Pinecone corpus (via project credentials)
- courses.html (v1 course registry)
- courses-v2.html (v2 course registry)
- Global web search (topic research only; NOT AIP signals like Google Trends/Reddit)

**Processing Flow:**
1. **Research Module** — Calls Claude (Sonnet) to synthesize research from Pinecone, course registries, and web search. Outputs: audience gaps, existing topic coverage, structural patterns, prerequisite analysis.
2. **Recommendation Generator** — Claude synthesizes research into specific answers (audience, topics, structure, prerequisites, assessment) with brief reasoning (1-2 sentences per recommendation).
3. **Planning Phase UI** — Presents recommendations with reasoning; accepts approval/modification.
4. **Course Builder** — Uses approved parameters to generate course (minimal change).

**Synchronous flow:** Research → Recommendations → Planning Questions → Approval/Modification → Build

**Recommendation style:** Prescriptive (one strong recommendation per question) with brief reasoning explaining why.

### Architectural Dependencies

1. **Web Search** — Implementation-agnostic; Claude's WebSearch tool is acceptable.
2. **Pinecone & Registry Access** — Pinecone credentials already in project. Skill may access via aesop-api proxy or directly (TBD in build phase). Graceful degradation: if Pinecone unavailable, warn user but continue with web search + courses.html/courses-v2.html only.
3. **Explanation Style** — Short (1-2 sentences), cite sources implicitly.
4. **Claude Model** — Use Sonnet (not Haiku) for better research quality. Same model/token budget used for recommendations as for course generation.

### Scope of Changes

1. **New Research Module** — Queries Pinecone, parses courses.html/courses-v2.html, runs web search. Input: course concept. Output: research findings (audience, topic coverage, structure patterns).
2. **New Recommendation Generator** — Synthesizes research into answers for each planning question with 1-2 sentence reasoning per answer.
3. **Modified Planning Phase** — Present recommendations first, then ask for approval/modification.
4. **Minimal Change to Course Builder** — Accept researched/approved parameters and proceed as normal.

All research done via Claude (Sonnet) + Anthropic SDK. No separate API keys or credentials needed.

### Key Risk

**Primary concern:** Course development becomes incorrect or takes excessive time due to poor research/recommendations.

**Mitigations:**
- Recommendations must map cleanly to actual planning questions (no mismatch).
- Graceful degradation if Pinecone unavailable.
- Use Sonnet (better quality) for research synthesis.
- User can manually correct/override recommendations; design expects some manual review to be part of the workflow.

**Assumption to validate:** Claude's research (via web search + Pinecone + course registries) is accurate and relevant enough to accelerate course development without creating delays or content errors.

### Design Verdict

✅ **This design serves the persona.** You get research-backed recommendations upfront, reducing cold-start friction on planning questions. No architectural blockers. Graceful degradation if Pinecone is unavailable. Next step: outline phases and dependencies in Phase 2.

---

*Saved: 2026-05-20 Design Discussion locked. Ready for Outline Plan.*
