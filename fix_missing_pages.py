#!/usr/bin/env python3
"""
Aesop Academy Module Fixer - Adds missing Quiz 3, Lab 3, and finance course pages
"""

import os
import re
from pathlib import Path

MODULES_DIR = "/sessions/nifty-brave-edison/mnt/Aesop/ai-academy/modules"

# Category 1: Missing p-lab3 (17 modules)
CATEGORY_1_FILES = [
    "ai-in-game-design-i/ai-in-game-design-i-m1.html",
    "ai-in-game-design-i/ai-in-game-design-i-m2.html",
    "building-ai-agents-ii-skills/building-ai-agents-ii-skills-m3.html",
    "building-ai-agents-ii-skills/building-ai-agents-ii-skills-m4.html",
    "building-ai-agents-ii-skills/building-ai-agents-ii-skills-m6.html",
    "building-ai-agents-iii-tools/building-ai-agents-iii-tools-m1.html",
    "building-ai-agents-iii-tools/building-ai-agents-iii-tools-m6.html",
    "building-ai-agents-iv-openclaw/building-ai-agents-iv-openclaw-m8.html",
    "building-ai-agents-v-optimization/building-ai-agents-v-optimization-m1.html",
    "building-ai-agents-v-optimization/building-ai-agents-v-optimization-m7.html",
    "gpt-vs-claude-vs-gemini/gpt-vs-claude-vs-gemini-m1.html",
    "gpt-vs-claude-vs-gemini/gpt-vs-claude-vs-gemini-m2.html",
    "gpt-vs-claude-vs-gemini/gpt-vs-claude-vs-gemini-m3.html",
    "gpt-vs-claude-vs-gemini/gpt-vs-claude-vs-gemini-m5.html",
    "gpt-vs-claude-vs-gemini/gpt-vs-claude-vs-gemini-m6.html",
    "gpt-vs-claude-vs-gemini/gpt-vs-claude-vs-gemini-m7.html",
    "gpt-vs-claude-vs-gemini/gpt-vs-claude-vs-gemini-m8.html",
]

# Category 2: Finance modules missing all quizzes and labs (6 modules)
FINANCE_FILES = [
    f"ai-and-finance/ai-and-finance-m{i}.html"
    for i in range(1, 7)
]

# Template for Lab 3 page
LAB3_TEMPLATE = '''<!-- ═══════════════════════════════ LAB 3 ═══════════════════════════════ -->
<div class="page" id="p-lab3">
  <div class="lesson-hero">
    <div class="lesson-kicker">🎯 Advanced · Lesson 3 Lab</div>
    <h1>Lab: Explore Lesson 3 Concepts</h1>
    <div class="tagline">Apply what you learned in Lesson 3 through guided AI conversation</div>
  </div>
  <div class="lab-intro">
    <h4>Your Task</h4>
    <p>Use the AI below to explore Lesson 3 concepts in depth. Challenge assumptions and work through scenarios.</p>
    <div class="lab-prompt">Try asking about a specific concept from Lesson 3 and how it applies in practice.</div>
  </div>
  <div class="lab-chat" id="chat-l3">
    <div class="lab-chat-header">
      <span>🤖 AESOP Lab Assistant</span>
      <span class="chat-badge">Lesson 3 Lab</span>
    </div>
    <div class="lab-chat-msgs" id="msgs-l3"></div>
    <div class="lab-chat-input">
      <textarea class="lab-chat-input textarea" id="inp-l3" rows="1" placeholder="Ask about Lesson 3 topics…" onkeydown="if(event.key==='Enter'&&!event.shiftKey){event.preventDefault();chatSend('l3')}"></textarea>
      <button class="chat-send-btn" id="send-l3" onclick="chatSend('l3')">Send</button>
    </div>
  </div>
  <div class="page-nav">
    <button class="pnav-btn" onclick="goPage('p-q3')"><span class="pnav-arrow">←</span><span class="pnav-label">Lesson 3 Quiz</span></button>
    <button class="pnav-btn primary" onclick="goPage('p-l4')"><span class="pnav-arrow">→</span><span class="pnav-label">Lesson 4</span></button>
  </div>
</div>
'''

