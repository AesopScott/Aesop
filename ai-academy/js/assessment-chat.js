// Assessment Chat — AESOP AI Academy
// Drives the student assessment conversation and completion flow

import { getOrCreateLearnerId, initializeLearnerRecord, addAssessmentMessage, updateAssessmentResults, updateQRRecoveryToken, setupOfflineSync } from './firebase-helpers.js';
import { generateQRCode, displayQRCode, getRecoveryInstructionsHTML } from './qr-generator.js';

const PROXY_URL = '/aesop-api/proxy.php';

// Assessment-specific guardrail (distinct from lab guardrail per lab-rules.md)
const ASSESSMENT_GUARDRAIL = `You are an AESOP AI Academy assessment assistant helping a student discover their best learning pathway.
Your ONLY job is to assess the student's current knowledge of and interest in AI topics through friendly conversation.
Stay strictly on topic: AI, machine learning, data science, technology, and learning preferences.
If students go off-topic, warmly redirect: "That's interesting — let's keep our focus on your AI learning journey for now."
Keep responses concise (under 120 words). Be encouraging and curiosity-driven.`;

const ASSESSMENT_SYSTEM_PROMPT = `${ASSESSMENT_GUARDRAIL}

You are running a structured but conversational AI aptitude and interest assessment. Your goal is to determine:
1. The student's APTITUDE: their existing AI/tech knowledge and reasoning ability (score 0-100)
2. Their INTERESTS: which AI topics excite them (tags: python, nlp, vision, ethics, robotics, business, creative, data, security, policy)

Conversation flow (5-7 exchanges total):
- Start: warm opener asking about their background with tech/computers
- Explore: 2-3 questions probing knowledge (what they've heard about AI, tools they've used, concepts they understand)
- Interest: 1-2 questions about what fascinates or worries them about AI
- Wrap-up: 1 closing question confirming their learning goals

When you have enough signal (5+ exchanges), include a special JSON block at the END of your response (hidden in HTML comment so it's parseable):
<!--ASSESSMENT_COMPLETE:{"aptitudeScore":XX,"interestTags":["tag1","tag2"],"completionFlag":true,"reasoning":"brief explanation"}-->

Do NOT reveal this JSON to the student. End the visible conversation warmly before including it.`;

const FALLBACK_REPLIES = [
  "That's a great starting point! Tell me — have you ever tried using any AI tools, even casually? Things like ChatGPT, image generators, or even Siri?",
  "Interesting! AI is definitely changing a lot. What draws you toward learning about it — is it more curiosity, career goals, or something else?",
  "Based on what you've shared, you seem to have a good intuition for how AI fits into the world. One more question: if you could pick one area to go deep on — things like coding, ethics, creative AI, or how it affects jobs — which feels most interesting to you?",
];

// Session state
let conversationHistory = [];
let exchangeCount = 0;
let isOffline = false;
let assessmentComplete = false;
let learnerId = null;
const COMPLETION_THRESHOLD = 5; // min exchanges before completion

/**
 * Initialize the assessment session
 */
export async function initAssessment() {
  setupOfflineSync();

  learnerId = getOrCreateLearnerId();
  await initializeLearnerRecord(learnerId);

  renderOpenerMessage();
}

/**
 * Render the AI opener message
 */
function renderOpenerMessage() {
  const opener = "Hi! I'm here to help you figure out the best AI learning path for you. This will take about 5 minutes — just a friendly conversation, no right or wrong answers. To start: how would you describe your relationship with technology so far? Are you someone who loves diving into new tech, or more of a cautious observer?";
  addMsgToUI('ai', opener);

  conversationHistory.push({ role: 'assistant', content: opener });
}

/**
 * Send a student message
 */
export async function assessmentSend() {
  const input = document.getElementById('assessment-input');
  const sendBtn = document.getElementById('assessment-send');
  if (!input || !sendBtn) return;

  const text = input.value.trim();
  if (!text || assessmentComplete) return;

  input.value = '';
  sendBtn.disabled = true;

  conversationHistory.push({ role: 'user', content: text });
  addMsgToUI('user', text);

  // Persist to Firebase (non-blocking)
  addAssessmentMessage(learnerId, 'user', text).catch(() => {});

  // Offline fallback
  if (isOffline) {
    const reply = fallbackReply();
    conversationHistory.push({ role: 'assistant', content: reply });
    addMsgToUI('ai', reply);
    addAssessmentMessage(learnerId, 'assistant', reply).catch(() => {});
    exchangeCount++;
    updateProgress();
    sendBtn.disabled = false;
    input.focus();
    return;
  }

  const thinkingEl = addMsgToUI('thinking', 'Thinking...');

  for (let attempt = 0; attempt < 2; attempt++) {
    try {
      const res = await fetch(PROXY_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          max_tokens: 500,
          system: ASSESSMENT_SYSTEM_PROMPT,
          messages: conversationHistory,
        }),
      });

      if (!res.ok) throw new Error('HTTP ' + res.status);

      const data = await res.json();
      const rawText = (data.content && data.content[0] && data.content[0].text) || '';

      if (thinkingEl && thinkingEl.parentNode) thinkingEl.remove();

      // Check for completion signal embedded in response
      const completionMatch = rawText.match(/<!--ASSESSMENT_COMPLETE:(.*?)-->/s);
      const visibleText = rawText.replace(/<!--ASSESSMENT_COMPLETE:.*?-->/s, '').trim();

      conversationHistory.push({ role: 'assistant', content: visibleText });
      addMsgToUI('ai', visibleText);
      addAssessmentMessage(learnerId, 'assistant', visibleText).catch(() => {});
      exchangeCount++;
      updateProgress();

      if (completionMatch) {
        try {
          const signals = JSON.parse(completionMatch[1]);
          await handleAssessmentComplete(signals);
        } catch (e) {
          console.error('Failed to parse completion signals:', e);
        }
      }

      sendBtn.disabled = false;
      input.focus();
      return;

    } catch (e) {
      if (attempt < 1) {
        await new Promise(r => setTimeout(r, 1500));
        continue;
      }

      if (thinkingEl && thinkingEl.parentNode) thinkingEl.remove();
      isOffline = true;
      addMsgToUI('error', '⚠ AI is temporarily unavailable. You can still complete this assessment in practice mode.');

      const reply = fallbackReply();
      conversationHistory.push({ role: 'assistant', content: reply });
      addMsgToUI('ai', reply);
      exchangeCount++;
      updateProgress();
    }
  }

  sendBtn.disabled = false;
  input.focus();
}

