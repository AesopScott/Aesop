// Taxonomy parser — AESOP AI Academy
// Course catalogue for the recommendation engine. Includes both v2 courses
// (modules/v2/) and a curated selection of live v1 elective courses.
// v1 URL pattern: /ai-academy/modules/electives-hub.html?course={id}
// v2 URL pattern: /ai-academy/modules/v2/{slug}/m1.html

const V1 = (id) => `/ai-academy/modules/electives-hub.html?course=${id}`;

// ── Course catalogue ──────────────────────────────────────────────────────

export const COURSE_CATALOGUE = [

  // ── V2 courses ────────────────────────────────────────────────────────
  {
    id: 'brainstorming-with-ai',
    name: 'Better Brainstorming with AI',
    path: '/ai-academy/modules/v2/brainstorming-with-ai/m1.html',
    difficulty: 'beginner',
    modules: 8,
    description: 'Use AI to break anchoring bias, generate divergent ideas, and converge on stronger solutions.',
  },
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

  // ── V1 beginner courses ───────────────────────────────────────────────
  {
    id: 'how-ai-actually-works',
    name: 'Inside the Machine: AI Unpacked',
    path: V1('how-ai-actually-works'),
    difficulty: 'beginner',
    modules: 6,
    description: 'Learn how AI systems actually work under the hood — without the hype.',
  },
  {
    id: 'ai-bias-and-fairness',
    name: 'Understanding AI Bias and Fairness',
    path: V1('ai-bias-and-fairness'),
    difficulty: 'beginner',
    modules: 4,
    description: 'Explore how AI systems develop bias and what fairness in AI really means.',
  },
  {
    id: 'gpt-vs-claude-vs-gemini',
    name: 'GPT vs. Claude vs. Gemini',
    path: V1('gpt-vs-claude-vs-gemini'),
    difficulty: 'beginner',
    modules: 8,
    description: 'Compare leading AI models to choose the right tool for your needs.',
  },
  {
    id: 'ai-and-the-future-of-work',
    name: 'AI and the Future of Work',
    path: V1('ai-and-the-future-of-work'),
    difficulty: 'beginner',
    modules: 8,
    description: 'Understand how AI is reshaping jobs, skills, and the modern workplace.',
  },
  {
    id: 'ai-and-creativity',
    name: 'AI & Creativity',
    path: V1('ai-and-creativity'),
    difficulty: 'beginner',
    modules: 8,
    description: 'Use AI as a creative partner for writing, art, music, and design.',
  },
  {
    id: 'build-ai-workflows-no-code',
    name: 'Build Powerful AI Without Coding',
    path: V1('build-ai-workflows-no-code'),
    difficulty: 'beginner',
    modules: 6,
    description: 'Build powerful AI workflows without writing a single line of code.',
  },

  // ── V1 intermediate courses ───────────────────────────────────────────
  {
    id: 'ai-ethics-v1',
    name: 'AI Ethics & Decision-Making',
    path: V1('ai-ethics'),
    difficulty: 'intermediate',
    modules: 8,
    description: 'Navigate the ethical dimensions of AI development and real-world deployment.',
  },
  {
    id: 'prompt-engineering-for-developers',
    name: 'Prompt Engineering for Developers',
    path: V1('prompt-engineering-for-developers'),
    difficulty: 'intermediate',
    modules: 8,
    description: 'Master advanced prompting techniques to get reliable, high-quality outputs from AI systems.',
  },
  {
    id: 'how-large-language-models-work',
    name: 'How Large Language Models Work',
    path: V1('how-large-language-models-work'),
    difficulty: 'intermediate',
    modules: 8,
    description: 'Deep dive into transformer architecture, training, and why LLMs behave the way they do.',
  },
  {
    id: 'ai-for-marketing-and-growth',
    name: 'AI for Marketing and Growth',
    path: V1('ai-for-marketing-and-growth'),
    difficulty: 'intermediate',
    modules: 8,
    description: 'Apply AI to marketing strategy, content creation, and measurable business growth.',
  },
  {
    id: 'building-ai-agents-i',
    name: 'Building AI Agents I — Use Cases',
    path: V1('building-ai-agents-i-use-cases'),
    difficulty: 'intermediate',
    modules: 8,
    description: 'Design and deploy AI agents for real-world use cases across domains.',
  },
  {
    id: 'ai-careers-and-research',
    name: 'AI Careers & Research',
    path: V1('ai-careers-and-research'),
    difficulty: 'intermediate',
    modules: 6,
    description: 'Navigate AI career paths, research opportunities, and what roles are actually hiring.',
  },
  {
    id: 'storytelling-with-ai',
    name: 'Storytelling with AI',
    path: V1('storytelling-with-ai'),
    difficulty: 'intermediate',
    modules: 8,
    description: 'Craft compelling narratives with AI as a collaborative creative partner.',
  },
  {
    id: 'ai-governance',
    name: 'AI Governance',
    path: V1('ai-governance'),
    difficulty: 'intermediate',
    modules: 9,
    description: 'Build frameworks for responsible AI governance in organizations and policy contexts.',
  },

  // ── V1 advanced courses ───────────────────────────────────────────────
  {
    id: 'applied-ai-development',
    name: 'Applied AI Development',
    path: V1('applied-ai-development'),
    difficulty: 'advanced',
    modules: 8,
    description: 'Build production-ready AI applications with modern frameworks, APIs, and deployment patterns.',
  },
  {
    id: 'rag-systems-from-scratch',
    name: 'RAG Systems from Scratch',
    path: V1('rag-systems-from-scratch'),
    difficulty: 'advanced',
    modules: 8,
    description: 'Build retrieval-augmented generation pipelines from the ground up.',
  },
  {
    id: 'ai-security-and-red-teaming',
    name: 'AI Security and Red-Teaming',
    path: V1('ai-security-and-red-teaming'),
    difficulty: 'advanced',
    modules: 8,
    description: 'Test and harden AI systems against prompt injection, jailbreaks, and adversarial attacks.',
  },
  {
    id: 'the-alignment-problem',
    name: 'The Alignment Problem',
    path: V1('the-alignment-problem'),
    difficulty: 'advanced',
    modules: 8,
    description: 'Examine AI alignment research, value learning, and the challenge of building safe AI.',
  },
  {
    id: 'building-an-ai-first-business',
    name: 'Building an AI-First Business',
    path: V1('building-an-ai-first-business'),
    difficulty: 'advanced',
    modules: 8,
    description: 'Launch and scale a business with AI at its core from strategy to execution.',
  },
  {
    id: 'deep-learning-for-builders',
    name: 'Deep Learning: Build Real Things',
    path: V1('deep-learning-for-builders'),
    difficulty: 'advanced',
    modules: 8,
    description: 'Build and train neural networks for real-world computer vision and NLP tasks.',
  },
  {
    id: 'pentesting-llm-applications',
    name: 'Pen Testing LLM Applications',
    path: V1('pentesting-llm-applications'),
    difficulty: 'advanced',
    modules: 8,
    description: 'Pen test LLM applications using the OWASP Top 10 for LLMs framework.',
  },
];

