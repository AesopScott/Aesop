// =============================================================================
// theladder-use-cases/use-cases-ladder.js
// Wiring layer between the Use-Cases catalog and the shared Ladder engines.
//
// This module is the Use-Cases analogue of theladder-products/products-ladder.js
// and theladder/concepts-ladder.js. It builds the descriptors/blueprints the
// shared engines need so a unified app can swap Concepts / Products / Use-Cases
// providers interchangeably. Like the other two providers, it imports NOTHING
// from the engines itself — the app owns engine construction — it only produces
// plain data the engines consume. The placement, certification, and catalog
// logic is lifted from the inline provider code in use-cases-app.js.
//
//   buildUseCasePlacementDescriptor(useCases, topicRanges) -> descriptor
//       Turns the flat use-case catalog into createPlacementEngine items + the
//       three-score grant rules adapted to *applied work-pattern fluency*. Item
//       ids are the bare String(useCase.id) namespace used by use-cases-app.js.
//
//   buildUseCaseBlueprint({ item, level, depth }) -> examiner blueprint
//       Per (use case, certification depth) examiner blueprint for
//       createCertificationEngine().buildExaminerSystemPrompt.
//
//   buildUseCaseCertContext({ item, depth, learnerId }) -> certification context
//       The context object recordCertificationResult / buildEvidencePacket need.
//
//   USE_CASE_CATALOG_URL / USE_CASE_TOPIC_RANGES / parseUseCaseCatalog(markdown)
//       The catalog config + parser lifted verbatim from use-cases-app.js so the
//       provider is self-contained (column schema id|name|topic|outcome|depth).
//
//   USE_CASE_IDENTITY_LEVELS — the three ACTIVE identity-assurance levels a
//       learner may resolve to before a use-case certification (doc-16):
//       self_attested, account_bound, identity_attested. proctored_verified is
//       intentionally absent — it is scaffolded, not active. This standardizes
//       Use-Cases onto the Products identity contract for the unified app, even
//       though the live use-cases-app uses use-cases-identity.js.
//
//   buildUseCaseIdentityAssurance(earnedAt, gate) -> identity-assurance record
//       Full doc-16-shaped identity-assurance record built from the learner's
//       pre-certification gate selection. Populated at gate time, stored into
//       the certification context, the credential record, and the evidence
//       packet (so the data-layer credential row carries the honest level).
//
//   CERT_DEPTHS — the three use-case certification depths (Certification /
//       Expert / Master) with doc-16 depth fields.
//
//   Plus helpers mirroring products-ladder.js: USE_CASE_INTEREST_KEYWORDS,
//   depthForLabel, identityLevelById, resolveUseCaseIdentityLevel.
// =============================================================================

// ---------------------------------------------------------------------------
// CATALOG CONFIG — lifted from use-cases-app.js so the provider is standalone.
// ---------------------------------------------------------------------------

export const USE_CASE_CATALOG_URL = '/docs/theladder-use-cases-catalog.md?v=1';

export const USE_CASE_TOPIC_RANGES = [
  { label: 'All use cases', start: 1, end: 300 },
  { label: 'Personal productivity + planning', start: 1, end: 15 },
  { label: 'Writing + communication', start: 16, end: 30 },
  { label: 'Research + knowledge work', start: 31, end: 45 },
  { label: 'Education + training', start: 46, end: 60 },
  { label: 'Software development', start: 61, end: 75 },
  { label: 'IT operations + cybersecurity', start: 76, end: 90 },
  { label: 'Data, BI + analytics', start: 91, end: 105 },
  { label: 'Marketing + content', start: 106, end: 120 },
  { label: 'Sales + revenue operations', start: 121, end: 135 },
  { label: 'Customer service + support', start: 136, end: 150 },
  { label: 'HR + people operations', start: 151, end: 165 },
  { label: 'Finance + accounting', start: 166, end: 180 },
  { label: 'Legal, risk + compliance', start: 181, end: 195 },
  { label: 'Healthcare + life sciences', start: 196, end: 210 },
  { label: 'Operations + supply chain', start: 211, end: 225 },
  { label: 'Manufacturing + field service', start: 226, end: 240 },
  { label: 'Retail + ecommerce', start: 241, end: 255 },
  { label: 'Creative, media + design', start: 256, end: 270 },
  { label: 'Government, nonprofit + public services', start: 271, end: 285 },
  { label: 'Strategy, leadership + governance', start: 286, end: 300 }
];

