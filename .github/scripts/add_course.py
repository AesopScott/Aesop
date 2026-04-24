#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
add_course.py — Zero-prompt course registration scanner.

Scans ai-academy/modules/ for course directories that have written module
HTML files but are not yet fully registered in every required location.
For each gap found, extracts metadata directly from the HTML files and
fills all registration locations automatically.

Locations updated:
  1. courses-data.json        module metadata + live flag
  2. courses.html             panel + mega-menu entry (marked Live)
  3. dashboard.html           K-12 teacher dashboard COURSES array
  4. i18n/courses.*.json      all 13 language files (English placeholder)
  5. course-registry.json     rebuilt by build_registry.py
  6. stats.json               rebuilt by build_stats.py

Usage:
    python .github/scripts/add_course.py           # dry-run (no changes)
    python .github/scripts/add_course.py --apply   # apply all changes
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

# Force UTF-8 stdout so Unicode characters (checkmarks, em-dashes, etc.)
# don't crash on Windows terminals that default to cp1252.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ── Paths ──────────────────────────────────────────────────────────────────────
REPO         = Path(__file__).resolve().parents[2]
SCRIPTS      = REPO / ".github" / "scripts"
MODULES_DIR  = REPO / "ai-academy" / "modules"
COURSES_HTML = REPO / "ai-academy" / "courses.html"
COURSES_DATA = MODULES_DIR / "courses-data.json"
REGISTRY     = MODULES_DIR / "course-registry.json"
DASHBOARD    = REPO / "ai-academy" / "dashboard.html"
I18N_DIR     = REPO / "i18n"
STATS_JSON   = REPO / "stats.json"

I18N_FILES = [
    "courses.ar.json", "courses.de.json", "courses.en.json",
    "courses.es.json", "courses.fa.json", "courses.fr.json",
    "courses.hi.json", "courses.ja.json", "courses.ko.json",
    "courses.ru.json", "courses.sw.json", "courses.ur.json",
    "courses.zh.json",
]

# Icon pool — cycled for new courses
ICONS = ["🧩", "🌐", "💡", "🔬", "📊", "🚀", "🎯", "⚙️", "🔭", "🖥️",
         "🤝", "🎨", "💼", "📡", "🛡️", "🧠", "⚡", "🔮"]

BAR_COLORS = ["teal", "purple", "green", "amber", "navy", "red", "blue", "gold"]

