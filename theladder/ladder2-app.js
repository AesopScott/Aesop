/* =============================================================================
 * ladder2-app.js — Unified Ladder orchestrator (Concepts · Products · Use Cases)
 *
 * One page, one engine. Training holds a focus TOGGLE that swaps the active
 * provider (concepts-ladder.js / products-ladder.js / use-cases-ladder.js) and
 * re-renders against the SAME shared engines (/theladder-shared/*). Placement,
 * training conversations, and certification all run through those engines so
 * the three former pages collapse into this single ladder2 experience.
 *
 * Sections wired here: Marketing (stats), Profile (certs/active course/feedback),
 * Assessment (placement → collapse-to-hub), Training (focus toggle + guided
 * conversation), Certification (account gate + identity assurance + proctoring).
 * ========================================================================== */

import { createPlacementEngine } from '/theladder-shared/placement-engine.js';
import { createCertificationEngine } from '/theladder-shared/certification-engine.js';
import {
  initDataLayer, loadLearnerRecord, saveLearnerProgress,
  recordCompletion, recordCertification
} from '/theladder-shared/data-layer.js';
import { initializeApp, getApps, getApp } from 'https://www.gstatic.com/firebasejs/10.12.0/firebase-app.js';
import {
  getAuth, onAuthStateChanged, sendSignInLinkToEmail,
  signInWithEmailAndPassword, signOut as fbSignOut
} from 'https://www.gstatic.com/firebasejs/10.12.0/firebase-auth.js';
import { FIREBASE_CONFIG } from '/ai-academy/js/firebase-config.js';

import { LADDER_TIERS } from './ladder-data.js?v=2';
import * as Concepts from './concepts-ladder.js';
import * as Products from '/theladder-products/products-ladder.js';
import * as UseCases from '/theladder-use-cases/use-cases-ladder.js';

const PROXY_URL = '/aesop-api/proxy.php';
const LS_FOCUS = 'aesop-ladder2-focus';
const LS_FEEDBACK = 'aesop-ladder2-feedback';
const LS_AUTH = 'aesop-ladder2-auth';
const LS_EMAIL = 'aesop-ladder2-emailForSignIn';

// Real Firebase auth (email-link sign-up + password sign-in). Set in
// initFirebaseAuth() after the data layer has created the default app.
let auth = null;

// Education tiers / roles offered as the certification "level".
const EDUCATION_TIERS = [
  'Elementary', 'Middle School', 'High School',
  'Young Adult', 'College', 'Workforce', 'Leadership'
];
const ADULT_TIERS = new Set(['Young Adult', 'College', 'Workforce', 'Leadership']);

// Proctoring levels surfaced in Certification (doc-16: external is scaffolded).
const PROCTORING_MODES = [
  { id: 'self', label: 'Self-proctored' },
  { id: 'authenticated', label: 'Authenticated (account-bound)' },
  { id: 'external', label: 'External proctor (scaffold — not yet active)', scaffold: true }
];

// --- Products catalog config (kept local so the live Products files are untouched) ---
const PRODUCTS_CATALOG_URL = '/docs/theladder-products-catalog.md?v=2';
const PRODUCT_CATEGORY_RANGES = [
  { label: 'AI assistants', start: 1, end: 20 },
  { label: 'Workplace + writing', start: 21, end: 35 },
  { label: 'Coding tools', start: 36, end: 61 },
  { label: 'Search + RAG', start: 62, end: 82 },
  { label: 'Vector databases', start: 83, end: 107 },
  { label: 'Data + analytics', start: 108, end: 126 },
  { label: 'Design + slides', start: 127, end: 146 },
  { label: 'Video + audio', start: 147, end: 166 },
  { label: 'Sales + support', start: 167, end: 191 },
  { label: 'Agents + automation', start: 192, end: 210 },
  { label: 'Model APIs + cloud', start: 211, end: 230 },
  { label: 'Regulated AI', start: 231, end: 250 }
];
function parseProductCatalog(markdown) {
  return markdown.split('\n')
    .filter((line) => /^\|\s*\d+\s*\|/.test(line))
    .map((line) => {
      const c = line.split('|').slice(1, -1).map((x) => x.trim());
      return { id: Number(c[0]), name: c[1], type: c[2], reason: c[3], depth: c[4] };
    })
    .filter((p) => Number.isFinite(p.id) && p.name);
}
function inRange(id, range) { return id >= range.start && id <= range.end; }

