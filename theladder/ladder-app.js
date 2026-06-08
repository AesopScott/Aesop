import { initializeApp } from 'https://www.gstatic.com/firebasejs/10.12.0/firebase-app.js';
import { getFirestore, doc, getDoc, setDoc } from 'https://www.gstatic.com/firebasejs/10.12.0/firebase-firestore.js';
import { FIREBASE_CONFIG } from '/ai-academy/js/firebase-config.js';
import { DEFAULT_RESOURCES, LADDER_TIERS, LADDER_VERSION, LANGUAGES } from './ladder-data.js';

const PROXY_URL = '/aesop-api/proxy.php';
const LS_ID = 'aesop-learner-id';
const LS_STATE = 'aesop-ladder-state';

const app = initializeApp(FIREBASE_CONFIG);
const db = getFirestore(app);

const state = {
  learnerId: localStorage.getItem(LS_ID) || '',
  language: 'en',
  customLanguage: '',
  goal: 'general',
  role: 'self-directed learner',
  activeTierId: LADDER_TIERS[0].id,
  activeTopicId: LADDER_TIERS[0].topics[0].id,
  messages: [],
  progress: {
    completedTopics: {},
    completedLabs: {},
    vocabulary: {},
    transcriptEvents: []
  }
};

const el = {
  languageSelect: document.getElementById('languageSelect'),
  customLanguageInput: document.getElementById('customLanguageInput'),
  learnerIdLabel: document.getElementById('learnerIdLabel'),
  learnerLookup: document.getElementById('learnerLookup'),
  lookupBtn: document.getElementById('lookupBtn'),
  newLearnerBtn: document.getElementById('newLearnerBtn'),
  goalSelect: document.getElementById('goalSelect'),
  roleInput: document.getElementById('roleInput'),
  progressBar: document.getElementById('progressBar'),
  progressText: document.getElementById('progressText'),
  tierList: document.getElementById('tierList'),
  activeTierLabel: document.getElementById('activeTierLabel'),
  activeTopicTitle: document.getElementById('activeTopicTitle'),
  completeTopicBtn: document.getElementById('completeTopicBtn'),
  vocabCount: document.getElementById('vocabCount'),
  vocabList: document.getElementById('vocabList'),
  resourceList: document.getElementById('resourceList'),
  researchBtn: document.getElementById('researchBtn'),
  startConversationBtn: document.getElementById('startConversationBtn'),
  chatLog: document.getElementById('chatLog'),
  chatForm: document.getElementById('chatForm'),
  chatInput: document.getElementById('chatInput'),
  labScenario: document.getElementById('labScenario'),
  labChecklist: document.getElementById('labChecklist'),
  completeLabBtn: document.getElementById('completeLabBtn'),
  transcriptList: document.getElementById('transcriptList'),
  exportTranscriptBtn: document.getElementById('exportTranscriptBtn')
};

function generateLearnerId() {
  const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
  let code = '';
  for (let i = 0; i < 4; i += 1) code += chars[Math.floor(Math.random() * chars.length)];
  return `AESOP-${code}`;
}

function topicKey(topicId) {
  return `${LADDER_VERSION}:${topicId}`;
}

function getActiveTier() {
  return LADDER_TIERS.find((tier) => tier.id === state.activeTierId) || LADDER_TIERS[0];
}

function getActiveTopic() {
  const tier = getActiveTier();
  return tier.topics.find((topic) => topic.id === state.activeTopicId) || tier.topics[0];
}

function allTopics() {
  return LADDER_TIERS.flatMap((tier) => tier.topics);
}

function saveLocal() {
  localStorage.setItem(LS_STATE, JSON.stringify({
    language: state.language,
    customLanguage: state.customLanguage,
    goal: state.goal,
    role: state.role,
    activeTierId: state.activeTierId,
    activeTopicId: state.activeTopicId,
    progress: state.progress
  }));
}