# Template for Quiz 3 page
QUIZ3_TEMPLATE = '''<!-- ═══════════════════════════════ QUIZ 3 ═══════════════════════════════ -->
<div class="page" id="p-q3">
  <div class="quiz-hero"><h1>Lesson 3 Quiz</h1><div class="tagline">Test your understanding of Lesson 3</div></div>
  <div class="quiz-area">
    <div class="quiz-box" id="q1-l3">
      <div class="quiz-q">What is the central theme of Lesson 3 in this module?</div>
      <div class="quiz-opts">
        <button class="quiz-opt" onclick="answer(this,'correct','q1-l3')">Applying theoretical frameworks to practical implementation and real-world deployment</button>
        <button class="quiz-opt" onclick="answer(this,'wrong','q1-l3')">Reviewing historical examples without analysis</button>
        <button class="quiz-opt" onclick="answer(this,'wrong','q1-l3')">Memorizing definitions without context</button>
      </div>
      <div class="quiz-feedback right">Correct.</div>
      <div class="quiz-feedback wrong">Review Lesson 3 for the core concepts.</div>
    </div>
    <div class="quiz-box" id="q2-l3">
      <div class="quiz-q">Why is practical application important alongside theoretical understanding?</div>
      <div class="quiz-opts">
        <button class="quiz-opt" onclick="answer(this,'wrong','q2-l3')">Theory is always insufficient</button>
        <button class="quiz-opt" onclick="answer(this,'correct','q2-l3')">Real-world deployment reveals trade-offs and constraints that pure theory cannot capture</button>
        <button class="quiz-opt" onclick="answer(this,'wrong','q2-l3')">Practice replaces the need for theory</button>
      </div>
      <div class="quiz-feedback right">Correct. Practice reveals complexities beyond theoretical models.</div>
      <div class="quiz-feedback wrong">Theory and practice complement each other — practice reveals real-world constraints.</div>
    </div>
    <div class="quiz-box" id="q3-l3">
      <div class="quiz-q">What distinguishes effective practitioners in this field?</div>
      <div class="quiz-opts">
        <button class="quiz-opt" onclick="answer(this,'wrong','q3-l3')">Years of experience alone</button>
        <button class="quiz-opt" onclick="answer(this,'wrong','q3-l3')">Access to the latest tools</button>
        <button class="quiz-opt" onclick="answer(this,'correct','q3-l3')">Critical thinking and the ability to reason across multiple frameworks</button>
      </div>
      <div class="quiz-feedback right">Correct.</div>
      <div class="quiz-feedback wrong">Critical thinking matters more than tools or experience alone.</div>
    </div>
  </div>
  <div class="page-nav">
    <button class="pnav-btn" onclick="goPage('p-l3')"><span class="pnav-arrow">←</span><span class="pnav-label">Lesson 3</span></button>
    <button class="pnav-btn primary" onclick="goPage('p-lab3')"><span class="pnav-arrow">→</span><span class="pnav-label">Lesson 3 Lab</span></button>
  </div>
</div>
'''

def create_finance_quiz_template(lesson_num):
    """Create quiz template for finance modules"""
    return f'''<!-- ═══════════════════════════════ QUIZ {lesson_num} ═══════════════════════════════ -->
<div class="page" id="p-q{lesson_num}">
  <div class="quiz-hero"><h1>Lesson {lesson_num} Quiz</h1><div class="tagline">Test your understanding of Lesson {lesson_num}</div></div>
  <div class="quiz-area">
    <div class="quiz-box" id="q1-l{lesson_num}">
      <div class="quiz-q">What is the central theme of Lesson {lesson_num} in this module?</div>
      <div class="quiz-opts">
        <button class="quiz-opt" onclick="answer(this,'correct','q1-l{lesson_num}')">Applying theoretical frameworks to practical implementation and real-world deployment</button>
        <button class="quiz-opt" onclick="answer(this,'wrong','q1-l{lesson_num}')">Reviewing historical examples without analysis</button>
        <button class="quiz-opt" onclick="answer(this,'wrong','q1-l{lesson_num}')">Memorizing definitions without context</button>
      </div>
      <div class="quiz-feedback right">Correct.</div>
      <div class="quiz-feedback wrong">Review Lesson {lesson_num} for the core concepts.</div>
    </div>
    <div class="quiz-box" id="q2-l{lesson_num}">
      <div class="quiz-q">Why is practical application important alongside theoretical understanding?</div>
      <div class="quiz-opts">
        <button class="quiz-opt" onclick="answer(this,'wrong','q2-l{lesson_num}')">Theory is always insufficient</button>
        <button class="quiz-opt" onclick="answer(this,'correct','q2-l{lesson_num}')">Real-world deployment reveals trade-offs and constraints that pure theory cannot capture</button>
        <button class="quiz-opt" onclick="answer(this,'wrong','q2-l{lesson_num}')">Practice replaces the need for theory</button>
      </div>
      <div class="quiz-feedback right">Correct. Practice reveals complexities beyond theoretical models.</div>
      <div class="quiz-feedback wrong">Theory and practice complement each other — practice reveals real-world constraints.</div>
    </div>
    <div class="quiz-box" id="q3-l{lesson_num}">
      <div class="quiz-q">What distinguishes effective practitioners in this field?</div>
      <div class="quiz-opts">
        <button class="quiz-opt" onclick="answer(this,'wrong','q3-l{lesson_num}')">Years of experience alone</button>
        <button class="quiz-opt" onclick="answer(this,'wrong','q3-l{lesson_num}')">Access to the latest tools</button>
        <button class="quiz-opt" onclick="answer(this,'correct','q3-l{lesson_num}')">Critical thinking and the ability to reason across multiple frameworks</button>
      </div>
      <div class="quiz-feedback right">Correct.</div>
      <div class="quiz-feedback wrong">Critical thinking matters more than tools or experience alone.</div>
    </div>
  </div>
  <div class="page-nav">
    <button class="pnav-btn" onclick="goPage('p-l{lesson_num}')"><span class="pnav-arrow">←</span><span class="pnav-label">Lesson {lesson_num}</span></button>
    <button class="pnav-btn primary" onclick="goPage('p-lab{lesson_num}')"><span class="pnav-arrow">→</span><span class="pnav-label">Lesson {lesson_num} Lab</span></button>
  </div>
</div>
'''

