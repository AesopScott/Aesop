/**
 * placement-engine.js — Catalog-agnostic placement assessment engine.
 *
 * Generalized from theladder/ladder-app.js (the Concepts ladder), where the
 * placement engine currently lives inline and is hard-wired to LADDER_TIERS.
 * This module lifts that logic into a reusable engine that any pathway
 * (tiers, products, use cases) can drive by supplying a catalog descriptor.
 *
 * It preserves the exact completion-signal contract used by the Concepts
 * ladder so transcripts, prompts, and AI responses stay compatible:
 *
 *     <!--LADDER_PLACEMENT_COMPLETE:{...}-->
 *
 * ---------------------------------------------------------------------------
 * PUBLIC API
 * ---------------------------------------------------------------------------
 *
 * createPlacementEngine(descriptor) -> engine
 *   Build an engine bound to one catalog. `descriptor` shape:
 *
 *   {
 *     // REQUIRED. Flat list of placeable items (tiers / products / use cases).
 *     // Each item: { id, label, group, order, interestText, isCoreItem? }
 *     //   id           string  unique item id (e.g. "tier-01")
 *     //   label        string  human label
 *     //   group        string  grouping key (e.g. tier id); used by grouping
 *     //   order        number  order within its group (used by core selection)
 *     //   interestText string  text matched against interest tag keywords
 *     //   isCoreItem   bool?    optional override: always assign as a core item
 *     items: [...],
 *
 *     // OPTIONAL. Allowed interest tags. Defaults to DEFAULT_INTEREST_TAGS.
 *     interestTags: ['technical', 'business', ...],
 *
 *     // OPTIONAL. Map of tag -> array of keyword substrings used to match
 *     // an item's interestText. Defaults to DEFAULT_INTEREST_KEYWORDS.
 *     interestKeywords: { technical: ['api', 'json', ...], ... },
 *
 *     // REQUIRED. Grant rules. Given the three normalized scores, returns the
 *     // array of GROUP ids the learner places out of (tests out of).
 *     //   (scores: { capabilityScore, technicalScore, governanceScore }) => string[]
 *     grantRules: (scores) => [...groupIds],
 *
 *     // OPTIONAL. coreItemsPerGroup: how many low-order items per non-granted
 *     // group are auto-assigned as "core". Default 4. Items flagged
 *     // isCoreItem are always assigned regardless of this number.
 *     coreItemsPerGroup: 4,
 *
 *     // OPTIONAL. Assessment dimensions for the system prompt + opener.
 *     // See buildPlacementSystemPrompt for shape. Sensible AI-fluency
 *     // defaults are provided.
 *     assessment: { role, dimensions, ... },
 *
 *     // OPTIONAL. Minimum learner replies before a placement signal is honored.
 *     // Default 5. Matches the Concepts ladder gate.
 *     minLearnerTurns: 5,
 *
 *     // OPTIONAL. Max length of the AI reasoning string kept. Default 500.
 *     maxReasoningLength: 500
 *   }
 *
 * engine.PLACEMENT_REGEX
 *   The completion-signal RegExp (identical to the Concepts ladder).
 *
 * engine.buildSystemPrompt({ languageLabel })
 *   Returns the placement assessor system prompt, parameterized by catalog
 *   descriptor + preferred language label.
 *
 * engine.placementOpener()
 *   Returns the first assistant message that kicks off the assessment.
 *
 * engine.parsePlacementResponse(rawText)
 *   -> { placement, visibleText }
 *   Strips the marker from learner-facing text, parses + normalizes the JSON.
 *   `placement` is null when no marker / invalid JSON.
 *
 * engine.normalizePlacementSignals(raw)
 *   -> normalized placement object (scores clamped, tags filtered, granted +
 *   assigned ids resolved). The grant/assignment resolver.
 *
 * engine.resolveGrantedGroups(scores) -> string[]
 *   Thin wrapper over descriptor.grantRules with clamped scores.
 *
 * engine.resolveAssignedItemIds(grantedGroupIds, interestTags) -> string[]
 *   Item-assignment resolver: for every non-granted group, returns its core
 *   items plus interest-matched items.
 *
 * engine.shouldApplyPlacement(placement, learnerTurnCount) -> boolean
 *   True when there is a placement signal AND learnerTurnCount >= minLearnerTurns.
 *
 * engine.clampInt / engine.normalizeTags
 *   Exposed helpers (used internally; handy for callers/tests).
 *
 * ---------------------------------------------------------------------------
 * INVARIANT: the completion-signal contract is fixed. Do not change the marker
 * string or the JSON keys (capabilityScore, technicalScore, governanceScore,
 * interestTags, reasoning) without updating every pathway in lockstep.
 * ---------------------------------------------------------------------------
 */