async function saveRemote() {
  if (!state.learnerId) return;
  try {
    await setDoc(doc(db, 'learners', state.learnerId), {
      learnerId: state.learnerId,
      lastActiveAt: new Date().toISOString(),
      ladderProgress: {
        version: LADDER_VERSION,
        language: state.language,
        customLanguage: state.customLanguage,
        goal: state.goal,
        role: state.role,
        activeTierId: state.activeTierId,
        activeTopicId: state.activeTopicId,
        completedTopics: state.progress.completedTopics,
        completedLabs: state.progress.completedLabs,
        vocabulary: state.progress.vocabulary,
        transcriptEvents: state.progress.transcriptEvents
      }
    }, { merge: true });
  } catch (error) {
    console.warn('Could not save ladder progress:', error);
  }
}

async function persist() {
  saveLocal();
  await saveRemote();
}

async function loadRemote(learnerId) {
  try {
    const snap = await getDoc(doc(db, 'learners', learnerId));
    if (!snap.exists()) {
      await setDoc(doc(db, 'learners', learnerId), {
        learnerId,
        createdAt: new Date().toISOString(),
        courseProgress: {},
        ladderProgress: {
          version: LADDER_VERSION,
          createdAt: new Date().toISOString()
        }
      }, { merge: true });
      return;
    }

    const data = snap.data();
    if (!data.ladderProgress) return;
    const ladder = data.ladderProgress;
    state.language = ladder.language || state.language;
    state.customLanguage = ladder.customLanguage || state.customLanguage;
    state.goal = ladder.goal || state.goal;
    state.role = ladder.role || state.role;
    state.activeTierId = ladder.activeTierId || state.activeTierId;
    state.activeTopicId = ladder.activeTopicId || state.activeTopicId;
    state.progress.completedTopics = ladder.completedTopics || {};
    state.progress.completedLabs = ladder.completedLabs || {};
    state.progress.vocabulary = ladder.vocabulary || {};
    state.progress.transcriptEvents = ladder.transcriptEvents || [];
  } catch (error) {
    console.warn('Could not load ladder progress:', error);
  }
}

function loadLocal() {
  try {
    const raw = localStorage.getItem(LS_STATE);
    if (!raw) return;
    const saved = JSON.parse(raw);
    state.language = saved.language || state.language;
    state.customLanguage = saved.customLanguage || state.customLanguage;
    state.goal = saved.goal || state.goal;
    state.role = saved.role || state.role;
    state.activeTierId = saved.activeTierId || state.activeTierId;
    state.activeTopicId = saved.activeTopicId || state.activeTopicId;
    state.progress = saved.progress || state.progress;
  } catch (error) {
    console.warn('Could not load local ladder state:', error);
  }
}

function addTranscript(eventType, title, detail) {
  state.progress.transcriptEvents.unshift({
    eventType,
    title,
    detail,
    topicId: getActiveTopic().id,
    topicTitle: getActiveTopic().title,
    tierTitle: getActiveTier().title,
    timestamp: new Date().toISOString(),
    evidence: 'self-reported'
  });
  state.progress.transcriptEvents = state.progress.transcriptEvents.slice(0, 80);
}

function renderLanguages() {
  el.languageSelect.innerHTML = LANGUAGES.map((language) => (
    `<option value="${language.code}">${language.label}</option>`
  )).join('');
  el.languageSelect.value = state.language;
}

function renderLearner() {
  el.learnerIdLabel.textContent = state.learnerId || 'Not started';
  el.learnerLookup.value = state.learnerId || '';
}

function completedCount() {
  return Object.keys(state.progress.completedTopics || {}).length;
}

function renderProgress() {
  const count = completedCount();
  const total = allTopics().length;
  const pct = total ? Math.round((count / total) * 100) : 0;
  el.progressBar.style.width = `${pct}%`;
  el.progressText.textContent = `${count} of ${total} rungs completed`;
}

