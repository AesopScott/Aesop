#!/usr/bin/env python3
"""
Comprehensive audit script for Aesop Academy course modules.
Checks all HTML module files for structural integrity and required elements.
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict
from html.parser import HTMLParser

class ModuleAuditResult:
    def __init__(self, course, module, filepath):
        self.course = course
        self.module = module
        self.filepath = filepath
        self.critical_issues = []
        self.warning_issues = []
        self.metadata = {}

    def add_critical(self, issue):
        self.critical_issues.append(issue)

    def add_warning(self, issue):
        self.warning_issues.append(issue)

    def has_issues(self):
        return bool(self.critical_issues or self.warning_issues)


class HTMLContentExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.page_ids = set()
        self.tab_refs = set()
        self.functions_found = set()
        self.variables_found = {}
        self.in_script = False
        self.script_content = ""
        self.chat_elements = set()
        self.button_onclick_refs = set()
        self.in_style = False

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)

        if tag == 'script':
            self.in_script = True
            self.script_content = ""
        elif tag == 'style':
            self.in_style = True
        elif tag == 'div':
            page_id = attrs_dict.get('id', '')
            if page_id.startswith('p-'):
                self.page_ids.add(page_id)
            if 'class' in attrs_dict and 'tab-strip' in attrs_dict.get('class', ''):
                pass  # Tab strip div found
        elif tag == 'div':
            page_id = attrs_dict.get('id', '')
            if page_id:
                self.page_ids.add(page_id)
            # Check for chat elements
            if 'id' in attrs_dict:
                elem_id = attrs_dict['id']
                if elem_id.startswith('chat-') or elem_id.startswith('msgs-') or elem_id.startswith('inp-'):
                    self.chat_elements.add(elem_id)
        elif tag == 'button' or tag == 'input' or tag == 'a':
            onclick = attrs_dict.get('onclick', '')
            if onclick:
                self.button_onclick_refs.add(onclick)

    def handle_endtag(self, tag):
        if tag == 'script':
            self.in_script = False
        elif tag == 'style':
            self.in_style = False

    def handle_data(self, data):
        if self.in_script:
            self.script_content += data
        elif self.in_style:
            pass


def extract_module_info(filepath):
    """Extract module info from filename."""
    filename = os.path.basename(filepath)
    match = re.match(r'(.+)-m(\d+)\.html', filename)
    if match:
        return match.group(1), int(match.group(2))
    return None, None


def audit_module(filepath, course_name):
    """Audit a single module HTML file."""
    module_name, module_num = extract_module_info(filepath)

    result = ModuleAuditResult(course_name, module_name, filepath)

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        result.add_critical(f"Cannot read file: {e}")
        return result

    # Extract HTML structure
    extractor = HTMLContentExtractor()
    try:
        extractor.handle_data = lambda data: (
            extractor.__dict__['script_content'].__add__(data)
            if extractor.in_script else None
        )
        # Better approach: just parse and extract manually
        content_lower = content.lower()
    except:
        pass

    # Manual regex-based extraction for reliability
    script_match = re.search(r'<script[^>]*>(.*?)</script>', content, re.DOTALL | re.IGNORECASE)
    script_content = script_match.group(1) if script_match else ""

    # Check for script block
    if not script_match:
        result.add_critical("Missing <script> block")
    else:
        result.metadata['has_script'] = True

    # Extract page divs
    page_divs = set(re.findall(r'<div[^>]*id=["\']?(p-[a-z0-9]+)["\']?', content))
    result.metadata['page_divs'] = page_divs

    # Extract tab references
    tab_pattern = r'goPage\(["\']?(p-[a-z0-9]+)["\']?\)'
    tab_refs = set(re.findall(tab_pattern, script_content))
    result.metadata['tab_refs'] = tab_refs

    # Extract function definitions
    functions = set()
    for func in ['goPage', 'answer', 'mtAnswer', 'chatSend', 'chatAppend']:
        if re.search(rf'function\s+{func}\s*\(|{func}\s*=\s*function|\bfunction\*?\s+{func}\s*\(', script_content):
            functions.add(func)
        elif re.search(rf'const\s+{func}\s*=|let\s+{func}\s*=|var\s+{func}\s*=', script_content):
            functions.add(func)
    result.metadata['functions'] = functions

    # Extract variables
    variables = {}
    for var in ['COURSE_ID', 'MODULE_ID', 'PROXY_URL', 'currentPageId', 'PAGE_TO_LESSON', 'LAB_SYSTEM_PROMPTS']:
        var_match = re.search(rf'(?:const|let|var)\s+{var}\s*=\s*["\']?([^"\';]+)["\']?', script_content)
        if var_match:
            variables[var] = var_match.group(1).strip()
    result.metadata['variables'] = variables

    # Extract chat elements
    chat_ids = set(re.findall(r'id=["\']?((?:chat|msgs|inp)-[a-z0-9]+)["\']?', content))
    result.metadata['chat_elements'] = chat_ids

    # Check critical issues

    # 1. Check for expected page divs (l1-l4, q1-q4, lab1-lab4, mt)
    expected_pages = {
        'p-l1', 'p-l2', 'p-l3', 'p-l4',
        'p-q1', 'p-q2', 'p-q3', 'p-q4',
        'p-lab1', 'p-lab2', 'p-lab3', 'p-lab4',
        'p-mt'
    }

    missing_pages = expected_pages - page_divs
    if missing_pages:
        result.add_critical(f"Missing page divs: {sorted(missing_pages)}")

    # 2. Check for tab references to non-existent pages
    invalid_tab_refs = tab_refs - page_divs
    if invalid_tab_refs:
        result.add_critical(f"Tab references non-existent pages: {sorted(invalid_tab_refs)}")

    # 3. Check for pages without tab references
    orphaned_pages = (page_divs & expected_pages) - tab_refs
    if orphaned_pages:
        result.add_critical(f"Pages exist but no tabs reference them: {sorted(orphaned_pages)}")

    # 4. Check for truncation (missing L4, Lab4, Q4, or MT)
    truncation_indicators = []
    if 'p-l4' not in page_divs:
        truncation_indicators.append("Lesson 4")
    if 'p-lab4' not in page_divs:
        truncation_indicators.append("Lab 4")
    if 'p-q4' not in page_divs:
        truncation_indicators.append("Quiz 4")
    if 'p-mt' not in page_divs:
        truncation_indicators.append("Module Test")
    if truncation_indicators:
        result.add_critical(f"Module appears truncated - missing: {', '.join(truncation_indicators)}")

    # 5. Check critical variables
    if 'COURSE_ID' not in variables:
        result.add_critical("Missing COURSE_ID variable")
    else:
        # Verify COURSE_ID matches folder name
        expected_course_id = course_name
        actual_course_id = variables['COURSE_ID']
        if actual_course_id != expected_course_id and actual_course_id.replace('-', '_') != expected_course_id.replace('-', '_'):
            result.add_critical(f"COURSE_ID mismatch: '{actual_course_id}' vs folder '{expected_course_id}'")

    if 'MODULE_ID' not in variables:
        result.add_critical("Missing MODULE_ID variable")

    if 'PROXY_URL' not in variables:
        result.add_critical("Missing PROXY_URL variable")

    # 6. Check critical functions
    if 'chatSend' not in functions:
        result.add_critical("Missing chatSend function")

    if 'goPage' not in functions:
        result.add_critical("Missing goPage function")

    # 7. Check LAB_SYSTEM_PROMPTS
    if 'LAB_SYSTEM_PROMPTS' not in variables:
        result.add_critical("Missing LAB_SYSTEM_PROMPTS variable")
    else:
        lab_prompts = variables.get('LAB_SYSTEM_PROMPTS', '')
        if not lab_prompts or lab_prompts == '{}':
            result.add_warning("LAB_SYSTEM_PROMPTS is empty")

    # 8. Check for chat elements
    required_chat_elements = set()
    for lesson in ['1', '2', '3', '4']:
        required_chat_elements.add(f'chat-l{lesson}')
        required_chat_elements.add(f'msgs-l{lesson}')
        required_chat_elements.add(f'inp-l{lesson}')

    missing_chat_elements = required_chat_elements - chat_ids
    if missing_chat_elements:
        result.add_critical(f"Missing chat elements: {sorted(missing_chat_elements)}")

    # Warning issues

    # 1. Check for quiz/answer functions
    answer_calls = set(re.findall(r'\banswer\s*\(\s*["\']?(\d+)["\']?', script_content))
    if not answer_calls:
        result.add_warning("No answer() function calls found in script")

    # 2. Check for module test answers
    mt_answer_calls = set(re.findall(r'\bmtAnswer\s*\(\s*["\']?(\d+)["\']?', script_content))
    if not mt_answer_calls:
        result.add_warning("No mtAnswer() function calls found in script")

    # 3. Check for page-nav sections
    if 'page-nav' not in content.lower():
        result.add_warning("No page-nav sections found")

    # 4. Check for module test threshold
    if 'threshold' not in script_content.lower() and 'passingScore' not in script_content.lower():
        result.add_warning("No module test threshold/passingScore found")

    return result


def main():
    base_path = '/sessions/nifty-brave-edison/mnt/Aesop/ai-academy/modules'

    # List of course folders to audit
    courses = [
        'building-ai-agents-i-use-cases',
        'building-ai-agents-ii-skills',
        'building-ai-agents-iii-tools',
        'building-ai-agents-iv-openclaw',
        'building-ai-agents-v-optimization',
        'ai-governance',
        'ai-in-society',
        'ai-ethics',
        'building-with-ai',
        'ai-in-healthcare',
        'ai-and-education',
        'ai-leadership',
        'ai-and-finance',
        'gpt_vs_claude_vs_gemini',
        'ai_in_game_design_i'
    ]

    all_results = {}
    total_modules = 0
    modules_with_issues = 0

    print("=" * 80)
    print("AESOP ACADEMY MODULE AUDIT REPORT")
    print("=" * 80)
    print()

    for course in courses:
        course_path = os.path.join(base_path, course)

        if not os.path.isdir(course_path):
            print(f"SKIPPED: Course directory not found: {course}")
            continue

        # Find all module HTML files
        module_files = sorted([
            f for f in os.listdir(course_path)
            if f.endswith('.html') and re.match(r'.+-m\d+\.html', f)
        ])

        if not module_files:
            print(f"SKIPPED: {course} (no module files found)")
            continue

        course_results = {}
        course_has_issues = False

        for module_file in module_files:
            filepath = os.path.join(course_path, module_file)
            result = audit_module(filepath, course)
            total_modules += 1

            course_results[module_file] = result

            if result.has_issues():
                modules_with_issues += 1
                course_has_issues = True

        all_results[course] = course_results

        if course_has_issues or True:  # Print all courses
            print(f"\nCOURSE: {course}")
            print("-" * 80)

            for module_file, result in course_results.items():
                if result.critical_issues or result.warning_issues:
                    print(f"\n  MODULE: {module_file}")

                    if result.critical_issues:
                        print(f"  [CRITICAL] ({len(result.critical_issues)} issues)")
                        for issue in result.critical_issues:
                            print(f"    - {issue}")

                    if result.warning_issues:
                        print(f"  [WARNING] ({len(result.warning_issues)} issues)")
                        for issue in result.warning_issues:
                            print(f"    - {issue}")

                    # Show metadata
                    if result.metadata.get('page_divs'):
                        pages = sorted(result.metadata['page_divs'])
                        print(f"  Page divs found: {', '.join(pages)}")

                    if result.metadata.get('variables'):
                        print(f"  Variables found: {', '.join(sorted(result.metadata['variables'].keys()))}")

                    if result.metadata.get('functions'):
                        print(f"  Functions found: {', '.join(sorted(result.metadata['functions']))}")
                else:
                    print(f"  MODULE: {module_file} - OK")

    # Summary
    print("\n" + "=" * 80)
    print("AUDIT SUMMARY")
    print("=" * 80)
    print(f"Total modules audited: {total_modules}")
    print(f"Modules with issues: {modules_with_issues}")
    print(f"Modules without issues: {total_modules - modules_with_issues}")

    # Aggregate stats
    critical_count = 0
    warning_count = 0
    for course_results in all_results.values():
        for result in course_results.values():
            critical_count += len(result.critical_issues)
            warning_count += len(result.warning_issues)

    print(f"\nTotal critical issues: {critical_count}")
    print(f"Total warning issues: {warning_count}")
    print("=" * 80)


if __name__ == '__main__':
    main()
