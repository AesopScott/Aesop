// theladder-v0.2.0 | 2026-06-10
// transcript-page.js — page entry module for /theladder/transcript.html
// (BUILD §6.6). Renders the document header, summary strip, credential cards,
// and the 15-row full record from real learner state. The evidence list
// (transcriptList), export button, and full-academy-transcript link keep
// their original ids and are handled by ladder-core.js.
import {
  initCore,
  registerPageRenderer,
  state,
  escapeHtml,
  topicKey,
  completedCount,
  buildCertificationTranscript
} from './ladder-core.js?v=1';
import { LADDER_TIERS } from './ladder-data.js?v=2';

const els = {
  learner: document.getElementById('tsLearner'),
  learnerId: document.getElementById('tsLearnerId'),
  issued: document.getElementById('tsIssued'),
  tiersCertified: document.getElementById('tsTiersCertified'),
  rungsCompleted: document.getElementById('tsRungsCompleted'),
  credentials: document.getElementById('tsCredentials'),
  credentialCards: document.getElementById('credentialCards'),
  recordRows: document.getElementById('fullRecordRows'),
  avatar: document.getElementById('navAvatar')
};

const pad = (n) => String(n).padStart(2, '0');
const ACCEPTED = new Set(['certified', 'passed', 'pass', 'verified']);

function formatDate(value) {
  const time = Date.parse(value || '');
  if (Number.isNaN(time)) return '—';
  return new Date(time).toLocaleDateString(undefined, { day: '2-digit', month: 'short', year: 'numeric' });
}

function certifiedRecords() {
  return buildCertificationTranscript().filter((record) => ACCEPTED.has(String(record.status || '').toLowerCase()));
}

// Verification uses the existing /ladder-credential.html flow (same query
// contract as the credential example link on the old page).
function verifyUrl(record) {
  const params = new URLSearchParams({
    learner: state.learnerId || 'AESOP',
    tier: record.ladderTierLabel || record.title || '',
    level: record.depthLabel || 'Certification',
    education: record.certificationTierLabel || '',
    earned: String(record.earnedAt || '').slice(0, 10)
  });
  return `/ladder-credential.html?${params.toString()}`;
}

function renderHeader() {
  if (els.learner) els.learner.textContent = state.authUser?.email || state.learnerId || 'Anonymous learner';
  if (els.learnerId) els.learnerId.textContent = state.learnerId || 'Not started';
  if (els.issued) els.issued.textContent = formatDate(new Date().toISOString());
  if (els.avatar) {
    const initials = (state.learnerId || '').replace(/^AESOP-/, '').slice(0, 2);
    els.avatar.hidden = !initials;
    els.avatar.textContent = initials;
    els.avatar.title = state.learnerId || '';
  }
}

function renderSummary(records) {
  const tierIds = new Set(records.map((record) => record.ladderTierId).filter(Boolean));
  if (els.tiersCertified) els.tiersCertified.textContent = String(tierIds.size);
  if (els.rungsCompleted) els.rungsCompleted.textContent = String(completedCount());
  if (els.credentials) els.credentials.textContent = String(records.length);
}

function renderCredentialCards(records) {
  if (!els.credentialCards) return;
  if (!records.length) {
    els.credentialCards.innerHTML = '<p class="small-muted" style="margin: 0;">No credentials yet — certify a tier to earn your first one.</p>';
    return;
  }
  els.credentialCards.innerHTML = records.map((record) => {
    const tier = LADDER_TIERS.find((item) => item.id === record.ladderTierId);
    const tierTag = tier ? `Tier ${pad(tier.order)} · ${escapeHtml(record.depthLabel || 'Certified')}` : escapeHtml(record.depthLabel || 'Certified');
    return `
      <div class="panel panel-accent" style="padding: 26px 28px;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px;">
          <span style="font-size: 11px; letter-spacing: .14em; text-transform: uppercase; color: var(--accent-ink); font-weight: 600;">${tierTag}</span>
          <span class="seal-check seal-check--sm">&check;</span>
        </div>
        <h3 class="h3" style="margin-bottom: 6px;">${escapeHtml(tier ? tier.name : (record.ladderTierLabel || record.title || 'Credential'))}</h3>
        <p style="font-size: 14px; color: var(--muted); margin: 0 0 22px; line-height: 1.6;">${escapeHtml(record.rationale || record.transcriptLine || '')}</p>
        <div style="display: flex; justify-content: space-between; align-items: center; gap: 10px; border-top: 1px solid var(--hair); padding-top: 16px;">
          <span style="font-size: 12.5px; color: var(--muted); overflow-wrap: anywhere;">${escapeHtml(record.id || '')} · ${formatDate(record.earnedAt)}</span>
          <a href="${verifyUrl(record)}" target="_blank" rel="noopener" style="font-size: 13px; font-weight: 600; color: var(--primary); white-space: nowrap;">Verify &rarr;</a>
        </div>
      </div>`;
  }).join('');
}

function tierRowData(tier, records) {
  const done = tier.topics.filter((topic) => state.progress.completedTopics[topicKey(topic.id)]).length;
  const tierRecords = records.filter((record) => record.ladderTierId === tier.id);
  const latest = tierRecords.reduce((max, record) => (
    String(record.earnedAt || '') > String(max?.earnedAt || '') ? record : max
  ), tierRecords[0] || null);
  let status = 'none';
  if (tierRecords.length) status = 'certified';
  else if (done > 0 || tier.id === state.activeTierId) status = 'progress';
  return { done, total: tier.topics.length, status, completedAt: latest?.earnedAt || null };
}

function renderFullRecord(records) {
  if (!els.recordRows) return;
  els.recordRows.innerHTML = LADDER_TIERS.map((tier) => {
    const row = tierRowData(tier, records);
    const dim = row.status === 'none' ? ' dim' : '';
    const pill = row.status === 'certified'
      ? '<span class="pill pill-certified">Certified</span>'
      : row.status === 'progress'
        ? '<span class="pill pill-progress">In progress</span>'
        : '<span class="pill-none">Not started</span>';
    const color = row.status === 'none' ? 'var(--faint)' : 'var(--ink)';
    return `
      <div class="record-grid record-row${dim}">
        <span class="display" style="font-size: 18px; color: ${color};">${pad(tier.order)}</span>
        <span style="font-size: 15px; color: ${color};">${escapeHtml(tier.name)}</span>
        <span style="font-size: 14px; color: var(--muted);">${row.done} / ${row.total}</span>
        <span style="font-size: 14px; color: var(--muted);">${row.completedAt ? formatDate(row.completedAt) : '—'}</span>
        <span style="text-align: right;">${pill}</span>
      </div>`;
  }).join('');
}

function renderTranscriptPage() {
  const records = certifiedRecords();
  renderHeader();
  renderSummary(records);
  renderCredentialCards(records);
  renderFullRecord(records);
}

registerPageRenderer(renderTranscriptPage);
initCore();
