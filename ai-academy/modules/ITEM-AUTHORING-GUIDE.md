# AESOP Academy Item Authoring Guide

**Version:** 1.0.0  
**Last Updated:** 2026-05-12  
**Purpose:** Quality standards for assessment item development in Phase 2

---

## 1. Quality Rubric (4-Point Scale)

Every item must pass review using this rubric. Average score must be ≥ 3.0; no criterion < 2.5.

### Criterion 1: Clarity (Question & Options Are Understandable)

| Score | Descriptor |
|-------|-----------|
| **4 - Exemplary** | Question is crystal clear, unambiguous; all options are distinct and easy to parse; no grammatical errors; language appropriate for target level |
| **3 - Proficient** | Question is clear with minimal re-reading; options distinct; minor grammatical issues that don't impede understanding |
| **2 - Developing** | Question somewhat ambiguous; requires re-reading to understand; some options unclear or hard to distinguish; grammatical errors present |
| **1 - Incomplete** | Question confusing or ambiguous; options poorly written or duplicate key ideas; significant grammatical/clarity issues |

**Checklist:**
- [ ] Single sentence per option (or very short); multi-line options must be necessary
- [ ] No double negatives ("Which is NOT...NOT true")
- [ ] Jargon defined or avoided
- [ ] Options parallel in structure and length (within 20% word count difference)
- [ ] No "all of the above" or "none of the above" options

---

### Criterion 2: Skill Alignment (Item Measures Intended Skill)

| Score | Descriptor |
|-------|-----------|
| **4 - Exemplary** | Item directly and clearly measures the stated skill; no unintended skills required; difficulty aligns with proficiency target |
| **3 - Proficient** | Item measures the stated skill; may require minor unintended skill (e.g., reading comprehension); appropriate difficulty |
| **2 - Developing** | Item partially measures the skill; significant unintended skill requirements; difficulty misaligned with target |
| **1 - Incomplete** | Item does not measure stated skill; measures different skill; inappropriate difficulty |

**Checklist:**
- [ ] Item requires the specific skill stated (not just general knowledge)
- [ ] Unintended skill requirements minimized (e.g., reading comprehension for a technical skill item)
- [ ] Difficulty matches proficiency target (Developing items easier than Proficient items)
- [ ] Item would be answered differently by experts vs. novices in the skill

---

### Criterion 3: Bloom's Taxonomy Level (Matches Target Cognitive Complexity)

| Score | Descriptor |
|-------|-----------|
| **4 - Exemplary** | Item clearly targets the stated Bloom's level; no lower-level items masquerading as higher (no trick questions); progression logical |
| **3 - Proficient** | Item primarily targets stated level; may touch adjacent levels; appropriate cognitive complexity |
| **2 - Developing** | Item targets stated level but also requires lower or higher; cognitive complexity misaligned |
| **1 - Incomplete** | Item targets wrong Bloom's level; cognitive complexity inappropriate |

**Checklist:**
- [ ] **Remember**: Asks for factual recall (define, list, identify)
- [ ] **Understand**: Asks for explanation or summary (explain, summarize, classify)
- [ ] **Apply**: Asks to use concept in new context (solve, demonstrate, interpret)
- [ ] **Analyze**: Asks to break down relationships (compare, distinguish, diagram)
- [ ] **Evaluate**: Asks to judge based on criteria (critique, appraise, defend)
- [ ] **Create**: Asks to generate new product (design, construct, develop)

**Examples by Level:**
- Remember: "Which of the following best defines machine learning?" (simple recall)
- Understand: "Why might a model trained on historical data show bias?" (requires explanation)
- Apply: "Given this dataset, which ML algorithm would you choose? Why?" (context-dependent choice)
- Analyze: "Compare supervised vs. unsupervised learning on these three dimensions..." (breakdown + comparison)
- Evaluate: "Which approach is better for this scenario? Defend your choice." (judgment with justification)
- Create: "Design an AI system to solve this real-world problem." (generate new solution)

---

### Criterion 4: Quality of Distractors (Wrong Options Are Plausible)

| Score | Descriptor |
|-------|-----------|
| **4 - Exemplary** | All 3 wrong options are plausible; based on common misconceptions; would appeal to students with incomplete understanding |
| **3 - Proficient** | Most wrong options plausible; some based on misconceptions; might eliminate 1 option easily |
| **2 - Developing** | Some wrong options implausible; weak misconception basis; students can guess from format |
| **1 - Incomplete** | Most/all wrong options obviously wrong; no misconception basis; trivial to eliminate; trick question |

