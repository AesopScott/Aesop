# Curriculum Alignment Logic

## Problem
Exams test what learners learned. Learners learn from courses. Courses teach vocabulary. Currently: no connection between these three systems.

## Solution: Three-Layer Architecture

### Layer 1: Course as Source of Truth
```
Course
├── Tier ID (T01, T02, etc)
├── Chapters (topics covered)
│   ├── Chapter ID
│   ├── Title
│   ├── Learning Objectives
│   ├── Key Points
│   └── Vocabulary Terms (whitelist)
├── Assessment Rubric (what matters)
└── Out-of-Scope (what's NOT taught)
```

**Rule:** Every word in an exam question must either be:
- In a chapter's vocabulary whitelist, OR
- Common language (the, a, is, what, etc.)

### Layer 2: Examiner as Course-Grounded

Examiner receives:
```
Examiner Input {
  tierID: "T01",
  certificationLevel: "Leadership",
  courseContent: LoadCourse(tierID),
  constraints: {
    vocabulary: courseContent.allVocabulary(),
    outOfScope: courseContent.outOfScope(),
    rubricDimensions: courseContent.rubric
  }
}
```

**Logic:** Examiner system prompt is dynamically built:
```
You are examining learners on: {course.title}

VOCABULARY YOU MAY TEST ON:
{course.vocabulary.join(", ")}

TOPICS YOU MUST COVER:
{course.chapters.map(c => c.title).join("\n")}

LEARNING OBJECTIVES:
{course.rubric.dimensions.join("\n")}

DO NOT TEST ON:
{course.outOfScope.join(", ")}

VALIDATE AGAINST:
- Key points from each chapter
- Learning objectives
- Real-world application
```

### Layer 3: Validation as Course-Referenced

When learner answers, validator checks:

```
ValidateCertification(attempt) {
  course = LoadCourse(attempt.tierID)
  
  For each examiner question:
    - Does it use only whitelisted vocabulary? ✓
    - Does it address a chapter topic? ✓
    - Does it align with rubric? ✓
  
  For each learner answer:
    - Does it demonstrate understanding of that chapter? ✓
    - Does it use correct vocabulary? ✓
    - Does it show reasoning grounded in course content? ✓
  
  If ANY question or answer fails validation:
    return FAIL (exam was not properly grounded)
  
  If learner demonstrates mastery of rubric dimensions:
    return PASS (certified)
}
```

## Data Flow

```
1. Learner selects Tier 1 → Leadership certification
   
2. System loads: tierCourseContent.T01
   
3. Examiner receives:
   - Course chapters and vocabulary
   - Rubric dimensions to test
   - Out-of-scope boundaries
   
4. Examiner generates questions grounded in course content
   CONSTRAINT: Every question tests something taught in a chapter
   
5. Learner answers questions
   
6. Validator checks:
   - Did examiner stay within course scope? ✓
   - Does learner understand course material? ✓
   - Did learner demonstrate rubric mastery? ✓
   
7. If all pass: CERTIFY
   If any fail: REJECT with specific reason
```

## Vocab Validation Logic

```javascript
function validateVocabulary(examQuestion, courseVocabulary) {
  const COMMON_WORDS = [
    'the', 'a', 'an', 'is', 'are', 'be', 'what', 'why', 'how',
    'and', 'or', 'but', 'in', 'on', 'at', 'to', 'from', 'for',
    'can', 'would', 'could', 'should', 'do', 'does', 'did',
    'you', 'your', 'they', 'them', 'their', 'we', 'our'
  ]
  
  const words = examQuestion.toLowerCase().split(/\s+/)
  
  for (word of words) {
    if (COMMON_WORDS.includes(word)) continue
    if (courseVocabulary.includes(word)) continue
    
    // Word found that's not in course vocab and not common
    return {
      valid: false,
      error: `"${word}" not in ${course.tier} vocabulary`,
      addToVocab: word  // Flag for curriculum review
    }
  }
  
  return { valid: true }
}
```

## Course Loading Logic

```javascript
function LoadCourse(tierID) {
  const course = tierCourseContent[tierID]
  if (!course) throw new Error(`Tier ${tierID} not found`)
  
  return {
    id: course.id,
    title: course.title,
    chapters: course.chapters,
    
    // Derived properties
    allVocabulary: () => 
      course.chapters.flatMap(c => c.vocabulary),
    
    allTopics: () =>
      course.chapters.map(c => c.title),
    
    allLearningObjectives: () =>
      course.chapters.flatMap(c => c.learningObjectives),
    
    rubric: course.assessmentRubric,
    
    outOfScope: () => {
      // Implicitly: everything not in this tier
      // Get all vocab from all OTHER tiers
      const allTiers = Object.keys(tierCourseContent)
      const otherVocab = allTiers
        .filter(t => t !== tierID)
        .flatMap(t => tierCourseContent[t].chapters)
        .flatMap(c => c.vocabulary)
      
      return otherVocab
    }
  }
}
```

