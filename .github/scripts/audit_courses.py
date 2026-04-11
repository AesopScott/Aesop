#!/usr/bin/env python3
"""
AESOP Course Audit Engine

Checks for:
  1. Internal link integrity (courses.html → modules, electives-hub refs, registry)
  2. File existence (module directories and HTML files vs what's referenced)
  3. Live site 404 checks (actually hits aesopacademy.org URLs)
  4. Course ID consistency across courses.html, electives-hub, and registry

Outputs a markdown report to aip/audit-report.md
"""

import json
import os
import re
import sys
import time
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

REPO_ROOT = Path(".")
COURSES_HTML = REPO_ROOT / "ai-academy" / "courses.html"
ELECTIVES_HUB = REPO_ROOT / "ai-academy" / "modules" / "electives-hub.html"
COURSE_REGISTRY = REPO_ROOT / "ai-academy" / "modules" / "course-registry.json"
MODULES_DIR = REPO_ROOT / "ai-academy" / "modules"
REPORT_PATH = REPO_ROOT / "aip" / "audit-report.md"
SITE_BASE = "https://aesopacademy.org"

# ── Helpers ──────────────────────────────────────────────────────────────────

def read_file(path):
    """Read file contents or return None."""
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return None


def http_check(url, timeout=10):
    """Check if a URL returns 200. Returns (status_code, error_msg)."""
    try:
        req = Request(url, headers={"User-Agent": "AESOP-Audit/1.0"})
        resp = urlopen(req, timeout=timeout)
        return resp.getcode(), None
    except HTTPError as e:
        return e.code, str(e)
    except URLError as e:
        return None, str(e)
    except Exception as e:
        return None, str(e)


# ── Audit Checks ─────────────────────────────────────────────────────────────

def audit_courses_html_links(html):
    """Extract all internal links from courses.html and check file existence."""
    issues = []
    info = []

    # Find all href links
    links = re.findall(r'href="(/ai-academy/[^"]*)"', html)

    # Deduplicate
    unique_links = sorted(set(links))
    info.append(f"Found {len(unique_links)} unique internal links in courses.html")

    for link in unique_links:
        # Strip query params for file check
        file_path = link.split("?")[0]
        full_path = REPO_ROOT / file_path.lstrip("/")

        if not full_path.exists():
            issues.append({
                "type": "MISSING_FILE",
                "severity": "error",
                "link": link,
                "expected_path": str(full_path),
                "msg": f"courses.html links to `{link}` but file does not exist"
            })
        else:
            info.append(f"  ✓ {link}")

    # Find electives-hub course params
    hub_links = re.findall(r'electives-hub\.html\?course=([a-z_]+)', html)
    unique_courses = sorted(set(hub_links))
    info.append(f"\nFound {len(unique_courses)} course links to electives-hub: {', '.join(unique_courses)}")

    return issues, info


def audit_electives_hub(html):
    """Check BASE_COURSES definitions and file patterns in electives-hub."""
    issues = []
    info = []

    # Extract BASE_COURSES entries
    # The format is: {id:'governance',title:'...',url:'/ai-academy/modules/ai-governance/',...}
    # These are dense single-line objects — match id and url fields within each
    courses = {}

    # Find all course object blocks that have both id and url
    # Match patterns like: {id:'governance',...,url:'/ai-academy/modules/ai-governance/',...}
    for match in re.finditer(r"\{id:'([^']+)'[^}]*url:'([^']+)'", html):
        courses[match.group(1)] = match.group(2)
    # Also handle double-quoted variants
    for match in re.finditer(r'\{id:"([^"]+)"[^}]*url:"([^"]+)"', html):
        if match.group(1) not in courses:
            courses[match.group(1)] = match.group(2)

    info.append(f"Found {len(courses)} BASE_COURSES in electives-hub")

    # Extract filePatterns
    pattern_matches = re.findall(
        r"['\"]([^'\"]+)['\"]\s*:\s*\(?n\)?\s*=>\s*`([^`]+)`",
        html
    )
    file_patterns = {}
    for cid, pattern in pattern_matches:
        # Convert template literal to a format string
        file_patterns[cid] = pattern.replace("${n}", "{n}")

    info.append(f"Found {len(file_patterns)} filePatterns: {', '.join(file_patterns.keys())}")

    # Extract module counts per course
    # Look for modules arrays in BASE_COURSES
    module_counts = {}
    for cid in courses:
        # Count module entries for this course - look for module IDs
        pattern = re.compile(rf"id\s*:\s*['\"][a-z]+-m(\d+)['\"]")
        # This is approximate — we'll verify against actual files instead

    # Check each BASE_COURSE has matching directory and files
    for cid, curl in courses.items():
        dir_path = REPO_ROOT / curl.lstrip("/")
        if not dir_path.exists():
            issues.append({
                "type": "MISSING_DIR",
                "severity": "error",
                "course_id": cid,
                "expected_dir": str(dir_path),
                "msg": f"BASE_COURSE `{cid}` references directory `{curl}` which does not exist"
            })
        else:
            # Check module files exist using file pattern
            if cid in file_patterns:
                pattern = file_patterns[cid]
                found_modules = 0
                missing_modules = []
                for n in range(1, 13):  # Check up to 12 modules
                    filename = pattern.replace("{n}", str(n))
                    # Also check with version suffix
                    matches = list(dir_path.glob(filename.replace(".html", "*.html")))
                    if matches:
                        found_modules += 1
                    elif n <= 8:  # Only flag missing for reasonable module counts
                        # Check if we've gone past the last module
                        if found_modules > 0 and n > found_modules:
                            break
                        missing_modules.append(filename)

                if found_modules > 0:
                    info.append(f"  ✓ {cid}: {found_modules} module files found in {curl}")
                    # Flag specific missing ones only if there's a gap
                    for m in missing_modules[:found_modules]:
                        issues.append({
                            "type": "MISSING_MODULE",
                            "severity": "warning",
                            "course_id": cid,
                            "msg": f"Module file `{m}` missing from `{curl}`"
                        })
                else:
                    issues.append({
                        "type": "NO_MODULES",
                        "severity": "error",
                        "course_id": cid,
                        "msg": f"No module files found for `{cid}` in `{curl}` (expected pattern: {pattern})"
                    })

    return issues, info, courses


