"""
Adds missing SEO tags to every live HTML page in the aesopacademy.org static site.

What it adds (only where the tag is absent):
  1. <meta name="description">  — generated from the page <title>
  2. <link rel="canonical">     — derived from the file path
  3. Open Graph block           — og:title/description/url/site_name/type/image
  4. Twitter Card block

Admin pages (ai-academy/admin/) receive <meta name="robots" content="noindex, nofollow">
instead of the discoverable tags above.

Skips: .claude/, archive/, es_old/, board/ directories.

Usage (run from repo root):
    python .github/scripts/seo_fix.py
"""

import html as html_mod
import re
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────

BASE_URL       = "https://aesopacademy.org"
DEFAULT_IMAGE  = "https://aesopacademy.org/og-image2.jpg"
SITE_NAME      = "AESOP AI Academy"
TWITTER_HANDLE = "@aesopacademy"
ROOT           = Path(__file__).resolve().parents[2]   # repo root

SKIP_DIR_NAMES = {".claude", "archive", "es_old", "board", "__pycache__"}
ADMIN_PREFIXES = ("ai-academy/admin",)

# Internal/draft files — excluded from SEO tag injection and sitemap
SKIP_FILES = {
    "aesop-academy-report-v1.2.html",
    "ai-academy/start-here-preview.html",
    "ai-academy/students.html",
    "ai-academy/transcript.html",
    "ai-academy/modules/aesop-module-generator.html",
    "ai-academy/modules/ai-curriculum-module0.html",
    "about/advisory-board-admin.html",
    "about/advisoryboard-form.html",
    "restaurant.html",
    "resume.html",
    "header-mockups.html",
    "course-selector-mockups.html",
    "find-skill-review.html",
    "free-ai-education-cover.html",
}

# ── Helpers ───────────────────────────────────────────────────────────────────