/**
 * Parse the Use-Cases catalog markdown into items. Lifted verbatim (in logic)
 * from use-cases-app.js parseCatalog. Reads pipe-table rows whose first cell is
 * a number; column schema is id | name | topic | outcome | depth.
 */
export function parseUseCaseCatalog(markdown) {
  return String(markdown || '')
    .split('\n')
    .filter((line) => /^\|\s*\d+\s*\|/.test(line))
    .map((line) => {
      const cells = line.split('|').slice(1, -1).map((cell) => cell.trim());
      return {
        id: Number(cells[0]),
        name: cells[1],
        topic: cells[2],
        outcome: cells[3],
        depth: cells[4]
      };
    })
    .filter((useCase) => Number.isFinite(useCase.id) && useCase.name);
}

// ---------------------------------------------------------------------------
// PLACEMENT — adapting the 3-score model to applied work-pattern fluency.
//
// The shared placement engine speaks in three normalized scores. The Concepts
// ladder reads them as general AI fluency / technical depth / governance depth.
// For the Use-Cases pathway we re-interpret the SAME three slots as work-pattern
// fluency, because what matters here is whether a learner already PERFORMS AI
// work in a topic — not abstract concept knowledge:
//
//   capabilityScore  -> APPLIES: does the learner already apply AI to real work
//                       tasks in this area (drafts, plans, analyses, support,
//                       decisions)? High = they live the use cases.
//   technicalScore   -> TOOLING/AUTOMATION DEPTH: comfort wiring tools, APIs,
//                       agents, data pipelines, and automations around the work.
//   governanceScore  -> RESPONSIBLE/CRITICAL JUDGMENT: verification, privacy,
//                       risk, policy, and the critical thinking to know when
//                       NOT to trust the output.
//
// grantRules returns the GROUP ids (topic labels) the learner places out of.
// Topics NOT granted get their core use cases (low order in range) plus any
// interest-matched use cases assigned. The thresholds below reproduce the
// Use-Cases grant logic from use-cases-app.js buildPlacementEngine.grantRules.
// ---------------------------------------------------------------------------

const PLACEMENT_GRANT_STRONG = 78;   // grant most topics
const PLACEMENT_GRANT_TECH = 72;     // technical/automation-heavy topics
const PLACEMENT_GRANT_GOV = 72;      // governance/judgment-heavy topics

// Topic groups whose use cases lean technical / automation-heavy.
const TECH_HEAVY_GROUPS = new Set([
  'Software development',
  'IT operations + cybersecurity',
  'Data, BI + analytics'
]);
// Topic groups whose use cases lean governance / critical-judgment-heavy.
const GOVERNANCE_HEAVY_GROUPS = new Set([
  'Legal, risk + compliance',
  'Healthcare + life sciences',
  'Government, nonprofit + public services',
  'Strategy, leadership + governance'
]);

// Interest keyword map tuned for the Use-Cases pathway (work-task language).
// Restated here so the descriptor is self-contained like the Products one.
export const USE_CASE_INTEREST_KEYWORDS = {
  technical: ['api', 'sdk', 'json', 'structured', 'function', 'tool', 'rag', 'vector', 'agent', 'model', 'code', 'coding', 'pipeline', 'deployment', 'integration'],
  business: ['business', 'workflow', 'marketing', 'sales', 'support', 'operations', 'crm', 'roi', 'enterprise', 'process', 'revenue'],
  governance: ['governance', 'law', 'legal', 'ethics', 'policy', 'privacy', 'risk', 'compliance', 'regulated', 'clinical', 'finance', 'security', 'audit'],
  creative: ['creative', 'image', 'video', 'audio', 'music', 'voice', 'media', 'content', 'design', 'slides', 'synthetic'],
  automation: ['automation', 'workflow', 'trigger', 'action', 'agent', 'orchestration', 'rpa', 'pipeline'],
  research: ['research', 'source', 'citation', 'fact', 'study', 'information', 'search', 'analysis', 'analytics'],
  security: ['security', 'prompt injection', 'red team', 'abuse', 'threat', 'privacy', 'incident', 'observability'],
  data: ['data', 'embedding', 'vector', 'retrieval', 'rag', 'search', 'metadata', 'analytics', 'bi', 'warehouse']
};