def audit_course_registry():
    """Check course-registry.json entries match actual files."""
    issues = []
    info = []

    content = read_file(COURSE_REGISTRY)
    if content is None:
        issues.append({
            "type": "MISSING_FILE",
            "severity": "error",
            "msg": "course-registry.json does not exist"
        })
        return issues, info, {}

    try:
        registry = json.loads(content)
    except json.JSONDecodeError as e:
        issues.append({
            "type": "INVALID_JSON",
            "severity": "error",
            "msg": f"course-registry.json has invalid JSON: {e}"
        })
        return issues, info, {}

    info.append(f"Found {len(registry)} courses in registry: {', '.join(registry.keys())}")

    for cid, course in registry.items():
        url = course.get("url", "")
        dir_path = REPO_ROOT / url.lstrip("/")

        if not dir_path.exists():
            issues.append({
                "type": "MISSING_DIR",
                "severity": "error",
                "course_id": cid,
                "msg": f"Registry course `{cid}` references `{url}` which does not exist"
            })
            continue

        # Check module files
        modules = course.get("modules", [])
        info.append(f"  Registry `{cid}`: {len(modules)} modules defined")

        for i, mod in enumerate(modules, 1):
            # Registry courses use pattern: {course_id}-m{n}.html
            filename = f"{cid}-m{i}.html"
            file_path = dir_path / filename
            if not file_path.exists():
                issues.append({
                    "type": "MISSING_MODULE",
                    "severity": "error",
                    "course_id": cid,
                    "msg": f"Registry module file `{filename}` missing from `{url}`"
                })
            else:
                info.append(f"    ✓ {filename}")

    return issues, info, registry


def audit_cross_references(html_courses, hub_courses, registry):
    """Check course IDs are consistent across all three sources."""
    issues = []
    info = []

    # courses.html course params
    courses_html_ids = set(re.findall(r'electives-hub\.html\?course=([a-z_]+)', html_courses))

    # electives-hub BASE_COURSES
    hub_ids = set(hub_courses.keys())

    # registry IDs
    registry_ids = set(registry.keys())

    # All known course IDs
    all_ids = courses_html_ids | hub_ids | registry_ids

    info.append(f"courses.html references: {sorted(courses_html_ids)}")
    info.append(f"electives-hub BASE_COURSES: {sorted(hub_ids)}")
    info.append(f"course-registry.json: {sorted(registry_ids)}")

    for cid in sorted(all_ids):
        in_courses = cid in courses_html_ids
        in_hub = cid in hub_ids
        in_registry = cid in registry_ids

        if in_courses and not in_hub and not in_registry:
            issues.append({
                "type": "ORPHAN_LINK",
                "severity": "error",
                "course_id": cid,
                "msg": f"Course `{cid}` is linked in courses.html but not defined in electives-hub or registry"
            })
        elif in_hub and not in_courses and cid not in registry_ids:
            issues.append({
                "type": "UNREACHABLE",
                "severity": "warning",
                "course_id": cid,
                "msg": f"Course `{cid}` is in electives-hub BASE_COURSES but not linked from courses.html"
            })

    return issues, info