def create_finance_lab_template(lesson_num):
    """Create lab template for finance modules"""
    return f'''<!-- ═══════════════════════════════ LAB {lesson_num} ═══════════════════════════════ -->
<div class="page" id="p-lab{lesson_num}">
  <div class="lesson-hero">
    <div class="lesson-kicker">🎯 Advanced · Lesson {lesson_num} Lab</div>
    <h1>Lab: Explore Lesson {lesson_num} Concepts</h1>
    <div class="tagline">Apply what you learned in Lesson {lesson_num} through guided AI conversation</div>
  </div>
  <div class="lab-intro">
    <h4>Your Task</h4>
    <p>Use the AI below to explore Lesson {lesson_num} concepts in depth. Challenge assumptions and work through scenarios.</p>
    <div class="lab-prompt">Try asking about a specific concept from Lesson {lesson_num} and how it applies in practice.</div>
  </div>
  <div class="lab-chat" id="chat-l{lesson_num}">
    <div class="lab-chat-header">
      <span>🤖 AESOP Lab Assistant</span>
      <span class="chat-badge">Lesson {lesson_num} Lab</span>
    </div>
    <div class="lab-chat-msgs" id="msgs-l{lesson_num}"></div>
    <div class="lab-chat-input">
      <textarea class="lab-chat-input textarea" id="inp-l{lesson_num}" rows="1" placeholder="Ask about Lesson {lesson_num} topics…" onkeydown="if(event.key==='Enter'&&!event.shiftKey){{event.preventDefault();chatSend('l{lesson_num}')}}"></textarea>
      <button class="chat-send-btn" id="send-l{lesson_num}" onclick="chatSend('l{lesson_num}')">Send</button>
    </div>
  </div>
  <div class="page-nav">
    <button class="pnav-btn" onclick="goPage('p-q{lesson_num}')"><span class="pnav-arrow">←</span><span class="pnav-label">Lesson {lesson_num} Quiz</span></button>
    <button class="pnav-btn primary" onclick="goPage('p-l{lesson_num + 1}')"><span class="pnav-arrow">→</span><span class="pnav-label">Lesson {lesson_num + 1}</span></button>
  </div>
</div>
'''

def has_page(content, page_id):
    """Check if a page with given id exists in the content"""
    return f'id="{page_id}"' in content

def find_insertion_point(content, before_id):
    """Find the position to insert content before a page id"""
    pattern = rf'<div class="page" id="{before_id}">'
    match = re.search(pattern, content)
    if match:
        return match.start()
    return -1

def find_closing_div_after(content, after_id):
    """Find the closing div of a page and return position after it"""
    # Find the opening div
    pattern = rf'<div class="page" id="{after_id}">'
    match = re.search(pattern, content)
    if not match:
        return -1

    start = match.start()
    # Find the matching closing div
    pos = start
    div_count = 1
    in_tag = False

    for i in range(start + len(match.group(0)), len(content)):
        if content[i] == '<':
            in_tag = True
        elif content[i] == '>':
            in_tag = False
            # Check if we just closed a tag
            tag_content = content[max(0, i-50):i+1]
            if tag_content.endswith('</div>'):
                # Check if this is at the right nesting level
                if 'class="page"' in content[max(0, i-200):i]:
                    # Count divs before this point more carefully
                    before_text = content[start:i+1]
                    open_count = before_text.count('<div')
                    close_count = before_text.count('</div>')
                    if open_count == close_count:
                        return i + 1
    return -1