// =============================================================================
// FOCUS REGISTRY — normalizes the three providers to one interface.
// =============================================================================
const FOCUSES = {
  concepts: {
    id: 'concepts', label: 'AI Concepts', pathway: 'concept',
    async loadCatalog() { return LADDER_TIERS; },
    buildGroups(tiers) {
      return tiers.map((tier) => ({
        id: tier.id,
        label: `${tier.name}: ${tier.title}`,
        items: (tier.topics || []).map((t) => ({ id: `topic-${t.id}`, label: t.title, raw: t }))
      }));
    },
    placementDescriptor(tiers) { return Concepts.buildConceptsPlacementDescriptor(tiers); },
    certItemForGroup(group) { return { tier: { id: group.id, name: group.label.split(':')[0], title: (group.label.split(':')[1] || '').trim(), topics: group.items.map((i) => i.raw) } }; },
    CERT_DEPTHS: Concepts.CERT_DEPTHS,
    depthForLabel: Concepts.depthForLabel,
    buildBlueprint: ({ item, level, depth }) => Concepts.buildConceptsBlueprint({ tier: item.tier, level, depth }),
    buildCertContext: ({ item, depth, learnerId }) => Concepts.buildConceptsCertContext({ tier: item.tier, depth, learnerId }),
    IDENTITY_LEVELS: Concepts.CONCEPTS_IDENTITY_LEVELS,
    resolveIdentityLevel: Concepts.resolveConceptsIdentityLevel,
    buildIdentityAssurance: Concepts.buildConceptsIdentityAssurance,
    identityLevelById: Concepts.identityLevelById
  },
  products: {
    id: 'products', label: 'Products', pathway: 'product',
    async loadCatalog() {
      const md = await fetch(PRODUCTS_CATALOG_URL).then((r) => r.text());
      return parseProductCatalog(md);
    },
    buildGroups(products) {
      return PRODUCT_CATEGORY_RANGES.map((range) => ({
        id: range.label,
        label: range.label,
        items: products.filter((p) => inRange(p.id, range)).map((p) => ({ id: `product-${p.id}`, label: p.name, raw: p }))
      })).filter((g) => g.items.length);
    },
    placementDescriptor(products) { return Products.buildProductPlacementDescriptor(products, PRODUCT_CATEGORY_RANGES); },
    certItemForGroup(group, item) { return { product: item ? item.raw : group.items[0]?.raw }; },
    CERT_DEPTHS: Products.CERT_DEPTHS,
    depthForLabel: Products.depthForLabel,
    buildBlueprint: ({ item, level, depth }) => Products.buildProductBlueprint({ product: item.product, level, depth }),
    buildCertContext: ({ item, depth, learnerId }) => Products.buildProductCertContext({ product: item.product, depth, learnerId }),
    IDENTITY_LEVELS: Products.PRODUCT_IDENTITY_LEVELS,
    resolveIdentityLevel: Products.resolveProductIdentityLevel,
    buildIdentityAssurance: Products.buildProductIdentityAssurance,
    identityLevelById: Products.identityLevelById
  },
  'use-cases': {
    id: 'use-cases', label: 'Use Cases', pathway: 'use-case',
    async loadCatalog() {
      const md = await fetch(UseCases.USE_CASE_CATALOG_URL).then((r) => r.text());
      return UseCases.parseUseCaseCatalog(md);
    },
    buildGroups(useCases) {
      return UseCases.USE_CASE_TOPIC_RANGES
        .filter((r) => !/^all /i.test(r.label))
        .map((range) => ({
          id: range.label,
          label: range.label,
          items: useCases.filter((u) => inRange(u.id, range)).map((u) => ({ id: String(u.id), label: u.name, raw: u }))
        })).filter((g) => g.items.length);
    },
    placementDescriptor(useCases) { return UseCases.buildUseCasePlacementDescriptor(useCases, UseCases.USE_CASE_TOPIC_RANGES); },
    certItemForGroup(group, item) { return { useCase: item ? item.raw : group.items[0]?.raw }; },
    CERT_DEPTHS: UseCases.CERT_DEPTHS,
    depthForLabel: UseCases.depthForLabel,
    buildBlueprint: ({ item, level, depth }) => UseCases.buildUseCaseBlueprint({ item: item.useCase, level, depth }),
    buildCertContext: ({ item, depth, learnerId }) => UseCases.buildUseCaseCertContext({ item: item.useCase, depth, learnerId }),
    IDENTITY_LEVELS: UseCases.USE_CASE_IDENTITY_LEVELS,
    resolveIdentityLevel: UseCases.resolveUseCaseIdentityLevel,
    buildIdentityAssurance: UseCases.buildUseCaseIdentityAssurance,
    identityLevelById: UseCases.identityLevelById
  }
};

// =============================================================================
// STATE
// =============================================================================
const certificationEngine = createCertificationEngine({ proxyUrl: PROXY_URL });
let placementEngine = null;

const state = {
  focusId: localStorage.getItem(LS_FOCUS) || 'concepts',
  catalog: null,
  groups: [],
  activeGroupId: null,
  activeItemId: null,
  placement: null,
  assessMessages: [],
  trainMessages: [],
  certMessages: [],
  activeCert: null,            // { item, level, depth, context, blueprint }
  identityGate: { levelId: null, adultAttested: false, identitySigned: false, proctoringId: 'self' },
  authUser: null,              // source of truth is Firebase onAuthStateChanged
  completed: {}                // itemId -> true (per focus, keyed focusId:itemId)
};

const $ = (id) => document.getElementById(id);
const setText = (id, v) => { const e = $(id); if (e) e.textContent = v; };
const focus = () => FOCUSES[state.focusId];
const escapeHtml = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

// =============================================================================
// PROXY helper (placement / training / examiner share one body shape)
// =============================================================================
async function askModel({ messages, systemPrompt, maxTokens = 800, model }) {
  const body = { messages, system_prompt: systemPrompt, max_tokens: maxTokens };
  if (model) body.model = model;
  const res = await fetch(PROXY_URL, {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body)
  });
  const data = await res.json();
  return data?.content?.[0]?.text || data?.error || 'I hit a snag. Please try again.';
}

