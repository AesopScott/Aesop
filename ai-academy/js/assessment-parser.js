// Assessment signal extraction parser — AESOP AI Academy
// Extracts aptitude score, interest tags, and completion flag from AI responses
// Consumed by assessment-chat.js and later by the taxonomy mapper (Phase 4)

import { INTEREST_TAGS } from './assessment-prompts.js';

// Regex to find the embedded completion signal in an AI response
const COMPLETION_REGEX = /<!--ASSESSMENT_COMPLETE:([\s\S]*?)-->/;

/**
 * Parse an AI response for an embedded completion signal.
 * Returns null if no signal is present (conversation still in progress).
 *
 * @param {string} rawText - Full AI response text
 * @returns {{ signals: AssessmentSignals|null, visibleText: string }}
 */
export function parseAssessmentResponse(rawText) {
  if (!rawText || typeof rawText !== 'string') {
    return { signals: null, visibleText: '' };
  }

  const match = rawText.match(COMPLETION_REGEX);

  // Strip the signal from visible text regardless of parse success
  const visibleText = rawText.replace(COMPLETION_REGEX, '').trim();

  if (!match) {
    return { signals: null, visibleText };
  }

  try {
    const raw = JSON.parse(match[1]);
    const signals = validateAndNormalizeSignals(raw);
    return { signals, visibleText };
  } catch (e) {
    console.error('Failed to parse assessment completion signal:', e, match[1]);
    return { signals: null, visibleText };
  }
}

/**
 * Validate and normalize raw signal data from the AI.
 * Clamps numeric values, filters tags to the allowed list, ensures required fields.
 *
 * @param {Object} raw
 * @returns {AssessmentSignals}
 */
function validateAndNormalizeSignals(raw) {
  // Aptitude score: integer 0-100
  const aptitudeScore = clampInt(raw.aptitudeScore ?? raw.aptitude_score ?? 0, 0, 100);

  // Interest tags: filter to allowed list, deduplicate, max 4
  const rawTags = Array.isArray(raw.interestTags ?? raw.interest_tags)
    ? (raw.interestTags ?? raw.interest_tags)
    : [];
  const interestTags = [...new Set(
    rawTags
      .map(t => String(t).toLowerCase().trim())
      .filter(t => INTEREST_TAGS.includes(t))
  )].slice(0, 4);

  // Completion flag: must be true
  const completionFlag = raw.completionFlag === true || raw.completion_flag === true;

  // Reasoning: string, max 300 chars
  const reasoning = String(raw.reasoning ?? '').slice(0, 300);

  // Aptitude band for human-readable display
  const aptitudeBand = getAptitudeBand(aptitudeScore);

  return {
    aptitudeScore,
    interestTags,
    completionFlag,
    reasoning,
    aptitudeBand,
    parsedAt: new Date().toISOString(),
  };
}

/**
 * Convert a numeric aptitude score to a named band.
 * Used by the taxonomy mapper and UI display.
 *
 * @param {number} score
 * @returns {'beginner'|'aware'|'intermediate'|'advanced'}
 */
export function getAptitudeBand(score) {
  if (score <= 25) return 'beginner';
  if (score <= 50) return 'aware';
  if (score <= 75) return 'intermediate';
  return 'advanced';
}

/**
 * Build a learner profile summary string for display and logging.
 *
 * @param {AssessmentSignals} signals
 * @returns {string}
 */
export function buildProfileSummary(signals) {
  const { aptitudeScore, aptitudeBand, interestTags } = signals;
  const tagList = interestTags.length > 0
    ? interestTags.join(', ')
    : 'general AI';
  return `Aptitude: ${aptitudeBand} (${aptitudeScore}/100) · Interests: ${tagList}`;
}

/**
 * Check whether a response indicates assessment completion.
 * Lightweight check — use parseAssessmentResponse for full extraction.
 *
 * @param {string} rawText
 * @returns {boolean}
 */
export function isAssessmentComplete(rawText) {
  return COMPLETION_REGEX.test(rawText);
}

// ── Helpers ───────────────────────────────────────────────────────────

function clampInt(value, min, max) {
  const n = parseInt(value, 10);
  if (isNaN(n)) return min;
  return Math.min(Math.max(n, min), max);
}

/**
 * @typedef {Object} AssessmentSignals
 * @property {number}   aptitudeScore  - 0-100
 * @property {string[]} interestTags   - subset of INTEREST_TAGS, max 4
 * @property {boolean}  completionFlag - always true when signals are present
 * @property {string}   reasoning      - AI explanation
 * @property {string}   aptitudeBand   - 'beginner'|'aware'|'intermediate'|'advanced'
 * @property {string}   parsedAt       - ISO timestamp
 */
