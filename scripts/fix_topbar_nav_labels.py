#!/usr/bin/env python3
"""
Replace bare ‹/› arrows in topbar-nav with labeled "← Prev" / "Next →" buttons
and update the CSS so they look like real navigation controls.
"""
import re
from pathlib import Path

OLD_CSS_BLOCK = """.topbar-nav{display:flex;align-items:center;gap:0.35rem;flex-shrink:0;}
.topbar-nav-btn{
  font-size:0.95rem;font-weight:700;color:var(--accent);text-decoration:none;
  padding:0.05rem 0.5rem;border-radius:3px;
  border:1px solid rgba(var(--accent-rgb),0.3);line-height:1.8;
  background:rgba(var(--accent-rgb),0.06);
  transition:all 0.15s;
}
.topbar-nav-btn:hover{background:rgba(var(--accent-rgb),0.18);border-color:rgba(var(--accent-rgb),0.55);}
.topbar-nav-btn.disabled{opacity:0.18;pointer-events:none;cursor:default;color:var(--text-dim);border-color:var(--border);background:transparent;}"""

NEW_CSS_BLOCK = """.topbar-nav{display:flex;align-items:center;gap:0.5rem;flex-shrink:0;}
.topbar-nav-btn{
  font-size:0.65rem;font-weight:700;letter-spacing:0.07em;text-transform:uppercase;
  color:var(--accent);text-decoration:none;white-space:nowrap;
  padding:0.28rem 0.75rem;border-radius:3px;
  border:1px solid rgba(var(--accent-rgb),0.35);
  background:rgba(var(--accent-rgb),0.07);
  transition:all 0.15s;
}
.topbar-nav-btn:hover{background:rgba(var(--accent-rgb),0.18);border-color:rgba(var(--accent-rgb),0.6);}
.topbar-nav-btn.disabled{display:none;}"""

# Also handle minified single-line versions from ai-project-scaffolding
OLD_CSS_MINIFIED_PAT = (
    r'\.topbar-nav-btn\{font-size:0\.95rem;font-weight:700;color:var\(--accent\);'
    r'text-decoration:none;padding:0\.05rem 0\.5rem;border-radius:3px;'
    r'border:1px solid rgba\(var\(--accent-rgb\),0\.3\);line-height:1\.8;'
    r'background:rgba\(var\(--accent-rgb\),0\.06\);transition:all 0\.15s;\}'
    r'\n\.topbar-nav-btn:hover\{background:rgba\(var\(--accent-rgb\),0\.18\);'
    r'border-color:rgba\(var\(--accent-rgb\),0\.55\);\}'
    r'\n\.topbar-nav-btn\.disabled\{opacity:0\.18;pointer-events:none;cursor:default;'
    r'color:var\(--text-dim\);border-color:var\(--border\);background:transparent;\}'
)
NEW_CSS_MINIFIED = (
    '.topbar-nav-btn{font-size:0.65rem;font-weight:700;letter-spacing:0.07em;text-transform:uppercase;'
    'color:var(--accent);text-decoration:none;white-space:nowrap;padding:0.28rem 0.75rem;border-radius:3px;'
    'border:1px solid rgba(var(--accent-rgb),0.35);background:rgba(var(--accent-rgb),0.07);transition:all 0.15s;}\n'
    '.topbar-nav-btn:hover{background:rgba(var(--accent-rgb),0.18);border-color:rgba(var(--accent-rgb),0.6);}\n'
    '.topbar-nav-btn.disabled{display:none;}'
)

def fix_html_labels(content):
    """Replace bare &#8249; / &#8250; arrows with labeled text inside topbar-nav."""
    def replace_in_nav(m):
        nav = m.group(0)
        nav = nav.replace('>&#8249;<', '>&#8592; Prev<')
        nav = nav.replace('>&#8250;<', '>Next &#8594;<')
        return nav

    return re.sub(r'<div class="topbar-nav">.*?</div>', replace_in_nav, content, flags=re.DOTALL)

def process(filepath):
    txt = filepath.read_text(encoding='utf-8')

    if 'Next &#8594;' in txt and '&#8592; Prev' in txt:
        return False  # already done

    changed = False

    # Update CSS block (multiline version)
    if OLD_CSS_BLOCK in txt:
        txt = txt.replace(OLD_CSS_BLOCK, NEW_CSS_BLOCK)
        changed = True

    # Update CSS (minified/single-line version)
    new_txt, n = re.subn(OLD_CSS_MINIFIED_PAT, NEW_CSS_MINIFIED, txt)
    if n:
        txt = new_txt
        changed = True

    # Update HTML labels
    new_txt = fix_html_labels(txt)
    if new_txt != txt:
        txt = new_txt
        changed = True

    if changed:
        filepath.write_text(txt, encoding='utf-8')
        return True
    return False

def main():
    base = Path(r'C:\Users\scott\Code\aesop\ai-academy\modules\v2')
    updated = 0
    for f in sorted(base.rglob('m[0-9]*.html')):
        if process(f):
            print(f'[ok] {f.parent.name}/{f.name}')
            updated += 1
    print(f'\n{updated} files updated.')

if __name__ == '__main__':
    main()
