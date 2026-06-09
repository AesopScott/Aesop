// ---------------------------------------------------------------------------
// Lightweight identity-assurance gate for certification (Task 30)
// ---------------------------------------------------------------------------
// Gates ONLY certification attempts (not ordinary courses). Records an
// identityAssurance level into the certification evidence packet via the
// shared certification engine's buildIdentityAssurance hook. Reuses the
// Firebase email/password + 18+ adult attestation pattern from
// theladder/ladder-auth.js. No proctoring claims are made here.
//
// Three levels (mirrors ladder-auth.js IDENTITY_ASSURANCE_LEVELS minus the
// inactive proctored_verified tier):
//   self_attested     - learner claims the work, no identity check
//   account_bound     - bound to a signed-in AESOP account + learner record
//   identity_attested - signed adult attestation before the attempt

const LS_IDENTITY_ASSURANCE = 'aesop-use-cases-identity-assurance';

export const IDENTITY_ASSURANCE_LEVELS = [
  { id: 'self_attested', requiresAccount: false, requiresAttestation: true, labelKey: 'selfAttested', descKey: 'selfAttestedDesc' },
  { id: 'account_bound', requiresAccount: true, requiresAttestation: true, labelKey: 'accountBound', descKey: 'accountBoundDesc' },
  { id: 'identity_attested', requiresAccount: true, requiresAttestation: true, labelKey: 'identityAttested', descKey: 'identityAttestedDesc' }
];

let authContext = null;
let authUser = null;

// Lazy-load Firebase auth the same way the request flow lazy-loads Firestore.
async function getAuthContext() {
  if (authContext) return authContext;
  const [{ initializeApp, getApps, getApp }, authModule, configModule] = await Promise.all([
    import('https://www.gstatic.com/firebasejs/10.12.0/firebase-app.js'),
    import('https://www.gstatic.com/firebasejs/10.12.0/firebase-auth.js'),
    import('/ai-academy/js/firebase-config.js')
  ]);
  const app = getApps().length ? getApp() : initializeApp(configModule.FIREBASE_CONFIG);
  const auth = authModule.getAuth(app);
  authContext = {
    auth,
    signIn: authModule.signInWithEmailAndPassword,
    createUser: authModule.createUserWithEmailAndPassword,
    onAuthStateChanged: authModule.onAuthStateChanged
  };
  authContext.onAuthStateChanged(auth, (user) => { authUser = user; });
  return authContext;
}

export function getStoredAssuranceLevel() {
  try {
    return localStorage.getItem(LS_IDENTITY_ASSURANCE) || 'self_attested';
  } catch {
    return 'self_attested';
  }
}

function storeAssuranceLevel(levelId) {
  try {
    localStorage.setItem(LS_IDENTITY_ASSURANCE, levelId);
  } catch { /* localStorage may be blocked */ }
}

