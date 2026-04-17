#!/usr/bin/env python3
"""Update site-wide language switcher to include Arabic (ar) and use the
current /ai-academy/modules/{lang}/courses.html layout.

Replaces the old anchor-pill switcher block and its pathing script.
Also fixes a stray duplicate ES button in electives-hub.html.
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# Pages that use the shared anchor-pill (#siteLangSwitch) pattern
ANCHOR_PILL_PAGES = [
    "ai-academy/courses.html",
    "ai-academy/modules/electives-hub.html",
    "ai-academy/modules/ar/courses.html",
    "ai-academy/modules/de/courses.html",
    "ai-academy/modules/es/courses.html",
    "ai-academy/modules/fa/courses.html",
    "ai-academy/modules/fr/courses.html",
    "ai-academy/modules/hi/courses.html",
    "ai-academy/modules/ja/courses.html",
    "ai-academy/modules/ko/courses.html",
    "ai-academy/modules/ru/courses.html",
    "ai-academy/modules/sw/courses.html",
    "ai-academy/modules/ur/courses.html",
    "ai-academy/modules/zh/courses.html",
]

NEW_PILL_HTML = '''<div id="siteLangSwitch" aria-label="Select language">
  <a href="#" data-lang="en" title="English">EN</a>
  <div class="sep"></div>
  <a href="#" data-lang="es" title="Español">ES</a>
  <div class="sep"></div>
  <a href="#" data-lang="hi" title="हिन्दी">हि</a>
  <div class="sep"></div>
  <a href="#" data-lang="ar" title="العربية">AR</a>
</div>'''

# URL mapping: EN canonical courses page is /ai-academy/courses.html.
# For every non-EN lang, navigation goes to /ai-academy/modules/{lang}/courses.html.
NEW_PILL_SCRIPT = '''<script>
(function(){
  var sw=document.getElementById('siteLangSwitch'); if(!sw) return;
  var LANGS=['es','hi','ar'];
  var EN_PATH='/ai-academy/courses.html';
  var p=location.pathname, current='en';
  // Detect current lang from path: /ai-academy/modules/{lang}/...
  var m=p.match(/\\/ai-academy\\/modules\\/([a-z]{2})\\//);
  if(m && LANGS.indexOf(m[1])!==-1) current=m[1];
  sw.querySelectorAll('[data-lang]').forEach(function(b){
    var c=b.dataset.lang;
    var t=(c==='en')?EN_PATH:('/ai-academy/modules/'+c+'/courses.html');
    b.setAttribute('href',t);
    b.classList.toggle('lang-active', c===current);
  });
})();
</script>'''

# Match the old anchor-pill HTML block (tolerates the duplicate-ES bug in
# electives-hub.html by consuming any trailing stray anchors before <script>).
OLD_PILL_RE = re.compile(
    r'<div id="siteLangSwitch"[^>]*>.*?</div>\s*'
    r'(?:<a[^>]*data-lang=[^>]*>.*?</a>\s*</div>\s*)?'
    r'<script>\s*\(function\(\)\{\s*var sw=document\.getElementById\(\'siteLangSwitch\'\);.*?\}\)\(\);\s*</script>',
    re.DOTALL,
)

def update_anchor_pill(path: Path) -> bool:
    s = path.read_text(encoding="utf-8")
    new = OLD_PILL_RE.sub(NEW_PILL_HTML + "\n" + NEW_PILL_SCRIPT, s)
    if new == s:
        print(f"NO MATCH: {path.relative_to(REPO)}")
        return False
    path.write_text(new, encoding="utf-8")
    print(f"UPDATED: {path.relative_to(REPO)}")
    return True

# ── ai-academy/index.html : button + switchSiteLang() variant ──
ACADEMY_HUB = REPO / "ai-academy/index.html"
ACADEMY_HUB_OLD_BUTTONS = re.compile(
    r'<div class="lang-toggle" id="langToggle">\s*'
    r'<button class="active" data-lang="en" onclick="switchSiteLang\(\'en\'\)">EN</button>\s*'
    r'<button data-lang="es" onclick="switchSiteLang\(\'es\'\)">ES</button>\s*'
    r'<button data-lang="hi" onclick="switchSiteLang\(\'hi\'\)">हि</button>\s*'
    r'</div>',
    re.DOTALL,
)
ACADEMY_HUB_NEW_BUTTONS = (
    '<div class="lang-toggle" id="langToggle">\n'
    '    <button class="active" data-lang="en" onclick="switchSiteLang(\'en\')">EN</button>\n'
    '    <button data-lang="es" onclick="switchSiteLang(\'es\')">ES</button>\n'
    '    <button data-lang="hi" onclick="switchSiteLang(\'hi\')">हि</button>\n'
    '    <button data-lang="ar" onclick="switchSiteLang(\'ar\')">AR</button>\n'
    '  </div>'
)
# Replace the switchSiteLang() + applyLang IIFE script block
ACADEMY_HUB_OLD_SCRIPT = re.compile(
    r'<script>\s*// URL-based language switch for the AI Academy hub\..*?\}\)\(\);\s*</script>',
    re.DOTALL,
)
ACADEMY_HUB_NEW_SCRIPT = '''<script>
  // URL-based language switch for the AI Academy hub.
  // EN stays on /ai-academy/. Other langs route to /ai-academy/modules/{lang}/courses.html.
  function switchSiteLang(lang){
    if(lang==='en'){ location.href='/ai-academy/'; return; }
    location.href='/ai-academy/modules/'+lang+'/courses.html';
  }
  (function(){
    var p=location.pathname, current='en';
    var m=p.match(/\\/ai-academy\\/modules\\/([a-z]{2})\\//);
    if(m) current=m[1];
    function applyLang(){
      var t=document.getElementById('langToggle');
      if(t){
        t.querySelectorAll('[data-lang]').forEach(function(b){
          b.classList.toggle('active', b.dataset.lang===current);
        });
      }
      if(current!=='en' && typeof setLang==='function'){
        try{ setLang(current); }catch(e){}
      }
    }
    if(document.readyState==='loading'){
      document.addEventListener('DOMContentLoaded', applyLang);
    } else { applyLang(); }
  })();
  </script>'''

def update_academy_hub():
    s = ACADEMY_HUB.read_text(encoding="utf-8")
    n1 = ACADEMY_HUB_OLD_BUTTONS.sub(ACADEMY_HUB_NEW_BUTTONS, s)
    if n1 == s: print("NO MATCH (buttons): ai-academy/index.html"); return False
    n2 = ACADEMY_HUB_OLD_SCRIPT.sub(ACADEMY_HUB_NEW_SCRIPT, n1)
    if n2 == n1: print("NO MATCH (script): ai-academy/index.html"); return False
    ACADEMY_HUB.write_text(n2, encoding="utf-8")
    print("UPDATED: ai-academy/index.html")
    return True

# ── Root index.html : .lang-btn pattern ──
ROOT_INDEX = REPO / "index.html"
ROOT_OLD = re.compile(
    r'<button class="lang-btn" data-lang="en"[^>]*>.*?</button>\s*'
    r'<button class="lang-btn" data-lang="es"[^>]*>.*?</button>\s*'
    r'<button class="lang-btn" data-lang="hi"[^>]*>.*?</button>',
    re.DOTALL,
)
ROOT_NEW = ('<button class="lang-btn" data-lang="en" title="English"><span class="fi fi-us lang-flag"></span> EN</button>\n'
            '      <button class="lang-btn" data-lang="es" title="Español"><span class="fi fi-mx lang-flag"></span> ES</button>\n'
            '      <button class="lang-btn" data-lang="hi" title="हिन्दी"><span class="fi fi-in lang-flag"></span> हि</button>\n'
            '      <button class="lang-btn" data-lang="ar" title="العربية"><span class="fi fi-sa lang-flag"></span> AR</button>')

def update_root_index():
    s = ROOT_INDEX.read_text(encoding="utf-8")
    n = ROOT_OLD.sub(ROOT_NEW, s)
    if n == s:
        print("NO MATCH: index.html")
        return False
    ROOT_INDEX.write_text(n, encoding="utf-8")
    print("UPDATED: index.html")
    return True

def main():
    results = []
    for rel in ANCHOR_PILL_PAGES:
        p = REPO / rel
        if not p.exists():
            print(f"MISSING: {rel}"); continue
        results.append(update_anchor_pill(p))
    results.append(update_academy_hub())
    results.append(update_root_index())
    ok = sum(1 for r in results if r)
    total = len(results)
    print(f"\n{ok}/{total} files updated")
    return 0 if ok == total else 1

if __name__ == "__main__":
    sys.exit(main())
