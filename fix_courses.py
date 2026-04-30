import sys, io, re

filepath = r"C:\Users\scott\Code\Aesop\ai-academy\courses.html"
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# --- Step 1: Extract orphaned completion blocks ---
# Lines 6621-6928 (0-indexed: 6620-6927)
orphan_section = lines[6620:6928]

blocks = []
current_block = []
for line in orphan_section:
    if line == '    </div>\n':
        if current_block:
            blocks.append(''.join(current_block))
            current_block = []
    else:
        current_block.append(line)
if current_block:
    blocks.append(''.join(current_block))

# Map blocks to panel IDs (blocks appear in order dv-35..dv-19 in the file)
panel_ids_in_file_order = ['dv-35','dv-34','dv-33','dv-32','dv-31','dv-30','dv-29',
                            'dv-28','dv-27','dv-26','dv-25','dv-24','dv-23','dv-22',
                            'dv-21','dv-20','dv-19']
block_by_id = {panel_ids_in_file_order[i]: blocks[i] for i in range(17)}

print(f"Found {len(blocks)} orphan blocks")

# --- Step 2: Rebuild the truncated panels section ---
# Truncated panels span lines 6477-6596 (0-indexed 6476-6595)
# Each panel ends after its desc div, followed by a blank line then the next panel
truncated_lines = lines[6476:6596]

new_truncated_lines = []
i = 0
while i < len(truncated_lines):
    line = truncated_lines[i]
    new_truncated_lines.append(line)

    # Check if this is a desc closing line (end of truncated panel content)
    if '<div class="core-panel__desc">' in line and '</div>' in line:
        next_line = truncated_lines[i+1] if i+1 < len(truncated_lines) else ''
        if next_line.strip() == '':
            # Find which panel we are in by looking back for its id
            panel_id = None
            for prev in reversed(new_truncated_lines):
                m = re.search(r'id="(dv-\d+)"', prev)
                if m:
                    panel_id = m.group(1)
                    break

            if panel_id and panel_id in block_by_id:
                completion = block_by_id[panel_id]
                new_truncated_lines.append(completion)
                i += 2  # skip the blank line
                continue
    i += 1

print(f"Rebuilt truncated section: {len(new_truncated_lines)} items (was {len(truncated_lines)} lines)")