// Renders the identity step into `container` and resolves with the chosen
// assurance descriptor (or null when cancelled). `deps` supplies:
//   t(key)            -> translation lookup
//   escapeHtml(value) -> HTML escaper
//   account { uid, email } -> current data-layer account binding (if any)
export function promptIdentityAssurance(container, deps) {
  const { t, escapeHtml, account = {} } = deps;
  return new Promise((resolve) => {
    const selected = getStoredAssuranceLevel();
    const options = IDENTITY_ASSURANCE_LEVELS
      .map((level) => `<option value="${level.id}"${level.id === selected ? ' selected' : ''}>${escapeHtml(t(level.labelKey))}</option>`)
      .join('');

    container.hidden = false;
    container.innerHTML = `
      <div class="uc-identity-gate" role="group" aria-label="${escapeHtml(t('identityAssurance'))}">
        <strong>${escapeHtml(t('identityStepHeading'))}</strong>
        <span>${escapeHtml(t('identityStepBody'))}</span>
        <label class="uc-identity-field">
          <span>${escapeHtml(t('identityAssuranceLevel'))}</span>
          <select id="ucIdentityLevel">${options}</select>
        </label>
        <p id="ucIdentityLevelDesc" class="uc-identity-desc"></p>
        <div id="ucIdentityAccount" class="uc-identity-account" hidden>
          <label class="uc-identity-field">
            <span>${escapeHtml(t('emailUsername'))}</span>
            <input id="ucIdentityEmail" type="email" autocomplete="email" value="${escapeHtml(account.email || '')}">
          </label>
          <label class="uc-identity-field">
            <span>${escapeHtml(t('password'))}</span>
            <input id="ucIdentityPassword" type="password" autocomplete="current-password">
          </label>
          <div class="uc-identity-account-actions">
            <button type="button" id="ucIdentitySignIn">${escapeHtml(t('signIn'))}</button>
            <button type="button" id="ucIdentityCreate">${escapeHtml(t('createAccount'))}</button>
          </div>
          <p id="ucIdentityAccountStatus" class="uc-identity-desc"></p>
        </div>
        <label class="uc-identity-attest">
          <input id="ucIdentityAttest" type="checkbox">
          <span>${escapeHtml(t('adultAttestation'))}</span>
        </label>
        <p id="ucIdentityError" class="uc-identity-error" hidden></p>
        <div class="uc-identity-actions">
          <button type="button" id="ucIdentityCancel">${escapeHtml(t('cancel'))}</button>
          <button type="button" id="ucIdentityBegin">${escapeHtml(t('beginCertification'))}</button>
        </div>
      </div>
    `;

    const levelSelect = container.querySelector('#ucIdentityLevel');
    const levelDesc = container.querySelector('#ucIdentityLevelDesc');
    const accountBlock = container.querySelector('#ucIdentityAccount');
    const accountStatus = container.querySelector('#ucIdentityAccountStatus');
    const emailInput = container.querySelector('#ucIdentityEmail');
    const passwordInput = container.querySelector('#ucIdentityPassword');
    const attestCheck = container.querySelector('#ucIdentityAttest');
    const errorEl = container.querySelector('#ucIdentityError');

    function levelFor(id) {
      return IDENTITY_ASSURANCE_LEVELS.find((level) => level.id === id) || IDENTITY_ASSURANCE_LEVELS[0];
    }
    function showError(message) {
      errorEl.hidden = !message;
      errorEl.textContent = message || '';
    }
    function setAccountStatus(message) {
      accountStatus.textContent = message || '';
    }
    function syncLevel() {
      const level = levelFor(levelSelect.value);
      levelDesc.textContent = t(level.descKey);
      accountBlock.hidden = !level.requiresAccount;
      if (authUser?.email && level.requiresAccount) {
        setAccountStatus(`${t('signedInAs')} ${authUser.email}`);
      } else {
        setAccountStatus('');
      }
      showError('');
    }
    levelSelect.addEventListener('change', syncLevel);
    syncLevel();
    // Pre-warm auth so onAuthStateChanged can reflect an existing session.
    getAuthContext().then(syncLevel).catch(() => { /* offline: account levels degrade below */ });

    async function handleAuth(creating) {
      const email = emailInput.value.trim();
      const password = passwordInput.value;
      if (!email || !password) {
        showError(t('accountRequiredError'));
        return;
      }
      try {
        const ctx = await getAuthContext();
        if (creating) {
          await ctx.createUser(ctx.auth, email, password);
        } else {
          await ctx.signIn(ctx.auth, email, password);
        }
        setAccountStatus(`${t('signedInAs')} ${email}`);
        showError('');
      } catch (error) {
        showError(error?.message || t('accountRequiredError'));
      }
    }
    container.querySelector('#ucIdentitySignIn').addEventListener('click', () => handleAuth(false));
    container.querySelector('#ucIdentityCreate').addEventListener('click', () => handleAuth(true));

    function cleanup() {
      container.hidden = true;
      container.innerHTML = '';
    }

    container.querySelector('#ucIdentityCancel').addEventListener('click', () => {
      cleanup();
      resolve(null);
    });

    container.querySelector('#ucIdentityBegin').addEventListener('click', () => {
      const level = levelFor(levelSelect.value);
      if (level.requiresAttestation && !attestCheck.checked) {
        showError(t('identityStepError'));
        return;
      }
      const boundUid = authUser?.uid || account.uid || '';
      const boundEmail = authUser?.email || account.email || '';
      if (level.requiresAccount && !boundUid && !boundEmail) {
        showError(t('accountRequiredError'));
        return;
      }
      storeAssuranceLevel(level.id);
      cleanup();
      resolve({
        level: level.id,
        attestedAdult: Boolean(attestCheck.checked),
        accountUid: level.requiresAccount ? boundUid : '',
        accountEmail: level.requiresAccount ? boundEmail : ''
      });
    });
  });
}

// Builds the identityAssurance record stored on the certification evidence
// packet. Shape matches what the data-layer persists (doc-16). No proctoring.
export function buildIdentityAssuranceRecord(selection, earnedAt, learnerId) {
  if (!selection) {
    return { level: 'self_attested', proctoring: 'none', attestedAdult: false, recordedAt: earnedAt };
  }
  return {
    level: selection.level,
    proctoring: 'none',
    attestedAdult: Boolean(selection.attestedAdult),
    learnerId: learnerId || '',
    accountUid: selection.accountUid || '',
    accountEmail: selection.accountEmail || '',
    recordedAt: earnedAt
  };
}
