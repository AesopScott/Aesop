// Silently checks Firebase auth; injects an admin link on board pages for scott@aesopacademy.org
import { initializeApp }              from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js';
import { getAuth, onAuthStateChanged } from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js';

const firebaseConfig = {
  apiKey:            'AIzaSyAPLGIn4wqgTL92VZFXuu8-ZgxMBBT2eKY',
  authDomain:        'playagame-f733d.firebaseapp.com',
  projectId:         'playagame-f733d',
  storageBucket:     'playagame-f733d.firebasestorage.app',
  messagingSenderId: '610508714644',
  appId:             '1:610508714644:web:b7df8f61ce21cf1281ba81'
};

const ADMIN_EMAILS = ['scott@aesopacademy.org'];

const app  = initializeApp(firebaseConfig, 'board-admin-link');
const auth = getAuth(app);

onAuthStateChanged(auth, user => {
  if (!user || !ADMIN_EMAILS.includes(user.email)) return;

  const link = document.createElement('a');
  link.href  = '/ai-academy/admin/board-approvals.html';
  link.textContent = '⚙ Board Approvals';
  link.style.cssText = [
    'position:fixed',
    'bottom:24px',
    'right:24px',
    'z-index:9000',
    'background:#0d1b2a',
    'color:#c9a05a',
    'border:1.5px solid rgba(201,160,90,0.45)',
    'border-radius:100px',
    'padding:0.45rem 1.1rem',
    'font-size:0.78rem',
    'font-weight:700',
    'letter-spacing:0.04em',
    'text-decoration:none',
    'box-shadow:0 4px 16px rgba(0,0,0,0.35)',
    'transition:background 0.15s,color 0.15s',
  ].join(';');

  link.addEventListener('mouseenter', () => {
    link.style.background = '#c9a05a';
    link.style.color      = '#0d1b2a';
  });
  link.addEventListener('mouseleave', () => {
    link.style.background = '#0d1b2a';
    link.style.color      = '#c9a05a';
  });

  document.body.appendChild(link);
});