# Maps keywords in course IDs → category label and mega-menu section
CATEGORY_MAP = {
    "governance":   ("Society",      "📚 Core Courses"),
    "society":      ("Society",      "📚 Core Courses"),
    "ethics":       ("Ethics",       "📚 Core Courses"),
    "bias":         ("Ethics",       "📚 Core Courses"),
    "fairness":     ("Ethics",       "📚 Core Courses"),
    "creativity":   ("Art & Design", "🎨 Art"),
    "graphic":      ("Art & Design", "🎨 Art"),
    "design":       ("Art & Design", "🎨 Art"),
    "art":          ("Art & Design", "🎨 Art"),
    "game":         ("Art & Design", "🎨 Art"),
    "music":        ("Art & Design", "🎨 Art"),
    "photo":        ("Art & Design", "🎨 Art"),
    "video":        ("Art & Design", "🎨 Art"),
    "business":     ("Business",     "💼 Business"),
    "venture":      ("Business",     "💼 Business"),
    "pitch":        ("Business",     "💼 Business"),
    "funding":      ("Business",     "💼 Business"),
    "marketing":    ("Business",     "💼 Business"),
    "finance":      ("Business",     "💼 Business"),
    "leadership":   ("Business",     "💼 Business"),
    "founder":      ("Business",     "💼 Business"),
    "procurement":  ("Business",     "💼 Business"),
    "model":        ("AI Models",    "📡 AI Models"),
    "llm":          ("AI Models",    "📡 AI Models"),
    "alignment":    ("AI Models",    "📡 AI Models"),
    "multimodal":   ("AI Progress",  "🔭 AI Progress"),
    "context":      ("AI Progress",  "🔭 AI Progress"),
    "hardware":     ("AI Progress",  "🔭 AI Progress"),
    "reasoning":    ("AI Progress",  "🔭 AI Progress"),
    "synthetic":    ("AI Progress",  "🔭 AI Progress"),
    "agent":        ("Development",  "⚙️ Development"),
    "build":        ("Development",  "⚙️ Development"),
    "security":     ("Development",  "⚙️ Development"),
    "deploy":       ("Development",  "⚙️ Development"),
    "evaluation":   ("Development",  "⚙️ Development"),
    "testing":      ("Development",  "⚙️ Development"),
    "prompt":       ("Development",  "⚙️ Development"),
    "rag":          ("Development",  "⚙️ Development"),
    "api":          ("Development",  "⚙️ Development"),
    "fine":         ("Development",  "⚙️ Development"),
    "code":         ("Development",  "⚙️ Development"),
    "job":          ("Society",      "📚 Core Courses"),
    "work":         ("Society",      "📚 Core Courses"),
    "automation":   ("Society",      "📚 Core Courses"),
    "media":        ("Society",      "📚 Core Courses"),
    "misinformation": ("Society",    "📚 Core Courses"),
    "healthcare":   ("Society",      "📚 Core Courses"),
    "education":    ("Society",      "📚 Core Courses"),
    "climate":      ("Society",      "📚 Core Courses"),
    "psychology":   ("Society",      "📚 Core Courses"),
    "consciousness": ("Society",     "📚 Core Courses"),
    "national":     ("Society",      "📚 Core Courses"),
    "career":       ("Society",      "📚 Core Courses"),
}


# ── HTML extraction ────────────────────────────────────────────────────────────

def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""


def extract_course_name(course_id: str, m1_html: str) -> str:
    """Extract course name from lesson-kicker in m1.html, or title-case the folder name."""
    match = re.search(r'class="lesson-kicker">([^·<]+)', m1_html)
    if match:
        return match.group(1).strip()
    # Fallback: title-case folder name, stripping "ai-" prefix only if the
    # result still makes sense (keep it for "AI Governance" etc.)
    name = course_id.replace("-", " ").replace("_", " ").title()
    # Capitalise "Ai" → "AI"
    name = re.sub(r'\bAi\b', 'AI', name)
    return name


def extract_description(m1_html: str) -> str:
    """Pull the tagline from the intro page of m1.html."""
    # Intro page tagline is inside the first .lesson-hero block
    intro_match = re.search(
        r'id="p-intro".*?<div class="tagline">(.*?)</div>',
        m1_html, re.DOTALL
    )
    if intro_match:
        desc = re.sub(r'<[^>]+>', '', intro_match.group(1)).strip()
        if desc:
            return desc
    # Fallback: first tagline in the file
    match = re.search(r'class="tagline">(.*?)</div>', m1_html, re.DOTALL)
    if match:
        return re.sub(r'<[^>]+>', '', match.group(1)).strip()
    return ""


def extract_modules(course_id: str, module_files: list[Path]) -> list[dict]:
    """Extract module title + subtitle from each module HTML file."""
    modules = []
    for i, mf in enumerate(module_files, 1):
        html = read_text(mf)
        # First lesson's <h1> is the module title
        lesson_h1 = re.search(
            r'class="lesson-kicker">[^<]*·\s*Lesson\s*1.*?<h1>(.*?)</h1>',
            html, re.DOTALL
        )
        title = ""
        if lesson_h1:
            title = re.sub(r'<[^>]+>', '', lesson_h1.group(1)).strip()

        # Tagline on lesson 1 is the subtitle
        lesson_section = re.search(
            r'class="lesson-kicker">[^<]*·\s*Lesson\s*1.*?class="tagline">(.*?)</div>',
            html, re.DOTALL
        )
        sub = ""
        if lesson_section:
            sub = re.sub(r'<[^>]+>', '', lesson_section.group(1)).strip()

        if not title:
            title = f"Module {i}"

        entry = {"n": i, "title": title}
        if sub:
            entry["sub"] = sub
        modules.append(entry)
    return modules


