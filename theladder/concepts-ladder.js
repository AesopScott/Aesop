// =============================================================================
// theladder/concepts-ladder.js
// Wiring layer between the AI-Concepts ladder (LADDER_TIERS) and the shared
// Ladder engines.
//
// This module is the Concepts analogue of theladder-products/products-ladder.js.
// It builds the descriptors/blueprints the shared engines need so that
// ladder-app.js can stay focused on UI + state. Like products-ladder.js, it
// imports NOTHING from the engines itself — the app owns engine construction —
// it only produces plain data the engines consume. Its sole data dependency is
// the Concepts catalog in ./ladder-data.js (LADDER_TIERS).
//
//   buildConceptsPlacementDescriptor(tiers) -> descriptor
//       Turns LADDER_TIERS (and their topics/rungs) into createPlacementEngine
//       items + the three-score grant rules adapted to *AI fluency*. Defaults to
//       the imported LADDER_TIERS when called with no argument.
//
//   buildConceptsBlueprint({ tier, level, depth }) -> examiner blueprint
//       Per (tier, certification depth) examiner blueprint for
//       createCertificationEngine().buildExaminerSystemPrompt.
//
//   buildConceptsCertContext({ tier, depth }) -> certification context
//       The context object recordCertificationResult / buildEvidencePacket need.
//
//   CONCEPTS_IDENTITY_LEVELS — the three ACTIVE identity-assurance levels a
//       learner may resolve to before a certification (doc-16): self_attested,
//       account_bound, identity_attested. proctored_verified is intentionally
//       absent — it is scaffolded, not active.
//
//   buildConceptsIdentityAssurance(earnedAt, gate) -> identity-assurance record
//       Full doc-16-shaped identity-assurance record built from the learner's
//       pre-certification gate selection. Populated at gate time, stored into
//       the certification context, the credential record, and the evidence
//       packet (so the data-layer credential row carries the honest level).
//
//   CERT_DEPTHS — the three certification depths (Certification / Expert /
//       Master) with doc-16 depth fields.
//
//   Plus helpers mirroring products-ladder.js: CONCEPTS_INTEREST_KEYWORDS,
//   depthForLabel, identityLevelById, resolveConceptsIdentityLevel.
// =============================================================================

import { LADDER_TIERS } from './ladder-data.js';

// ---------------------------------------------------------------------------
// PLACEMENT — adapting the 3-score model to AI fluency (the Concepts pathway).
//
// The shared placement engine speaks in three normalized scores. The Concepts
// ladder reads them in their native sense (this IS the pathway the engine
// defaults were tuned for):
//
//   capabilityScore  -> GENERAL AI FLUENCY. Vocabulary, limits, prompting,
//                       verification, everyday use. Drives placement up the
//                       early-to-middle conceptual tiers.
//   technicalScore   -> TECHNICAL DEPTH. APIs, JSON, code, data, RAG, agents,
//                       evals, deployment. Gates the builder-grade tiers
//                       (Application Development through System Reliability).
//   governanceScore  -> GOVERNANCE DEPTH. Privacy, copyright, ethics, law,
//                       security, vendor risk, policy. Gates the law/ethics and
//                       strategy tiers.
//
// grantRules returns the GROUP ids (tier ids) the learner places out of. Tiers
// NOT granted get their core topics (low order in range) plus any
// interest-matched topics assigned. So: grant the tiers the learner is fluent
// in; assign specific topics inside the tiers they still need.
//
// The thresholds below preserve the existing Concepts ladder grant logic
// (ladder-app.js grantRules, per-tier capability/technical/governance gates).
// ---------------------------------------------------------------------------

// Map each tier id to which score axis (or combination) gates placing out of
// it, and the threshold. Mirrors the Concepts ladder's per-tier grant rules.
const TIER_GRANT_GATES = {
  'tier-01': (s) => s.capabilityScore >= 25,
  'tier-02': (s) => s.capabilityScore >= 35,
  'tier-03': (s) => s.capabilityScore >= 45,
  'tier-04': (s) => s.capabilityScore >= 55,
  'tier-05': (s) => s.capabilityScore >= 60,
  'tier-06': (s) => s.capabilityScore >= 65,
  'tier-07': (s) => s.capabilityScore >= 70,
  'tier-08': (s) => s.capabilityScore >= 70 && s.technicalScore >= 45,
  'tier-09': (s) => s.capabilityScore >= 75 && s.technicalScore >= 55,
  'tier-10': (s) => s.capabilityScore >= 80 && s.technicalScore >= 65,
  'tier-11': (s) => s.capabilityScore >= 85 && s.technicalScore >= 75,
  'tier-12': (s) => s.capabilityScore >= 75 && s.technicalScore >= 55,
  'tier-13': (s) => s.capabilityScore >= 70 && s.governanceScore >= 55,
  'tier-14': (s) => s.capabilityScore >= 88 && s.technicalScore >= 80,
  'tier-15': (s) => s.capabilityScore >= 80 && s.governanceScore >= 50
};