function renderChat(el, messages) {
  el.innerHTML = messages.map((m) => `
    <div class="l2-msg l2-msg--${m.role === 'user' ? 'user' : 'guide'}">
      <span class="l2-msg__role">${m.role === 'user' ? 'You' : 'Guide'}</span>
      <div class="l2-msg__body">${escapeHtml(m.content).replace(/\n/g, '<br>')}</div>
    </div>`).join('');
  el.scrollTop = el.scrollHeight;
}

// =============================================================================
// BOOT
// =============================================================================
async function init() {
  setupTheme();
  setupNavActions();
  setupFocusToggle();
  setupAssessment();
  setupTraining();
  setupCertification();
  setupProfile();
  setupAuth();
  renderHeroSignup();   // set the signed-out display state before first paint

  initDataLayer().catch((e) => console.warn('data-layer init failed (local-only)', e));
  try {
    const rec = await loadLearnerRecord();
    if (rec) hydrate(rec);
  } catch (e) { console.warn('learner record load failed', e); }
  initFirebaseAuth();

  await activateFocus(state.focusId);
  renderAuthGates();
  renderHeroSignup();
  renderMarketing();
  renderLadderL();
  renderProfile();
}

function hydrate(rec) {
  // pull completed counts + active course hints from the durable record
  const progressKeys = { concept: 'ladderProgress', product: 'productProgress', 'use-case': 'useCaseProgress' };
  Object.entries(progressKeys).forEach(([pathway, key]) => {
    const starts = rec?.[key]?.courseStarts || {};
    Object.entries(starts).forEach(([itemId, v]) => {
      if (v?.status === 'completed') state.completed[`${pathway}:${itemId}`] = true;
    });
  });
  state._record = rec;
}

// =============================================================================
// THEME / NAV
// =============================================================================
function setupTheme() {
  const btn = $('l2DarkToggle');
  const SUN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="4.2"/><line x1="12" y1="1.5" x2="12" y2="4"/><line x1="12" y1="20" x2="12" y2="22.5"/><line x1="1.5" y1="12" x2="4" y2="12"/><line x1="20" y1="12" x2="22.5" y2="12"/><line x1="4.4" y1="4.4" x2="6.2" y2="6.2"/><line x1="17.8" y1="17.8" x2="19.6" y2="19.6"/><line x1="4.4" y1="19.6" x2="6.2" y2="17.8"/><line x1="17.8" y1="6.2" x2="19.6" y2="4.4"/></svg>';
  const MOON = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';
  const sync = () => {
    const dark = document.documentElement.getAttribute('data-theme') === 'dark';
    // show the mode you'll switch TO: moon in light, sun in dark
    btn.innerHTML = dark ? SUN : MOON;
    btn.setAttribute('aria-label', dark ? 'Switch to light mode' : 'Switch to dark mode');
  };
  btn?.addEventListener('click', () => {
    const dark = document.documentElement.getAttribute('data-theme') === 'dark';
    if (dark) { document.documentElement.removeAttribute('data-theme'); localStorage.setItem('aesop-theme', 'light'); }
    else { document.documentElement.setAttribute('data-theme', 'dark'); localStorage.setItem('aesop-theme', 'dark'); }
    sync();
  });
  sync();
  // minimal language select (placeholder — unified i18n is a follow-up)
  const lang = $('l2Lang');
  if (lang && !lang.options.length) {
    lang.innerHTML = '<option value="en">English</option>';
  }
}

function setupNavActions() {
  // hero focus list (marketing right panel)
  const list = $('l2HeroFocusList');
  if (list) {
    list.innerHTML = Object.values(FOCUSES).map((f) =>
      `<button class="l2-btn l2-btn--ghost" data-jump-focus="${f.id}" style="justify-content:flex-start;">${f.label} →</button>`).join('');
    list.querySelectorAll('[data-jump-focus]').forEach((b) => b.addEventListener('click', async () => {
      await activateFocus(b.dataset.jumpFocus);
      document.getElementById('training')?.scrollIntoView({ behavior: 'smooth' });
    }));
  }

  // Release a stuck nav :hover. The gold underline can light up with no intent two ways:
  //  - clicking an in-page anchor smooth-scrolls the section under a stationary mouse
  //    (no mouseleave fires), and
  //  - scrolling (incl. scroll-snap back to the top) lands a nav word under a resting
  //    cursor — so :hover engages without any mouse movement (notably under Profile).
  // On click or scroll, drop the words as pointer targets (clears :hover); the next
  // real mouse move restores them so genuine hover still works.
  let navHoverArmed = false;
  const releaseNavHover = () => {
    document.querySelectorAll('.l2-navlink').forEach((a) => { a.style.pointerEvents = 'none'; });
    if (navHoverArmed) return;
    navHoverArmed = true;
    window.addEventListener('mousemove', () => {
      navHoverArmed = false;
      document.querySelectorAll('.l2-navlink').forEach((a) => { a.style.pointerEvents = ''; });
    }, { once: true });
  };
  document.querySelectorAll('.l2-navlink').forEach((a) => a.addEventListener('click', releaseNavHover));
  window.addEventListener('scroll', releaseNavHover, { passive: true });
}

// =============================================================================
// FOCUS TOGGLE
// =============================================================================
function setupFocusToggle() {
  $('l2FocusToggle')?.querySelectorAll('.l2-focus-btn').forEach((btn) => {
    btn.addEventListener('click', () => activateFocus(btn.dataset.focus));
  });
}