function renderTiers() {
  el.tierList.innerHTML = LADDER_TIERS.map((tier) => {
    const done = tier.topics.filter((topic) => state.progress.completedTopics[topicKey(topic.id)]).length;
    const active = tier.id === state.activeTierId ? ' active' : '';
    return `
      <div class="tier-item">
        <button class="tier-button${active}" type="button" data-tier-id="${tier.id}" style="--tier-accent:${tier.accent}">
          <span class="tier-number">${tier.order}</span>
          <span class="tier-meta">
            <strong>${tier.name}</strong>
            <small>${tier.title}</small>
          </span>
          <span class="tier-progress">${done}/${tier.topics.length}</span>
        </button>
      </div>
    `;
  }).join('');

  el.tierList.querySelectorAll('[data-tier-id]').forEach((button) => {
    button.addEventListener('click', () => {
      const tier = LADDER_TIERS.find((item) => item.id === button.dataset.tierId);
      state.activeTierId = tier.id;
      state.activeTopicId = tier.topics[0].id;
      state.messages = [];
      persist();
      render();
    });
  });
}

function renderTopicPicker(tier) {
  const existing = document.querySelector('.topic-strip');
  if (existing) existing.remove();

  const strip = document.createElement('div');
  strip.className = 'topic-strip';
  strip.style.cssText = 'display:flex;gap:.45rem;overflow:auto;padding:.75rem;background:#fff;border:1px solid var(--ladder-line);border-top:0';
  strip.innerHTML = tier.topics.map((topic) => {
    const done = state.progress.completedTopics[topicKey(topic.id)] ? 'done' : '';
    const active = topic.id === state.activeTopicId ? 'active' : '';
    return `<button class="secondary ${done} ${active}" type="button" data-topic-id="${topic.id}" title="${topic.title}">${topic.order}</button>`;
  }).join('');

  document.querySelector('.topic-head').after(strip);
  strip.querySelectorAll('[data-topic-id]').forEach((button) => {
    button.addEventListener('click', () => {
      state.activeTopicId = button.dataset.topicId;
      state.messages = [];
      persist();
      render();
    });
  });
}

function renderVocabulary(tier) {
  el.vocabCount.textContent = `${tier.vocabulary.length} terms`;
  el.vocabList.innerHTML = tier.vocabulary.map((term) => {
    const key = `${tier.id}:${term}`;
    const done = state.progress.vocabulary[key] ? ' done' : '';
    return `<button class="vocab-pill${done}" type="button" data-vocab="${term}">${term}</button>`;
  }).join('');

  el.vocabList.querySelectorAll('[data-vocab]').forEach((button) => {
    button.addEventListener('click', async () => {
      const key = `${tier.id}:${button.dataset.vocab}`;
      state.progress.vocabulary[key] = !state.progress.vocabulary[key];
      if (state.progress.vocabulary[key]) {
        addTranscript('vocabulary_marked', button.dataset.vocab, `Marked vocabulary term in ${tier.title}.`);
      }
      await persist();
      render();
    });
  });
}

function resourcesForTopic(topic) {
  const title = topic.title.toLowerCase();
  return DEFAULT_RESOURCES.filter((resource) => resource.topicHints.some((hint) => title.includes(hint.toLowerCase())));
}

function renderResources(topic) {
  const resources = resourcesForTopic(topic);
  const base = resources.length ? resources : DEFAULT_RESOURCES.slice(0, 3);
  el.resourceList.innerHTML = base.map((resource) => (
    `<a class="resource-chip" href="${resource.url}" target="_blank" rel="noopener">${resource.label}</a>`
  )).join('');
}

function labChecklist(topic) {
  return [
    `Explain ${topic.title} in your own words.`,
    'Use one researched resource or video to challenge your first explanation.',
    'Apply the idea to your selected goal or role.',
    'Identify one risk, limitation, or failure mode.',
    'Ask the AI guide to decide whether you are ready to mark the rung confident.'
  ];
}

function renderLab(topic) {
  el.labScenario.textContent = `Lab: use AI as a guarded coach to investigate "${topic.title}", then produce a short evidence trail that shows discovery, critical thinking, and application.`;
  el.labChecklist.innerHTML = labChecklist(topic).map((item) => `<li>${item}</li>`).join('');
}

