// Taxonomy parser — AESOP AI Academy
// Extracts course + skill data from courses-v2.html for the recommendation engine.
// Data is inlined here (single source: courses-v2.html COURSES + COVERAGE arrays).
// Update this file whenever courses-v2.html COURSES or COVERAGE changes.

// ── Course catalogue (from courses-v2.html COURSES array) ─────────────────

export const COURSE_CATALOGUE = [
  {
    id: 'ethics',
    name: 'AI Ethics & Decision Making',
    path: '/ai-academy/modules/v2/ai-ethics-decision-making/m1.html',
    difficulty: 'intermediate',
    modules: 8,
    description: 'Evaluate AI impacts across society, governance, and human rights. Build a governance framework from first principles.',
  },
  {
    id: 'building-with-ai',
    name: 'Building with AI',
    path: '/ai-academy/modules/v2/building-with-ai/m1.html',
    difficulty: 'intermediate',
    modules: 8,
    description: 'Move from prompting to building. Design and deploy AI-powered workflows, prompts, and integrations.',
  },
  {
    id: 'agents',
    name: 'Building AI Agents: Use Cases',
    path: '/ai-academy/modules/v2/building-ai-agents-use-cases/m1.html',
    difficulty: 'intermediate',
    modules: 8,
    description: 'Design, deploy, and govern AI agents. Explore real use cases from content creation to decision support.',
  },
  {
    id: 'leveraging-rag',
    name: 'Leveraging RAG for AI Development',
    path: '/ai-academy/modules/v2/leveraging-rag-ai-development/m1.html',
    difficulty: 'advanced',
    modules: 8,
    description: 'Build retrieval-augmented generation systems. Connect AI to your own data for grounded, accurate outputs.',
  },
  {
    id: 'building-agentic-pipelines',
    name: 'Building Agentic Pipelines',
    path: '/ai-academy/modules/v2/building-agentic-pipelines/m1.html',
    difficulty: 'advanced',
    modules: 8,
    description: 'Design automated multi-step AI pipelines. Handle routing, orchestration, and failure recovery at scale.',
  },
  {
    id: 'ai-command-center',
    name: 'Build a Command Center',
    path: '/ai-academy/modules/v2/ai-command-center/m1.html',
    difficulty: 'advanced',
    modules: 8,
    description: 'Architect a personal AI command center with skill routing, session logging, and governance controls.',
  },
  {
    id: 'brainstorming-with-ai',
    name: 'Better Brainstorming with AI',
    path: '/ai-academy/modules/v2/brainstorming-with-ai/m1.html',
    difficulty: 'beginner',
    modules: 8,
    description: 'Use AI to break anchoring bias, generate divergent ideas, and converge on stronger solutions.',
  },
];

// ── Interest-tag → course affinity map ────────────────────────────────────
// Each tag maps to an ordered list of course IDs (strongest fit first).
// Used by the mapper to score courses against a student's interest profile.

export const TAG_AFFINITY = {
  python:      ['building-with-ai', 'leveraging-rag', 'agents', 'building-agentic-pipelines', 'ai-command-center'],
  nlp:         ['leveraging-rag', 'building-with-ai', 'agents', 'ai-command-center'],
  vision:      ['agents', 'building-with-ai', 'leveraging-rag'],
  ethics:      ['ethics', 'building-with-ai', 'agents', 'building-agentic-pipelines'],
  robotics:    ['agents', 'building-agentic-pipelines', 'ai-command-center'],
  business:    ['building-with-ai', 'brainstorming-with-ai', 'agents', 'ethics'],
  creative:    ['brainstorming-with-ai', 'building-with-ai', 'agents'],
  data:        ['leveraging-rag', 'building-with-ai', 'building-agentic-pipelines'],
  security:    ['ethics', 'agents', 'building-agentic-pipelines', 'ai-command-center'],
  policy:      ['ethics', 'agents', 'building-with-ai'],
  automation:  ['building-agentic-pipelines', 'agents', 'ai-command-center', 'building-with-ai'],
  tools:       ['ai-command-center', 'building-with-ai', 'agents', 'building-agentic-pipelines'],
  careers:     ['building-with-ai', 'ethics', 'brainstorming-with-ai', 'agents'],
  society:     ['ethics', 'brainstorming-with-ai', 'building-with-ai'],
};

// ── Aptitude band → eligible difficulty levels ────────────────────────────
// Controls which difficulty tiers a learner can be recommended.

export const BAND_DIFFICULTY = {
  beginner:     ['beginner', 'intermediate'],
  aware:        ['beginner', 'intermediate'],
  intermediate: ['intermediate', 'advanced'],
  advanced:     ['intermediate', 'advanced'],
};

// ── Prerequisite map ──────────────────────────────────────────────────────
// If a course is recommended, name any prerequisite the student should know about.

export const PREREQUISITES = {
  'leveraging-rag':             ['building-with-ai'],
  'building-agentic-pipelines': ['agents', 'building-with-ai'],
  'ai-command-center':          ['agents', 'building-with-ai'],
};

// ── Lookup helpers ────────────────────────────────────────────────────────

/** Return the full course object for a given ID, or null. */
export function getCourse(id) {
  return COURSE_CATALOGUE.find(c => c.id === id) || null;
}

/** Return all courses matching a given difficulty tier. */
export function getCoursesByDifficulty(difficulty) {
  return COURSE_CATALOGUE.filter(c => c.difficulty === difficulty);
}