async function activateFocus(focusId) {
  if (!FOCUSES[focusId]) focusId = 'concepts';
  state.focusId = focusId;
  localStorage.setItem(LS_FOCUS, focusId);

  // toggle active button
  $('l2FocusToggle')?.querySelectorAll('.l2-focus-btn').forEach((b) =>
    b.classList.toggle('is-active', b.dataset.focus === focusId));
  $('l2FocusLabel').textContent = focus().label;

  $('l2GroupStatus').textContent = 'Loading rungs…';
  state.catalog = await focus().loadCatalog();
  state.groups = focus().buildGroups(state.catalog);
  placementEngine = createPlacementEngine(focus().placementDescriptor(state.catalog));

  // reset active selection to first group/item
  state.activeGroupId = state.groups[0]?.id || null;
  state.activeItemId = state.groups[0]?.items[0]?.id || null;
  state.trainMessages = [];

  renderRail();
  renderActiveItem();
  renderCertConfig();
}

// =============================================================================
// TRAINING — rail + guided conversation
// =============================================================================
function setupTraining() {
  $('l2StartChat')?.addEventListener('click', startTrainingChat);
  $('l2ChatForm')?.addEventListener('submit', submitTrainingChat);
  $('l2CompleteBtn')?.addEventListener('click', markComplete);
}

function activeGroup() { return state.groups.find((g) => g.id === state.activeGroupId) || state.groups[0]; }
function activeItem() { const g = activeGroup(); return g?.items.find((i) => i.id === state.activeItemId) || g?.items[0]; }

function renderRail() {
  const rail = $('l2GroupRail');
  const total = state.groups.reduce((n, g) => n + g.items.length, 0);
  const done = Object.keys(state.completed).filter((k) => k.startsWith(`${focus().pathway}:`)).length;
  $('l2GroupStatus').textContent = `${done} / ${total} rungs in ${focus().label}`;
  rail.innerHTML = state.groups.map((g, i) => {
    const open = g.id === state.activeGroupId;
    return `<div class="l2-rail-group ${open ? 'is-open' : ''}">
      <button class="l2-rail-grouphead" data-group="${g.id}">
        <span class="l2-rail-num">${i + 1}</span>
        <span class="l2-rail-meta"><strong>${escapeHtml(g.label)}</strong><small>${g.items.length} rungs</small></span>
      </button>
      ${open ? `<div class="l2-rail-items">${g.items.map((it) =>
        `<button class="l2-rail-item ${it.id === state.activeItemId ? 'is-active' : ''}" data-item="${it.id}">${escapeHtml(it.label)}</button>`).join('')}</div>` : ''}
    </div>`;
  }).join('');
  rail.querySelectorAll('[data-group]').forEach((b) => b.addEventListener('click', () => {
    state.activeGroupId = b.dataset.group;
    const g = activeGroup();
    state.activeItemId = g.items[0]?.id || null;
    state.trainMessages = [];
    renderRail(); renderActiveItem();
  }));
  rail.querySelectorAll('[data-item]').forEach((b) => b.addEventListener('click', () => {
    state.activeItemId = b.dataset.item;
    state.trainMessages = [];
    renderRail(); renderActiveItem();
  }));
}

function renderActiveItem() {
  const g = activeGroup(); const it = activeItem();
  $('l2ActiveGroupLabel').textContent = g ? g.label : focus().label;
  $('l2ActiveItemTitle').textContent = it ? it.label : 'Select a rung';
  $('l2ChatSummary').textContent = it
    ? `Learn "${it.label}" through a guided conversation. The guide teaches, challenges, applies, and checks readiness.`
    : 'Pick a rung from the list to begin.';
  renderChat($('l2ChatLog'), state.trainMessages);
  renderCertTarget();
}

async function startTrainingChat() {
  const it = activeItem();
  if (!it) return;
  state.trainMessages = [{ role: 'assistant', content: `Let's work through "${it.label}". What do you already know about it, and where would you like to start?` }];
  renderChat($('l2ChatLog'), state.trainMessages);
}

async function submitTrainingChat(e) {
  e.preventDefault();
  const input = $('l2ChatInput');
  const content = input.value.trim();
  if (!content) return;
  const it = activeItem();
  if (!state.trainMessages.length) await startTrainingChat();
  state.trainMessages.push({ role: 'user', content });
  input.value = '';
  renderChat($('l2ChatLog'), state.trainMessages);
  const raw = await askModel({
    messages: state.trainMessages,
    systemPrompt: `You are a training guide for "${it.label}" in the ${focus().label} ladder of the AESOP AI Academy. Teach through guided conversation — ask, give examples, apply, and surface limitations. Engage until the learner demonstrates sufficient understanding. When ready to end, write "COURSE_COMPLETE" on its own final line.`,
    maxTokens: 700
  });
  const isDone = raw.includes('COURSE_COMPLETE');
  const visible = raw.replace(/COURSE_COMPLETE\s*$/gm, '').replace(/<!--[\s\S]*?-->/g, '').trim();
  state.trainMessages.push({ role: 'assistant', content: visible });
  renderChat($('l2ChatLog'), state.trainMessages);
  if (isDone) markComplete();
}