function topicForId(id, topicRanges) {
  const topic = topicRanges.find((range) => (
    range.label !== 'All use cases' && id >= range.start && id <= range.end
  ));
  return topic ? topic.label : 'Unassigned';
}

function topicStartForId(id, topicRanges) {
  const topic = topicRanges.find((range) => (
    range.label !== 'All use cases' && id >= range.start && id <= range.end
  ));
  return topic ? topic.start : id;
}

/**
 * Build a createPlacementEngine descriptor from the use-case catalog.
 * Items use the topic/category label as `group`, and order within the topic so
 * the lowest-numbered use cases in each non-granted topic are auto-assigned
 * core. Item id namespace = bare String(useCase.id) (matches use-cases-app.js).
 *
 * @param {Array} useCases    parsed catalog items ({ id, name, topic, outcome, depth })
 * @param {Array} topicRanges the topic-range table (defaults to USE_CASE_TOPIC_RANGES)
 */
export function buildUseCasePlacementDescriptor(useCases, topicRanges = USE_CASE_TOPIC_RANGES) {
  const items = (useCases || []).map((useCase) => {
    const group = useCase.topic || topicForId(useCase.id, topicRanges);
    return {
      id: String(useCase.id),
      label: useCase.name,
      group,
      // order within the topic block; core items are the first few per topic.
      order: useCase.id - topicStartForId(useCase.id, topicRanges) + 1,
      interestText: `${useCase.name} ${useCase.topic} ${useCase.outcome}`
    };
  });

  return {
    items,
    interestKeywords: USE_CASE_INTEREST_KEYWORDS,
    coreItemsPerGroup: 4,
    minLearnerTurns: 5,
    grantRules({ capabilityScore, technicalScore, governanceScore }) {
      const granted = new Set();
      const groups = [...new Set(items.map((item) => item.group))];
      groups.forEach((group) => {
        // Strong general applied fluency grants out of most topics.
        if (capabilityScore >= PLACEMENT_GRANT_STRONG) {
          granted.add(group);
          return;
        }
        // Technical/automation-heavy topics need both applied fluency AND
        // tooling depth to test out.
        if (TECH_HEAVY_GROUPS.has(group)
          && technicalScore >= PLACEMENT_GRANT_TECH
          && capabilityScore >= PLACEMENT_GRANT_TECH) {
          granted.add(group);
          return;
        }
        // Governance/judgment-heavy topics need responsible-judgment depth AND
        // applied fluency to test out.
        if (GOVERNANCE_HEAVY_GROUPS.has(group)
          && governanceScore >= PLACEMENT_GRANT_GOV
          && capabilityScore >= PLACEMENT_GRANT_GOV) {
          granted.add(group);
        }
      });
      return [...granted];
    },
    assessment: {
      product: 'AESOP AI Academy Use Cases',
      role: 'use-case placement assessor',
      intro: 'Your job is to assess how the learner already applies AI to real work, how deep their tooling/automation is, and how strong their responsible-use judgment is — then decide which use-case topics they can test out of and which specific use cases to assign.',
      exchangeGuidance: 'Run a 5-7 exchange assessment. Ask one question at a time. Be warm, direct, and practical. Focus on the work they actually do.',
      dimensions: [
        'Applied work fluency (capabilityScore): does the learner already apply AI to real tasks — drafting, planning, analysis, support, decisions?',
        'Tooling and automation depth (technicalScore): comfort wiring tools, APIs, agents, data pipelines, and automations around the work.',
        'Responsible and critical judgment (governanceScore): verification habits, privacy, risk, policy, and knowing when NOT to trust AI output.',
        'Interests: which work areas energize them enough to keep learning.',
        'Application context: what work outcomes they want to be able to perform after learning.'
      ],
      styleGuidance: 'Use realistic work scenarios, not trivia. Ask at least one automation/tooling question and one risk/judgment question. Do not punish beginners. If they clearly do advanced work, press deeper.',
      redirectGuidance: 'Stay on placement for AI use-case training. If they go off topic, redirect.',
      opener: 'Let us place you across the use-case catalog. Tell me about the AI work you already do: what tasks do you use AI for at work or school, which tools, and where do you most want to get stronger?'
    }
  };
}