def should_skip(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    if rel in SKIP_FILES:
        return True
    for part in path.relative_to(ROOT).parts[:-1]:
        if part in SKIP_DIR_NAMES:
            return True
    return False


def is_admin(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    return any(rel.startswith(p) for p in ADMIN_PREFIXES)


def has_tag(content: str, pattern: str) -> bool:
    return bool(re.search(pattern, content, re.IGNORECASE))


def extract_tag(content: str, pattern: str) -> str:
    m = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
    return m.group(1).strip() if m else ""


def clean_html(text: str) -> str:
    return re.sub(r"\s+", " ", html_mod.unescape(text)).strip()


def canonical_url(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    return f"{BASE_URL}/" if rel == "index.html" else f"{BASE_URL}/{rel}"


def make_description(title_raw: str) -> str:
    t = clean_html(title_raw)

    # "Course Name — Module N: Subtitle"
    m = re.match(
        r"^(.+?)\s*[—–\-]+\s*Module\s+(\d+):\s*(.+)$", t, re.IGNORECASE
    )
    if m:
        course, num, subtitle = m.group(1).strip(), m.group(2), m.group(3).strip()
        desc = (
            f"Module {num} of the {course} course: {subtitle}. "
            f"Story-driven AI literacy at AESOP AI Academy."
        )
    else:
        base = re.sub(
            r"\s*[—–\-]+\s*AESOP\s+AI\s+Academy\s*$", "", t, flags=re.IGNORECASE
        ).strip()
        desc = (
            f"{base}. "
            f"Part of AESOP AI Academy's story-driven AI literacy curriculum "
            f"for learners of all ages."
        )

    if len(desc) > 155:
        desc = desc[:152].rsplit(" ", 1)[0].rstrip(",;:") + "..."
    return desc


def get_existing_description(content: str) -> str:
    d = extract_tag(content, r'name=["\']description["\'][^>]*content=["\']([^"\']*)["\']')
    if not d:
        d = extract_tag(content, r'content=["\']([^"\']*)["\'][^>]*name=["\']description["\']')
    return clean_html(d)


def get_existing_canonical(content: str) -> str:
    c = extract_tag(content, r'rel=["\']canonical["\'][^>]*href=["\']([^"\']*)["\']')
    if not c:
        c = extract_tag(content, r'href=["\']([^"\']*)["\'][^>]*rel=["\']canonical["\']')
    return c.strip()


# ── File processor ────────────────────────────────────────────────────────────

def process(path: Path) -> list[str] | None:
    text = path.read_text(encoding="utf-8", errors="replace")

    if "</head>" not in text.lower():
        return None

    admin = is_admin(path)
    inserts: list[str] = []
    added: list[str] = []

    # Admin pages: noindex only
    if admin:
        if not has_tag(text, r'name=["\']robots["\']'):
            inserts.append('<meta name="robots" content="noindex, nofollow">')
            added.append("noindex")
        if inserts:
            _write(path, text, inserts)
        return added or None

    # Extract title — required for all other tags
    title_raw = extract_tag(text, r"<title[^>]*>(.*?)</title>")
    if not title_raw:
        return None

    title = clean_html(title_raw)

    # 1. Meta description
    if not has_tag(text, r'name=["\']description["\']'):
        desc = make_description(title_raw)
        inserts.append(
            f'<meta name="description" content="{html_mod.escape(desc, quote=True)}">'
        )
        added.append("description")
        desc_value = desc
    else:
        desc_value = get_existing_description(text) or make_description(title_raw)

    # 2. Canonical
    if not has_tag(text, r'rel=["\']canonical["\']'):
        canon = canonical_url(path)
        inserts.append(f'<link rel="canonical" href="{canon}">')
        added.append("canonical")
        canon_value = canon
    else:
        canon_value = get_existing_canonical(text) or canonical_url(path)

    # 3. Open Graph
    if not has_tag(text, r"og:title"):
        et = html_mod.escape(title, quote=True)
        ed = html_mod.escape(desc_value[:200], quote=True)
        inserts.append(
            f'<meta property="og:title" content="{et}">\n'
            f'<meta property="og:description" content="{ed}">\n'
            f'<meta property="og:url" content="{canon_value}">\n'
            f'<meta property="og:site_name" content="{SITE_NAME}">\n'
            f'<meta property="og:type" content="website">\n'
            f'<meta property="og:image" content="{DEFAULT_IMAGE}">'
        )
        added.append("og_tags")

    # 4. Twitter Card
    if not has_tag(text, r"twitter:card"):
        et = html_mod.escape(title, quote=True)
        ed = html_mod.escape(desc_value[:200], quote=True)
        inserts.append(
            f'<meta name="twitter:card" content="summary_large_image">\n'
            f'<meta name="twitter:site" content="{TWITTER_HANDLE}">\n'
            f'<meta name="twitter:title" content="{et}">\n'
            f'<meta name="twitter:description" content="{ed}">\n'
            f'<meta name="twitter:image" content="{DEFAULT_IMAGE}">'
        )
        added.append("twitter_card")

    if inserts:
        _write(path, text, inserts)

    return added or None


def _write(path: Path, original: str, inserts: list[str]) -> None:
    block = "\n" + "\n".join(inserts) + "\n"
    new_text = re.sub(
        r"(</head>)", block + r"\1", original, count=1, flags=re.IGNORECASE
    )
    path.write_text(new_text, encoding="utf-8", errors="replace")


# ── Runner ────────────────────────────────────────────────────────────────────

def main() -> None:
    counts: dict[str, int] = {}
    files_changed = 0
    files_skipped = 0

    for path in sorted(ROOT.rglob("*.html")):
        if should_skip(path):
            files_skipped += 1
            continue

        result = process(path)
        if result:
            files_changed += 1
            rel = path.relative_to(ROOT).as_posix()
            print(f"  [{', '.join(result)}]  {rel}")
            for tag in result:
                counts[tag] = counts.get(tag, 0) + 1

    print("\n-- Summary --------------------------------------------------")
    print(f"  Files changed : {files_changed}")
    print(f"  Files skipped : {files_skipped}  (archive / .claude / es_old / board)")
    for tag, n in sorted(counts.items()):
        print(f"  {tag:<20}: +{n}")


if __name__ == "__main__":
    main()