def audit_live_site(html_courses):
    """Hit live URLs on aesopacademy.org to check for 404s."""
    issues = []
    info = []

    # Collect URLs to check
    urls = []

    # Main pages
    urls.append(f"{SITE_BASE}/ai-academy/courses.html")
    urls.append(f"{SITE_BASE}/ai-academy/modules/electives-hub.html")
    urls.append(f"{SITE_BASE}/ai-academy/modules/course-registry.json")

    # All internal links from courses.html
    internal_links = re.findall(r'href="(/ai-academy/[^"#]*)"', html_courses)
    for link in sorted(set(internal_links)):
        file_path = link.split("?")[0]
        urls.append(f"{SITE_BASE}{file_path}")

    # Module directories for live courses
    live_course_dirs = []
    # Check registry courses
    registry_content = read_file(COURSE_REGISTRY)
    if registry_content:
        try:
            registry = json.loads(registry_content)
            for cid, course in registry.items():
                url = course.get("url", "")
                modules = course.get("modules", [])
                for i in range(1, len(modules) + 1):
                    urls.append(f"{SITE_BASE}{url}{cid}-m{i}.html")
        except json.JSONDecodeError:
            pass

    # Check base courses that have files
    base_dirs = {
        "governance": ("/ai-academy/modules/ai-governance/", "ai-governance-m{}.html", 8),
        "society": ("/ai-academy/modules/ai-society/", "ai-in-society-m{}.html", 8),
        "ethics": ("/ai-academy/modules/ai-ethics/", "ai-ethics-m{}.html", 8),
        "building": ("/ai-academy/modules/building_with_ai/", "building_with_ai-m{}.html", 8),
    }
    for cid, (base_url, pattern, count) in base_dirs.items():
        for n in range(1, count + 1):
            urls.append(f"{SITE_BASE}{base_url}{pattern.format(n)}")

    # Deduplicate
    urls = sorted(set(urls))
    info.append(f"Checking {len(urls)} live URLs...")

    checked = 0
    errors = 0
    for url in urls:
        status, err = http_check(url)
        checked += 1

        if status == 200:
            info.append(f"  ✓ {status} {url}")
        elif status == 404:
            errors += 1
            issues.append({
                "type": "LIVE_404",
                "severity": "error",
                "url": url,
                "msg": f"404 Not Found: `{url}`"
            })
        elif status is not None:
            errors += 1
            issues.append({
                "type": "LIVE_ERROR",
                "severity": "warning",
                "url": url,
                "status": status,
                "msg": f"HTTP {status}: `{url}`"
            })
        else:
            errors += 1
            issues.append({
                "type": "LIVE_UNREACHABLE",
                "severity": "warning",
                "url": url,
                "msg": f"Could not reach: `{url}` — {err}"
            })

        # Rate limit: don't hammer the server
        if checked % 10 == 0:
            time.sleep(1)

    info.append(f"\nLive check complete: {checked} URLs checked, {errors} issues found")
    return issues, info


def audit_module_file_integrity():
    """Check all module HTML files for COURSE_ID / MODULE_ID consistency."""
    issues = []
    info = []

    module_dirs = [d for d in MODULES_DIR.iterdir() if d.is_dir() and not d.name.startswith(".") and d.name not in ("archive",)]
    total_files = 0

    for d in sorted(module_dirs):
        html_files = sorted(d.glob("*.html"))
        if not html_files:
            continue

        for f in html_files:
            total_files += 1
            content = read_file(f)
            if content is None:
                continue

            # Check for COURSE_ID
            cid_match = re.search(r"const\s+COURSE_ID\s*=\s*['\"]([^'\"]+)['\"]", content)
            mid_match = re.search(r"const\s+MODULE_ID\s*=\s*['\"]([^'\"]+)['\"]", content)

            if not cid_match:
                issues.append({
                    "type": "NO_COURSE_ID",
                    "severity": "warning",
                    "file": str(f.relative_to(REPO_ROOT)),
                    "msg": f"Module file `{f.name}` has no COURSE_ID constant"
                })

    info.append(f"Scanned {total_files} module HTML files across {len(module_dirs)} directories")
    return issues, info


# ── Report Generator ─────────────────────────────────────────────────────────