// ---------------------------------------------------------------------------
// CERTIFICATION — three use-case depths reusing the doc-16 depth fields.
// Mapped from use-cases-app.js certificationOptions (id/label/summary/outcome/
// evidence/passingStandard/review) into the products-ladder.js depth shape.
// ---------------------------------------------------------------------------

export const CERT_DEPTHS = [
  {
    id: 'certification',
    label: 'Certification',
    certificationTierLabel: 'Use Case Certification',
    outcome: 'certification path evidence',
    evidence: 'clear competency evidence for the selected use case at the certification tier',
    passingStandard: 'solid rubric performance with no critical failures',
    review: 'AI-assessed, auditable, and challengeable'
  },
  {
    id: 'expert-challenge',
    label: 'Expert certification',
    certificationTierLabel: 'Use Case Expert Certification',
    outcome: 'expert-level evidence for advanced credit',
    evidence: 'strong transfer, edge-case reasoning, and defensible tradeoff analysis',
    passingStandard: 'high rubric performance, independent reasoning, and confident defense under challenge',
    review: 'AI-assessed with human review recommended for public or employment claims'
  },
  {
    id: 'mastery-challenge',
    label: 'Master certification',
    certificationTierLabel: 'Use Case Master Certification',
    outcome: 'mastery evidence and portfolio-quality artifact',
    evidence: 'original synthesis, portfolio-grade artifact, standards mapping, and leadership-level defense',
    passingStandard: 'near-expert rubric performance across all dimensions with no unresolved evidence gaps',
    review: 'AI-assessed with human or panel review recommended before external credential claims'
  }
];

export function depthForLabel(label) {
  return CERT_DEPTHS.find((depth) => depth.label === label) || CERT_DEPTHS[0];
}

/**
 * Examiner blueprint for buildExaminerSystemPrompt(blueprint).
 * `level` is the course level the learner studied (Beginner/Intermediate/...),
 * used only to flavor the item label; the depth drives examiner rigor.
 */
export function buildUseCaseBlueprint({ item, level, depth }) {
  const itemLabel = item.name;
  return {
    itemLabel,
    educationTierLabel: level ? `${level} use-case course` : 'Use-case course',
    certificationTierLabel: depth.certificationTierLabel,
    standards: 'O*NET, WEF, NIST AI RMF',
    depthLabel: depth.label,
    depthOutcome: depth.outcome,
    depthEvidence: depth.evidence,
    depthPassingStandard: depth.passingStandard,
    depthReview: depth.review,
    languageLabel: 'English'
  };
}

/**
 * Context object for recordCertificationResult / buildEvidencePacket.
 * Field names follow what certification-engine.js reads (itemId/itemLabel,
 * testDepth*, certificationTier*, blueprintId, standards, attemptId). Matches
 * concepts-ladder.js buildConceptsCertContext field-for-field.
 */
export function buildUseCaseCertContext({ item, depth, learnerId }) {
  const attemptId = `usecasecert_${item.id}_${depth.id}_${Date.now()}`;
  return {
    attemptId,
    pathway: 'use-case',
    learnerId: learnerId || '',
    itemId: item.id,
    itemLabel: item.name,
    certificationTierId: depth.id,
    certificationTierLabel: depth.certificationTierLabel,
    standards: 'O*NET, WEF, NIST AI RMF',
    testDepthId: depth.id,
    testDepthLabel: depth.label,
    testDepthOutcome: depth.outcome,
    testDepthEvidence: depth.evidence,
    testDepthPassingStandard: depth.passingStandard,
    testDepthReview: depth.review,
    blueprintId: `use-case:${item.id}:${depth.id}`,
    blueprintVersion: 'v0.1',
    rubricVersion: 'v1',
    systemPromptVersion: 'v1'
  };
}

