# Expert Challenge: AI Orientation
## Leadership-Tier Certification Test

---

## Rubric Dimensions (Plain Language)

You'll be evaluated on:

1. **Conceptual accuracy** — Do you understand what AI is and is not, with precision?
2. **Vocabulary fluency** — Can you use technical terms (machine learning, generative, determinism, alignment) accurately?
3. **Applied judgment** — Can you apply AI/not-AI distinctions to real leadership decisions?
4. **Evidence quality** — Can you cite credible sources (research, standards, cases)?
5. **Reasoning defense** — Can you explain and defend your thinking under challenge?
6. **Risk awareness** — Can you identify limitations and where claims about AI break down?
7. **Standards alignment** — Does your reasoning map to NIST AI RMF, EU AI Act, WEF?

---

## Phase 1: Diagnostic Question

**What is the single most important distinction between what AI is and what it is not?**

Use at least two of these terms correctly in your answer:
- Machine learning
- Rule-based logic
- Determinism
- Statistical inference

Show your thinking. Don't worry about perfection—I'm listening for whether you can separate hype from engineering.

---

## Phase 1: Clarification Challenge

Here's the tension:

**Rule-based system** typically means:
- Explicit IF-THEN rules written by humans
- Deterministic (same input → same output, always)
- Transparent logic you can audit

**Neural network** (which powers GPT, DALL-E, etc.):
- Learns patterns from data, not from hand-coded rules
- Probabilistic (same input → different outputs possible)
- "Black box"—weights are opaque

**My questions for you:**

1. When a large language model uses tokens to predict the next word, is it really operating on **rule-based logic**, or is it operating on **learned statistical patterns** (weights, attention, matrix operations) that behave like rules but aren't explicitly written by humans?

2. What's the meaningful difference, and why does it matter for a leader to know which one it is?

3. You correctly identified that AI is not a simple database lookup. But you also said "rule-based logic." Can something be both **not a database AND not actually rule-based**? What would that be called instead?

---

## Phase 2: Vocabulary + Edge Case

**A financial services firm deploys a rule-based credit scoring system that was trained on historical lending data using logistic regression (a statistical model). It makes decisions via explicit thresholds: "If credit score > 650 AND income > $50K, approve."**

1. Is this AI? Why or why not?

2. Does it matter whether the threshold numbers were hand-coded or learned from data?

3. What's your reasoning?

---

## Phase 2: Follow-Up Challenge

**My questions:**

1. Is it **more like traditional AI** (learned patterns) or **more like a database lookup** (deterministic, auditable)?

2. More important for a CRO: What does the EU AI Act care about—the learning method, or the explainability and auditability of the decision?

3. Where would you place this system, and why?

---

## Phase 2: Deeper Probe

**My questions:**

1. Predicting the "next word in a sequence" is a mathematical calculation of likelihood. An LLM computes: P(word_n | word_1, word_2, ... word_n-1). That's a probability distribution over the vocabulary. "Proximity" and "likelihood" are the same thing mathematically. **So what's the real difference you're trying to name?**

2. On the EU AI Act point: Here's the edge case: An LLM can be repeatable (set temperature=0) and traceable (log the prompt + tokens). **Does that make it compliant with the EU AI Act's definition of "AI system"?**

3. Or does the Act care about something else—like **high-risk use cases** (hiring, lending, criminal justice) regardless of whether the system is an LLM or logistic regression? **What's your reading?**

---

## Phase 3: Risk & Limitation

**Name one misconception that leaders commonly have about AI that your reasoning just corrected.**

And:

**What would change your mind about whether an LLM could be used for financial scoring?** (What evidence or technical advance would shift your position?)

---

## Phase 3: Constraint

**Here's your constraint: Pick the misconception that, if a leader believed it, would most directly lead them to make a bad decision about whether and how to deploy AI in their organization.**

In other words: **Which false belief is most dangerous?**

Once you name it, explain:
1. What leaders wrongly believe
2. Why it's false (use what you've learned)
3. What bad decision it leads to

---

## Phase 3: Defense Challenge

**Question 1: The Risk**

An organization deploys an AI writing tool to 500 customer service reps with no baseline measurement and minimal training. After 2 weeks, management claims "productivity is up."

**What specific organizational or governance risk has this created?** (Use NIST AI RMF language if you can: governance, risk, monitoring, traceability.)

---

**Question 2: The Evidence**

You're the CRO advising the board on a $5M AI workforce rollout. 

**What two specific, measurable data points must you collect before you commit that money? And why does each one matter to the decision?**

(Example format: "We need [measurement], because without it, we cannot [specific decision consequence].")

---

**Question 3: The Week 1 Trap**

A team shows 40% output gain in the first week of AI tool use. 

**Why is this not reliable evidence for long-term productivity impact?** (Hint: Think about learning curves, selection effects, context shift, or measurement validity.)

---

## Phase 3: Standards & Evidence Challenge

**My questions:**

1. Are you willing to go find **one peer-reviewed study** on psychological/cultural impact of AI in the workforce, read it, and tell me what it actually says (not what AI summarized)?

2. **Explain why** NIST and the EU Act prioritize governance before cultural assessment—and whether that's wrong or whether there's a reason they sequenced it that way?

Or should we proceed with what we have and I'll give you an honest pass/fail based on current evidence?

---

## Final Assessment Question

**Here's the edge case:**

A leader wants to measure psychological and cultural impact before and after AI deployment. But unlike "lines of code" or "CRM entries," these are **qualitative and subjective** (stress, autonomy, job satisfaction).

1. **How do you measure and audit the unmeasurable?**

2. **What happens if your "before" measurement shows AI adoption will cause psychological harm—do you not deploy it? Or do you deploy it anyway and mitigate?**

This is where your framework meets real governance tradeoffs.

**What's your answer?**
