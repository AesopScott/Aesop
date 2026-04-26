import re, os, sys, glob

ROOT = 'C:/Users/scott/Code/Aesop/ai-academy/modules'

files = [
    f for f in glob.glob(ROOT + '/**/*-m*.html', recursive=True)
    if 'archive' not in f.replace('\\', '/')
    and 'i18n' not in f.replace('\\', '/')
]

BUTTON_HTML = (
    '\n  <div class="pnav" style="padding:1.25rem 2.5rem 2rem;display:flex;gap:0.75rem;">\n'
    "    <button class=\"pnav-btn primary\" onclick=\"goPage('p-l1')\">Begin Lesson 1 →</button>\n"
    '  </div>'
)

PATTERN = re.compile(
    r'(\n  </div>\n</div>)(\n+)((?:<!--[^\n]*-->\n)*)([ ]*<div[^>]*id="p-l1")',
    re.DOTALL
)

patched = 0
already = 0
no_match = 0

for path in sorted(files):
    raw = open(path, encoding='utf-8', errors='replace').read()

    if "goPage('p-l1')" in raw and 'Begin Lesson 1' in raw:
        already += 1
        continue

    if 'id="p-intro"' not in raw or 'id="p-l1"' not in raw:
        no_match += 1
        continue

    new_raw, n = PATTERN.subn(
        lambda m: BUTTON_HTML + m.group(1) + m.group(2) + m.group(3) + m.group(4),
        raw,
        count=1
    )

    if n == 0:
        no_match += 1
        continue

    open(path, 'w', encoding='utf-8').write(new_raw)
    patched += 1

print(f'Patched: {patched}  |  Already done: {already}  |  No match: {no_match}  |  Total: {len(files)}')