**Checklist (for Multiple Choice Items):**
- [ ] Each wrong option targets a specific common misconception
- [ ] Wrong options are plausible to someone with incomplete understanding
- [ ] No "obviously wrong" options (e.g., "purple dinosaur")
- [ ] No trick questions (questions designed to deceive)
- [ ] No use of determiners like "always," "never," "all," "none" in wrong options (students learn to avoid these)
- [ ] Correct answer not systematically longer/shorter than distractors

**Common Misconceptions to Leverage:**
- For ML items: Confusing correlation with causation; thinking more data always helps
- For prompt engineering items: Assuming longer prompts are always better; not understanding temperature effects
- For ethics items: Focusing on intent rather than impact; not recognizing systemic bias
- For LLM items: Thinking models understand concepts vs. pattern-matching; confusing training data with test data

---

### Criterion 5: Accessibility (Item Inclusive & Non-Biased)

| Score | Descriptor |
|-------|-----------|
| **4 - Exemplary** | Item accessible to all learners regardless of background; unbiased scenarios; no jargon without definition; inclusive language |
| **3 - Proficient** | Generally accessible; minor jargon or scenario-specificity; mostly unbiased |
| **2 - Developing** | Some accessibility barriers; jargon present; biased scenarios or language; excludes some populations |
| **1 - Incomplete** | Significant accessibility barriers; assumes specific background; biased or exclusionary content |