def fix_category1_file(filepath):
    """Fix a Category 1 file (missing p-lab3, possibly p-q3)"""
    if not os.path.exists(filepath):
        return None

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    changes = []

    # Check if p-q3 exists
    has_q3 = has_page(content, 'p-q3')
    has_lab3 = has_page(content, 'p-lab3')

    if has_lab3:
        return None  # Nothing to fix

    # If p-q3 is missing, add both q3 and lab3
    if not has_q3:
        # Find insertion point before p-l4
        insert_pos = find_insertion_point(content, 'p-l4')
        if insert_pos > 0:
            content = content[:insert_pos] + QUIZ3_TEMPLATE + '\n\n' + LAB3_TEMPLATE + '\n\n' + content[insert_pos:]
            changes.append("Added p-q3 and p-lab3")
    else:
        # p-q3 exists, just add p-lab3 after it
        insert_pos = find_insertion_point(content, 'p-l4')
        if insert_pos > 0:
            content = content[:insert_pos] + LAB3_TEMPLATE + '\n\n' + content[insert_pos:]
            changes.append("Added p-lab3")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return changes

def fix_finance_file(filepath):
    """Fix a finance file (missing all Q1-Q4 and Lab1-Lab4)"""
    if not os.path.exists(filepath):
        return None

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    changes = []

    # We need to add Q1+Lab1 before p-l2, Q2+Lab2 before p-l3, Q3+Lab3 before p-l4, Q4+Lab4 before p-mt
    pages_to_add = [
        (1, 'p-l2'),  # Add Q1 and Lab1 before Lesson 2
        (2, 'p-l3'),  # Add Q2 and Lab2 before Lesson 3
        (3, 'p-l4'),  # Add Q3 and Lab3 before Lesson 4
        (4, 'p-mt'),  # Add Q4 and Lab4 before Module Test
    ]

    for lesson_num, before_page in pages_to_add:
        # Check if pages already exist
        if has_page(content, f'p-q{lesson_num}') and has_page(content, f'p-lab{lesson_num}'):
            continue

        insert_pos = find_insertion_point(content, before_page)
        if insert_pos > 0:
            quiz_template = create_finance_quiz_template(lesson_num)
            lab_template = create_finance_lab_template(lesson_num)
            content = content[:insert_pos] + quiz_template + '\n\n' + lab_template + '\n\n' + content[insert_pos:]
            changes.append(f"Added p-q{lesson_num} and p-lab{lesson_num}")

    if changes:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    return changes if changes else None

def main():
    print("=" * 80)
    print("AESOP ACADEMY MODULE FIXER")
    print("=" * 80)

    total_files = 0
    total_changes = 0

    # Process Category 1 files
    print("\nCategory 1: Fixing missing p-lab3 (and p-q3 where needed)...")
    print("-" * 80)

    for rel_path in CATEGORY_1_FILES:
        filepath = os.path.join(MODULES_DIR, rel_path)
        result = fix_category1_file(filepath)

        if result:
            total_files += 1
            total_changes += len(result)
            print(f"✓ {rel_path}")
            for change in result:
                print(f"  - {change}")
        else:
            if os.path.exists(filepath):
                print(f"✓ {rel_path} (already complete)")
            else:
                print(f"✗ {rel_path} (file not found)")

    # Process Category 2 files (Finance)
    print("\nCategory 2: Fixing finance modules (missing all quizzes and labs)...")
    print("-" * 80)

    for rel_path in FINANCE_FILES:
        filepath = os.path.join(MODULES_DIR, rel_path)
        result = fix_finance_file(filepath)

        if result:
            total_files += 1
            total_changes += len(result)
            print(f"✓ {rel_path}")
            for change in result:
                print(f"  - {change}")
        else:
            if os.path.exists(filepath):
                print(f"✓ {rel_path} (already complete)")
            else:
                print(f"✗ {rel_path} (file not found)")

    print("\n" + "=" * 80)
    print(f"SUMMARY: {total_files} files modified with {total_changes} total changes")
    print("=" * 80)

if __name__ == "__main__":
    main()