/**
 * Handle assessment completion — save signals, generate QR
 */
async function handleAssessmentComplete(signals) {
  assessmentComplete = true;

  const { aptitudeScore = 0, interestTags = [], completionFlag = true, reasoning = '' } = signals;

  // Disable input
  const input = document.getElementById('assessment-input');
  const sendBtn = document.getElementById('assessment-send');
  if (input) input.disabled = true;
  if (sendBtn) sendBtn.disabled = true;

  // Save assessment results
  await updateAssessmentResults(learnerId, {
    completed: true,
    completedAt: new Date().toISOString(),
    conversationHistory,
    aptitudeScore,
    interestTags,
    completionFlag,
    reasoning,
  });

  // Generate QR recovery token
  const recoveryToken = generateRecoveryToken(learnerId);
  const qrResult = await generateQRCode(learnerId, recoveryToken);

  if (qrResult && !qrResult.errorMessage) {
    await updateQRRecoveryToken(learnerId, {
      token: recoveryToken,
      generatedAt: new Date().toISOString(),
      qrCodeSvg: qrResult.svg || qrResult.dataUrl,
      expiresAt: null,
    });
  }

  // Show completion UI
  showCompletionCard(qrResult, recoveryToken, { aptitudeScore, interestTags });
}

/**
 * Show the completion card with QR code
 */
function showCompletionCard(qrResult, recoveryToken, signals) {
  const card = document.getElementById('assessment-complete');
  if (!card) return;

  // Populate pathway placeholder
  const pathwayEl = document.getElementById('completion-pathway-hint');
  if (pathwayEl && signals.interestTags.length > 0) {
    pathwayEl.textContent = `Based on your interests in ${signals.interestTags.slice(0, 2).join(' and ')}, we're generating your personalized learning path.`;
  }

  // Show QR code
  if (qrResult && qrResult.dataUrl) {
    const qrContainer = document.getElementById('qr-code-display');
    if (qrContainer) {
      displayQRCode('qr-code-display', qrResult.dataUrl, {
        width: '200px',
        height: '200px',
        showLabel: true,
        label: 'Screenshot this to recover your learner ID later',
      });
    }
  }

  // Show learner ID for manual backup
  const idEl = document.getElementById('learner-id-display');
  if (idEl) idEl.textContent = learnerId;

  card.classList.add('visible');
  card.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/**
 * Add a message to the chat UI
 * @returns {HTMLElement} the created element
 */
function addMsgToUI(role, text) {
  const container = document.getElementById('assessment-messages');
  if (!container) return null;

  const div = document.createElement('div');
  div.className = `assessment-msg ${role}`;
  div.textContent = text;
  container.appendChild(div);
  container.scrollTop = container.scrollHeight;
  return div;
}

/**
 * Update progress bar
 */
function updateProgress() {
  const fill = document.getElementById('assessment-progress-fill');
  const label = document.getElementById('assessment-progress-label');
  if (!fill) return;

  const pct = Math.min(Math.round((exchangeCount / COMPLETION_THRESHOLD) * 100), 100);
  fill.style.width = pct + '%';
  if (label) label.textContent = assessmentComplete ? 'Complete!' : `${exchangeCount} of ~${COMPLETION_THRESHOLD} exchanges`;
}

/**
 * Generate a simple recovery token
 * @private
 */
function generateRecoveryToken(learnerId) {
  const suffix = Math.random().toString(36).slice(2, 8).toUpperCase();
  return `${learnerId.slice(0, 8)}-${suffix}`;
}

/**
 * Get a fallback reply in offline mode
 * @private
 */
function fallbackReply() {
  return FALLBACK_REPLIES[Math.min(exchangeCount, FALLBACK_REPLIES.length - 1)];
}