**Checklist:**
- [ ] No stereotypes or biased scenarios (e.g., "nurse" = female, "CEO" = male)
- [ ] Scenarios inclusive (don't assume specific cultural context, ability, gender, etc.)
- [ ] Jargon either avoided or defined on first use
- [ ] Names in scenarios are diverse
- [ ] No idioms or cultural references without explanation
- [ ] Questions accessible to non-native English speakers (clear, direct language)
- [ ] Scenarios don't assume socioeconomic privilege (e.g., "your research team")
- [ ] Visual elements (if any) have alt-text describing

---

## 2. Bloom's Taxonomy Levels (With AI/Tech Examples)

### Remember (Lowest Cognitive Level)
**Goal:** Recall facts, definitions, terminology  
**Verbs:** Define, identify, list, recall, recognize, name, state

**Examples:**
- "What does LLM stand for?"
- "Which of the following is a type of bias in machine learning?"
- "Identify the correct definition of 'prompt engineering.'"

**Item Structure:** Straightforward factual question; correct answer is verifiable from course materials

---

### Understand (L2)
**Goal:** Explain ideas, interpret meaning, classify, summarize  
**Verbs:** Explain, summarize, interpret, classify, describe, discuss, compare

**Examples:**
- "Why might a model trained on 1990s data show gender bias when used in 2026?"
- "Which of these scenarios best illustrates the difference between supervised and unsupervised learning?"
- "What is the relationship between prompt clarity and model output quality?"

**Item Structure:** Requires student to explain **why** or make a connection; not just recall

---

### Apply (L3)
**Goal:** Use information in new situation, solve problems, demonstrate usage  
**Verbs:** Apply, use, solve, demonstrate, construct, modify, adapt

**Examples:**
- "Given this customer service problem, which AI approach would you apply? Why?"
- "Write a prompt that would help an LLM explain quantum computing to a 10-year-old."
- "You observe the model produces worse results for women. What would you do first?"

**Item Structure:** Presents a scenario or problem; asks student to apply a concept learned

---

### Analyze (L4)
**Goal:** Break down relationships, distinguish between parts, identify patterns  
**Verbs:** Analyze, compare, distinguish, differentiate, diagram, separate

**Examples:**
- "Compare the training data requirements for supervised vs. unsupervised learning. What are the trade-offs?"
- "In this case study, identify which biases are systemic vs. which are data-driven. Explain your reasoning."
- "Analyze why this prompt produces inconsistent outputs. What components could be improved?"

**Item Structure:** Requires breaking down complex ideas; comparison; analysis of trade-offs

---

### Evaluate (L5)
**Goal:** Make judgments based on criteria, defend positions, appraise quality  
**Verbs:** Evaluate, critique, defend, appraise, judge, justify, recommend

**Examples:**
- "Review this AI hiring system. Is it biased? What evidence would convince you?"
- "Recommend which algorithm to use for this problem, defending your choice against alternatives."
- "Evaluate this prompt engineering approach. What are its strengths and limitations?"

**Item Structure:** Asks student to make judgment and justify it; multiple defensible answers possible

---

### Create (L6, Highest)
**Goal:** Put elements together to form new product, design original solutions  
**Verbs:** Design, construct, create, develop, propose, invent, compose

**Examples:**
- "Design an AI system to detect and mitigate bias in hiring decisions. Describe your approach."
- "Create a multi-step prompt engineering strategy to improve model performance on complex reasoning."
- "Develop an assessment strategy to evaluate whether an AI system is safe to deploy."

**Item Structure:** Open-ended; asks student to create something new; significant cognitive demand

---

## 3. Skill-Specific Authoring Patterns

### Foundational Skills (understand-ai-basics, grasp-llm-behavior, recognize-ai-limitations)

**Pattern 1: Concept Identification**
```
Question: Which of the following best describes [concept]?
Options: 
- Correct answer (clear definition)
- Misconception 1 (common wrong understanding)
- Misconception 2 (different common error)
- Misconception 3 (plausible distractor)
```

**Pattern 2: Scenario Analysis**
```
Scenario: [Real or realistic situation involving the concept]
Question: What is happening in this scenario? / Why does this happen?
Options: [Possible explanations, one correct]
```

**Pattern 3: Limitation Recognition**
```
Scenario: [Student proposes or observes a model behavior]
Question: What limitation of AI models does this demonstrate?
Options: [Possible limitations - hallucination, bias, overfitting, etc.]
```

### Applied Skills (write-clear-prompts, design-multi-turn-conversations)

**Pattern 1: Prompt Comparison**
```
Question: Which of these prompts would produce better results? Why?
Option A: [Vague prompt]
Option B: [Clear, structured prompt]
Option C: [Overly complex prompt]
Option D: [Prompt that makes common error]
```

**Pattern 2: Iterative Refinement**
```
Initial Prompt: [Student's attempt or given example]
Model Response: [Shows problem/limitation]
Question: How would you refine this prompt to improve the output?
Options: [Different refinement approaches]
```

**Pattern 3: Conversation Design**
```
Goal: [Specific outcome for multi-turn conversation]
Question: What would be a good second turn to steer the conversation toward [goal]?
Options: [Different follow-up prompts]
```

### Conceptual Skills (understand-ai-ethics, identify-ai-bias)

**Pattern 1: Case Analysis**
```
Case Study: [Real or realistic ethical dilemma or bias scenario]
Question: What [ethical principle/bias type/fairness issue] is at play here?
Options: [Different ethical frameworks or bias types]
Ideal Feedback: [Explanation of why the scenario illustrates this concept]
```

**Pattern 2: Detection & Mitigation**
```
Scenario: [System showing bias or ethical issue]
Question: How would you detect/measure this bias?
Options: [Different analytical approaches - DIF, disaggregated metrics, etc.]
```

**Pattern 3: Framework Application**
```
Scenario: [Real situation]
Question: How would you apply [ethics framework/governance principle] to this situation?
Options: [Different applications or interpretations]
```

### Advanced Skills (design-ai-agents, implement-ai-workflows)

**Pattern 1: Design Challenge**
```
Problem: [Real-world challenge]
Question: Design an AI system/agent to solve this. Describe: [architecture, key decisions, trade-offs]
Rubric: [Point-based for design quality, feasibility, thoughtfulness about constraints]
```

**Pattern 2: Trade-Off Analysis**
```
Scenario: [Design choice with multiple valid options]
Question: Compare these two approaches. Which would you choose for [context]? Why?
Options: [Different design choices with trade-offs]
```

**Pattern 3: Implementation Evaluation**
```
Code/Design: [Example implementation or approach]
Question: What would you change about this design? What's missing?
Options/Rubric: [Points for identifying architectural issues, improvements, edge cases]
```

---

## 4. Item Review Checklist

**Before submitting for peer review, author should verify:**

### Clarity & Writing
- [ ] Question is grammatically correct and clear (no double negatives)
- [ ] All options are grammatically parallel in structure
- [ ] Options are similar in length (within 20% word count)
- [ ] No "all of the above" or "none of the above"
- [ ] No jargon without definition
- [ ] Sentence reads naturally (not stiff or awkward)

### Skill & Bloom's Alignment
- [ ] Item directly measures the stated skill (not just general knowledge)
- [ ] Unintended skill requirements are minimal
- [ ] Difficulty appropriate for target proficiency level
- [ ] Bloom's level clearly matches intent (Remember is recall, Apply shows application, etc.)

### Distractors (for MC Items)
- [ ] Each wrong option targets a plausible misconception
- [ ] No obviously wrong options
- [ ] Correct answer not systematically longer/shorter
- [ ] Correct answer is unambiguously correct (not "best of many")

### Accessibility & Inclusivity
- [ ] No stereotypes (gender, race, cultural, socioeconomic)
- [ ] Scenarios inclusive and don't assume specific background
- [ ] Language accessible (clear, direct, no unnecessary idioms)
- [ ] Names and examples diverse

### Feedback (for all items)
- [ ] Correct feedback explains **why** the right answer is right
- [ ] Incorrect feedback addresses common misconceptions
- [ ] Both feedbacks educational (not just "correct/wrong")

---

## 5. Item Difficulty & Discrimination

**Item Difficulty (p-value):**  
- p = proportion of pilot students who answered correctly
- Target range: 0.30-0.70 (items in this range discriminate well)
- p < 0.30 = too hard; p > 0.70 = too easy
- **Action**: If p outside range after pilot, revise or replace

**Item Discrimination (r):**  
- r = correlation between item score and total skill score
- Target: r ≥ 0.25 (item correlates with overall skill performance)
- r < 0.15 = item doesn't align with skill; needs revision
- **Action**: If r < 0.25 after pilot, investigate why and revise

**Cronbach's α (per skill):**  
- α = internal consistency for all items measuring a skill
- Target: α ≥ 0.75 (consistent measurement)
- If α < 0.75, items may not cohere; needs revision or replacement

---

## 6. Common Authoring Mistakes to Avoid

### Mistake 1: Unclear or Ambiguous Questions
❌ "What is true about AI?" (too broad, unclear what to evaluate)  
✅ "Which of the following is a limitation of transformer models?" (specific, clear)

### Mistake 2: Trick Questions
❌ "Which is NOT a reason for bias? (A) training data  (B) model architecture  (C) the color of the developer's shirt" (trick answer to eliminate)  
✅ "Which of these is a source of bias in AI systems? ..." (straightforward)

### Mistake 3: Obvious Correct Answer
❌ "What does LLM stand for? (A) Purple dinosaur (B) Large Language Model (C) Lunch Ladies Monthly (D) Lemon-Lime Marmalade"  
✅ "What does LLM stand for? (A) Linear Language Matrix (B) Large Language Model (C) Low-Level Markup (D) Lateral Learning Method"

### Mistake 4: Options of Vastly Different Lengths
❌ "Option A: yes" vs "Option B: A model can fail in surprising ways when the training data doesn't match the deployment context"  
✅ Keep all options within 20% word count of each other

### Mistake 5: Unintended Skill Requirements
❌ Asking about AI ethics using jargon-heavy explanations that require reading comprehension expert beyond the skill being measured  
✅ Use clear language; test the **skill** not reading/writing ability

### Mistake 6: Biased or Exclusionary Scenarios
❌ Scenario assuming students are from wealthy families or specific cultural backgrounds  
✅ Use generic, inclusive scenarios that don't assume privilege

### Mistake 7: Multiple Valid Answers
❌ "Which is the best AI algorithm?" (no universally best; multiple correct depending on context)  
✅ "Which algorithm would be most appropriate for this specific problem? Why?" (context-dependent with defensible answer)

---

## 7. Quality Assurance Process

**Step 1: Author Drafts (Solo)**
- Author writes item following this guide
- Author self-checks against review checklist

**Step 2: Peer Review (2 Reviewers)**
- Each reviewer independently rates on 5 criteria (1-4 scale)
- Reviewers add comments on specific issues
- Average score must be ≥ 3.0; no criterion < 2.5

**Step 3: Author Revision (if needed)**
- If average < 3.0, author discusses feedback with reviewers
- Author revises item addressing concerns
- Resubmit for 2nd round review

**Step 4: Final Approval**
- Once passing score achieved, item locked in item-bank.json
- Item ready for pilot deployment

---

## References

- Bloom, B. S., et al. (1956). *Taxonomy of educational objectives: The classification of educational goals*. David McKay Company.
- Anderson, L. W., & Krathwohl, D. R. (Eds.). (2001). *A taxonomy for learning, teaching, and assessing: A revision of Bloom's taxonomy of educational objectives*. Longman.
- Tavakol, M., & Dennick, R. (2011). Making sense of Cronbach's alpha. *International Journal of Medical Education*, 2, 53-55.