// ── Interest-tag → course affinity map ────────────────────────────────────
// Each tag maps to an ordered list of course IDs (strongest fit first).
// V2 courses appear first within each tier since they are the current curriculum.

export const TAG_AFFINITY = {
  python:      ['building-with-ai', 'applied-ai-development', 'leveraging-rag', 'agents', 'building-agentic-pipelines', 'ai-command-center', 'prompt-engineering-for-developers', 'deep-learning-for-builders', 'rag-systems-from-scratch'],
  nlp:         ['leveraging-rag', 'how-large-language-models-work', 'prompt-engineering-for-developers', 'building-with-ai', 'agents', 'ai-command-center', 'rag-systems-from-scratch', 'deep-learning-for-builders'],
  vision:      ['agents', 'building-with-ai', 'leveraging-rag', 'deep-learning-for-builders', 'applied-ai-development'],
  ethics:      ['ethics', 'ai-ethics-v1', 'ai-bias-and-fairness', 'the-alignment-problem', 'building-with-ai', 'agents', 'building-agentic-pipelines', 'ai-governance'],
  robotics:    ['agents', 'building-agentic-pipelines', 'ai-command-center', 'building-ai-agents-i', 'applied-ai-development'],
  business:    ['building-with-ai', 'ai-for-marketing-and-growth', 'building-an-ai-first-business', 'brainstorming-with-ai', 'build-ai-workflows-no-code', 'agents', 'ethics'],
  creative:    ['brainstorming-with-ai', 'ai-and-creativity', 'storytelling-with-ai', 'building-with-ai', 'agents'],
  data:        ['leveraging-rag', 'rag-systems-from-scratch', 'building-with-ai', 'building-agentic-pipelines', 'deep-learning-for-builders', 'applied-ai-development'],
  security:    ['ai-security-and-red-teaming', 'pentesting-llm-applications', 'ethics', 'agents', 'building-agentic-pipelines', 'ai-command-center'],
  policy:      ['ethics', 'ai-governance', 'the-alignment-problem', 'ai-ethics-v1', 'agents', 'building-with-ai'],
  automation:  ['building-agentic-pipelines', 'build-ai-workflows-no-code', 'agents', 'building-ai-agents-i', 'ai-command-center', 'building-with-ai'],
  tools:       ['gpt-vs-claude-vs-gemini', 'ai-command-center', 'building-with-ai', 'agents', 'build-ai-workflows-no-code', 'building-agentic-pipelines'],
  careers:     ['ai-and-the-future-of-work', 'ai-careers-and-research', 'building-with-ai', 'ethics', 'brainstorming-with-ai', 'agents'],
  society:     ['ethics', 'ai-bias-and-fairness', 'the-alignment-problem', 'ai-governance', 'brainstorming-with-ai', 'building-with-ai'],
};

// ── Aptitude band → eligible difficulty levels ────────────────────────────

export const BAND_DIFFICULTY = {
  beginner:     ['beginner', 'intermediate'],
  aware:        ['beginner', 'intermediate'],
  intermediate: ['intermediate', 'advanced'],
  advanced:     ['intermediate', 'advanced'],
};

// ── Prerequisite map ──────────────────────────────────────────────────────

export const PREREQUISITES = {
  'leveraging-rag':             ['building-with-ai'],
  'building-agentic-pipelines': ['agents', 'building-with-ai'],
  'ai-command-center':          ['agents', 'building-with-ai'],
  'rag-systems-from-scratch':   ['prompt-engineering-for-developers'],
  'pentesting-llm-applications':['ai-security-and-red-teaming'],
  'applied-ai-development':     ['prompt-engineering-for-developers'],
  'deep-learning-for-builders': ['how-large-language-models-work'],
};

// ── Lookup helpers ────────────────────────────────────────────────────────

export function getCourse(id) {
  return COURSE_CATALOGUE.find(c => c.id === id) || null;
}

export function getCoursesByDifficulty(difficulty) {
  return COURSE_CATALOGUE.filter(c => c.difficulty === difficulty);
}
