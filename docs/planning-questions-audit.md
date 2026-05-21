# Planning Questions Audit

Maps each planning question in the `/aesop-course-builder` Stage 1 interview to its corresponding research recommendation. Ensures 1:1 coverage — every question the skill asks has a research-backed answer ready before the user is prompted.

---

## Question-to-Recommendation Map

| # | Planning Question | Recommendation Key | Source |
|---|---|----|---|
| 1 | Target audience (who should take this course?) | `target_audience` | `audienceGaps` from registry + web search |
| 2 | Core topics (what are the 3–5 main topics?) | `core_topics` | `topicCoverage` from registry + web search |
| 3 | Module structure (8 modules? Format?) | `module_structure` | `structuralPatterns.averageModulesPerCourse` from registry |
| 4 | Assessment approach (debate, skill, build labs?) | `assessment_approach` | `structuralPatterns.assessmentApproaches` from registry |
| 5 | Prerequisites (what skills should students have?) | `prerequisites` | `prerequisites` from registry + web search |

**Coverage:** 5 of 5 planning questions have corresponding recommendations. ✓

---

## Questions NOT Covered by Research (Manual — Always Asked)

These require Scott's intent and cannot be inferred from corpus data:

| Question | Reason Not Researchable |
|---|---|
| Course title / slug | Brand decision, not data-driven |
| One-sentence catalog description | Marketing copy, requires author voice |
| Core problem statement (what learners can't do → will do) | Pedagogical intent, author decision |
| Governance standards focus (EU AI Act, NIST, etc.) | Compliance / curriculum alignment decision |
| Specific real-world scenarios or industries | Domain specificity, author knowledge |

---

## Recommendation Confidence Levels

| Key | Confidence | Notes |
|---|---|---|
| `target_audience` | High when web search available; Medium on registry-only | Corpus gap analysis is reliable; demand signals need web search |
| `core_topics` | Medium | Registry shows what exists, not what's missing globally |
| `module_structure` | High | Registry average is reliable (all v2 courses are 8 modules) |
| `assessment_approach` | High | Aesop v2 format is standardized (2 Debate / 3 Skill / 3 Build) |
| `prerequisites` | Medium | Inferred from audience complexity; web search improves this |

---

## Fallback Behavior

When the Claude API is unavailable, all 5 recommendations fall back to registry-derived values. The `researchBacked` flag is set to `false` and displayed to the user as a warning. Scott may still approve, modify, or reject any recommendation.

---

**Last updated:** 2026-05-20  
**Maintained by:** Task #1 — course development engine research feature