function markComplete() {
  const it = activeItem(); if (!it) return;
  const key = `${focus().pathway}:${it.id}`;
  state.completed[key] = true;
  recordCompletion({
    pathway: focus().pathway, itemId: it.id, itemType: focus().label,
    itemName: it.label, level: '', status: 'completed', source: 'ai_verified',
    completedAt: new Date().toISOString()
  }).catch((err) => console.warn('recordCompletion failed (kept local)', err));
  saveLearnerProgress(focus().pathway, { version: 'v1', lastItemId: it.id, lastItemLabel: it.label }).catch(() => {});
  renderRail(); renderMarketing(); renderProfile();
}

// =============================================================================
// ASSESSMENT — placement conversation, collapse to hub on complete
// =============================================================================
function setupAssessment() {
  $('l2StartPlacement')?.addEventListener('click', startPlacement);
  $('l2ResetPlacement')?.addEventListener('click', () => {
    state.assessMessages = []; state.placement = null;
    document.body.classList.remove('placement-complete');
    $('l2PlacementStatus').textContent = 'Not placed yet';
    renderChat($('l2AssessLog'), state.assessMessages);
    renderPlacementProgress();
  });
  $('l2AssessForm')?.addEventListener('submit', submitAssessment);
}

function startPlacement() {
  if (!placementEngine) return;
  state.assessMessages = [{ role: 'assistant', content: placementEngine.placementOpener() }];
  renderChat($('l2AssessLog'), state.assessMessages);
  $('l2AssessInput')?.focus();
  renderPlacementProgress();
}

function learnerTurns() { return state.assessMessages.filter((m) => m.role === 'user').length; }

async function submitAssessment(e) {
  e.preventDefault();
  if (!placementEngine) return;
  const input = $('l2AssessInput');
  const content = input.value.trim();
  if (!content) return;
  if (!state.assessMessages.length) startPlacement();
  state.assessMessages.push({ role: 'user', content });
  input.value = '';
  renderChat($('l2AssessLog'), state.assessMessages);
  renderPlacementProgress();
  const raw = await askModel({
    messages: state.assessMessages,
    systemPrompt: placementEngine.buildSystemPrompt({ languageLabel: 'English' }),
    maxTokens: 800
  });
  const { placement, visibleText } = placementEngine.parsePlacementResponse(raw);
  state.assessMessages.push({ role: 'assistant', content: visibleText });
  renderChat($('l2AssessLog'), state.assessMessages);
  renderPlacementProgress();
  if (placementEngine.shouldApplyPlacement(placement, learnerTurns())) applyPlacement(placement);
}

function applyPlacement(placement) {
  state.placement = placement;
  $('l2PlacementStatus').textContent = 'Placement complete';
  $('l2PlacementSummary').textContent = placement.reasoning || 'Your placed-out tiers and assigned rungs are saved.';
  document.body.classList.add('placement-complete');
  saveLearnerProgress(focus().pathway, {
    version: 'v1',
    placement: { ...placement }
  }).catch(() => {});
  renderMarketing();
}

function renderPlacementProgress() {
  $('l2AssessTurns').textContent = `${learnerTurns()} responses`;
  const pct = Math.min(100, Math.round((learnerTurns() / 6) * 100));
  const bar = $('l2AssessProgressBar');
  if (bar) bar.style.width = `${pct}%`;
}

// =============================================================================
// CERTIFICATION — config, gates, examiner conversation, validation, record
// =============================================================================
function setupCertification() {
  $('l2CertTierSelect')?.addEventListener('change', () => { renderAuthGates(); renderCertConfig(); });
  $('l2CertDepthSelect')?.addEventListener('change', renderCertTarget);
  $('l2IdentitySelect')?.addEventListener('change', () => {
    state.identityGate.levelId = $('l2IdentitySelect').value;
    renderIdentityGate();
  });
  $('l2ProctoringSelect')?.addEventListener('change', () => { state.identityGate.proctoringId = $('l2ProctoringSelect').value; });
  $('l2IdentityAttest')?.addEventListener('change', () => { state.identityGate.identitySigned = $('l2IdentityAttest').checked; renderIdentityGate(); });
  $('l2AdultAttest')?.addEventListener('change', () => { state.identityGate.adultAttested = $('l2AdultAttest').checked; renderAuthGates(); });
  $('l2AccountSignIn')?.addEventListener('click', () => signIn(false));
  $('l2AccountCreate')?.addEventListener('click', () => signIn(true));
  $('l2AccountSignOut')?.addEventListener('click', signOut);
  $('l2StartCert')?.addEventListener('click', startCertification);
  $('l2CertForm')?.addEventListener('submit', submitCertChat);
  $('l2FinalizeCert')?.addEventListener('click', () => finalizeCertification(true));
  $('l2EndCert')?.addEventListener('click', endCertification);
}

function renderCertConfig() {
  const tierSel = $('l2CertTierSelect');
  if (tierSel && !tierSel.dataset.filled) {
    tierSel.innerHTML = EDUCATION_TIERS.map((t) => `<option value="${t}">${t}</option>`).join('');
    tierSel.dataset.filled = '1';
  }
  const depthSel = $('l2CertDepthSelect');
  depthSel.innerHTML = focus().CERT_DEPTHS.map((d) => `<option value="${d.label}">${d.label}</option>`).join('');

  const idSel = $('l2IdentitySelect');
  idSel.innerHTML = focus().IDENTITY_LEVELS.map((lvl) => `<option value="${lvl.id}">${lvl.label}</option>`).join('');
  if (!state.identityGate.levelId) state.identityGate.levelId = focus().IDENTITY_LEVELS[0]?.id;
  idSel.value = state.identityGate.levelId;

  const procSel = $('l2ProctoringSelect');
  procSel.innerHTML = PROCTORING_MODES.map((p) => `<option value="${p.id}">${p.label}</option>`).join('');
  procSel.value = state.identityGate.proctoringId;

  renderIdentityGate();
  renderCertTarget();
}