export const PLACEMENT_REGEX = /<!--LADDER_PLACEMENT_COMPLETE:([\s\S]*?)-->/;

export const DEFAULT_INTEREST_TAGS = [
  'technical', 'business', 'governance', 'creative',
  'automation', 'research', 'security', 'data', 'strategy', 'education'
];

export const DEFAULT_INTEREST_KEYWORDS = {
  technical: ['api', 'json', 'structured', 'function', 'tool', 'rag', 'vector', 'agent', 'model', 'code', 'deployment'],
  business: ['business', 'workflow', 'marketing', 'sales', 'support', 'operations', 'strategy', 'roi'],
  governance: ['governance', 'law', 'ethics', 'policy', 'privacy', 'risk', 'compliance', 'copyright', 'bias'],
  creative: ['creative', 'image', 'video', 'audio', 'media', 'content', 'design', 'synthetic'],
  automation: ['automation', 'workflow', 'trigger', 'action', 'agent', 'tool', 'orchestration'],
  research: ['research', 'source', 'citation', 'fact', 'study', 'information', 'search'],
  security: ['security', 'prompt injection', 'red team', 'abuse', 'threat', 'privacy'],
  data: ['data', 'embedding', 'vector', 'retrieval', 'rag', 'search', 'metadata']
};

const DEFAULT_ASSESSMENT = {
  role: 'placement assessor',
  product: 'AESOP AI Academy',
  intro: 'Your job is to assess BOTH interest and capability, then decide what the learner can test out of and what they should be assigned.',
  exchangeGuidance: 'Run a 5-7 exchange assessment. Ask one question at a time. Be warm, direct, and practical.',
  dimensions: [
    'General AI fluency: vocabulary, limits, prompting, verification, everyday use.',
    'Technical depth: APIs, JSON, code, data, RAG, agents, evals, deployment.',
    'Governance depth: privacy, copyright, ethics, law, security, vendor risk, policy.',
    'Interests: what topics energize them enough to keep learning.',
    'Application context: what they want to be able to do after learning.'
  ],
  styleGuidance: 'Use light scenario questions, not trivia. Include at least one technical calibration question and one governance/risk question. Do not make beginners feel punished. If they are technical, increase depth.',
  redirectGuidance: 'Stay on assessment. If they go off topic, redirect to AI learning placement.',
  opener: 'Let us place you. I will assess both what you already know and what you actually care about learning. First: describe your current relationship with AI. What tools have you used, what have you built or tried, and what feels most interesting or useful to you?'
};

const VERIFIED_EVIDENCE = 'verified';

export function clampInt(value, min, max) {
  const n = parseInt(value, 10);
  if (Number.isNaN(n)) return min;
  return Math.min(Math.max(n, min), max);
}

export function normalizeTags(value, allowed = DEFAULT_INTEREST_TAGS, max = 5) {
  const allowedSet = new Set(allowed);
  const raw = Array.isArray(value) ? value : [];
  const tags = raw
    .map((tag) => String(tag).toLowerCase().trim())
    .filter((tag) => allowedSet.has(tag));
  return [...new Set(tags)].slice(0, max);
}

