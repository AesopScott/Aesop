// Account creation — lands the passwordless email-verification link, then sets a password.
// Flow: hero form sent a sign-in link -> this page finishes sign-in (email now verified)
// -> learner attaches a password -> redirect home, signed in.
import { initializeApp } from 'https://www.gstatic.com/firebasejs/10.12.0/firebase-app.js';
import {
  getAuth, isSignInWithEmailLink, signInWithEmailLink,
  EmailAuthProvider, linkWithCredential, updatePassword
} from 'https://www.gstatic.com/firebasejs/10.12.0/firebase-auth.js';
import { FIREBASE_CONFIG } from '/ai-academy/js/firebase-config.js';

const auth = getAuth(initializeApp(FIREBASE_CONFIG));
const LS_EMAIL = 'aesop-ladder2-emailForSignIn';
const HOME = '/theladder/ladder2.html';

const el = (id) => document.getElementById(id);
const show = (id) => { const n = el(id); if (n) n.hidden = false; };
const hide = (id) => { const n = el(id); if (n) n.hidden = true; };

function setError(targetId, message) {
  const n = el(targetId);
  if (!n) return;
  n.textContent = message || '';
  n.hidden = !message;
}

// --- entry: validate the link, then resolve the email (storage or prompt) ---
async function start() {
  if (!isSignInWithEmailLink(auth, window.location.href)) {
    hide('caVerifying');
    show('caBadLink');
    return;
  }
  const email = localStorage.getItem(LS_EMAIL);
  if (!email) {
    // Link opened on a different device/browser than it was requested from.
    hide('caVerifying');
    show('caNeedEmail');
    return;
  }
  await completeSignIn(email);
}

// --- finish the passwordless sign-in (this verifies the email) ---
async function completeSignIn(email) {
  try {
    await signInWithEmailLink(auth, email, window.location.href);
    localStorage.removeItem(LS_EMAIL);
    // Bind the learner id; the home page initialises the data layer + record on return.
    localStorage.setItem('aesop-learner-id', auth.currentUser.uid);
    el('caEmailEcho').textContent = auth.currentUser.email || email;
    hide('caVerifying');
    hide('caNeedEmail');
    show('caSetPw');
  } catch (error) {
    hide('caVerifying');
    hide('caNeedEmail');
    show('caBadLink');
  }
}

// --- cross-device email confirmation ---
el('caNeedEmailBtn')?.addEventListener('click', () => {
  const email = el('caNeedEmailInput').value.trim();
  if (!email) { setError('caErrorNeed', 'Enter the email you used to sign up.'); return; }
  setError('caErrorNeed', '');
  completeSignIn(email);
});

// --- set the password on the now-verified account ---
el('caSetPwBtn')?.addEventListener('click', async () => {
  const pw = el('caPassword').value;
  const pw2 = el('caPassword2').value;
  setError('caError', '');
  if (pw.length < 8) { setError('caError', 'Use at least 8 characters.'); return; }
  if (pw !== pw2) { setError('caError', 'Passwords do not match.'); return; }

  const user = auth.currentUser;
  if (!user) { setError('caError', 'Your session expired. Please open the email link again.'); return; }

  const btn = el('caSetPwBtn');
  btn.disabled = true;
  try {
    const credential = EmailAuthProvider.credential(user.email, pw);
    try {
      await linkWithCredential(user, credential);
    } catch (linkErr) {
      // Returning user who already has a password provider — just update it.
      if (linkErr.code === 'auth/provider-already-linked' || linkErr.code === 'auth/email-already-in-use') {
        await updatePassword(user, pw);
      } else {
        throw linkErr;
      }
    }
    window.location.href = HOME;
  } catch (error) {
    btn.disabled = false;
    const friendly = error.code === 'auth/weak-password'
      ? 'That password is too weak — try a longer one.'
      : `Could not save your password (${error.code || 'error'}). Please try again.`;
    setError('caError', friendly);
  }
});

start();
