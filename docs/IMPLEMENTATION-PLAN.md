# Curriculum Alignment Implementation Plan

## Goal
Implement the curriculum alignment system so that courses, exams, and vocabulary are tightly coupled. No learner can be certified on content they were not taught.

## Critical Path (Shortest sequence to working system)

### PHASE 1: Foundation (Prepare data structures)
**Goal:** Get course data into the system and loadable

#### 1.1 - Expand tier course content (Tiers 4-12)
**Files:** `docs/tier-course-content.js`
- Complete Tiers 4-12 with chapters, vocabulary, learning objectives
- Map all existing vocabulary from `ladder-data.js` to tiers
- Identify any unmapped vocabulary
- **Owner:** You (domain knowledge of curriculum)
- **Effort:** 4-6 hours
- **Blocks:** Everything else
- **Done when:** All 12 tiers have chapters, vocab, objectives, rubrics

#### 1.2 - Validate course content against ladder-data.js vocabulary
**Files:** `theladder/ladder-data.js`, `docs/tier-course-content.js`
- Verify every vocabulary term in `ladder-data.js` appears in a tier chapter
- Verify no tier chapter uses vocabulary not in ladder-data
- Identify gaps or mismatches
- **Owner:** Me (script to validate)
- **Effort:** 1 hour
- **Blocks:** Nothing (checks against 1.1)
- **Done when:** No warnings, all vocab mapped

### PHASE 2: System Integration (Wire courses into examiner)
**Goal:** Examiner reads course content and uses it to generate questions

#### 2.1 - Load course content in ladder-app.js
**Files:** `theladder/ladder-app.js`
- Import `tier-course-content.js`
- Create `LoadCourse(tierID)` function
- Store course in `state.evaluationContext` when exam starts
- **Owner:** Me
- **Effort:** 30 mins
- **Blocks:** 2.2, 2.3
- **Done when:** `callGuide()` receives courseContent parameter

#### 2.2 - Build dynamic examiner system prompt from course
**Files:** `theladder/ladder-app.js`
- Create `buildExaminerPrompt(tierID, certLevel)` function
- Include course chapters, vocabulary, rubric
- Include out-of-scope topics to avoid
- Pass to examiner in system prompt
- **Owner:** Me
- **Effort:** 45 mins
- **Blocks:** 2.3
- **Done when:** Examiner receives course-grounded prompt

#### 2.3 - Test examiner with course-grounded prompt
**Files:** `theladder/ladder-app.js`, test session
- Run Tier 1 exam with new dynamic prompt
- Verify examiner uses only Tier 1 vocabulary
- Verify examiner references course chapters
- Verify exam questions address learning objectives
- **Owner:** You (test & feedback)
- **Effort:** 30 mins
- **Blocks:** 3.1
- **Done when:** Examiner questions are clearly grounded in course

### PHASE 3: Validation (Ensure exam and answers match course)
**Goal:** Validator checks that both exam and learner understanding are course-aligned

#### 3.1 - Add vocabulary validation to certification validator
**Files:** `theladder-shared/certification-engine.js`
- Implement `validateVocabulary(text, courseVocab)` function
- Check every significant word in exam question is in course vocab
- Check every significant word in learner answer is in course vocab
- Flag any out-of-scope words
- **Owner:** Me
- **Effort:** 1 hour
- **Blocks:** 3.2, 3.3
- **Done when:** Vocab validation works and reports violations

#### 3.2 - Add course grounding validation
**Files:** `theladder-shared/certification-engine.js`
- Implement `questionAddressesCourseContent(question, course)` function
- Check that question addresses at least one chapter topic
- Check that question relates to a learning objective
- Flag questions that don't connect to course content
- **Owner:** Me
- **Effort:** 1.5 hours
- **Blocks:** 3.3
- **Done when:** Validator rejects out-of-scope exam questions

#### 3.3 - Add answer validation against course content
**Files:** `theladder-shared/certification-engine.js`
- Implement `assessUnderstanding(answer, question, courseChapters)` function
- Check that learner demonstrates understanding of taught material
- Score against learning objectives, not generic knowledge
- Flag answers that show memorization without understanding
- **Owner:** Me
- **Effort:** 2 hours
- **Blocks:** 3.4
- **Done when:** Validator assesses understanding, not just knowledge

#### 3.4 - Integrate validation into certification result
**Files:** `theladder-shared/certification-engine.js`, `theladder/ladder-app.js`
- Update `recordCertificationResult()` to call full validation suite
- If exam out of scope: return FAIL with reason
- If answer shows insufficient understanding: return FAIL with reason
- If passes all checks: CERTIFY with rubric score
- **Owner:** Me
- **Effort:** 1 hour
- **Blocks:** 4.1
- **Done when:** Certification has three validation gates

### PHASE 4: Testing & Iteration (Verify system works)
**Goal:** System enforces curriculum alignment; exams are grounded; learners are certified fairly

#### 4.1 - Test Tier 1 certification end-to-end
**Files:** All integration
- Create test user
- Load Tier 1 course content
- Run exam with new course-grounded prompt
- Verify examiner asks only Tier 1 questions
- Answer questions
- Verify validator checks answers against Tier 1 content
- Verify certification succeeds if appropriate
- **Owner:** You (test & iterate)
- **Effort:** 1 hour
- **Blocks:** 4.2
- **Done when:** E2E test passes for Tier 1