function selectedDepth() { return focus().depthForLabel($('l2CertDepthSelect').value); }
function selectedLevel() { return $('l2CertTierSelect').value || EDUCATION_TIERS[0]; }

function renderCertTarget() {
  const it = activeItem();
  const depth = selectedDepth();
  $('l2CertTarget').textContent = it
    ? `${it.label} — ${selectedLevel()}, ${depth ? depth.label : ''}`
    : 'Choose a rung in Training, then set your level here.';
}

function renderIdentityGate() {
  const gate = { ...state.identityGate, account: state.authUser };
  let resolved;
  try { resolved = focus().resolveIdentityLevel(gate); } catch { resolved = null; }
  const requiresSig = resolved?.requiresSignature;
  // proctoring field visible for the external/authenticated choice or when sig required
  const showProc = true;
  $('l2ProctoringField').hidden = !showProc;
  // attestation visible when the chosen level needs a signature
  $('l2IdentityAttestLabel').hidden = !requiresSig;
  const notice = $('l2IdentityNotice');
  if (resolved) {
    notice.hidden = false;
    notice.textContent = (focus().identityLevelById(state.identityGate.levelId)?.description) ||
      (resolved.requiresSignature ? 'This level requires an identity attestation.' : 'Self-attested level.');
  }
}

// --- simplified account gate (prototype auth: local identity bound to email) ---
function renderAuthGates() {
  const signedIn = Boolean(state.authUser);
  const adultTier = ADULT_TIERS.has(selectedLevel());

  // Training gate: show when an account would be needed to persist
  const trainGate = $('l2TrainingGate');
  if (trainGate) trainGate.hidden = signedIn;

  // Certification account gate
  const acctGate = $('l2AccountGate');
  const acctForm = $('l2AccountForm');
  const status = $('l2AccountStatus');
  const msg = $('l2AccountMsg');
  if (acctGate) acctGate.hidden = false;
  if (status) status.textContent = signedIn ? `Signed in: ${state.authUser.email}` : adultTier ? 'Adult account required' : 'Account optional';
  if (msg) msg.textContent = signedIn
    ? 'Your certifications and transcript events are saved to this account.'
    : adultTier ? 'Adult education tiers require a verified account before certifying.'
      : 'Sign in to save certifications to your transcript (optional for non-adult tiers).';
  if (acctForm) acctForm.hidden = signedIn;
  $('l2AccountSignOut').hidden = !signedIn;
  $('l2AdultAttestLabel').hidden = !adultTier;
}

// --- real Firebase auth: email-link sign-up + password sign-in --------------
function initFirebaseAuth() {
  try {
    // Reuse the app the data layer created; never double-init (it would clash).
    const app = getApps().length ? getApp() : initializeApp(FIREBASE_CONFIG);
    auth = getAuth(app);
    onAuthStateChanged(auth, onAuthChange);
  } catch (e) {
    console.warn('[ladder2] Firebase auth unavailable', e);
  }
}

function onAuthChange(user) {
  if (user) {
    state.authUser = { email: user.email, uid: user.uid, emailVerified: user.emailVerified };
    localStorage.setItem('aesop-learner-id', user.uid);
    initDataLayer({ learnerId: user.uid }).catch(() => {});
  } else {
    state.authUser = null;
  }
  localStorage.removeItem(LS_AUTH);   // retire the old local-prototype token
  renderAuthGates();
  renderHeroSignup();
}

function setStatus(id, message, kind) {
  const n = $(id);
  if (!n) return;
  n.hidden = !message;
  n.dataset.state = kind || '';
  if (kind === 'ok') n.innerHTML = message; else n.textContent = message;
}

// Send the passwordless verification link; it lands on create-account.html,
// which finishes sign-in (email verified) and collects a password.
async function sendVerification(email, statusId) {
  const clean = String(email || '').trim();
  if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(clean)) {
    setStatus(statusId, 'Enter a valid email address.', 'error');
    return;
  }
  if (!auth) {
    setStatus(statusId, 'Sign-up is unavailable right now. Please try again shortly.', 'error');
    return;
  }
  try {
    const actionCodeSettings = { url: `${location.origin}/theladder/create-account.html`, handleCodeInApp: true };
    await sendSignInLinkToEmail(auth, clean, actionCodeSettings);
    localStorage.setItem(LS_EMAIL, clean);
    setStatus(statusId, `Check <b>${escapeHtml(clean)}</b> for a link to verify your email and finish creating your account.`, 'ok');
  } catch (e) {
    setStatus(statusId, `Could not send the link (${e.code || 'error'}). Please try again.`, 'error');
  }
}

async function passwordSignIn(email, password, statusId) {
  if (!auth) return;
  try {
    await signInWithEmailAndPassword(auth, String(email).trim(), password);
    setStatus(statusId, '', '');
  } catch (e) {
    setStatus(statusId, 'Sign in failed — check your email and password.', 'error');
  }
}

