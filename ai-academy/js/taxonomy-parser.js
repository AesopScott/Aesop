// Taxonomy parser — AESOP AI Academy
// Imports the full 130-course catalogue and exports tag-affinity, aptitude-band
// rules, prerequisites, and lookup helpers used by taxonomy-mapper.js.
// Course data lives in taxonomy-catalogue.js (kept separate to stay under 800 lines).

export { COURSE_CATALOGUE, getCourse, getCoursesByDifficulty } from './taxonomy-catalogue.js';

// ── Interest-tag → course affinity map ────────────────────────────────────────
// Each tag maps to an ordered list of course IDs, strongest fit first.
// V2 courses are listed first within each relevance tier.

export const TAG_AFFINITY = {

  // Developer / Python / API / coding
  python: [
    'building-with-ai', 'applied-ai-development', 'leveraging-rag', 'agents',
    'building-agentic-pipelines', 'ai-command-center', 'project-scaffolding',
    'prompt-engineering-for-developers', 'deep-learning-for-builders',
    'rag-systems-from-scratch', 'working-with-the-anthropic-api',
    'deploying-and-monitoring-ai', 'evaluation-and-testing-for-ai',
    'building-ai-agents-iii-tools', 'building-ai-agents-iv-openclaw',
    'building-ai-agents-v-optimization', 'building-agents-vertex-ai',
    'vertex-ai-data-agents', 'claude-code', 'ai-code-review-fundamentals',
    'security-auditing-ai-generated-code', 'code-audit-workflows-team-standards',
  ],

  // Language models, prompting, transformers, text AI
  nlp: [
    'leveraging-rag', 'how-large-language-models-work', 'prompt-engineering-for-developers',
    'building-with-ai', 'agents', 'ai-command-center', 'project-scaffolding',
    'rag-systems-from-scratch', 'deep-learning-for-builders',
    'working-with-the-anthropic-api', 'the-context-window-race',
    'the-reasoning-revolution', 'conversational-ai-chatbots',
    'voice-and-real-time-ai', 'synthetic-data-and-self-improvement',
    'prompt-engineering-that-works', 'claude-cowork', 'claude-code',
    'whats-really-inside-ai', 'how-machines-learn', 'the-alignment-problem',
  ],

  // Image, visual AI, computer vision
  vision: [
    'image-generation-models', 'photography-and-ai', 'ai-for-graphic-design',
    'computer-vision-in-daily-life', 'real-or-rendered', 'spot-the-fake-ai-content',
    'deepfakes-and-synthetic-media', 'ai-lens-on-the-world',
    'deep-learning-for-builders', 'agents', 'building-with-ai',
    'ai-and-creativity', 'make-it-yours-creating-with-ai', 'creating-with-ai-tools',
    'ai-and-architecture', 'ai-in-game-design-i', 'ai-in-gaming-and-interactive-media',
  ],

  // AI ethics, bias, fairness, moral reasoning
  ethics: [
    'ethics', 'ai-ethics', 'ai-bias-and-fairness', 'coded-unfair-ai-bias-exposed',
    'ai-ethics-foundations', 'the-alignment-problem', 'ai-alignment-for-everyone',
    'ai-safety-and-alignment', 'ai-safety-and-alignment-basics', 'ai-safety-for-everyone',
    'ai-hype-critical-thinking', 'what-ai-knows-about-you', 'is-the-robot-being-fair',
    'ai-and-fake-information', 'ai-misinformation', 'deepfakes-and-synthetic-media',
    'human-ai-interaction', 'digital-citizenship-and-ai', 'truth-detectives-ai-and-fake-info',
    'ai-and-media', 'ai-governance', 'is-ai-telling-you-the-truth', 'ai-in-society',
    'ai-agent-safety-when-things-go-wrong',
  ],

  // Autonomous systems, robots, agentic AI
  robotics: [
    'agents', 'building-agentic-pipelines', 'ai-command-center', 'ai-autonomous-systems',
    'ai-agents-in-the-wild', 'building-ai-agents-i-use-cases',
    'building-ai-agents-ii-skills', 'building-ai-agents-iii-tools',
    'building-ai-agents-iv-openclaw', 'building-ai-agents-v-optimization',
    'ai-agent-risk-and-oversight', 'ai-agent-safety-when-things-go-wrong',
    'pentesting-ai-agents', 'building-agents-vertex-ai', 'vertex-ai-data-agents',
    'building-with-ai', 'how-large-language-models-work',
  ],

  // Business, marketing, entrepreneurship, professional tools
  business: [
    'building-with-ai', 'ai-for-marketing-and-growth', 'building-an-ai-first-business',
    'brainstorming-with-ai', 'build-ai-workflows-no-code', 'agents', 'ethics',
    'ai-tools-for-solo-founders', 'ai-for-product-development',
    'ai-risk-for-business-leaders', 'ai-for-small-business-managers',
    'ai-for-small-business-owners', 'agile-ai-side-projects',
    'funding-and-pitching-ai-ventures', 'ai-leadership', 'ai-for-job-hunting',
    'ai-side-hustle-money', 'claude-cowork', 'ai-work-and-automation-realities',
    'project-scaffolding', 'ai-for-small-business-managers',
  ],

  // Art, writing, design, storytelling, creative expression
  creative: [
    'brainstorming-with-ai', 'ai-and-creativity', 'storytelling-with-ai',
    'ai-and-the-writer-s-voice', 'photography-and-ai', 'performing-arts-and-ai',
    'ai-for-graphic-design', 'ai-in-game-design-i', 'ai-and-your-creative-work',
    'make-it-yours-creating-with-ai', 'creating-with-ai-tools',
    'ai-in-gaming-and-interactive-media', 'building-with-ai', 'agents',
    'ai-and-architecture', 'image-generation-models', 'talking-to-ai-prompt-writing',
    'robot-speak-talk-to-ai', 'wispr-flow', 'ai-and-fake-information',
  ],

  // Data science, ML, evaluation, benchmarks, analytics
  data: [
    'leveraging-rag', 'rag-systems-from-scratch', 'building-with-ai',
    'building-agentic-pipelines', 'deep-learning-for-builders', 'applied-ai-development',
    'model-evaluation-and-benchmarks', 'evaluation-and-testing-for-ai',
    'vertex-ai-data-agents', 'the-hardware-race', 'synthetic-data-and-self-improvement',
    'whats-really-inside-ai', 'how-machines-learn', 'explainable-ai',
    'ai-in-science', 'how-large-language-models-work', 'the-reasoning-revolution',
    'building-agents-vertex-ai',
  ],

  // Security, red-teaming, pentesting, adversarial AI
  security: [
    'ai-security-and-red-teaming', 'pentesting-llm-applications', 'pentesting-ai-agents',
    'ai-augmented-reconnaissance', 'ai-network-pentesting',
    'security-auditing-ai-generated-code', 'code-audit-workflows-team-standards',
    'ai-code-review-fundamentals', 'ethics', 'agents', 'building-agentic-pipelines',
    'ai-command-center', 'ai-agent-risk-and-oversight',
    'ai-agent-safety-when-things-go-wrong', 'what-ai-knows-about-you',
    'evaluation-and-testing-for-ai', 'deepfakes-and-synthetic-media',
  ],

  // Governance, regulation, legal, public policy
  policy: [
    'ethics', 'ai-governance', 'ai-governance-regulation', 'the-alignment-problem',
    'ai-ethics', 'ai-in-society', 'ai-safety-and-alignment', 'ai-safety-for-everyone',
    'ai-safety-and-alignment-basics', 'agents', 'building-with-ai',
    'ai-and-national-security', 'ai-alignment-for-everyone', 'ai-agent-risk-and-oversight',
    'human-ai-interaction', 'ai-ethics-foundations', 'ai-in-healthcare',
    'ai-and-education', 'ai-and-finance', 'ai-and-media', 'ai-consciousness-and-philosophy',
  ],

  // Workflows, automation, no-code, pipelines, productivity
  automation: [
    'building-agentic-pipelines', 'build-ai-workflows-no-code', 'agents',
    'building-ai-agents-i-use-cases', 'building-ai-agents-ii-skills',
    'building-ai-agents-iii-tools', 'building-ai-agents-iv-openclaw',
    'building-ai-agents-v-optimization', 'ai-command-center', 'building-with-ai',
    'vertex-ai-data-agents', 'building-agents-vertex-ai', 'agile-ai-side-projects',
    'ai-work-and-automation-realities', 'ai-work-and-automation-deep-dive',
    'project-scaffolding', 'claude-cowork',
  ],

  // Specific AI tools, model comparisons, productivity apps
  tools: [
    'gpt-vs-claude-vs-gemini', 'ai-command-center', 'building-with-ai', 'agents',
    'build-ai-workflows-no-code', 'building-agentic-pipelines', 'claude-ai-chat',
    'claude-cowork', 'claude-code', 'wispr-flow', 'running-models-locally',
    'pick-the-right-ai-tool', 'gemini-for-college-life', 'prompt-engineering-that-works',
    'model-evaluation-and-benchmarks', 'project-scaffolding',
    'ai-tools-for-solo-founders', 'ai-tools-for-real-teaching', 'voice-and-real-time-ai',
    'conversational-ai-chatbots', 'how-ai-actually-works',
  ],

  // Jobs, career development, future of work
  careers: [
    'ai-and-the-future-of-work', 'ai-careers-and-research', 'building-with-ai',
    'ethics', 'brainstorming-with-ai', 'agents', 'ai-for-job-hunting',
    'ai-job-market-impact', 'ai-work-and-automation-realities',
    'ai-work-and-automation-deep-dive', 'ai-side-hustle-money', 'future-of-work-ai',
    'ai-for-product-development', 'agile-ai-side-projects',
    'ai-for-small-business-managers', 'ai-for-marketing-and-growth',
    'funding-and-pitching-ai-ventures', 'ai-leadership',
  ],

  // Social impact, education, healthcare, environment, society
  society: [
    'ethics', 'ai-bias-and-fairness', 'the-alignment-problem', 'ai-governance',
    'brainstorming-with-ai', 'building-with-ai', 'ai-in-society', 'ai-and-education',
    'ai-in-healthcare', 'ai-and-climate', 'ai-and-media', 'ai-social-media',
    'ai-psychology-and-behavior', 'ai-and-finance', 'ai-in-science',
    'ai-consciousness-and-philosophy', 'the-future-of-intelligence',
    'ai-and-national-security', 'human-ai-interaction', 'ai-and-the-future-of-work',
    'digital-citizenship-and-ai', 'ai-tools-for-real-teaching', 'ai-tutor-under-the-hood',
    'how-ai-tutors-work', 'ai-alignment-for-everyone', 'what-s-coming-next',
  ],
};