def infer_category(course_id: str) -> tuple[str, str]:
    """Return (sub_label_word, mega_menu_section) based on course ID keywords."""
    lower = course_id.lower()
    for kw, (sub, section) in CATEGORY_MAP.items():
        if kw in lower:
            return sub, section
    return "Elective", "📚 Core Courses"


# ── Find unregistered courses ──────────────────────────────────────────────────

def load_json(path: Path) -> dict | list:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def find_unregistered() -> list[dict]:
    """
    Return a list of course dicts for every module directory that has at least
    one written HTML file and is missing from any registration location.

    No prerequisite steps required — if a course isn't in courses-data.json
    yet, metadata is extracted from the HTML files and it's added automatically.
    """
    registry       = load_json(REGISTRY) if REGISTRY.exists() else {}
    cdata          = load_json(COURSES_DATA) if COURSES_DATA.exists() else {"courses": []}
    courses_html   = read_text(COURSES_HTML)
    dashboard_html = read_text(DASHBOARD)

    registered_ids   = set(registry.keys())
    courses_data_ids = {c["id"] for c in cdata.get("courses", [])}
    dashboard_ids    = set(re.findall(r"id:'([^']+)'", dashboard_html))

    en_json = I18N_DIR / "courses.en.json"
    en_data = load_json(en_json) if en_json.exists() else {}

    results = []
    icon_offset = len([v for v in registry.values()
                       if isinstance(v, dict) and v.get("status") == "live"])

    for d in sorted(MODULES_DIR.iterdir()):
        if not d.is_dir() or d.name.startswith("."):
            continue

        module_files = sorted(d.glob(f"{d.name}-m*.html"))
        if not module_files:
            continue

        course_id = d.name

        # Check which locations are missing this course.
        # For courses.html we look for the LIVE Enter Course link rather than
        # any substring occurrence of the course ID — AIP draft placeholders
        # (e.g. "aip-whats-really-inside-ai" in the mega-menu) contain the
        # course ID as a substring and would cause a false negative.
        missing_courses_data = course_id not in courses_data_ids
        missing_registry     = course_id not in registered_ids
        missing_html         = f"electives-hub.html?course={course_id}" not in courses_html
        missing_dashboard    = course_id not in dashboard_ids

        # Extract data from HTML (name needed for i18n check)
        m1_html      = read_text(module_files[0])
        name         = extract_course_name(course_id, m1_html)
        missing_i18n = name not in en_data

        # Skip if fully registered in every location
        if not any([missing_courses_data, missing_registry,
                    missing_html, missing_dashboard, missing_i18n]):
            continue

        desc                   = extract_description(m1_html)
        modules                = extract_modules(course_id, module_files)
        sub_word, mega_section = infer_category(course_id)

        icon_offset += 1
        icon      = ICONS[icon_offset % len(ICONS)]
        bar_color = BAR_COLORS[icon_offset % len(BAR_COLORS)]

        results.append({
            "id":           course_id,
            "name":         name,
            "desc":         desc,
            "modules":      modules,
            "n_mods":       len(module_files),
            "icon":         icon,
            "bar":          bar_color,
            "sub_word":     sub_word,
            "mega_section": mega_section,
            "url":          f"/ai-academy/modules/electives-hub.html?course={course_id}",
            "missing": {
                "courses_data": missing_courses_data,
                "registry":     missing_registry,
                "html":         missing_html,
                "dashboard":    missing_dashboard,
                "i18n":         missing_i18n,
            }
        })

    return results


# ── Registration steps ─────────────────────────────────────────────────────────

