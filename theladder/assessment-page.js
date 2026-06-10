// theladder-v0.2.0 | 2026-06-10
// assessment-page.js — page entry module for /theladder/assessment.html
// (BUILD §6.4). Drives the three-phase shell (intro → conversation → result)
// around the real conversational placement engine in ladder-core.js. The
// engine's own elements (assessment log/form, status, profile prompt,
// metrics) keep their original ids and are rendered by the core.
import {
  initCore,
  registerPageRenderer,
  state,
  getActiveTier,
  getActiveTopic,
  startPlacementAssessment,
  resetPlacementAssessment,
  userAssessmentTurns,
  climbUrlFor
} from './ladder-core.js?v=1';

const els = {
  intro: document.getElementById('assessIntro'),
  conversation: document.getElementById('placementSection'),
  result: document.getElementById('assessResult'),
  progressFill: document.getElementById('assessProgressFill'),
  begin: document.getElementById('beginAssessmentBtn'),
  retake: document.getElementById('retakePlacementBtn'),
  resultTierNum: document.getElementById('resultTierNum'),
  resultTierName: document.getElementById('resultTierName'),
  resultStatTiersOut: document.getElementById('resultStatTiersOut'),
  resultStatRungsGranted: document.getElementById('resultStatRungsGranted'),
  resultStatRungsAssigned: document.getElementById('resultStatRungsAssigned'),
  resultStartBtn: document.getElementById('resultStartBtn')
};

const pad = (n) => String(n).padStart(2, '0');

function currentPhase() {
  if (state.progress.placement) return 'result';
  if ((state.progress.assessmentMessages || []).length) return 'conversation';
  return 'intro';
}

// Cosmetic header progress (BUILD §6.4): advances per learner turn, 100% on result.
function progressPercent(phase) {
  if (phase === 'intro') return 0;
  if (phase === 'result') return 100;
  return Math.min(90, 15 + userAssessmentTurns() * 15);
}

function renderResult() {
  const placement = state.progress.placement;
  if (!placement) return;
  const tier = getActiveTier();
  const placedOutRungs = Object.values(state.progress.completedTopics || {})
    .filter((record) => record?.status === 'placed_out').length;
  if (els.resultTierNum) els.resultTierNum.textContent = `Tier ${pad(tier.order)}`;
  if (els.resultTierName) els.resultTierName.textContent = tier.name;
  if (els.resultStatTiersOut) els.resultStatTiersOut.textContent = String((placement.grantedTierIds || []).length);
  if (els.resultStatRungsGranted) els.resultStatRungsGranted.textContent = String(placedOutRungs);
  if (els.resultStatRungsAssigned) els.resultStatRungsAssigned.textContent = String((placement.assignedTopicIds || []).length);
  if (els.resultStartBtn) {
    els.resultStartBtn.textContent = `Start climbing from Tier ${tier.order}`;
    els.resultStartBtn.href = climbUrlFor(getActiveTopic());
  }
}

function renderPhase() {
  const phase = currentPhase();
  if (els.intro) els.intro.hidden = phase !== 'intro';
  if (els.conversation) els.conversation.hidden = phase !== 'conversation';
  if (els.result) els.result.hidden = phase !== 'result';
  if (els.progressFill) els.progressFill.style.width = `${progressPercent(phase)}%`;
  if (phase === 'result') renderResult();
}

els.begin?.addEventListener('click', () => {
  startPlacementAssessment();
});
els.retake?.addEventListener('click', () => {
  resetPlacementAssessment();
});

registerPageRenderer(renderPhase);
initCore();
