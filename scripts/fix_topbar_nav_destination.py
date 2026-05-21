#!/usr/bin/env python3
"""
Update topbar nav buttons to show the destination module number:
  "Next →"  →  "Module 2 →"
  "← Prev"  →  "← Module 3"
"""
import re
from pathlib import Path


def get_module_num(filename):
    m = re.search(r'm(\d+)\.html', filename)
    return int(m.group(1)) if m else None


def update_nav_buttons(content, module_num, total):
    """Replace Next/Prev text with explicit module numbers."""

    prev_num = module_num - 1
    next_num = module_num + 1

    # "Next →" / "Next &#8594;" → "Module N →"
    if module_num < total:
        content = content.replace(
            '>Next &#8594;</a>',
            f'>Module {next_num} &#8594;</a>'
        )

    # "← Prev" / "&#8592; Prev" → "← Module N"
    if module_num > 1:
        # In an <a> tag
        content = content.replace(
            '>&#8592; Prev</a>',
            f'>&#8592; Module {prev_num}</a>'
        )
        # In a <span> tag (disabled)
        content = content.replace(
            '>&#8592; Prev</span>',
            f'>&#8592; Module {prev_num}</span>'
        )

    return content


def process(filepath, module_num, total):
    txt = filepath.read_text(encoding='utf-8')

    # Skip if already done
    if f'>Module {module_num + 1} &#8594;</a>' in txt or (module_num == total and f'>&#8592; Module {module_num - 1}<' in txt):
        return False

    new_txt = update_nav_buttons(txt, module_num, total)
    if new_txt != txt:
        filepath.write_text(new_txt, encoding='utf-8')
        return True
    return False


def main():
    base = Path(r'C:\Users\scott\Code\aesop\ai-academy\modules\v2')
    updated = 0

    for course_dir in sorted(base.glob('*')):
        if not course_dir.is_dir():
            continue
        modules = sorted(course_dir.glob('m[0-9]*.html'))
        total = len(modules)
        for module_file in modules:
            n = get_module_num(module_file.name)
            if n is None:
                continue
            if process(module_file, n, total):
                print(f'[ok] {course_dir.name}/{module_file.name}')
                updated += 1

    print(f'\n{updated} files updated.')


if __name__ == '__main__':
    main()