// Certification-gate buttons reuse the same auth: Create -> email link, Sign in -> password.
function signIn(creating) {
  if (creating) { sendVerification($('l2AccountEmail')?.value, 'l2AccountError'); return; }
  passwordSignIn($('l2AccountEmail')?.value, $('l2AccountPassword')?.value, 'l2AccountError');
}

function signOut() {
  if (auth) fbSignOut(auth).catch(() => {});
}

// Hero sign-up / sign-in form (bottom of the marketing section).
function setupAuth() {
  $('l2SignupForm')?.addEventListener('submit', (e) => { e.preventDefault(); sendVerification($('l2SignupEmail')?.value, 'l2SignupMsg'); });
  $('l2SigninToggle')?.addEventListener('click', (e) => { e.preventDefault(); const f = $('l2SigninForm'); if (f) f.style.display = (f.style.display === 'flex') ? 'none' : 'flex'; });
  $('l2SigninForm')?.addEventListener('submit', (e) => { e.preventDefault(); passwordSignIn($('l2SigninEmail')?.value, $('l2SigninPw')?.value, 'l2SignupMsg'); });
  $('l2HeroSignOut')?.addEventListener('click', signOut);
}

function renderHeroSignup() {
  const signedIn = Boolean(state.authUser);
  // The forms / signed-in box use display:flex (and the link inline-block) in CSS,
  // which overrides the [hidden] attribute — so toggle inline display directly.
  const setDisp = (id, shown, mode) => { const n = $(id); if (n) n.style.display = shown ? mode : 'none'; };
  setDisp('l2SignupForm', !signedIn, 'flex');
  setDisp('l2SigninToggle', !signedIn, 'inline-block');
  setDisp('l2SigninForm', false, 'flex');       // collapsed by default; the toggle opens it
  setDisp('l2SignedIn', signedIn, 'flex');       // sign-out only when actually signed in
  if (signedIn) setText('l2SignedInEmail', state.authUser.email || '');
}

async function startCertification() {
  const it = activeItem();
  if (!it) { alert('Pick a rung in Training first.'); return; }
  const adultTier = ADULT_TIERS.has(selectedLevel());
  if (adultTier && !state.authUser) { document.getElementById('l2AccountGate')?.scrollIntoView({ behavior: 'smooth' }); return; }

  const depth = selectedDepth();
  const certItem = focus().certItemForGroup(activeGroup(), it);
  const blueprint = focus().buildBlueprint({ item: certItem, level: selectedLevel(), depth });
  blueprint.languageLabel = 'English';
  const context = focus().buildCertContext({ item: certItem, depth, learnerId: state.authUser?.uid || '' });
  context.identityAssurance = focus().buildIdentityAssurance(new Date().toISOString(), { ...state.identityGate, account: state.authUser });
  context.proctoringMode = state.identityGate.proctoringId;

  state.activeCert = { item: it, level: selectedLevel(), depth, blueprint, context };
  state.certMessages = [{ role: 'user', content: 'I am ready to begin the certification exam.' }];
  $('l2CertModeBar').hidden = false;
  $('l2CertExamSummary').textContent = `Examining: ${it.label} — ${selectedLevel()}, ${depth.label}. An independent model validates the result before any credential is recorded.`;
  renderChat($('l2CertLog'), []);
  await callExaminer();
}

async function callExaminer() {
  if (!state.activeCert) return;
  const raw = await askModel({
    messages: state.certMessages,
    systemPrompt: certificationEngine.buildExaminerSystemPrompt(state.activeCert.blueprint),
    maxTokens: 900
  });
  const { certificationResult, rubricDimensions, visibleText } = certificationEngine.parseExaminerResponse(raw);
  state.certMessages.push({ role: 'assistant', content: visibleText });
  renderChat($('l2CertLog'), state.certMessages.filter((m) => m.content));
  state._pendingResult = certificationResult;
  state._pendingRubric = rubricDimensions;
  if (certificationResult) finalizeCertification(false);
}

async function submitCertChat(e) {
  e.preventDefault();
  if (!state.activeCert) { alert('Start a certification above first.'); return; }
  const input = $('l2CertInput');
  const content = input.value.trim();
  if (!content) return;
  state.certMessages.push({ role: 'user', content });
  input.value = '';
  renderChat($('l2CertLog'), state.certMessages.filter((m) => m.content));
  await callExaminer();
}

async function finalizeCertification(askForDetermination) {
  if (!state.activeCert) return;
  if (askForDetermination && !state._pendingResult) {
    state.certMessages.push({ role: 'user', content: 'Please render your final determination now with the rubric evaluation and result marker.' });
    await callExaminer();
    return;
  }
  if (!state._pendingResult) return;
  appendSystemNote('Validating with an independent second model…');
  const outcome = await certificationEngine.recordCertificationResult({
    context: state.activeCert.context,
    result: state._pendingResult,
    conversationMessages: state.certMessages,
    hooks: {
      buildIdentityAssurance: (earnedAt) => focus().buildIdentityAssurance(earnedAt, { ...state.identityGate, account: state.authUser }),
      onCredential: (record) => {
        const packet = certificationEngine.buildEvidencePacket({
          context: state.activeCert.context, result: state._pendingResult,
          rubricDimensions: state._pendingRubric, validation: record.validation,
          extra: { proctoringMode: state.identityGate.proctoringId }
        });
        packet.pathway = focus().pathway;
        recordCertification(packet, record.validation).catch((err) => console.warn('recordCertification failed', err));
      }
    }
  });
  reportOutcome(outcome);
}

