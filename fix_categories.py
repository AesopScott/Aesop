"""
Reorganize courses.html mega-menu categories.
Run: python fix_categories.py

Changes:
1. Move 5 pentesting courses from "Strategy & Org" to Pro "Cybersecurity"
2. Move 3 dev-tool courses from "Strategy & Org" to "Development"
3. Move 4 business courses from "Strategy & Org" to "Business Essentials"
4. Move "AI Code Review Fundamentals" from "Development" to Pro "Cybersecurity"
5. Move "AI Threats: Stay Safe Online" from "Art & Creativity" to YA "Cybersecurity"
6. Create new YA group "AI Tools & Apps" and move 12 non-arts courses there
   from "Art & Creativity"
"""

import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\Users\scott\Code\Aesop\ai-academy\courses.html', encoding='utf-8') as f:
    html = f.read()


# ── Helpers ───────────────────────────────────────────────────────────────────

def remove_by_panel(content, panel_id):
    """Remove a button whose data-panel matches panel_id. Returns (html, btn_str)."""
    pattern = r'[ \t]*<button[^>]+data-panel="' + re.escape(panel_id) + r'"[^>]*>[^<]+</button>[ \t]*\n?'
    m = re.search(pattern, content)
    if not m:
        print(f"  WARNING: button not found for data-panel={panel_id!r}")
        return content, None
    btn = m.group().strip()
    content = content[:m.start()] + content[m.end():]
    print(f"  removed [{panel_id}]")
    return content, btn


def remove_by_course(content, course_id):
    """Remove a button whose data-course matches course_id. Returns (html, btn_str)."""
    pattern = r'[ \t]*<button[^>]+data-course="' + re.escape(course_id) + r'"[^>]*>[^<]+</button>[ \t]*\n?'
    m = re.search(pattern, content)
    if not m:
        print(f"  WARNING: button not found for data-course={course_id!r}")
        return content, None
    btn = m.group().strip()
    content = content[:m.start()] + content[m.end():]
    print(f"  removed [{course_id}]")
    return content, btn


def find_group_end(content, cat_substring):
    """Return the char index of the </div> that closes the mega-group containing cat_substring."""
    cat_pos = content.find(cat_substring)
    if cat_pos < 0:
        return None
    group_start = content.rfind('<div class="mega-group', 0, cat_pos)
    if group_start < 0:
        return None
    pos = group_start
    depth = 0
    while pos < len(content):
        om = re.search(r'<div\b', content[pos:])
        cm = re.search(r'</div>', content[pos:])
        if cm and (not om or cm.start() < om.start()):
            depth -= 1
            if depth == 0:
                return pos + cm.start()  # position of </div>
            pos = pos + cm.end()
        elif om:
            depth += 1
            pos = pos + om.end()
        else:
            break
    return None


def append_to_group(content, cat_substring, btn):
    """Append btn just before closing </div> of the mega-group identified by cat_substring."""
    end = find_group_end(content, cat_substring)
    if end is None:
        print(f"  WARNING: group not found for {cat_substring!r}")
        return content
    insertion = '\n          ' + btn
    content = content[:end] + insertion + '\n        ' + content[end:]
    print(f"  appended to [{cat_substring}]")
    return content


# ─────────────────────────────────────────────────────────────────────────────
# 1. Pentesting courses: Strategy & Org → Pro Cybersecurity
# ─────────────────────────────────────────────────────────────────────────────
print("\n=== 1. Pentesting → Pro Cybersecurity ===")
PENTEST_PANELS = [
    'aip-ai-network-pentesting',
    'aip-ai-web-app-pentesting',
    'aip-ai-augmented-reconnaissance',
    'aip-pentesting-ai-agents',
    'aip-pentesting-llm-applications',
]
for panel in PENTEST_PANELS:
    html, btn = remove_by_panel(html, panel)
    if btn:
        # Pro Cybersecurity comes after the YA Cybersecurity; use the second occurrence
        # Find the second "Cybersecurity" group (in the Pro tier)
        first = html.find('🔒 Cybersecurity')
        second = html.find('🔒 Cybersecurity', first + 1)
        target = '🔒 Cybersecurity' if second < 0 else None
        # Use position-aware approach: append to the second Cybersecurity group
        if second >= 0:
            end = find_group_end(html, html[second:second + 20])
            if end:
                html = html[:end] + '\n          ' + btn + '\n        ' + html[end:]
                print(f"    appended to Pro Cybersecurity")
        else:
            html = append_to_group(html, '🔒 Cybersecurity', btn)