export function createPlacementEngine(descriptor = {}) {
  const items = Array.isArray(descriptor.items) ? descriptor.items : [];
  const interestTags = descriptor.interestTags || DEFAULT_INTEREST_TAGS;
  const interestKeywords = descriptor.interestKeywords || DEFAULT_INTEREST_KEYWORDS;
  const coreItemsPerGroup = Number.isFinite(descriptor.coreItemsPerGroup) ? descriptor.coreItemsPerGroup : 4;
  const minLearnerTurns = Number.isFinite(descriptor.minLearnerTurns) ? descriptor.minLearnerTurns : 5;
  const maxReasoningLength = Number.isFinite(descriptor.maxReasoningLength) ? descriptor.maxReasoningLength : 500;
  const assessment = { ...DEFAULT_ASSESSMENT, ...(descriptor.assessment || {}) };

  if (typeof descriptor.grantRules !== 'function') {
    throw new Error('createPlacementEngine: descriptor.grantRules must be a function (scores) => groupId[]');
  }
  const grantRules = descriptor.grantRules;

  function resolveGrantedGroups(scores) {
    const capabilityScore = clampInt(scores.capabilityScore ?? 0, 0, 100);
    const technicalScore = clampInt(scores.technicalScore ?? 0, 0, 100);
    const governanceScore = clampInt(scores.governanceScore ?? 0, 0, 100);
    const granted = grantRules({ capabilityScore, technicalScore, governanceScore });
    return Array.isArray(granted) ? granted : [];
  }

  function itemMatchesInterest(item, tags) {
    const haystack = String(item.interestText || item.label || '').toLowerCase();
    return tags.some((tag) => {
      const words = interestKeywords[tag] || [tag];
      return words.some((word) => haystack.includes(word));
    });
  }

  function isCoreItem(item) {
    if (item.isCoreItem === true) return true;
    const order = Number(item.order ?? Number.MAX_SAFE_INTEGER);
    return order <= coreItemsPerGroup;
  }

  function resolveAssignedItemIds(grantedGroupIds, tags) {
    const granted = new Set(grantedGroupIds);
    const assigned = [];
    items.forEach((item) => {
      if (granted.has(item.group)) return;
      const core = isCoreItem(item);
      const matched = itemMatchesInterest(item, tags);
      if ((core || matched) && !assigned.includes(item.id)) {
        assigned.push(item.id);
      }
    });
    return assigned;
  }

  function normalizePlacementSignals(raw = {}) {
    const capabilityScore = clampInt(raw.capabilityScore ?? raw.aptitudeScore ?? 0, 0, 100);
    const technicalScore = clampInt(raw.technicalScore ?? raw.technical_score ?? 0, 0, 100);
    const governanceScore = clampInt(raw.governanceScore ?? raw.governance_score ?? 0, 0, 100);
    const tags = normalizeTags(raw.interestTags ?? raw.interest_tags, interestTags);
    const grantedTierIds = resolveGrantedGroups({ capabilityScore, technicalScore, governanceScore });
    return {
      completedAt: new Date().toISOString(),
      capabilityScore,
      technicalScore,
      governanceScore,
      interestTags: tags,
      grantedTierIds,
      assignedTopicIds: resolveAssignedItemIds(grantedTierIds, tags),
      reasoning: String(raw.reasoning || '').slice(0, maxReasoningLength),
      evidence: VERIFIED_EVIDENCE
    };
  }

  function parsePlacementResponse(rawText) {
    const text = String(rawText || '');
    const visibleText = text.replace(PLACEMENT_REGEX, '').trim();
    const match = text.match(PLACEMENT_REGEX);
    if (!match) return { placement: null, visibleText };
    try {
      return { placement: normalizePlacementSignals(JSON.parse(match[1])), visibleText };
    } catch (error) {
      console.warn('Could not parse placement signal:', error);
      return { placement: null, visibleText };
    }
  }

  function buildSystemPrompt({ languageLabel = 'English' } = {}) {
    const dimensionLines = assessment.dimensions
      .map((dim, index) => `${index + 1}. ${dim}`)
      .join('\n');
    return `You are The ${assessment.product} ${assessment.role}.

${assessment.intro}

Preferred language: ${languageLabel}.

${assessment.exchangeGuidance}

Assess these dimensions:
${dimensionLines}

${assessment.styleGuidance}

Allowed interestTags:
${interestTags.join(', ')}

When you have enough signal after at least ${minLearnerTurns} learner replies:
1. Give a short visible summary.
2. Append this exact marker on a new line:
<!--LADDER_PLACEMENT_COMPLETE:{"capabilityScore":NN,"technicalScore":NN,"governanceScore":NN,"interestTags":["tag1","tag2"],"reasoning":"one concise sentence"}-->

Rules:
- Scores are integers 0-100.
- interestTags must use the allowed list.
- Do not mention the marker or JSON to the learner.
- ${assessment.redirectGuidance}`;
  }

  function placementOpener() {
    return assessment.opener;
  }

  function shouldApplyPlacement(placement, learnerTurnCount) {
    return Boolean(placement) && Number(learnerTurnCount) >= minLearnerTurns;
  }

  return {
    PLACEMENT_REGEX,
    descriptor: { items, interestTags, interestKeywords, coreItemsPerGroup, minLearnerTurns },
    buildSystemPrompt,
    placementOpener,
    parsePlacementResponse,
    normalizePlacementSignals,
    resolveGrantedGroups,
    resolveAssignedItemIds,
    shouldApplyPlacement,
    clampInt,
    normalizeTags: (value) => normalizeTags(value, interestTags)
  };
}