function reportOutcome(outcome) {
  const map = {
    awarded: '✅ Credential awarded — validated by an independent model and written to your transcript.',
    not_awarded: 'Validation passed, but the result did not meet the certification bar this time.',
    validation_failed: '⚠️ The independent validator did not confirm the result, so no credential was recorded.',
    retry_offered: 'You may answer a few follow-up questions to complete validation.'
  };
  appendSystemNote(map[outcome?.outcome] || 'Certification flow complete.');
  if (outcome?.outcome === 'awarded') { renderMarketing(); renderProfile(); }
  state._pendingResult = null; state._pendingRubric = null;
}

function appendSystemNote(text) {
  const el = $('l2CertLog');
  el.insertAdjacentHTML('beforeend', `<div class="l2-msg l2-msg--system"><div class="l2-msg__body">${escapeHtml(text)}</div></div>`);
  el.scrollTop = el.scrollHeight;
}

function endCertification() {
  state.activeCert = null; state.certMessages = []; state._pendingResult = null;
  $('l2CertModeBar').hidden = true;
  $('l2CertExamSummary').textContent = 'Start a certification above to begin the examined conversation.';
  renderChat($('l2CertLog'), []);
}

// =============================================================================
// MARKETING / PROFILE
// =============================================================================
function totalCompleted() { return Object.keys(state.completed).length; }
function certCount() { return (state._record?.ladderCertifications || []).length; }

function renderMarketing() {
  // Marketing hero stats/ribbons were removed; these setters are no-ops if the
  // elements are absent. Kept guarded so the live progress shows if re-added.
  const total = state.groups.reduce((n, g) => n + g.items.length, 0);
  setText('l2StatCourses', `${Object.keys(state.completed).filter((k) => k.startsWith(`${focus().pathway}:`)).length} / ${total}`);
  setText('l2StatTiers', String(state.placement?.grantedTierIds?.length || 0));
  const certs = state._record?.ladderCertifications || [];
  const byDepth = (d) => certs.filter((c) => (c.testDepth || c.certificationTier || '').toLowerCase().includes(d)).length;
  setText('l2StatCertified', String(byDepth('cert')));
  setText('l2StatExpert', String(byDepth('expert')));
  setText('l2StatMastery', String(byDepth('master')));
  setText('l2HeroCertCount', String(certs.length));
}

// Replace the "L" in the LADDER wordmark with an actual ladder (two rails +
// rungs forming the stem, plus the L's foot). Pure DOM + inline SVG so no CSS
// file is touched; scales with the headline via em units, inherits the navy.
function renderLadderL() {
  const h1 = document.querySelector('#marketing h1');
  if (!h1 || h1.dataset.ladderL) return;
  const node = [...h1.childNodes].find((n) => n.nodeType === 3 && n.textContent.includes('L'));
  if (!node) return;
  const txt = node.textContent;
  const idx = txt.indexOf('L');
  if (idx < 0) return;
  h1.setAttribute('aria-label', h1.textContent.trim());   // keep "The Ladder AI" for screen readers
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.setAttribute('viewBox', '0 0 62 100');
  svg.setAttribute('aria-hidden', 'true');
  svg.style.cssText = 'height:0.72em;width:auto;vertical-align:baseline;fill:currentColor;margin:0 0.04em;';
  svg.innerHTML =
    '<rect x="6" y="0" width="9" height="84"/>' +       // left rail
    '<rect x="26" y="0" width="9" height="84"/>' +      // right rail
    '<rect x="13" y="11" width="15" height="7"/>' +     // rungs (evenly spaced, clear of the foot)
    '<rect x="13" y="28" width="15" height="7"/>' +
    '<rect x="13" y="45" width="15" height="7"/>' +
    '<rect x="13" y="62" width="15" height="7"/>' +
    '<rect x="6" y="79" width="56" height="21"/>';      // foot of the L (matches the E's bar thickness)
  const frag = document.createDocumentFragment();
  frag.append(document.createTextNode(txt.slice(0, idx)), svg, document.createTextNode(txt.slice(idx + 1)));
  h1.replaceChild(frag, node);
  h1.dataset.ladderL = '1';
}

function setupProfile() {
  $('l2FeedbackForm')?.addEventListener('submit', (e) => {
    e.preventDefault();
    const entry = {
      type: $('l2FeedbackType').value,
      email: $('l2FeedbackEmail').value.trim(),
      message: $('l2FeedbackMessage').value.trim(),
      at: new Date().toISOString(),
      focus: state.focusId
    };
    if (!entry.message) return;
    const log = JSON.parse(localStorage.getItem(LS_FEEDBACK) || '[]');
    log.push(entry);
    localStorage.setItem(LS_FEEDBACK, JSON.stringify(log));
    $('l2FeedbackForm').reset();
    const sent = $('l2FeedbackSent'); sent.hidden = false;
    setTimeout(() => { sent.hidden = true; }, 4000);
  });
}

function renderProfile() {
  setText('l2ProfileCertCount', String(certCount()));
  const it = activeItem();
  if (it) {
    setText('l2ActiveCourseTitle', it.label);
    setText('l2ActiveCourseMeta', `${focus().label} · ${activeGroup()?.label || ''}`);
  }
}

init();
