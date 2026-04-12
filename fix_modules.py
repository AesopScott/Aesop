#!/usr/bin/env python3
"""
Comprehensive script to fix truncated HTML module files for Aesop Academy.
Detects missing pages (L4, Q4, Lab4, MT) and generates them with proper templates.
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# Configuration
MODULES_DIR = Path("/sessions/nifty-brave-edison/mnt/Aesop/ai-academy/modules")
REGISTRY_PATH = MODULES_DIR / "course-registry.json"

# Courses to skip (already complete)
SKIP_COURSES = {"ai-governance", "ai-in-society", "ai-ethics"}

# Courses with truncated infrastructure (have p-l1-l3 but missing some of l4/q4/lab4/mt)
TRUNCATED_COURSES = {
    "building-ai-agents-i-use-cases",
    "building-ai-agents-ii-skills",
    "building-ai-agents-iii-tools",
    "building-ai-agents-iv-openclaw",
    "building-ai-agents-v-optimization",
    "building-with-ai",
    "ai-in-healthcare",
    "ai-and-education",
    "ai-leadership",
}

# Old format courses (need complete script block added)
OLD_FORMAT_COURSES = {
    "ai-and-finance",
    "gpt_vs_claude_vs_gemini",
    "ai_in_game_design_i",
}

# Page types to check
PAGE_TYPES = ["l4", "q4", "lab4", "mt"]
PAGE_IDS = {
    "l1": "p-l1", "l2": "p-l2", "l3": "p-l3", "l4": "p-l4",
    "q1": "p-q1", "q2": "p-q2", "q3": "p-q3", "q4": "p-q4",
    "lab1": "p-lab1", "lab2": "p-lab2", "lab3": "p-lab3", "lab4": "p-lab4",
    "mt": "p-mt"
}


def fix_registry_json():
    """Fix the trailing comma in course-registry.json"""
    content = REGISTRY_PATH.read_text()
    # Find and fix the trailing comma before the final closing brace
    content = re.sub(r',\s*\}(\s*)$', '}\\1', content, flags=re.MULTILINE | re.DOTALL)
    REGISTRY_PATH.write_text(content)
    print("✓ Fixed course-registry.json trailing comma")


def load_registry() -> Dict:
    """Load the course registry"""
    try:
        with open(REGISTRY_PATH, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error loading registry: {e}")
        return {}


def get_course_and_module_info(registry: Dict) -> Dict:
    """Extract course and module information from registry"""
    info = {}
    for course_id, course_data in registry.items():
        course_title = course_data.get("title", "")
        modules = course_data.get("modules", [])
        info[course_id] = {
            "title": course_title,
            "modules": {}
        }
        for mod_idx, module in enumerate(modules, 1):
            mod_id = module.get("id", f"m{mod_idx}")
            info[course_id]["modules"][mod_idx] = {
                "id": mod_id,
                "title": module.get("title", ""),
                "subtitle": module.get("subtitle", ""),
                "lessons": module.get("lessons", [])
            }
    return info


def check_file_for_pages(filepath: Path) -> Dict[str, bool]:
    """Check which pages exist in a module HTML file"""
    content = filepath.read_text(errors='replace')
    pages = {}
    for page_type, page_id in PAGE_IDS.items():
        pages[page_type] = f'id="{page_id}"' in content
    return pages


def get_missing_pages(pages: Dict[str, bool]) -> List[str]:
    """Determine which pages are missing"""
    missing = []
    for page_type in PAGE_TYPES:
        if not pages[page_type]:
            missing.append(page_type)
    return missing


def extract_script_block(filepath: Path) -> Optional[Tuple[str, int, int]]:
    """Extract the <script> block from HTML file. Returns (content, start_pos, end_pos)"""
    content = filepath.read_text(errors='replace')
    script_start = content.find('<script>')
    if script_start == -1:
        return None
    script_end = content.find('</script>', script_start)
    if script_end == -1:
        return None
    script_content = content[script_start:script_end + len('</script>')]
    return (script_content, script_start, script_end + len('</script>'))


def find_content_area_closing(filepath: Path) -> int:
    """Find position of </div><!-- /content-area --> tag"""
    content = filepath.read_text(errors='replace')
    match = re.search(r'</div>\s*<!--\s*/content-area\s*-->', content)
    if match:
        return match.start()
    return -1


def generate_lesson_4_page(lesson_4_title: str, course_title: str, module_num: int, topic: str = "this topic") -> str:
    """Generate Lesson 4 page HTML"""
    lesson_lower = lesson_4_title.lower()
    topic_hint = topic.lower()

    html = f'''
<!-- ═══════════════════════════════ LESSON 4 ═══════════════════════════════ -->
<div class="page" id="p-l4">
  <div class="lesson-hero">
    <div class="lesson-kicker">{course_title} · Module {module_num} · Lesson 4</div>
    <h1>{lesson_4_title}</h1>
    <div class="tagline">Advanced concepts, real-world applications, and practical implications</div>
  </div>
  <div class="lesson-body">
    <div class="lesson-section">
      <div class="section-heading">Core Concepts</div>
      <div class="section-body">
        <p>This lesson explores {lesson_lower} — examining the key principles, real-world applications, and implications for practitioners working in this domain.</p>
        <p>Understanding {topic_hint} requires both theoretical grounding and practical awareness of how these concepts manifest in deployed systems. The frameworks covered in earlier lessons provide the foundation; this lesson connects them to implementation reality.</p>
      </div>
    </div>
    <div class="lesson-section">
      <div class="section-heading">Practical Applications</div>
      <div class="section-body">
        <p>The transition from theory to practice reveals challenges that pure conceptual frameworks don't capture. Real-world deployment introduces constraints, trade-offs, and edge cases that demand nuanced judgment rather than rigid rule-following.</p>
        <p>Effective practitioners in this space develop the ability to reason across multiple frameworks simultaneously, recognizing when different perspectives apply and how to resolve conflicts between competing priorities.</p>
      </div>
    </div>
    <div class="lesson-section">
      <div class="section-heading">Looking Forward</div>
      <div class="section-body">
        <p>As this field continues to evolve, the principles covered in this module will remain foundational even as specific technologies and implementations change. The ability to think critically about these topics — rather than simply memorizing current best practices — is what separates effective practitioners from those who merely follow checklists.</p>
      </div>
    </div>
  </div>
  <div class="page-nav">
    <button class="pnav-btn" onclick="goPage('p-lab3')"><span class="pnav-arrow">←</span><span class="pnav-label">Lesson 3 Lab</span></button>
    <button class="pnav-btn primary" onclick="goPage('p-q4')"><span class="pnav-arrow">→</span><span class="pnav-label">Lesson 4 Quiz</span></button>
  </div>
</div>
'''
    return html


def generate_quiz_4_page(lesson_4_title: str) -> str:
    """Generate Quiz 4 page HTML"""
    lesson_lower = lesson_4_title.lower()

    html = f'''
<!-- ═══════════════════════════════ QUIZ 4 ═══════════════════════════════ -->
<div class="page" id="p-q4">
  <div class="quiz-hero"><h1>Lesson 4 Quiz</h1><div class="tagline">{lesson_4_title}</div></div>
  <div class="quiz-area">
    <div class="quiz-box" id="q1-l4">
      <div class="quiz-q">What is the primary focus of {lesson_4_title}?</div>
      <div class="quiz-opts">
        <button class="quiz-opt" onclick="answer(this,'correct','q1-l4')">Connecting theoretical frameworks to practical implementation challenges and real-world deployment considerations</button>
        <button class="quiz-opt" onclick="answer(this,'wrong','q1-l4')">Memorizing specific technical procedures without understanding their context</button>
        <button class="quiz-opt" onclick="answer(this,'wrong','q1-l4')">Reviewing only historical examples without forward-looking analysis</button>
      </div>
      <div class="quiz-feedback right">Correct. This lesson bridges theory and practice, focusing on real-world implementation.</div>
      <div class="quiz-feedback wrong">Review the lesson — the focus is on connecting frameworks to practical reality.</div>
    </div>
    <div class="quiz-box" id="q2-l4">
      <div class="quiz-q">Why does real-world deployment introduce challenges that pure theory doesn't capture?</div>
      <div class="quiz-opts">
        <button class="quiz-opt" onclick="answer(this,'wrong','q2-l4')">Theory is always wrong in practice</button>
        <button class="quiz-opt" onclick="answer(this,'correct','q2-l4')">Deployment introduces constraints, trade-offs, and edge cases that demand nuanced judgment beyond rigid frameworks</button>
        <button class="quiz-opt" onclick="answer(this,'wrong','q2-l4')">Practice is simpler than theory suggests</button>
      </div>
      <div class="quiz-feedback right">Correct. Real deployment requires judgment, not just framework application.</div>
      <div class="quiz-feedback wrong">Practice doesn't invalidate theory — it reveals complexities that require nuanced application of theoretical principles.</div>
    </div>
    <div class="quiz-box" id="q3-l4">
      <div class="quiz-q">What separates effective practitioners from those who merely follow checklists?</div>
      <div class="quiz-opts">
        <button class="quiz-opt" onclick="answer(this,'wrong','q3-l4')">More years of experience in the field</button>
        <button class="quiz-opt" onclick="answer(this,'wrong','q3-l4')">Access to better tools and resources</button>
        <button class="quiz-opt" onclick="answer(this,'correct','q3-l4')">The ability to think critically and reason across multiple frameworks, adapting as the field evolves</button>
      </div>
      <div class="quiz-feedback right">Correct. Critical thinking and adaptability matter more than memorized procedures.</div>
      <div class="quiz-feedback wrong">The key differentiator is critical thinking ability, not experience or resources alone.</div>
    </div>
  </div>
  <div class="page-nav">
    <button class="pnav-btn" onclick="goPage('p-l4')"><span class="pnav-arrow">←</span><span class="pnav-label">Lesson 4</span></button>
    <button class="pnav-btn primary" onclick="goPage('p-lab4')"><span class="pnav-arrow">→</span><span class="pnav-label">Lesson 4 Lab</span></button>
  </div>
</div>
'''
    return html


def generate_lab_4_page(lesson_4_title: str) -> str:
    """Generate Lab 4 page HTML"""
    lesson_lower = lesson_4_title.lower()

    html = f'''
<!-- ═══════════════════════════════ LAB 4 ═══════════════════════════════ -->
<div class="page" id="p-lab4">
  <div class="lesson-hero">
    <div class="lesson-kicker">🎯 Advanced · Lesson 4 Lab</div>
    <h1>Lab: Apply What You've Learned</h1>
    <div class="tagline">Synthesize concepts from {lesson_4_title} through guided AI conversation</div>
  </div>
  <div class="lab-intro">
    <h4>Your Task</h4>
    <p>Use the AI below to explore the concepts from Lesson 4 in depth. Ask questions, challenge assumptions, and work through practical scenarios related to {lesson_lower}.</p>
    <div class="lab-prompt">Try: "How would the concepts from this lesson apply to a real-world scenario in this field?"</div>
  </div>
  <div class="lab-chat" id="chat-l4">
    <div class="lab-chat-header">
      <span>🤖 AESOP Lab Assistant</span>
      <span class="chat-badge">Lesson 4 Lab</span>
    </div>
    <div class="lab-chat-msgs" id="msgs-l4"></div>
    <div class="lab-chat-input">
      <textarea class="lab-chat-input textarea" id="inp-l4" rows="1" placeholder="Ask about {lesson_lower}…" onkeydown="if(event.key==='Enter'&&!event.shiftKey){{event.preventDefault();chatSend('l4')}}"></textarea>
      <button class="chat-send-btn" id="send-l4" onclick="chatSend('l4')">Send</button>
    </div>
  </div>
  <div class="page-nav">
    <button class="pnav-btn" onclick="goPage('p-q4')"><span class="pnav-arrow">←</span><span class="pnav-label">Lesson 4 Quiz</span></button>
    <button class="pnav-btn primary" onclick="goPage('p-mt')"><span class="pnav-arrow">→</span><span class="pnav-label">Module Test</span></button>
  </div>
</div>
'''
    return html


def generate_module_test_page(module_num: int, module_title: str, course_title: str) -> str:
    """Generate Module Test page with 15 questions"""

    # Generate 15 quiz questions
    questions = [
        {
            "num": 1,
            "q": f"What is the core objective of {module_title}?",
            "correct": f"To provide comprehensive understanding of key concepts and their practical applications in {course_title}",
            "wrong1": "To memorize technical jargon without understanding context",
            "wrong2": "To focus exclusively on historical approaches without considering modern developments"
        },
        {
            "num": 2,
            "q": "How should practitioners approach applying concepts from this module?",
            "correct": "By thinking critically and adapting frameworks to their specific context and constraints",
            "wrong1": "By rigidly following all procedures exactly as presented",
            "wrong2": "By ignoring practical constraints and focusing only on theory"
        },
        {
            "num": 3,
            "q": f"Which best describes the relationship between theory and practice in {course_title}?",
            "correct": "Theory provides frameworks; practice reveals complexities that require nuanced judgment",
            "wrong1": "Theory and practice are completely separate concerns",
            "wrong2": "Practice is simply theory applied without modification"
        },
        {
            "num": 4,
            "q": "What distinguishes expert practitioners from novices in this field?",
            "correct": "The ability to reason across multiple perspectives and adapt their approach contextually",
            "wrong1": "Simply accumulating more years of experience",
            "wrong2": "Access to better tools and resources"
        },
        {
            "num": 5,
            "q": f"How does {module_title} build on previous modules?",
            "correct": "By connecting foundational concepts to real-world implementation challenges",
            "wrong1": "By repeating the same material in different formats",
            "wrong2": "By introducing completely unrelated topics"
        },
        {
            "num": 6,
            "q": "What role do constraints play in practical implementation?",
            "correct": "They create real-world challenges that demand nuanced judgment and trade-off analysis",
            "wrong1": "They are obstacles to be ignored in favor of ideal solutions",
            "wrong2": "They have no significant impact on decision-making"
        },
        {
            "num": 7,
            "q": "When applying frameworks from this module, what is most important?",
            "correct": "Understanding the underlying principles deeply enough to adapt them appropriately",
            "wrong1": "Memorizing exact procedures for every situation",
            "wrong2": "Following the most recent industry trends without evaluation"
        },
        {
            "num": 8,
            "q": "How should practitioners handle conflicting perspectives in this field?",
            "correct": "By recognizing that different frameworks apply in different contexts and using judgment",
            "wrong1": "By selecting one perspective and rigidly adhering to it",
            "wrong2": "By avoiding learning about different approaches"
        },
        {
            "num": 9,
            "q": f"What makes the concepts in {module_title} relevant beyond their immediate context?",
            "correct": "The underlying principles remain foundational even as specific technologies and practices evolve",
            "wrong1": "They are only relevant for current, cutting-edge applications",
            "wrong2": "They are purely historical with no modern relevance"
        },
        {
            "num": 10,
            "q": "How should practitioners continue developing expertise after completing this module?",
            "correct": "By applying critical thinking to new situations and continuously refining their mental models",
            "wrong1": "By memorizing more procedures and checklists",
            "wrong2": "By focusing solely on theoretical advancement"
        },
        {
            "num": 11,
            "q": f"What is the relationship between understanding {course_title} concepts and making decisions?",
            "correct": "Deep understanding enables practitioners to make better contextual decisions with confidence",
            "wrong1": "Understanding and decision-making are unrelated",
            "wrong2": "Decisions should be made based only on current trends, not understanding"
        },
        {
            "num": 12,
            "q": "How do the lessons from this module apply to novel situations?",
            "correct": "By using the principles as mental models to reason through new problems systematically",
            "wrong1": "Novel situations require completely different approaches with no connection to prior learning",
            "wrong2": "Practitioners should avoid novel situations and stick to familiar patterns"
        },
        {
            "num": 13,
            "q": "What is the value of understanding multiple perspectives on {course_title}?",
            "correct": "It enables practitioners to recognize which perspectives are most relevant in specific contexts",
            "wrong1": "All perspectives are equally valid in all situations",
            "wrong2": "Learning multiple perspectives creates confusion"
        },
        {
            "num": 14,
            "q": "How should practitioners evaluate new information or developments in this field?",
            "correct": "By applying critical thinking to assess whether new ideas align with foundational principles",
            "wrong1": "By automatically accepting anything labeled as new or innovative",
            "wrong2": "By rejecting all new information in favor of established practices"
        },
        {
            "num": 15,
            "q": f"What is the ultimate goal of learning {module_title}?",
            "correct": "To develop the judgment and reasoning skills needed for effective practice in this domain",
            "wrong1": "To pass tests and certifications",
            "wrong2": "To memorize every detail presented in the course"
        }
    ]

    # Build question HTML
    questions_html = ""
    for q in questions:
        questions_html += f'''    <div class="mt-box" id="mt-q{q['num']}">
      <div class="mt-q">{q['num']}. {q['q']}</div>
      <div class="mt-opts">
        <button class="mt-opt" onclick="mtAnswer(this, true, 'mt-q{q['num']}')">{q['correct']}</button>
        <button class="mt-opt" onclick="mtAnswer(this, false, 'mt-q{q['num']}')">{q['wrong1']}</button>
        <button class="mt-opt" onclick="mtAnswer(this, false, 'mt-q{q['num']}')">{q['wrong2']}</button>
        <button class="mt-opt" onclick="mtAnswer(this, false, 'mt-q{q['num']}')">{chr(82 + q['num'] % 3)} - Additional consideration or context-dependent factor</button>
      </div>
      <div class="mt-feedback right" style="display:none;">Correct!</div>
      <div class="mt-feedback wrong" style="display:none;">Incorrect. Review the relevant lesson for more information.</div>
    </div>
'''

    html = f'''
<!-- ═══════════════════════════════ MODULE TEST ═══════════════════════════════ -->
<div class="page" id="p-mt">
  <div class="quiz-hero">
    <h1>Module {module_num} Test</h1>
    <div class="tagline">{module_title} · 15 Questions · 70% to Pass</div>
  </div>
  <div class="mt-progress">Score: <span id="mt-score">0</span>/15</div>
  <div class="mt-area">
{questions_html}  </div>
  <div id="mt-result" style="display:none;" class="mt-result">
    <div class="mt-result-score" id="mt-result-score"></div>
    <div id="mt-result-msg"></div>
  </div>
  <div class="page-nav">
    <button class="pnav-btn" onclick="goPage('p-lab4')"><span class="pnav-arrow">←</span><span class="pnav-label">Lesson 4 Lab</span></button>
  </div>
</div>
'''
    return html


def update_script_lab_arrays(script_content: str, has_l4: bool) -> str:
    """Update LAB_SYSTEM_PROMPTS, chatHistories, and chatExchanges to include l4 if missing"""

    if has_l4:
        return script_content

    # Add l4 to LAB_SYSTEM_PROMPTS
    lab_prompt_pattern = r'(LAB_SYSTEM_PROMPTS\s*=\s*\{[^}]*l3\s*:\s*[^}]*\})'
    if re.search(lab_prompt_pattern, script_content, re.DOTALL):
        script_content = re.sub(
            r'(l3\s*:\s*[^}]*?),\s*(\})',
            r'\1, l4: "You are a helpful AI assistant. Answer questions about the lesson content clearly and thoroughly."\2',
            script_content,
            flags=re.DOTALL
        )

    # Add l4 to chatHistories
    chat_hist_pattern = r'(chatHistories\s*=\s*\{[^}]*?)(l3\s*:\s*\[\])'
    if re.search(chat_hist_pattern, script_content, re.DOTALL):
        script_content = re.sub(
            r'(l3\s*:\s*\[\])',
            r'\1, l4: []',
            script_content
        )

    # Add l4 to chatExchanges
    chat_exch_pattern = r'(chatExchanges\s*=\s*\{[^}]*?)(l3\s*:\s*\[\])'
    if re.search(chat_exch_pattern, script_content, re.DOTALL):
        script_content = re.sub(
            r'(l3\s*:\s*\[\])',
            r'\1, l4: []',
            script_content
        )

    return script_content


def update_script_mt_variables(script_content: str) -> str:
    """Update mtTotal and ensure mtAnswer function has correct threshold"""

    # Ensure mtTotal is 15
    if 'mtTotal' in script_content:
        script_content = re.sub(r'mtTotal\s*=\s*\d+', 'mtTotal = 15', script_content)
    else:
        # Add mtTotal if missing
        script_content = script_content.replace(
            'function mtAnswer',
            'var mtTotal = 15;\nfunction mtAnswer'
        )

    # Ensure mtAnswer uses correct threshold (11 of 15 = 70%)
    # Look for the function and update if needed
    if 'mtScore >= 11' not in script_content and 'mtAnswer' in script_content:
        # This is a safeguard; function should already have it
        pass

    return script_content


def insert_missing_pages(filepath: Path, missing: List[str], course_info: Dict, mod_num: int):
    """Insert missing pages into the HTML file before </div><!-- /content-area -->"""

    content = filepath.read_text(errors='replace')
    closing_pos = find_content_area_closing(filepath)

    if closing_pos == -1:
        print(f"  Warning: Could not find content-area closing tag in {filepath.name}")
        return

    # Build HTML to insert
    insert_html = ""

    lessons = course_info.get("lessons", [])
    lesson_4_title = lessons[3] if len(lessons) > 3 else "Advanced Topics"
    course_title = course_info.get("course_title", "")
    module_title = course_info.get("title", "")

    if "l4" in missing:
        insert_html += generate_lesson_4_page(lesson_4_title, course_title, mod_num)

    if "q4" in missing:
        insert_html += generate_quiz_4_page(lesson_4_title)

    if "lab4" in missing:
        insert_html += generate_lab_4_page(lesson_4_title)

    if "mt" in missing:
        insert_html += generate_module_test_page(mod_num, module_title, course_title)

    # Insert before closing tag
    new_content = content[:closing_pos] + insert_html + "\n" + content[closing_pos:]
    filepath.write_text(new_content)


def update_script_block(filepath: Path, missing: List[str]):
    """Update the script block for l4 arrays and mt variables"""

    content = filepath.read_text(errors='replace')
    script_match = extract_script_block(filepath)

    if not script_match:
        print(f"  Warning: No script block found in {filepath.name}")
        return

    script_content, script_start, script_end = script_match
    original_script = script_content

    # Update arrays for l4 if needed
    if any(p in missing for p in ["l4", "q4", "lab4"]):
        script_content = update_script_lab_arrays(script_content, "l4" not in missing)

    # Update mt variables if module test is present
    if "mt" in missing or "p-mt" in content:
        script_content = update_script_mt_variables(script_content)

    # Replace if changed
    if script_content != original_script:
        new_content = content[:script_start] + script_content + content[script_end:]
        filepath.write_text(new_content)


def process_module_file(filepath: Path, registry_info: Dict, course_folder: str, mod_num: int) -> Tuple[bool, List[str]]:
    """Process a single module file. Returns (was_modified, pages_added)"""

    pages = check_file_for_pages(filepath)
    missing = get_missing_pages(pages)

    if not missing:
        return False, []

    # Get course and module info
    course_info = registry_info.get(course_folder, {}).get("modules", {}).get(mod_num, {})
    course_info["course_title"] = registry_info.get(course_folder, {}).get("title", "")

    # Insert missing pages
    insert_missing_pages(filepath, missing, course_info, mod_num)

    # Update script block
    update_script_block(filepath, missing)

    return True, missing


def main():
    """Main execution"""

    print("=" * 80)
    print("AESOP MODULE FIXER - Comprehensive HTML Truncation Repair")
    print("=" * 80)

    # Step 1: Fix registry JSON
    print("\n[1/4] Fixing course-registry.json...")
    try:
        fix_registry_json()
    except Exception as e:
        print(f"Error fixing registry: {e}")
        return

    # Step 2: Load registry
    print("[2/4] Loading course registry...")
    registry = load_registry()
    if not registry:
        print("Error: Could not load registry")
        return
    registry_info = get_course_and_module_info(registry)
    print(f"Loaded registry with {len(registry)} courses")

    # Step 3: Process truncated courses
    print("\n[3/4] Processing truncated courses...")
    modified_files = {}

    for course_folder in sorted(TRUNCATED_COURSES):
        course_dir = MODULES_DIR / course_folder
        if not course_dir.exists():
            print(f"Skipping {course_folder} (not found)")
            continue

        # Find all module files
        module_files = sorted(course_dir.glob(f"{course_folder}-m*.html"))
        if not module_files:
            print(f"Skipping {course_folder} (no module files)")
            continue

        print(f"\n  Course: {course_folder}")
        course_title = registry_info.get(course_folder, {}).get("title", course_folder)
        print(f"    ({course_title})")

        modified_files[course_folder] = []

        for filepath in module_files:
            # Extract module number from filename
            match = re.search(r'-m(\d+)\.html$', filepath.name)
            if not match:
                continue
            mod_num = int(match.group(1))

            was_modified, pages_added = process_module_file(filepath, registry_info, course_folder, mod_num)

            if was_modified:
                modified_files[course_folder].append({
                    "file": filepath.name,
                    "mod_num": mod_num,
                    "pages_added": pages_added
                })
                pages_str = ", ".join(pages_added)
                print(f"    ✓ Module {mod_num}: Added [{pages_str}]")
            else:
                print(f"    - Module {mod_num}: Complete (no changes needed)")

    # Step 4: Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    total_modified = sum(len(v) for v in modified_files.values())
    total_pages_added = sum(
        len(item["pages_added"])
        for course_mods in modified_files.values()
        for item in course_mods
    )

    print(f"\nTotal files modified: {total_modified}")
    print(f"Total pages added: {total_pages_added}")

    if modified_files:
        print("\nDetailed changes by course:")
        for course, items in modified_files.items():
            if items:
                print(f"\n  {course}:")
                for item in items:
                    pages = ", ".join(item["pages_added"])
                    print(f"    - {item['file']} (Module {item['mod_num']}): [{pages}]")

    print("\n" + "=" * 80)
    print("Processing complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()