# ─────────────────────────────────────────────────────────────────────────────
# 2. Dev-tool courses: Strategy & Org → Development
# ─────────────────────────────────────────────────────────────────────────────
print("\n=== 2. Dev tools → Development ===")
DEV_PANELS = [
    'aip-ai-coding-tools-for-dev-teams',
    'aip-ai-workflow-automation-n8n',
    'aip-building-multi-agent-teams-crewai',
]
for panel in DEV_PANELS:
    html, btn = remove_by_panel(html, panel)
    if btn:
        html = append_to_group(html, '⚙️ Development', btn)


# ─────────────────────────────────────────────────────────────────────────────
# 3. Business courses: Strategy & Org → Business Essentials
# ─────────────────────────────────────────────────────────────────────────────
print("\n=== 3. Business → Business Essentials ===")
BUS_PANELS = [
    'bu-7',   # Building an AI-First Business
    'bu-11',  # AI for Small Business Managers
    'bu-8',   # AI for Finance and Operations
    'bu-10',  # Procurement and Vendor Evaluation
]
for panel in BUS_PANELS:
    html, btn = remove_by_panel(html, panel)
    if btn:
        html = append_to_group(html, '💡 Business Essentials', btn)


# ─────────────────────────────────────────────────────────────────────────────
# 4. AI Code Review: Development → Pro Cybersecurity
# ─────────────────────────────────────────────────────────────────────────────
print("\n=== 4. AI Code Review → Pro Cybersecurity ===")
html, btn = remove_by_panel(html, 'aip-ai-code-review-fundamentals')
if btn:
    first = html.find('🔒 Cybersecurity')
    second = html.find('🔒 Cybersecurity', first + 1)
    if second >= 0:
        end = find_group_end(html, html[second:second + 20])
        if end:
            html = html[:end] + '\n          ' + btn + '\n        ' + html[end:]
            print("  appended to Pro Cybersecurity")
    else:
        html = append_to_group(html, '🔒 Cybersecurity', btn)


# ─────────────────────────────────────────────────────────────────────────────
# 5. AI Threats: Art & Creativity → YA Cybersecurity
# ─────────────────────────────────────────────────────────────────────────────
print("\n=== 5. AI Threats → YA Cybersecurity ===")
html, btn = remove_by_course(html, 'ai-and-cybersecurity-protect-yourself')
if btn:
    # YA Cybersecurity is the FIRST occurrence of '🔒 Cybersecurity'
    html = append_to_group(html, '🔒 Cybersecurity', btn)


# ─────────────────────────────────────────────────────────────────────────────
# 6. Create new YA group "AI Tools & Apps"; move 12 non-arts courses from
#    "Art & Creativity"
# ─────────────────────────────────────────────────────────────────────────────
print("\n=== 6. Create YA 'AI Tools & Apps' group ===")
TOOLS_COURSES = [
    'ai-agent-safety-when-things-go-wrong',   # AI Agents: What Could Go Wrong
    'launch-your-ai-startup',                  # Build an AI Startup From Scratch
    'chatgpt-for-students-freelancers',        # ChatGPT: Your Unfair Advantage
    'claude-for-real-work',                    # Claude: Write, Research, Build
    'deep-learning-for-builders',              # Deep Learning: Build Real Things
    'gemini-for-college-life',                 # Gemini: AI for School and Life
    'ai-hype-critical-thinking',               # Is the AI Hype Even Real?
    'agile-ai-side-projects',                  # Launch Your AI Side Project
    'notion-ai-for-students',                  # NotionAI: Study, Plan, Build
    'open-source-ai-why-it-matters',           # Open Source AI: Use It, Own It
    'prompt-engineering-that-works',           # Prompt Engineering: Get More Out
    'python-for-ai-projects',                  # Python for AI: Zero to Project
]

collected = []
for course_id in TOOLS_COURSES:
    html, btn = remove_by_course(html, course_id)
    if btn:
        collected.append(btn)

if collected:
    # Insert the new group right after the closing </div> of "Art & Creativity"
    art_pos = html.find('🎨 Art')
    if art_pos < 0:
        art_pos = html.find('Art &amp; Creativity')
    art_end = find_group_end(html, html[art_pos:art_pos + 25])
    if art_end is not None:
        btn_block = '\n          '.join(collected)
        new_group = (
            '\n        <div class="mega-group">'
            '\n          <div class="mega-cat">🛠️ AI Tools &amp; Apps</div>'
            '\n          ' + btn_block +
            '\n        </div>'
        )
        html = html[:art_end + len('</div>')] + new_group + html[art_end + len('</div>'):]
        print(f"  Created YA group '🛠️ AI Tools & Apps' with {len(collected)} courses")
    else:
        print("  WARNING: could not locate end of Art & Creativity group")
else:
    print("  WARNING: no courses collected for new group")


# ─────────────────────────────────────────────────────────────────────────────
# Write result
# ─────────────────────────────────────────────────────────────────────────────
with open(r'C:\Users\scott\Code\Aesop\ai-academy\courses.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("\n✓ courses.html saved")
