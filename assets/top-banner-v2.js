(function () {
  'use strict';

  if (document.getElementById('topBanner')) return;

  var _pageUrl = document.location.href;
  var _baseDir = _pageUrl.substring(0, _pageUrl.lastIndexOf('/') + 1);

  var CSS = '' +
    'html { scroll-padding-top: 54px; }' +
    'body { padding-top: 54px; overflow-x: hidden; }' +
    'body > nav.nav { display: none !important; }' +
    'body > #siteLangSwitch { display: none !important; }' +
    '.top-banner { position: fixed; top: 0; left: 0; right: 0; z-index: 9999;' +
    '  background: var(--navy-mid, #16293d); color: #fff;' +
    '  box-shadow: 0 2px 16px rgba(13,27,42,0.45);' +
    '  font-family: var(--font-sans), system-ui, sans-serif; }' +
    '.tb-inner { display: flex; align-items: center; justify-content: space-between;' +
    '  padding: 0 3rem; height: 54px;' +
    '  overflow-x: auto; -webkit-overflow-scrolling: touch;' +
    '  scrollbar-width: none; }' +
    '.tb-inner::-webkit-scrollbar { display: none; }' +
    '.tb-brand { flex-shrink: 0; display: inline-flex; align-items: center;' +
    '  color: #fff !important; text-decoration: none;' +
    '  background: none !important; border: none !important; border-radius: 0 !important;' +
    '  font-family: var(--font-display), Georgia, serif; font-weight: 800;' +
    '  font-size: 1.05rem; letter-spacing: 0.02em;' +
    '  padding: 0 1rem 0 0; margin-right: 0.75rem;' +
    '  border-right: 1px solid rgba(255,255,255,0.14) !important;' +
    '  transition: color 0.15s; white-space: nowrap; }' +
    '.tb-brand em { font-style: italic; color: var(--gold, #c9a05a);' +
    '  font-weight: 700; margin-left: 0.3rem; }' +
    '.tb-brand:hover, .tb-brand:focus-visible {' +
    '  color: var(--gold, #c9a05a) !important; background: none !important;' +
    '  border-color: transparent !important; outline: none; }' +
    '.tb-brand:hover { border-right-color: rgba(255,255,255,0.14) !important; }' +
    '.tb-nav-center { display: flex; align-items: center; gap: 0; }' +
    '.tb-nav-center a { display: inline-flex; align-items: center; gap: 0.3rem;' +
    '  flex-shrink: 0; background: transparent;' +
    '  color: rgba(255,255,255,0.72) !important; padding: 0 0.9rem; height: 54px;' +
    '  text-decoration: none; font-size: 0.9rem; font-weight: 500;' +
    '  border: none; border-radius: 0;' +
    '  transition: color 0.15s, background 0.15s;' +
    '  white-space: nowrap; }' +
    '.tb-nav-center a:hover, .tb-nav-center a:focus-visible {' +
    '  color: #fff !important; background: rgba(255,255,255,0.07); outline: none; }' +
    '.tb-nav-center a.is-active { color: var(--gold, #c9a05a) !important; }' +
    '.tb-spacer { margin-left: auto; }' +
    '.tb-start-btn { flex-shrink: 0; display: inline-flex; align-items: center;' +
    '  background: var(--gold, #c9a05a); color: var(--navy, #0f1923) !important;' +
    '  border: none; border-radius: 2rem; padding: 0.35rem 1rem;' +
    '  font-size: 0.78rem; font-weight: 700; letter-spacing: 0.04em;' +
    '  text-transform: uppercase; text-decoration: none; white-space: nowrap;' +
    '  cursor: pointer; margin-right: 0.75rem;' +
    '  transition: background 0.15s, transform 0.15s; }' +
    '.tb-start-btn:hover { background: var(--gold-light, #dbb87a); transform: translateY(-1px); }' +
    '.tb-lang-select { display: inline-flex; align-items: center;' +
    '  padding: 0.3rem 2rem 0.3rem 0.75rem;' +
    '  background: rgba(255,255,255,0.06);' +
    '  border: 1px solid rgba(255,255,255,0.15); border-radius: 2rem;' +
    '  color: #fff !important; font-size: 0.78rem; font-weight: 600;' +
    '  cursor: pointer; flex-shrink: 0;' +
    '  appearance: none; -webkit-appearance: none;' +
    '  background-image: url("data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 24 24\' fill=\'none\' stroke=\'white\' stroke-width=\'2\'%3E%3Cpath d=\'M6 9l6 6 6-6\'/%3E%3C/svg%3E");' +
    '  background-repeat: no-repeat; background-position: right 0.5rem center; background-size: 0.85rem;' +
    '  font-family: var(--font-sans), system-ui, sans-serif; }' +
    '.tb-lang-select option { background: #16293d; color: #fff; }' +
    '.tb-lang-select:hover { border-color: rgba(255,255,255,0.3); }' +
    '.tb-hamburger { display: none; }' +
    '.tb-drawer-overlay, .tb-drawer { display: none; }' +
    '[data-theme="dark"] .tb-lang-select { color: #e2e8f0 !important; }' +
    '[data-theme="dark"] .top-banner { background: #16293d; }' +
    '[data-theme="dark"] .tb-nav-center a { color: rgba(255,255,255,0.65) !important; }' +
    '@media (max-width: 1300px) {' +
    '  .tb-inner { padding: 0 2rem; }' +
    '  .tb-nav-center a { font-size: 0.84rem; padding: 0 0.65rem; }' +
    '  .tb-brand { font-size: 0.95rem; }' +
    '  .tb-lang-select { font-size: 0.7rem; padding: 0.25rem 1.75rem 0.25rem 0.6rem; background-size: 0.75rem; }' +
    '}' +
    '@media (max-width: 1100px) {' +
    '  .tb-nav-center a { font-size: 0.8rem; padding: 0 0.5rem; }' +
    '}' +
    '@media (max-width: 860px) {' +
    '  .tb-nav-center a { font-size: 0.76rem; padding: 0 0.35rem; }' +
    '  .tb-lang-select { font-size: 0.65rem; padding: 0.2rem 1.5rem 0.2rem 0.5rem; background-size: 0.65rem; }' +
    '  .tb-start-btn { font-size: 0.7rem; padding: 0.3rem 0.7rem; }' +
    '}' +
    '@media (max-width: 760px) {' +
    '  html { scroll-padding-top: 0; }' +
    '  body { padding-top: 0; }' +
    '  .top-banner { position: static; }' +
    '  .tb-inner { flex-wrap: nowrap; height: 54px;' +
    '    padding: 0 1rem; justify-content: space-between; }' +
    '  .tb-nav-center { display: none; }' +
    '  .tb-spacer { display: none; }' +
    '  .tb-start-btn { display: none; }' +
    '  .tb-lang-select { display: none; }' +
    '  .tb-hamburger { display: inline-flex; align-items: center; justify-content: center;' +
    '    width: 36px; height: 36px; border: none; background: transparent;' +
    '    color: #fff; cursor: pointer; border-radius: 6px;' +
    '    font-size: 1.5rem; line-height: 1; padding: 0; flex-shrink: 0; }' +
    '  .tb-drawer-overlay { position: fixed; inset: 0; z-index: 100000;' +
    '    background: rgba(0,0,0,0.5); display: none; }' +
    '  .tb-drawer-overlay.open { display: block; }' +
    '  .tb-drawer { display: flex; position: fixed; top: 0; right: -280px; width: 280px;' +
    '    height: 100vh; z-index: 100001;' +
    '    background: var(--navy-mid, #16293d);' +
    '    flex-direction: column; gap: 0.25rem;' +
    '    padding: 4.5rem 1.5rem 2rem;' +
    '    transition: right 0.3s ease; overflow-y: auto;' +
    '    box-shadow: -4px 0 24px rgba(0,0,0,0.35); }' +
    '  .tb-drawer.open { right: 0; }' +
    '  .tb-drawer-close { position: absolute; top: 12px; right: 16px;' +
    '    background: none; border: none; color: rgba(255,255,255,0.5);' +
    '    font-size: 1.5rem; cursor: pointer; padding: 4px;' +
    '    line-height: 1; }' +
    '  .tb-drawer-close:hover { color: #fff; }' +
    '  .tb-drawer .tb-drawer-nav a { display: block; padding: 0.8rem 0;' +
    '    font-size: 1rem; color: rgba(255,255,255,0.8) !important;' +
    '    text-decoration: none; border-bottom: 1px solid rgba(255,255,255,0.06);' +
    '    font-weight: 500; transition: color 0.15s; }' +
    '  .tb-drawer .tb-drawer-nav a:hover { color: var(--gold, #c9a05a) !important; }' +
    '  .tb-drawer .tb-drawer-nav a.is-active { color: var(--gold, #c9a05a) !important; }' +
    '  .tb-drawer .tb-start-btn { display: inline-flex; margin: 1rem 0;' +
    '    justify-content: center; font-size: 0.85rem; padding: 0.6rem 1.2rem; }' +
    '  .tb-drawer .tb-drawer-lang-label { display: block; margin-top: 1rem;' +
    '    font-size: 0.72rem; color: rgba(255,255,255,0.4);' +
    '    font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em; }' +
    '  .tb-drawer .tb-drawer-lang { display: flex; flex-wrap: wrap; gap: 0.35rem; margin-top: 0.6rem; }' +
    '  .tb-drawer .tb-drawer-lang .lang-btn { background: transparent;' +
    '    color: rgba(255,255,255,0.65) !important; border: 1px solid rgba(255,255,255,0.1);' +
    '    padding: 0.35rem 0.55rem; font-size: 0.72rem; font-weight: 600;' +
    '    cursor: pointer; border-radius: 2rem; display: inline-flex;' +
    '    align-items: center; gap: 0.3rem; transition: all 0.15s; }' +
    '  .tb-drawer .tb-drawer-lang .lang-btn:hover { background: rgba(255,255,255,0.08);' +
    '    color: #fff !important; }' +
    '  .tb-drawer .tb-drawer-lang .lang-btn.lang-active {' +
    '    background: var(--gold, #c9a05a); color: var(--navy, #0f1923) !important;' +
    '    border-color: var(--gold); }' +
    '  .tb-drawer .tb-drawer-lang .lang-btn .fi { display: inline-block;' +
    '    width: 1rem; height: 0.7rem; vertical-align: -1px; border-radius: 1px;' +
    '    background-size: cover; background-position: center;' +
    '    box-shadow: 0 0 0 1px rgba(255,255,255,0.12); }' +
    '}';

  var LANGS = [
    { code: 'en', label: 'EN', flag: 'fi-us', title: 'English' },
    { code: 'es', label: 'ES', flag: 'fi-mx', title: 'Espa\u00F1ol' },
    { code: 'hi', label: '\u0939\u093F', flag: 'fi-in', title: '\u0939\u093F\u0928\u094D\u0926\u0940' },
    { code: 'ar', label: 'AR', flag: 'fi-sa', title: '\u0627\u0644\u0639\u0631\u0628\u064A\u0629' },
    { code: 'zh-TW', label: 'TW', flag: 'fi-tw', title: '\u7E41\u9AD4\u4E2D\u6587' },
    { code: 'ko', label: 'KO', flag: 'fi-kr', title: '\uD55C\uAD6D\uC5B4' },
    { code: 'ur', label: 'UR', flag: 'fi-pk', title: '\u0627\u0631\u062F\u0648' },
    { code: 'tr', label: 'TR', flag: 'fi-tr', title: 'T\u00FCrk\u00E7e' }
  ];

  function langOptionHTML(code, label, flag, title) {
    return '<option value="' + code + '" data-flag="' + flag + '" title="' + title + '">' +
      label + '</option>';
  }

  function langBtnHTML(code, flag, title) {
    var displayName = { en: 'EN', es: 'ES', hi: '\u0939\u093F', ar: 'AR', 'zh-TW': 'TW', ko: 'KO', ur: 'UR', tr: 'TR' }[code] || code;
    return '<button class="lang-btn" data-lang="' + code + '" title="' + title + '">' +
      '<span class="fi ' + flag + '"></span> ' + displayName + '</button>';
  }

  var langOpts = '';
  var langBtns = '';
  for (var i = 0; i < LANGS.length; i++) {
    var l = LANGS[i];
    langOpts += langOptionHTML(l.code, l.label, l.flag, l.title);
    langBtns += langBtnHTML(l.code, l.flag, l.title);
  }

  var HTML = '' +
    '<div id="topBanner" class="top-banner">' +
    '  <nav class="tb-inner">' +
    '    <a class="tb-brand" href="' + _baseDir + '"><img src="' + _baseDir + 'favicon_512.png" width="28" height="28" alt="" aria-hidden="true" style="border-radius:4px;margin-right:0.5rem;flex-shrink:0;">AESOP<em>AI Academy</em></a>' +
    '    <div class="tb-nav-center">' +
    '      <a href="' + _baseDir + 'ai-academy/courses-v2.html">Courses</a>' +
    '      <a href="' + _baseDir + 'ai-academy/assessment.html">Find Your Path</a>' +
    '      <a href="' + _baseDir + 'pedagogy.html">How It Works</a>' +
    '      <a href="' + _baseDir + 'about/mission.html">About</a>' +
    '      <a href="' + _baseDir + 'institutional-procurement.html">For Schools</a>' +
    '    </div>' +
    '    <div style="display:flex;align-items:center;gap:0.35rem;">' +
    '      <a href="' + _baseDir + 'ai-academy/assessment.html" class="tb-start-btn" id="tbStartBtn">Start Learning</a>' +
    '      <select class="tb-lang-select" id="langSelector" aria-label="Select language">' +
    '        <option value="" disabled>Language</option>' +
    langOpts +
    '      </select>' +
    '      <button class="tb-hamburger" id="tbHamburger" aria-label="Menu" aria-expanded="false">&#9776;</button>' +
    '    </div>' +
    '  </nav>' +
    '  <div class="tb-drawer-overlay" id="tbDrawerOverlay"></div>' +
    '  <div class="tb-drawer" id="tbDrawer">' +
    '    <button class="tb-drawer-close" id="tbDrawerClose" aria-label="Close menu">&times;</button>' +
    '    <div class="tb-drawer-nav">' +
    '      <a href="' + _baseDir + 'ai-academy/courses-v2.html">Courses</a>' +
    '      <a href="' + _baseDir + 'ai-academy/assessment.html">Find Your Path</a>' +
    '      <a href="' + _baseDir + 'pedagogy.html">How It Works</a>' +
    '      <a href="' + _baseDir + 'about/mission.html">About</a>' +
    '      <a href="' + _baseDir + 'institutional-procurement.html">For Schools</a>' +
    '    </div>' +
    '    <a href="' + _baseDir + 'ai-academy/assessment.html" class="tb-start-btn" id="tbStartBtnMobile">Start Learning</a>' +
    '    <span class="tb-drawer-lang-label">Language</span>' +
    '    <div class="tb-drawer-lang" id="langSelectorMobile">' +
    langBtns +
    '    </div>' +
    '  </div>' +
    '</div>';

  if (!document.querySelector('link[href*="flag-icons"]')) {
    var flagLink = document.createElement('link');
    flagLink.rel = 'stylesheet';
    flagLink.href = 'https://cdnjs.cloudflare.com/ajax/libs/flag-icon-css/6.6.6/css/flag-icons.min.css';
    (document.head || document.documentElement).appendChild(flagLink);
  }

  var styleEl = document.createElement('style');
  styleEl.textContent = CSS;
  (document.head || document.documentElement).appendChild(styleEl);

  function mount() {
    var target = document.getElementById('topBanner-mount');
    if (target) {
      target.outerHTML = HTML;
    } else if (document.body) {
      document.body.insertAdjacentHTML('afterbegin', HTML);
    } else {
      document.addEventListener('DOMContentLoaded', mount, { once: true });
      return;
    }
    var banner = document.getElementById('topBanner');
    if (banner) {
      var h = banner.getBoundingClientRect().height;
      var isMobile = window.innerWidth <= 760;
      if (h > 0 && !isMobile) document.body.style.paddingTop = h + 'px';
    }
    if (!document.querySelector('script[src*="auth-modal.js"]')) {
      var authScript = document.createElement('script');
      authScript.src = _baseDir + 'assets/auth-modal.js';
      authScript.defer = true;
      document.body.appendChild(authScript);
    }
    wireBehaviors();
  }

  function getLangCode() {
    var path = location.pathname;
    var m = path.match(/\/ai-academy\/modules\/([a-zA-Z-]+)\//);
    return m ? m[1] : 'en';
  }

  function navigateLang(code) {
    location.href = (code === 'en') ? _baseDir : _baseDir + 'ai-academy/modules/' + code + '/courses.html';
  }

  function wireBehaviors() {
    var current = getLangCode();

    var desktopSel = document.getElementById('langSelector');
    if (desktopSel) {
      desktopSel.value = current;
      desktopSel.addEventListener('change', function () {
        navigateLang(this.value);
      });
    }

    var mobileSel = document.getElementById('langSelectorMobile');
    if (mobileSel) {
      mobileSel.querySelectorAll('.lang-btn').forEach(function (btn) {
        var code = btn.dataset.lang;
        btn.classList.toggle('lang-active', code === current);
        btn.addEventListener('click', function () {
          navigateLang(code);
        });
      });
    }

    (function () {
      var cur = location.pathname;
      var links = document.querySelectorAll('.tb-nav-center a, .tb-drawer-nav a');
      for (var i = 0; i < links.length; i++) {
        var a = links[i];
        var href = a.getAttribute('href') || '';
        if (/^https?:\/\//.test(href)) continue;
        var linkPath = href.split('#')[0];
        var isDir = linkPath.slice(-1) === '/';
        var active = isDir ? cur.indexOf(linkPath) === 0 : cur === linkPath;
        if (active) a.classList.add('is-active');
      }
    })();

    function wireStartBtn(btn) {
      if (!btn) return;
      btn.addEventListener('click', function (e) {
        if (typeof window.openAuthModal !== 'function') return;
        var loggedIn = document.getElementById('authView-loggedin');
        if (loggedIn && loggedIn.style.display !== 'none') return;
        e.preventDefault();
        window.openAuthModal('signup', btn.getAttribute('href'));
        closeDrawer();
      });
    }
    wireStartBtn(document.getElementById('tbStartBtn'));
    wireStartBtn(document.getElementById('tbStartBtnMobile'));

    function closeDrawer() {
      var drawer = document.getElementById('tbDrawer');
      var overlay = document.getElementById('tbDrawerOverlay');
      var hamburger = document.getElementById('tbHamburger');
      if (drawer) drawer.classList.remove('open');
      if (overlay) overlay.classList.remove('open');
      if (hamburger) hamburger.setAttribute('aria-expanded', 'false');
    }

    function openDrawer() {
      var drawer = document.getElementById('tbDrawer');
      var overlay = document.getElementById('tbDrawerOverlay');
      var hamburger = document.getElementById('tbHamburger');
      if (drawer) drawer.classList.add('open');
      if (overlay) overlay.classList.add('open');
      if (hamburger) hamburger.setAttribute('aria-expanded', 'true');
    }

    var hamburger = document.getElementById('tbHamburger');
    if (hamburger) {
      hamburger.addEventListener('click', function () {
        var drawer = document.getElementById('tbDrawer');
        var isOpen = drawer && drawer.classList.contains('open');
        if (isOpen) { closeDrawer(); } else { openDrawer(); }
      });
    }

    var overlay = document.getElementById('tbDrawerOverlay');
    if (overlay) {
      overlay.addEventListener('click', closeDrawer);
    }

    var closeBtn = document.getElementById('tbDrawerClose');
    if (closeBtn) {
      closeBtn.addEventListener('click', closeDrawer);
    }

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeDrawer();
    });

    var drawerLinks = document.querySelectorAll('.tb-drawer-nav a');
    for (var j = 0; j < drawerLinks.length; j++) {
      drawerLinks[j].addEventListener('click', closeDrawer);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', mount, { once: true });
  } else {
    mount();
  }
})();