def generate_report(all_issues, all_info, sections):
    """Generate a markdown audit report."""
    from datetime import datetime, timezone

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    errors = [i for i in all_issues if i.get("severity") == "error"]
    warnings = [i for i in all_issues if i.get("severity") == "warning"]

    lines = []
    lines.append(f"# AESOP Course Audit Report")
    lines.append(f"")
    lines.append(f"**Generated:** {now}")
    lines.append(f"**Status:** {'🔴 ISSUES FOUND' if errors else '🟡 WARNINGS' if warnings else '🟢 ALL CLEAR'}")
    lines.append(f"**Errors:** {len(errors)} · **Warnings:** {len(warnings)}")
    lines.append(f"")
    lines.append(f"---")

    for section_name, section_issues, section_info in sections:
        lines.append(f"")
        lines.append(f"## {section_name}")
        lines.append(f"")

        s_errors = [i for i in section_issues if i.get("severity") == "error"]
        s_warnings = [i for i in section_issues if i.get("severity") == "warning"]

        if not s_errors and not s_warnings:
            lines.append(f"✅ No issues found.")
        else:
            if s_errors:
                lines.append(f"### Errors ({len(s_errors)})")
                lines.append(f"")
                for i in s_errors:
                    lines.append(f"- 🔴 **{i['type']}**: {i['msg']}")
                lines.append(f"")

            if s_warnings:
                lines.append(f"### Warnings ({len(s_warnings)})")
                lines.append(f"")
                for i in s_warnings:
                    lines.append(f"- 🟡 **{i['type']}**: {i['msg']}")
                lines.append(f"")

    # Summary
    lines.append(f"---")
    lines.append(f"")
    lines.append(f"## Summary")
    lines.append(f"")
    if errors:
        lines.append(f"**{len(errors)} error(s) require attention:**")
        lines.append(f"")
        for i in errors:
            lines.append(f"1. {i['msg']}")
    elif warnings:
        lines.append(f"Only warnings found — no critical issues.")
    else:
        lines.append(f"All checks passed. No broken links or missing files detected.")

    return "\n".join(lines)


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("AESOP Course Audit Engine")
    print("=" * 60)

    all_issues = []
    sections = []

    # 1. courses.html link check
    print("\n[1/5] Auditing courses.html internal links...")
    html_courses = read_file(COURSES_HTML)
    if html_courses is None:
        print("  ERROR: courses.html not found!")
        sys.exit(1)
    issues1, info1 = audit_courses_html_links(html_courses)
    all_issues.extend(issues1)
    sections.append(("Internal Links (courses.html)", issues1, info1))
    print(f"  {len(issues1)} issues found")

    # 2. electives-hub check
    print("\n[2/5] Auditing electives-hub.html...")
    html_hub = read_file(ELECTIVES_HUB)
    if html_hub:
        issues2, info2, hub_courses = audit_electives_hub(html_hub)
    else:
        issues2, info2, hub_courses = [{"type":"MISSING_FILE","severity":"error","msg":"electives-hub.html not found"}], [], {}
    all_issues.extend(issues2)
    sections.append(("Electives Hub", issues2, info2))
    print(f"  {len(issues2)} issues found")

    # 3. course-registry.json check
    print("\n[3/5] Auditing course-registry.json...")
    issues3, info3, registry = audit_course_registry()
    all_issues.extend(issues3)
    sections.append(("Course Registry", issues3, info3))
    print(f"  {len(issues3)} issues found")

    # 4. Cross-reference check
    print("\n[4/5] Checking cross-references...")
    issues4, info4 = audit_cross_references(html_courses, hub_courses, registry)
    all_issues.extend(issues4)
    sections.append(("Cross-References", issues4, info4))
    print(f"  {len(issues4)} issues found")

    # 5. Live site check
    print("\n[5/5] Checking live site URLs...")
    issues5, info5 = audit_live_site(html_courses)
    all_issues.extend(issues5)
    sections.append(("Live Site (aesopacademy.org)", issues5, info5))
    print(f"  {len(issues5)} issues found")

    # 6. Module file integrity (bonus)
    print("\n[Bonus] Checking module file integrity...")
    issues6, info6 = audit_module_file_integrity()
    all_issues.extend(issues6)
    sections.append(("Module File Integrity", issues6, info6))
    print(f"  {len(issues6)} issues found")

    # Generate report
    report = generate_report(all_issues, [], sections)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(report, encoding="utf-8")

    errors = [i for i in all_issues if i.get("severity") == "error"]
    warnings = [i for i in all_issues if i.get("severity") == "warning"]

    print(f"\n{'=' * 60}")
    print(f"AUDIT COMPLETE")
    print(f"  Errors:   {len(errors)}")
    print(f"  Warnings: {len(warnings)}")
    print(f"  Report:   {REPORT_PATH}")
    print(f"{'=' * 60}")

    # Exit with error code if critical issues found
    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