## Examiner System Prompt Generator

```javascript
function buildExaminerPrompt(tier, certLevel) {
  const course = LoadCourse(tier)
  
  return `
You are certifying learners on: ${course.title}
Certification Level: ${certLevel}

LEARNERS HAVE STUDIED THESE TOPICS:
${course.chapters.map(c => `- ${c.title}: ${c.description}`).join('\n')}

VOCABULARY YOU MAY TEST ON (and only these words):
${course.allVocabulary().sort().join(', ')}

YOUR EXAM MUST ADDRESS THESE LEARNING OBJECTIVES:
${course.allLearningObjectives().map(obj => `- ${obj}`).join('\n')}

YOUR ASSESSMENT RUBRIC:
${Object.entries(course.rubric).map(([key, val]) => `- ${val}`).join('\n')}

DO NOT TEST ON:
${course.outOfScope().slice(0, 20).join(', ')} [and other advanced topics]

VALIDATION RULES:
1. Every question must test something from the chapters above
2. Every question must use only whitelisted vocabulary
3. Every learner answer must show understanding of taught material
4. If learner uses vocabulary not taught, that's a red flag (hallucination or guessing)
5. Leadership certification requires judgment, not just definition recall
  `
}
```

## Validation Logic

```javascript
function validateCertification(attempt, examQuestions, learnerAnswers) {
  const course = LoadCourse(attempt.tierID)
  
  // Step 1: Validate exam itself
  for (let question of examQuestions) {
    const vocabCheck = validateVocabulary(question, course.allVocabulary())
    if (!vocabCheck.valid) {
      return {
        valid: false,
        reason: `Exam question uses out-of-scope vocabulary: ${vocabCheck.error}`,
        type: 'EXAM_OUT_OF_SCOPE'
      }
    }
    
    const topicCheck = questionAddressesCourseContent(question, course)
    if (!topicCheck.valid) {
      return {
        valid: false,
        reason: `Exam question doesn't address course content`,
        type: 'EXAM_NOT_GROUNDED'
      }
    }
  }
  
  // Step 2: Validate learner understanding
  for (let i = 0; i < learnerAnswers.length; i++) {
    const answer = learnerAnswers[i]
    const question = examQuestions[i]
    
    const understanding = assessUnderstanding(
      answer,
      question,
      course.chapters
    )
    
    if (understanding.score < 0.7) {
      return {
        valid: false,
        reason: `Insufficient understanding of course material on question ${i+1}`,
        type: 'INSUFFICIENT_UNDERSTANDING',
        detail: understanding.gaps
      }
    }
  }
  
  // Step 3: Check rubric mastery
  const rubricScore = scoreAgainstRubric(
    learnerAnswers,
    course.rubric,
    attempt.certLevel
  )
  
  if (rubricScore < 0.75) {
    return {
      valid: false,
      reason: `Did not demonstrate rubric mastery (${rubricScore}%)`,
      type: 'RUBRIC_FAILURE'
    }
  }
  
  return {
    valid: true,
    score: rubricScore,
    certLevel: attempt.certLevel
  }
}
```

## The Invariant

**No learner can be certified on content they were not taught.**

This is enforced by:
1. Examiner can only ask about course vocabulary
2. Validator checks questions are course-grounded
3. Validator checks answers demonstrate course understanding
4. No side-channel knowledge is credited

## Integration Points

### In ladder-app.js:
```javascript
const courseContent = LoadCourse(state.evaluationContext.ladderTierId)
const examinerPrompt = buildExaminerPrompt(
  state.evaluationContext.ladderTierId,
  state.evaluationContext.certificationTierLabel
)
// Pass courseContent + examinerPrompt to callGuide()
```

### In certification-engine.js:
```javascript
function recordCertificationResult(result) {
  const courseContent = LoadCourse(context.ladderTierId)
  
  const validation = validateCertification(
    context,
    context.examQuestions,
    context.learnerAnswers,
    courseContent  // NEW: course context
  )
  
  if (!validation.valid) {
    return { status: 'failed', reason: validation.reason }
  }
  
  // ... rest of certification logic
}
```

## Summary: The Logic Loop

1. **Courses define what's taught** (vocabulary, topics, objectives)
2. **Exams test what's taught** (grounded in course content, vocabulary-constrained)
3. **Validation ensures coherence** (no out-of-scope testing, answers demonstrate understanding)
4. **Certification is a promise** (learner understands what the course covers)

This is a system, not a collection of rules.