def register_courses_data(course: dict, cdata: dict) -> None:
    """Add or update this course in courses-data.json."""
    existing = next((c for c in cdata.get("courses", []) if c["id"] == course["id"]), None)
    if existing:
        existing["live"] = True
        return
    cdata.setdefault("courses", []).append({
        "id":          course["id"],
        "name":        course["name"],
        "icon":        course["icon"],
        "description": course["desc"],
        "live":        True,
        "modules":     course["modules"],
    })


def next_dv_id(html: str) -> int:
    nums = [int(m) for m in re.findall(r'id="dv-(\d+)"', html)]
    return max(nums, default=0) + 1


def build_live_panel(dv: int, course: dict) -> str:
    n_mods = course["n_mods"]
    name   = course["name"]
    desc   = course["desc"]
    icon   = course["icon"]
    url    = course["url"]

    mod_rows = ""
    for m in course["modules"]:
        sub_html = f'<div class="core-mod__sub">{m["sub"]}</div>' if m.get("sub") else ""
        mod_rows += (
            f'          <div class="core-mod">'
            f'<div class="core-mod__num">M{m["n"]}</div>'
            f'<div class="core-mod__info">'
            f'<div class="core-mod__title">{m["title"]}</div>'
            f'{sub_html}</div></div>\n'
        )

    return f"""
      <div class="core-panel" id="dv-{dv}">
        <div class="core-panel__header">
          <span class="core-panel__icon">{icon}</span>
          <div class="core-panel__meta">
            <div class="core-panel__title">{name}</div>
            <div class="core-panel__desc">{desc}</div>
          </div>
          <div class="core-panel__badges">
            <span class="core-badge-live">Live</span>
            <span class="core-badge-mods">{n_mods} Modules</span>
          </div>
        </div>
        <div class="core-modules-label">Course modules</div>
        <div class="core-modules-grid">
{mod_rows.rstrip()}
        </div>
        <a class="core-panel__cta" href="{url}">Enter Course →</a>
      </div>
"""


def register_courses_html(course: dict, html: str) -> str:
    """Add panel + mega-menu button. Returns updated HTML."""
    # Guard on the LIVE Enter Course link rather than any substring of the
    # course ID. AIP draft placeholder buttons (e.g. "aip-whats-really-inside-ai")
    # contain the course ID as a substring and would cause a spurious early-return.
    if f"electives-hub.html?course={course['id']}" in html:
        return html  # live panel already present

    dv = next_dv_id(html)

    # Insert panel before closing tag of the dv section
    last_dv_match = list(re.finditer(r'id="dv-\d+"', html))
    if last_dv_match:
        last_dv_pos = last_dv_match[-1].start()
        close_pos   = html.find("    </div>", last_dv_pos)
        if close_pos != -1:
            panel = build_live_panel(dv, course)
            html  = html[:close_pos] + panel + html[close_pos:]

    # Add mega-menu button in the right section, alphabetically
    section_label = course["mega_section"]
    cat_pos = html.find(f'<div class="mega-cat">{section_label}</div>')
    if cat_pos != -1:
        next_cat = html.find('<div class="mega-cat">', cat_pos + len(section_label))
        section_end = next_cat if next_cat != -1 else html.find('</div>', cat_pos + 30)
        section = html[cat_pos:section_end]

        btn_pat = re.compile(r'        <button class="mega-link[^"]*"[^>]*>([^<]+)</button>')
        buttons = list(btn_pat.finditer(section))

        new_btn = (
            f'        <button class="mega-link mega-link--live" '
            f'data-panel="dv-{dv}" onclick="megaSelect(this,\'dv-{dv}\')">'
            f'{course["name"]}</button>'
        )

        insert_offset = None
        for btn in buttons:
            if btn.group(1).lower() > course["name"].lower():
                insert_offset = btn.start()
                break
        if insert_offset is None:
            insert_offset = len(section) if not buttons else buttons[-1].end() + 1

        abs_insert = cat_pos + insert_offset
        html = html[:abs_insert] + new_btn + "\n" + html[abs_insert:]

    return html