# --- Step 3: Define the 3 new youth panels ---
youth_panels = (
    '      <div class="core-panel" id="aip-how-ai-actually-works" data-course="how-ai-actually-works">\n'
    '        <div class="core-panel__header">\n'
    '          <span class="core-panel__icon">\U0001f916</span>\n'
    '          <div class="core-panel__meta">\n'
    '            <div class="core-panel__title">Inside the Machine: AI Unpacked</div>\n'
    '            <div class="core-panel__desc">What AI actually is, how it works, and why understanding it changes how you use it.</div>\n'
    '          </div>\n'
    '          <div class="core-panel__badges">\n'
    '            <span class="core-badge-live"><span class="live-dot"></span> Live</span>\n'
    '            <span class="core-badge-mods">6 Modules</span>\n'
    '          </div>\n'
    '        </div>\n'
    '        <div class="core-modules-label">Course modules</div>\n'
    '        <div class="core-modules-grid">\n'
    '          <div class="core-mod"><div class="core-mod__num">M1</div><div class="core-mod__info"><div class="core-mod__title">What Is AI, Really?</div></div></div>\n'
    '          <div class="core-mod"><div class="core-mod__num">M2</div><div class="core-mod__info"><div class="core-mod__title">How AI Learns</div></div></div>\n'
    "          <div class=\"core-mod\"><div class=\"core-mod__num\">M3</div><div class=\"core-mod__info\"><div class=\"core-mod__title\">What AI Can and Can't Do</div></div></div>\n"
    '          <div class="core-mod"><div class="core-mod__num">M4</div><div class="core-mod__info"><div class="core-mod__title">AI in Your World</div></div></div>\n'
    '          <div class="core-mod"><div class="core-mod__num">M5</div><div class="core-mod__info"><div class="core-mod__title">Talking to AI</div></div></div>\n'
    '          <div class="core-mod"><div class="core-mod__num">M6</div><div class="core-mod__info"><div class="core-mod__title">What Comes Next</div></div></div>\n'
    '        </div>\n'
    '        <a href="/ai-academy/modules/electives-hub.html?course=how-ai-actually-works" class="core-panel__cta">Enter Course →</a>\n'
    '      </div>\n'
    '      <div class="core-panel" id="aip-robot-speak-talk-to-ai" data-course="robot-speak-talk-to-ai">\n'
    '        <div class="core-panel__header">\n'
    '          <span class="core-panel__icon">\U0001f5e3️</span>\n'
    '          <div class="core-panel__meta">\n'
    '            <div class="core-panel__title">Robot Speak: Talk to AI!</div>\n'
    '            <div class="core-panel__desc">Learn to communicate with AI tools so they actually understand you — and you understand them.</div>\n'
    '          </div>\n'
    '          <div class="core-panel__badges">\n'
    '            <span class="core-badge-live"><span class="live-dot"></span> Live</span>\n'
    '            <span class="core-badge-mods">6 Modules</span>\n'
    '          </div>\n'
    '        </div>\n'
    '        <div class="core-modules-label">Course modules</div>\n'
    '        <div class="core-modules-grid">\n'
    '          <div class="core-mod"><div class="core-mod__num">M1</div><div class="core-mod__info"><div class="core-mod__title">How AI Understands Words</div></div></div>\n'
    '          <div class="core-mod"><div class="core-mod__num">M2</div><div class="core-mod__info"><div class="core-mod__title">Writing Good Prompts</div></div></div>\n'
    '          <div class="core-mod"><div class="core-mod__num">M3</div><div class="core-mod__info"><div class="core-mod__title">When AI Gets It Wrong</div></div></div>\n'
    '          <div class="core-mod"><div class="core-mod__num">M4</div><div class="core-mod__info"><div class="core-mod__title">Making AI Work for You</div></div></div>\n'
    '          <div class="core-mod"><div class="core-mod__num">M5</div><div class="core-mod__info"><div class="core-mod__title">Asking Better Questions</div></div></div>\n'
    '          <div class="core-mod"><div class="core-mod__num">M6</div><div class="core-mod__info"><div class="core-mod__title">Your AI Conversation</div></div></div>\n'
    '        </div>\n'
    '        <a href="/ai-academy/modules/electives-hub.html?course=robot-speak-talk-to-ai" class="core-panel__cta">Enter Course →</a>\n'
    '      </div>\n'
    '      <div class="core-panel" id="aip-truth-detectives-ai-and-fake-info" data-course="truth-detectives-ai-and-fake-info">\n'
    '        <div class="core-panel__header">\n'
    '          <span class="core-panel__icon">\U0001f50d</span>\n'
    '          <div class="core-panel__meta">\n'
    '            <div class="core-panel__title">Truth Detectives: AI vs. Fake News</div>\n'
    '            <div class="core-panel__desc">Become a truth detective — spot fake news, deepfakes, and AI-generated lies before they fool you.</div>\n'
    '          </div>\n'
    '          <div class="core-panel__badges">\n'
    '            <span class="core-badge-live"><span class="live-dot"></span> Live</span>\n'
    '            <span class="core-badge-mods">6 Modules</span>\n'
    '          </div>\n'
    '        </div>\n'
    '        <div class="core-modules-label">Course modules</div>\n'
    '        <div class="core-modules-grid">\n'
    '          <div class="core-mod"><div class="core-mod__num">M1</div><div class="core-mod__info"><div class="core-mod__title">The Story That Fooled Everyone</div></div></div>\n'
    '          <div class="core-mod"><div class="core-mod__num">M2</div><div class="core-mod__info"><div class="core-mod__title">The Anatomy of an AI-Generated Lie</div></div></div>\n'
    '          <div class="core-mod"><div class="core-mod__num">M3</div><div class="core-mod__info"><div class="core-mod__title">Deepfakes: Real or Not?</div></div></div>\n'
    '          <div class="core-mod"><div class="core-mod__num">M4</div><div class="core-mod__info"><div class="core-mod__title">The Clues Real Detectives Use</div></div></div>\n'
    '          <div class="core-mod"><div class="core-mod__num">M5</div><div class="core-mod__info"><div class="core-mod__title">You Decide: Publish or Delete?</div></div></div>\n'
    '          <div class="core-mod"><div class="core-mod__num">M6</div><div class="core-mod__info"><div class="core-mod__title">Broadcast Your Truth Verdict</div></div></div>\n'
    '        </div>\n'
    '        <a href="/ai-academy/modules/electives-hub.html?course=truth-detectives-ai-and-fake-info" class="core-panel__cta">Enter Course →</a>\n'
    '      </div>\n'
)

# --- Step 4: Assemble the new file ---
# before: everything before dv-19 (lines 0-6475)
before = lines[:6476]
# dv-36 unchanged: lines[6596:6619] (0-indexed), line 6597-6619 (1-indexed)
dv36 = lines[6596:6619]
# after orphaned sections: lines[6929:] starts with "    </div>\n" (panels container close)
after = lines[6929:]

print(f"before: {len(before)} lines")
print(f"dv36: {len(dv36)} lines, starts={repr(dv36[0].rstrip()[:60])}, ends={repr(dv36[-1].rstrip())}")
print(f"after[0]: {repr(after[0].rstrip())} (should be '    </div>')")
print(f"after[1]: {repr(after[1].rstrip())}")

new_lines = before + new_truncated_lines + dv36 + [youth_panels] + after

print(f"\nOld total lines: {len(lines)}")
print(f"New total items: {len(new_lines)}")

# Write back
with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("File written successfully!")