function renderChat() {
  if (!state.messages.length) {
    el.chatLog.innerHTML = '<div class="message assistant"><strong>Guide</strong>Select Start to begin a guided conversation for this rung.</div>';
    return;
  }
  el.chatLog.innerHTML = state.messages.map((message) => (
    `<div class="message ${message.role === 'user' ? 'user' : 'assistant'}"><strong>${message.role === 'user' ? 'You' : 'Guide'}</strong>${escapeHtml(message.content)}</div>`
  )).join('');
  el.chatLog.scrollTop = el.chatLog.scrollHeight;
}

function renderTranscript() {
  if (!state.progress.transcriptEvents.length) {
    el.transcriptList.innerHTML = '<div class="transcript-event"><strong>No events yet</strong><small>Complete conversations, vocabulary, labs, or rungs to build a transcript.</small></div>';
    return;
  }

  el.transcriptList.innerHTML = state.progress.transcriptEvents.map((event) => (
    `<div class="transcript-event"><strong>${event.title}</strong><small>${event.eventType} - ${new Date(event.timestamp).toLocaleString()}</small><p>${event.detail}</p></div>`
  )).join('');
}

function renderTopic() {
  const tier = getActiveTier();
  const topic = getActiveTopic();
  el.activeTierLabel.textContent = `${tier.name} - ${topic.id}`;
  el.activeTopicTitle.textContent = topic.title;
  el.completeTopicBtn.textContent = state.progress.completedTopics[topicKey(topic.id)] ? 'Confident' : 'Mark confident';
  renderTopicPicker(tier);
  renderVocabulary(tier);
  renderResources(topic);
  renderLab(topic);
  renderChat();
}

function renderControls() {
  el.languageSelect.value = state.language;
  el.customLanguageInput.value = state.customLanguage || '';
  el.customLanguageInput.style.display = state.language === 'custom' ? '' : 'none';
  el.goalSelect.value = state.goal;
  el.roleInput.value = state.role;
}

function render() {
  renderLearner();
  renderControls();
  renderProgress();
  renderTiers();
  renderTopic();
  renderTranscript();
}

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;')
    .replace(/\n/g, '<br>');
}

function systemPromptFor(topic, tier) {
  const language = state.language === 'custom'
    ? (state.customLanguage || 'the learner selected language')
    : (LANGUAGES.find((item) => item.code === state.language)?.label || 'English');
  return `You are The Ladder guide inside AESOP AI Academy. You are strictly scoped to the selected topic: ${topic.title}.

Learner role: ${state.role}.
Learner goal: ${state.goal}.
Tier: ${tier.name} - ${tier.title}.
Preferred language: ${language}. Translate your learner-facing responses into this language unless the learner asks otherwise.

Use this guarded teaching pattern:
1. Diagnose what the learner already understands.
2. Ask vocabulary questions using relevant terms from this tier.
3. Force discovery by asking the learner to compare, question, and verify.
4. Push application to the learner's role or goal.
5. Ask for one risk, limitation, or misconception.
6. End by telling the learner whether they are ready to mark the rung confident.

Do not act as a general assistant. If the learner goes off topic, warmly redirect them back to ${topic.title}. Do not simply lecture. Ask questions and require the learner to reason. Keep responses concise enough for an interactive learning session.`;
}

async function callGuide() {
  const topic = getActiveTopic();
  const tier = getActiveTier();
  try {
    const response = await fetch(PROXY_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        messages: state.messages,
        system_prompt: systemPromptFor(topic, tier),
        max_tokens: 700
      })
    });
    const data = await response.json();
    const text = data?.content?.[0]?.text || data?.error || 'The guide could not respond. Use practice mode: explain the topic, name one risk, and ask yourself what evidence would change your mind.';
    state.messages.push({ role: 'assistant', content: text });
  } catch (error) {
    state.messages.push({
      role: 'assistant',
      content: 'AI is temporarily unavailable. Practice mode: explain the topic in your own words, name one example, name one limitation, and decide what you still need to verify.'
    });
  }
  renderChat();
  await persist();
}

