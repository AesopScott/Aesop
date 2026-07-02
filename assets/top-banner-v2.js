(function () {
  'use strict';

  if (document.getElementById('topBanner')) return;

  var _pageUrl = document.location.href;
  var _baseDir = _pageUrl.substring(0, _pageUrl.lastIndexOf('/') + 1);

  var CSS = '' +
    'html { scroll-padding-top: 64px; }' +
    'body { padding-top: 64px; overflow-x: hidden; }' +
    'body > nav.nav { display: none !important; }' +
    'body > #siteLangSwitch { display: none !important; }' +
    '.top-banner { position: fixed; top: 0; left: 0; right: 0; z-index: 9999;' +
    '  background: var(--navy-mid, #16293d); color: #fff;' +
    '  box-shadow: 0 2px 16px rgba(13,27,42,0.45);' +
    '  font-family: var(--font-sans), system-ui, sans-serif; }' +
    '.tb-inner { display: flex; align-items: center;' +
    '  padding: 0 12.5%; height: 54px;' +
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
    '.tb-inner a { display: inline-flex; align-items: center; gap: 0.3rem;' +
    '  flex-shrink: 0; background: transparent;' +
    '  color: rgba(255,255,255,0.72) !important; padding: 0 0.9rem; height: 100%;' +
    '  text-decoration: none; font-size: 0.9rem; font-weight: 500;' +
    '  border: none; border-radius: 0;' +
    '  transition: color 0.15s, background 0.15s;' +
    '  white-space: nowrap; }' +
    '.tb-inner a:hover, .tb-inner a:focus-visible {' +
    '  color: #fff !important; background: rgba(255,255,255,0.07); outline: none; }' +
    '.tb-inner a.is-active { color: var(--gold, #c9a05a) !important; }' +
    '.tb-spacer { margin-left: auto; }' +
    '.tb-lang { display: inline-flex; align-items: stretch;' +
    '  background: rgba(255,255,255,0.06);' +
    '  border: 1px solid rgba(255,255,255,0.12); border-radius: 2rem;' +
    '  overflow: hidden; padding: 0; flex-shrink: 0; }' +
    '.tb-lang .lang-btn { background: transparent; color: #fff !important;' +
    '  border: none; padding: 0.22rem 0.4rem; font-size: 0.65rem;' +
    '  font-weight: 600; letter-spacing: 0.03em; cursor: pointer;' +
    '  display: inline-flex; align-items: center; gap: 0.3rem;' +
    '  transition: background 0.15s, color 0.15s; }' +
    '.tb-lang .lang-btn:hover { background: rgba(255,255,255,0.08); }' +
    '.tb-lang .lang-btn.lang-active {' +
    '  background: var(--gold, #c9a05a); color: var(--navy, #0f1923) !important; }' +
    '.tb-lang .lang-divider { width: 1px; background: rgba(255,255,255,0.12); }' +
    '.tb-lang .lang-btn .fi { display: inline-block; width: 1.1rem; height: 0.8rem; vertical-align: -1px; margin-right: 0.25rem; border-radius: 1px; background-size: cover; background-position: center; box-shadow: 0 0 0 1px rgba(255,255,255,0.12); }' +
    '[data-theme="dark"] .top-banner { background: #16293d; }' +
    '[data-theme="dark"] .tb-inner a { color: rgba(255,255,255,0.65) !important; }' +
    '@media (max-width: 1300px) {' +
    '  .tb-inner { padding: 0 8%; }' +
    '  .tb-inner a { font-size: 0.84rem; padding: 0 0.75rem; }' +
    '  .tb-brand { font-size: 0.95rem; }' +
    '  .tb-lang .lang-btn { padding: 0.2rem 0.32rem; font-size: 0.6rem; }' +
    '}' +
    '@media (max-width: 760px) {' +
    '  html { scroll-padding-top: 108px; }' +
    '  body { padding-top: 108px; }' +
    '  .tb-inner { flex-wrap: wrap; height: auto; padding: 0.5rem 1.25rem; gap: 0.25rem; }' +
    '  .tb-inner a { height: auto; padding: 0.4rem 0.6rem; font-size: 0.82rem; }' +
    '}';

  var HTML = '' +
    '<div id="topBanner" class="top-banner">' +
    '  <nav class="tb-inner">' +
    '    <a class="tb-brand" href="' + _baseDir + '"><img src="' + _baseDir + 'favicon_512.png" width="28" height="28" alt="" aria-hidden="true" style="border-radius:4px;margin-right:0.5rem;flex-shrink:0;">AESOP<em>AI Academy</em></a>' +
    '    <a href="' + _baseDir + 'ai-academy/courses-v2.html">Courses</a>' +
    '    <a href="' + _baseDir + 'ai-academy/assessment.html">Find Your Path</a>' +
    '    <a href="' + _baseDir + 'pedagogy.html">How It Works</a>' +
    '    <a href="' + _baseDir + 'about/mission.html">About</a>' +
    '    <a href="' + _baseDir + 'institutional-procurement.html">For Schools</a>' +
    '    <span class="tb-spacer"></span>' +
    '    <div class="tb-lang" id="langSelector">' +
    '      <button class="lang-btn" data-lang="en" title="English"><span class="fi fi-us"></span> EN</button>' +
    '      <div class="lang-divider"></div>' +
    '      <button class="lang-btn" data-lang="es" title="Espa\u00F1ol"><span class="fi fi-mx"></span> ES</button>' +
    '      <div class="lang-divider"></div>' +
    '      <button class="lang-btn" data-lang="hi" title="\u0939\u093F\u0928\u094D\u0926\u0940"><span class="fi fi-in"></span> \u0939\u093F</button>' +
    '      <div class="lang-divider"></div>' +
    '      <button class="lang-btn" data-lang="ar" title="\u0627\u0644\u0639\u0631\u0628\u064A\u0629"><span class="fi fi-sa"></span> AR</button>' +
    '      <div class="lang-divider"></div>' +
    '      <button class="lang-btn" data-lang="zh-TW" title="\u7e41\u9ad4\u4e2d\u6587"><span class="fi fi-tw"></span> TW</button>' +
    '      <div class="lang-divider"></div>' +
    '      <button class="lang-btn" data-lang="ko" title="\ud55c\uad6d\uc5b4"><span class="fi fi-kr"></span> KO</button>' +
    '      <div class="lang-divider"></div>' +
    '      <button class="lang-btn" data-lang="ur" title="\u0627\u0631\u062f\u0648"><span class="fi fi-pk"></span> UR</button>' +
    '      <div class="lang-divider"></div>' +
    '      <button class="lang-btn" data-lang="tr" title="T\u00fcrk\u00e7e"><span class="fi fi-tr"></span> TR</button>' +
    '    </div>' +
    '  </nav>' +
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
      if (h > 0) document.body.style.paddingTop = h + 'px';
    }
    if (!document.querySelector('script[src*="auth-modal.js"]')) {
      var authScript = document.createElement('script');
      authScript.src = _baseDir + 'assets/auth-modal.js';
      authScript.defer = true;
      document.body.appendChild(authScript);
    }
    wireBehaviors();
  }

  function wireBehaviors() {
    var sel = document.getElementById('langSelector');
    if (sel) {
      var path = location.pathname;
      var current = 'en';
      var m = path.match(/\/ai-academy\/modules\/([a-zA-Z-]+)\//);
      if (m) current = m[1];
      sel.querySelectorAll('.lang-btn').forEach(function (btn) {
        var code = btn.dataset.lang;
        btn.classList.toggle('lang-active', code === current);
        btn.addEventListener('click', function () {
          location.href = (code === 'en') ? _baseDir : _baseDir + 'ai-academy/modules/' + code + '/courses.html';
        });
      });
    }

    (function () {
      var cur = location.pathname;
      document.querySelectorAll('.tb-inner a').forEach(function (a) {
        var href = a.getAttribute('href') || '';
        if (/^https?:\/\//.test(href)) return;
        var linkPath = href.split('#')[0];
        var isDir = linkPath.slice(-1) === '/';
        var active = isDir ? cur.indexOf(linkPath) === 0 : cur === linkPath;
        if (active) a.classList.add('is-active');
      });
    })();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', mount, { once: true });
  } else {
    mount();
  }
})();