// Interest keyword map tuned for the Concepts pathway. Mirrors the engine
// defaults (DEFAULT_INTEREST_KEYWORDS) so concept reason-text matches well;
// restated here so the descriptor is self-contained like the Products one.
export const CONCEPTS_INTEREST_KEYWORDS = {
  technical: ['api', 'sdk', 'json', 'structured', 'function', 'tool', 'rag', 'vector', 'agent', 'model', 'code', 'embedding', 'deployment', 'inference', 'schema'],
  business: ['business', 'workflow', 'marketing', 'sales', 'support', 'operations', 'strategy', 'roi', 'enterprise', 'process'],
  governance: ['governance', 'law', 'legal', 'ethics', 'policy', 'privacy', 'risk', 'compliance', 'copyright', 'bias', 'consent', 'audit'],
  creative: ['creative', 'image', 'video', 'audio', 'music', 'voice', 'media', 'content', 'design', 'synthetic', 'storyboard'],
  automation: ['automation', 'workflow', 'trigger', 'action', 'agent', 'orchestration', 'webhook', 'integration', 'no-code'],
  research: ['research', 'source', 'citation', 'fact', 'study', 'information', 'search', 'summary', 'synthesis'],
  security: ['security', 'prompt injection', 'red team', 'abuse', 'threat', 'privacy', 'jailbreak', 'exfiltration'],
  data: ['data', 'embedding', 'vector', 'retrieval', 'rag', 'search', 'metadata', 'chunking', 'index']
};

/**
 * Build a createPlacementEngine descriptor from the Concepts catalog.
 * Items use the tier id as `group`, and order within the tier so the
 * lowest-order topics in each non-granted tier are auto-assigned core.
 *
 * @param {Array} [tiers] LADDER_TIERS-shaped array. Defaults to the imported
 *                        LADDER_TIERS.
 */
export function buildConceptsPlacementDescriptor(tiers = LADDER_TIERS) {
  const items = [];
  tiers.forEach((tier) => {
    (tier.topics || []).forEach((topic) => {
      items.push({
        id: `topic-${topic.id}`,
        label: topic.title,
        group: tier.id,
        order: topic.order,
        interestText: `${topic.title} ${tier.name} ${tier.title} ${(tier.vocabulary || []).join(' ')}`
      });
    });
  });

  return {
    items,
    interestKeywords: CONCEPTS_INTEREST_KEYWORDS,
    coreItemsPerGroup: 3,
    minLearnerTurns: 5,
    grantRules(scores) {
      return Object.entries(TIER_GRANT_GATES)
        .filter(([, test]) => {
          try { return Boolean(test(scores)); } catch { return false; }
        })
        .map(([tierId]) => tierId);
    },
    assessment: {
      product: 'AESOP AI Academy',
      role: 'placement assessor',
      intro: 'Your job is to assess BOTH interest and capability across AI fluency, then decide which conceptual tiers the learner can test out of and which specific topics to assign.',
      exchangeGuidance: 'Run a 5-7 exchange assessment. Ask one question at a time. Be warm, direct, and practical. Anchor questions in real AI use, not abstract theory.',
      dimensions: [
        'General AI fluency (capabilityScore): vocabulary, limits, prompting, verification, everyday use.',
        'Technical depth (technicalScore): APIs, JSON, code, data, RAG, agents, evals, deployment.',
        'Governance depth (governanceScore): privacy, copyright, ethics, law, security, vendor risk, policy.',
        'Interests: which topics energize them enough to keep learning.',
        'Application context: what they want to be able to do after learning.'
      ],
      styleGuidance: 'Use light scenario questions, not trivia. Include at least one technical calibration question and one governance/risk question. Do not make beginners feel punished. If they are technical, probe API, retrieval, and agent depth.',
      redirectGuidance: 'Stay on AI-fluency placement. If they go off topic, redirect to AI concept placement.',
      opener: 'Let us place you across the AI concepts ladder. I will gauge what you already understand well and what you actually want to learn. First: how do you currently use AI, what for, and where do you feel least confident?'
    }
  };
}