// ---------------------------------------------------------------------------
// IDENTITY ASSURANCE — lightweight pre-certification gate (doc-16).
//
// Standardized onto the Products identity contract so the unified app can swap
// providers interchangeably. Before a learner STARTS any certification depth,
// the app presents an identity step that resolves to one of the three ACTIVE
// levels below. The resolved record is stored on the certification context and
// flows into both the credential record and the evidence packet.
// proctored_verified is NOT offered here — it is scaffolded in doc-16 but has
// no provider workflow yet, so we never claim it. (The live use-cases-app uses
// use-cases-identity.js; this module provides the unified-app contract.)
// ---------------------------------------------------------------------------

export const USE_CASE_IDENTITY_LEVELS = [
  {
    id: 'self_attested',
    label: 'Self-attested',
    requiresSignature: false,
    accountRequired: false,
    description: 'You claim the work. No account or identity check beyond this browser session.'
  },
  {
    id: 'account_bound',
    label: 'Account-bound',
    requiresSignature: false,
    accountRequired: true,
    description: 'Your attempt is tied to a signed-in AESOP account, learner ID, and saved transcript record.'
  },
  {
    id: 'identity_attested',
    label: 'Identity-attested',
    requiresSignature: true,
    accountRequired: false,
    description: 'You sign an identity statement before the attempt, confirming you are the person named on the credential.'
  }
];

export function identityLevelById(levelId) {
  return USE_CASE_IDENTITY_LEVELS.find((level) => level.id === levelId) || null;
}

/**
 * Resolve the honest identity-assurance level from a gate selection. Never
 * blocks: if no account is present we fall back to self_attested (or
 * identity_attested when the learner signs the identity statement).
 *
 * @param {object} gate
 * @param {string} [gate.levelId]      learner's chosen level id
 * @param {boolean} [gate.adultAttested]   18+ adult attestation checkbox
 * @param {boolean} [gate.identitySigned]  identity-statement signature (for identity_attested)
 * @param {object|null} [gate.account]     { uid, email } when a Firebase user is signed in
 * @returns {{level:string, requiresSignature:boolean, accountRequired:boolean, adultAttested:boolean, identitySigned:boolean, account:object|null}}
 */
export function resolveUseCaseIdentityLevel(gate = {}) {
  const account = gate.account && gate.account.uid ? gate.account : null;
  let levelId = gate.levelId;
  let level = identityLevelById(levelId);

  // account_bound requires a signed-in account; without one, fall back honestly.
  if (level && level.id === 'account_bound' && !account) {
    levelId = gate.identitySigned ? 'identity_attested' : 'self_attested';
    level = identityLevelById(levelId);
  }
  // No explicit choice: prefer account_bound when signed in, else the honest
  // signed/unsigned self level.
  if (!level) {
    levelId = account ? 'account_bound' : (gate.identitySigned ? 'identity_attested' : 'self_attested');
    level = identityLevelById(levelId);
  }

  return {
    level: level.id,
    requiresSignature: level.requiresSignature,
    accountRequired: level.accountRequired,
    adultAttested: Boolean(gate.adultAttested),
    identitySigned: Boolean(gate.identitySigned),
    account
  };
}

/**
 * Full doc-16-shaped identity-assurance record. Built at gate time from the
 * resolved level so the credential record + evidence packet carry the honest
 * level, account binding, and attestation. proctoringRequired is always false
 * and proctoringMode is always 'none' on this pathway.
 *
 * @param {string} earnedAt  ISO timestamp the credential/attempt is stamped with
 * @param {object} gate      gate selection (see resolveUseCaseIdentityLevel)
 */
export function buildUseCaseIdentityAssurance(earnedAt = new Date().toISOString(), gate = {}) {
  const resolved = resolveUseCaseIdentityLevel(gate);
  const meta = identityLevelById(resolved.level);
  // "attested" tracks the identity-statement signature; account_bound and
  // self_attested do not sign, so attested is false unless the learner signed.
  const attested = resolved.requiresSignature ? resolved.identitySigned : false;
  return {
    level: resolved.level,
    label: meta ? meta.label : resolved.level,
    status: resolved.level,
    accountRequired: resolved.accountRequired,
    accountUid: resolved.account ? resolved.account.uid : '',
    accountEmail: resolved.account ? (resolved.account.email || '') : '',
    adultAttested: resolved.adultAttested,
    attested,
    attestedAt: attested ? earnedAt : null,
    proctoringRequired: false,
    proctoringMode: 'none'
  };
}