#### 4.2 - Test out-of-scope rejection
**Files:** All integration, deliberate test case
- Create test where examiner tries to ask Tier 10 question
- Verify validator catches it and rejects
- Create test where learner gives answer beyond Tier 1 scope
- Verify validator flags it
- **Owner:** Me (set up), You (verify behavior)
- **Effort:** 45 mins
- **Blocks:** 4.3
- **Done when:** System rejects out-of-scope content

#### 4.3 - Test Tier 2-3 exams
**Files:** `docs/tier-course-content.js`, integration
- Run exam for Tier 2 (Prompting Mastery)
- Verify uses Tier 2 vocabulary only
- Run exam for Tier 3 (Research & Verification)
- Verify uses Tier 3 vocabulary only
- **Owner:** You (test), Me (fix issues)
- **Effort:** 1.5 hours
- **Blocks:** 4.4
- **Done when:** Tiers 1-3 all work correctly

#### 4.4 - Document exam behavior
**Files:** `docs/` folder
- Document what makes Tier 1 / 2 / 3 exams different
- Document vocabulary boundaries
- Document what learners should expect
- **Owner:** Me (draft), You (review)
- **Effort:** 1 hour
- **Blocks:** 5.1
- **Done when:** Clear documentation of system behavior

### PHASE 5: Scale (Extend to all tiers)
**Goal:** System works for all 12 tiers

#### 5.1 - Complete all tier course content
**Files:** `docs/tier-course-content.js`
- Finish Tiers 4-12 if not done in Phase 1
- Validate all tiers against vocabulary
- **Owner:** You
- **Effort:** 8-10 hours
- **Blocks:** 5.2
- **Done when:** All tiers complete

#### 5.2 - Test one tier from middle (Tier 6-7)
**Files:** Integration
- Run full exam flow for a middle tier
- Verify course content loads correctly
- Verify examiner is grounded
- Verify validator works
- Fix any bugs
- **Owner:** Me (implementation), You (test)
- **Effort:** 2 hours
- **Blocks:** 5.3
- **Done when:** Middle tiers work

#### 5.3 - Test one tier from end (Tier 11-12)
**Files:** Integration
- Run full exam flow for an advanced tier
- Same verification as 5.2
- **Owner:** Me (implementation), You (test)
- **Effort:** 1.5 hours
- **Blocks:** 5.4
- **Done when:** Advanced tiers work

#### 5.4 - Full system validation
**Files:** All
- Create test matrix: all tiers × all cert levels
- Run sampling of tests
- Fix any remaining issues
- **Owner:** Me (run tests), You (validate results)
- **Effort:** 2 hours
- **Blocks:** Done
- **Done when:** System stable across all tiers

## Timeline

| Phase | Tasks | Effort | Owner | Duration |
|-------|-------|--------|-------|----------|
| 1 | Content expansion + validation | 5-7 hours | You + Me | 1-2 days |
| 2 | System integration | 2 hours | Me | 0.5 day |
| 3 | Validation logic | 5.5 hours | Me | 1 day |
| 4 | Testing & iteration | 4 hours | You + Me | 1 day |
| 5 | Scale to all tiers | 13-15 hours | You + Me | 2-3 days |
| **Total** | | **30 hours** | | **5-7 days** |

## Dependencies & Blockers

```
Phase 1.1 (Tier content)
    ↓
Phase 1.2 (Validation) ──→ Phase 2.1 (Load)
                             ↓
                          Phase 2.2 (Prompt)
                             ↓
                          Phase 2.3 (Test) ──→ Phase 3.1 (Vocab validation)
                                                 ↓
                                              Phase 3.2 (Grounding)
                                                 ↓
                                              Phase 3.3 (Understanding)
                                                 ↓
                                              Phase 3.4 (Integrate)
                                                 ↓
                                              Phase 4.1 (E2E test)
                                                 ↓
                                              Phase 4.2 (Rejection test)
                                                 ↓
                                              Phase 4.3 (Tier 2-3)
                                                 ↓
                                              Phase 4.4 (Documentation)
                                                 ↓
                                              Phase 5.1 (Complete content)
                                                 ↓
                                              Phase 5.2-5.4 (Scale)
```

## Success Criteria

**Phase 1:** ✓ All 12 tiers have chapters, vocabulary, learning objectives
**Phase 2:** ✓ Examiner receives course-grounded system prompt
**Phase 3:** ✓ Validator has three gates (vocab, grounding, understanding)
**Phase 4:** ✓ Tier 1-3 certification works end-to-end without bugs
**Phase 5:** ✓ All 12 tiers work; system scales properly

## Key Assumptions

1. You will provide Tier 4-12 course content (chapters, vocab, objectives)
2. Learner data can be updated/re-run for testing
3. Course content can be loaded at runtime (not compiled)
4. Validator has access to original course material when checking answers

## Risks

| Risk | Impact | Mitigation |
|------|--------|-----------|
| Tier content incomplete | Blocks scale | Phase 1.1 is explicit deliverable |
| Examiner ignores grounding | Undermines system | Phase 2.3 catches with testing |
| Validator too strict | Rejects fair answers | Phase 4 iteration tunes thresholds |
| Performance impact | Slow exams | Cache course content, lazy-load |

## Next Steps

**Start with:** Phase 1.1
- You: Complete Tier 4-12 course content
- Me: Create validation script to check it
- Proceed to Phase 2 once content is solid

**First code change:** Phase 2.1
- Load course content in ladder-app.js
- Wire it through to examiner

Ready?