def register_dashboard(course: dict, html: str) -> str:
    """Add course to dashboard.html COURSES array. Returns updated HTML."""
    if course["id"] in html:
        return html

    courses_match = re.search(r"(const COURSES\s*=\s*\[)(.*?)(\s*\];)", html, re.DOTALL)
    if not courses_match:
        return html

    new_entry = (
        f"      {{ id:'{course['id']}', title:'{course['name']}', "
        f"sub:'{course['name']}', icon:'{course['icon']}', "
        f"bar:'{course['bar']}', modules:{course['n_mods']}, "
        f"url:'{course['url']}' }},"
    )
    insert_pos = courses_match.start(3)
    return html[:insert_pos] + "\n" + new_entry + html[insert_pos:]


def register_i18n(course: dict) -> None:
    """Add course name + description to all 13 i18n files."""
    keys = {course["name"]: course["name"]}
    if course["desc"]:
        keys[course["desc"]] = course["desc"]

    for filename in I18N_FILES:
        path = I18N_DIR / filename
        if not path.exists():
            continue
        data = load_json(path)
        changed = False
        for key, val in keys.items():
            if key not in data:
                data[key] = val
                changed = True
        if changed:
            save_json(path, data)


def run_script(name: str) -> bool:
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / name)],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"  ✗ {name} failed:")
        print((result.stdout + result.stderr)[-400:])
        return False
    return True


# ── Main ───────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true",
                        help="Apply changes (default: dry-run)")
    args = parser.parse_args()

    courses = find_unregistered()

    if not courses:
        print("✓ All module directories are fully registered. Nothing to do.")
        return

    print(f"Found {len(courses)} course(s) with registration gaps:\n")
    for c in courses:
        missing = [k for k, v in c["missing"].items() if v]
        print(f"  {c['id']}")
        print(f"    Name:    {c['name']}")
        print(f"    Modules: {c['n_mods']}")
        print(f"    Missing: {', '.join(missing)}")
        if not args.apply:
            print(f"    Desc:    {c['desc'][:80]}…" if len(c['desc']) > 80 else f"    Desc:    {c['desc']}")
        print()

    if not args.apply:
        print("Dry-run complete. Run with --apply to register these courses.")
        return

    # Load mutable state once
    cdata     = load_json(COURSES_DATA)
    html      = read_text(COURSES_HTML)
    dash_html = read_text(DASHBOARD)

    for c in courses:
        print(f"Registering {c['id']}…")

        if c["missing"]["courses_data"]:
            register_courses_data(c, cdata)
            print(f"  ✓ courses-data.json")

        if c["missing"]["html"]:
            html = register_courses_html(c, html)
            print(f"  ✓ courses.html (panel + mega-menu)")

        if c["missing"]["dashboard"]:
            dash_html = register_dashboard(c, dash_html)
            print(f"  ✓ dashboard.html")

        if c["missing"]["i18n"]:
            register_i18n(c)
            print(f"  ✓ i18n files (13 languages)")

    # Write updated files
    save_json(COURSES_DATA, cdata)
    COURSES_HTML.write_text(html, encoding="utf-8")
    DASHBOARD.write_text(dash_html, encoding="utf-8")

    # Rebuild derived files
    if run_script("build_registry.py"):
        print("  ✓ course-registry.json rebuilt")
    if run_script("build_stats.py"):
        print("  ✓ stats.json rebuilt")

    # Write registration report for the notification script
    report_path = REPO / "aip" / "registration-report.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    save_json(report_path, {
        "registered": [
            {
                "id":      c["id"],
                "name":    c["name"],
                "n_mods":  c["n_mods"],
                "url":     c["url"],
                "desc":    c["desc"],
            }
            for c in courses
        ]
    })
    print(f"\n✓ Done. {len(courses)} course(s) registered.")
    print(f"  Report written to aip/registration-report.json")


if __name__ == "__main__":
    main()