async function startConversation() {
  const topic = getActiveTopic();
  state.messages = [{
    role: 'user',
    content: `Start my guided conversation for "${topic.title}". Diagnose my current understanding first, then lead me through discovery, critical thinking, and application.`
  }];
  renderChat();
  await callGuide();
  addTranscript('guided_conversation_started', topic.title, `Started a guided conversation for ${topic.id}.`);
  await persist();
  renderTranscript();
}

async function submitChat(event) {
  event.preventDefault();
  const value = el.chatInput.value.trim();
  if (!value) return;
  state.messages.push({ role: 'user', content: value });
  el.chatInput.value = '';
  renderChat();
  await callGuide();
}

async function markTopicComplete() {
  const topic = getActiveTopic();
  state.progress.completedTopics[topicKey(topic.id)] = {
    status: 'confident',
    completedAt: new Date().toISOString(),
    language: state.language
  };
  addTranscript('topic_confident', topic.title, `Marked ${topic.id} confident on The Ladder.`);
  await persist();
  render();
}

async function markLabComplete() {
  const topic = getActiveTopic();
  state.progress.completedLabs[topicKey(topic.id)] = {
    status: 'completed',
    completedAt: new Date().toISOString(),
    evidence: 'self-reported'
  };
  addTranscript('lab_completed', `${topic.title} lab`, `Completed the guarded lab checklist for ${topic.id}.`);
  await persist();
  render();
}

function exportTranscript() {
  const payload = {
    learnerId: state.learnerId,
    ladderVersion: LADDER_VERSION,
    exportedAt: new Date().toISOString(),
    completedTopics: state.progress.completedTopics,
    completedLabs: state.progress.completedLabs,
    transcriptEvents: state.progress.transcriptEvents
  };
  const blob = new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement('a');
  anchor.href = url;
  anchor.download = `${state.learnerId || 'aesop'}-ladder-transcript.json`;
  anchor.click();
  URL.revokeObjectURL(url);
}

function findVideos() {
  const topic = getActiveTopic();
  const query = encodeURIComponent(`${topic.title} AI explained tutorial`);
  addTranscript('resource_discovery_requested', topic.title, `Requested YouTube discovery for "${topic.title}".`);
  persist();
  window.open(`https://www.youtube.com/results?search_query=${query}`, '_blank', 'noopener');
  renderTranscript();
}

function bindEvents() {
  el.languageSelect.addEventListener('change', async () => {
    state.language = el.languageSelect.value;
    await persist();
    renderControls();
  });

  el.customLanguageInput.addEventListener('change', async () => {
    state.customLanguage = el.customLanguageInput.value.trim();
    await persist();
  });

  el.goalSelect.addEventListener('change', async () => {
    state.goal = el.goalSelect.value;
    await persist();
  });

  el.roleInput.addEventListener('change', async () => {
    state.role = el.roleInput.value.trim() || 'self-directed learner';
    await persist();
  });

  el.lookupBtn.addEventListener('click', async () => {
    const id = el.learnerLookup.value.trim().toUpperCase();
    if (!id.startsWith('AESOP-')) return;
    state.learnerId = id;
    localStorage.setItem(LS_ID, id);
    await loadRemote(id);
    await persist();
    render();
  });

  el.newLearnerBtn.addEventListener('click', async () => {
    state.learnerId = generateLearnerId();
    localStorage.setItem(LS_ID, state.learnerId);
    try {
      await setDoc(doc(db, 'learners', state.learnerId), {
        learnerId: state.learnerId,
        createdAt: new Date().toISOString(),
        courseProgress: {}
      }, { merge: true });
    } catch (error) {
      console.warn('Could not create learner record immediately:', error);
    }
    await persist();
    render();
  });

  el.startConversationBtn.addEventListener('click', startConversation);
  el.chatForm.addEventListener('submit', submitChat);
  el.completeTopicBtn.addEventListener('click', markTopicComplete);
  el.completeLabBtn.addEventListener('click', markLabComplete);
  el.exportTranscriptBtn.addEventListener('click', exportTranscript);
  el.researchBtn.addEventListener('click', findVideos);
}

async function init() {
  loadLocal();
  renderLanguages();
  bindEvents();
  if (state.learnerId) await loadRemote(state.learnerId);
  render();
}

init();