// ---------------------------------------------------------------------------
// CERTIFICATION — three depths reusing the doc-16 depth fields.
// ---------------------------------------------------------------------------

export const CERT_DEPTHS = [
  {
    id: 'certification',
    label: 'Certification',
    certificationTierLabel: 'Concepts Certification',
    outcome: 'Competent, defensible understanding of the tier for everyday AI work.',
    evidence: 'A guided assignment plus explanations of core concepts, fit, and one limitation.',
    passingStandard: 'Demonstrates correct core-concept understanding, safe defaults, and accurate explanation.',
    review: 'AI examiner with independent second-model validation.'
  },
  {
    id: 'expert',
    label: 'Expert certification',
    certificationTierLabel: 'Concepts Expert Certification',
    outcome: 'Chooses the right approach, troubleshoots limits, compares alternatives, and can teach another learner.',
    evidence: 'A non-trivial scenario solved with a justified approach, plus a comparison against an alternative concept or technique.',
    passingStandard: 'Transfers understanding to a new context, handles edge cases, and defends the approach.',
    review: 'AI examiner with independent second-model validation; higher ambiguity.'
  },
  {
    id: 'master',
    label: 'Master certification',
    certificationTierLabel: 'Concepts Master Certification',
    outcome: 'Designs a production-grade solution, evaluates risk, documents evidence, and defends every choice.',
    evidence: 'Portfolio-quality artifact: a production-ready design with risk controls and evidence.',
    passingStandard: 'Original synthesis, standards mapping, risk governance, and leadership-level defense.',
    review: 'AI examiner with independent second-model validation; mastery rigor.'
  }
];

export function depthForLabel(label) {
  return CERT_DEPTHS.find((depth) => depth.label === label) || CERT_DEPTHS[0];
}

/**
 * Examiner blueprint for buildExaminerSystemPrompt(blueprint).
 * `level` is the education tier the learner studied at (College/Workforce/...),
 * used only to flavor the item label; the depth drives examiner rigor.
 */
export function buildConceptsBlueprint({ tier, level, depth }) {
  const itemLabel = `${tier.name} (${tier.title})`;
  return {
    itemLabel,
    educationTierLabel: level ? `${level} concepts course` : 'Concepts course',
    certificationTierLabel: depth.certificationTierLabel,
    standards: `AESOP AI Fluency — ${tier.name}`,
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
 * testDepth*, certificationTier*, blueprintId, standards, attemptId).
 */
export function buildConceptsCertContext({ tier, depth, learnerId }) {
  const attemptId = `conceptcert_${tier.id}_${depth.id}_${Date.now()}`;
  return {
    attemptId,
    pathway: 'concepts',
    learnerId: learnerId || '',
    itemId: tier.id,
    itemLabel: `${tier.name} (${tier.title})`,
    certificationTierId: depth.id,
    certificationTierLabel: depth.certificationTierLabel,
    standards: `AESOP AI Fluency — ${tier.name}`,
    testDepthId: depth.id,
    testDepthLabel: depth.label,
    testDepthOutcome: depth.outcome,
    testDepthEvidence: depth.evidence,
    testDepthPassingStandard: depth.passingStandard,
    testDepthReview: depth.review,
    blueprintId: `concepts:${tier.id}:${depth.id}`,
    blueprintVersion: 'v0.1',
    rubricVersion: 'v1',
    systemPromptVersion: 'v1'
  };
}

// ---------------------------------------------------------------------------
// IDENTITY ASSURANCE — lightweight pre-certification gate (doc-16).
//
// Before a learner STARTS any certification depth, ladder-app.js presents an
// identity step that resolves to one of the three ACTIVE levels below. The
// resolved record is stored on the certification context and flows into both
// the credential record and the evidence packet. proctored_verified is NOT
// offered here — it is scaffolded in doc-16 but has no provider workflow yet,
// so we never claim it.
// ---------------------------------------------------------------------------

export const CONCEPTS_IDENTITY_LEVELS = [
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
  return CONCEPTS_IDENTITY_LEVELS.find((level) => level.id === levelId) || null;
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
export function resolveConceptsIdentityLevel(gate = {}) {
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
 * @param {object} gate      gate selection (see resolveConceptsIdentityLevel)
 */
export function buildConceptsIdentityAssurance(earnedAt = new Date().toISOString(), gate = {}) {
  const resolved = resolveConceptsIdentityLevel(gate);
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