// ── Aptitude band → eligible difficulty levels ────────────────────────────────
// Beginners can stretch into intermediate; advanced learners stay at intermediate+.

export const BAND_DIFFICULTY = {
  beginner:     ['beginner', 'intermediate'],
  aware:        ['beginner', 'intermediate'],
  intermediate: ['intermediate', 'advanced'],
  advanced:     ['intermediate', 'advanced'],
};

// ── Prerequisite map ──────────────────────────────────────────────────────────

export const PREREQUISITES = {
  'leveraging-rag':                    ['building-with-ai'],
  'building-agentic-pipelines':        ['agents', 'building-with-ai'],
  'ai-command-center':                 ['agents', 'building-with-ai'],
  'rag-systems-from-scratch':          ['prompt-engineering-for-developers'],
  'pentesting-llm-applications':       ['ai-security-and-red-teaming'],
  'pentesting-ai-agents':              ['ai-security-and-red-teaming'],
  'applied-ai-development':            ['prompt-engineering-for-developers'],
  'deep-learning-for-builders':        ['how-large-language-models-work'],
  'building-ai-agents-ii-skills':      ['building-ai-agents-i-use-cases'],
  'building-ai-agents-iii-tools':      ['building-ai-agents-ii-skills'],
  'building-ai-agents-iv-openclaw':    ['building-ai-agents-iii-tools'],
  'building-ai-agents-v-optimization': ['building-ai-agents-iv-openclaw'],
  'building-agents-vertex-ai':         ['building-ai-agents-i-use-cases'],
  'vertex-ai-data-agents':             ['building-with-ai'],
  'deploying-and-monitoring-ai':       ['building-with-ai'],
  'evaluation-and-testing-for-ai':     ['building-with-ai'],
  'working-with-the-anthropic-api':    ['prompt-engineering-for-developers'],
  'code-audit-workflows-team-standards':['ai-code-review-fundamentals'],
  'security-auditing-ai-generated-code':['ai-security-and-red-teaming'],
};
