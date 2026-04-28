"""
Generates sitemap.xml for aesopacademy.org from the live HTML files on disk.

Excludes: .claude/, archive/, es_old/, board/, admin pages, fragments (no <head>),
          and the internal/draft files listed in SKIP_FILES.

Usage (run from repo root):
    python .github/scripts/build_sitemap.py
"""

from datetime import datetime, timezone
from pathlib import Path

BASE = "https://aesopacademy.org"
ROOT = Path(__file__).resolve().parents[2]
I18N = {"ar", "de", "es", "fa", "fr", "hi", "ja", "ko", "ru", "sw", "ur", "zh"}

SKIP_DIR_NAMES = {".claude", "archive", "es_old", "board", "__pycache__", "AI Academy Documents"}
ADMIN_PREFIXES = ("ai-academy/admin",)
SKIP_REL_PREFIXES = ("about/board-meetings/", "scheduling/")

# Internal/draft files — keep in sync with seo_fix.py SKIP_FILES
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


def should_skip(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    if rel in SKIP_FILES:
        return True
    if any(rel.startswith(p) for p in ADMIN_PREFIXES + SKIP_REL_PREFIXES):
        return True
    for part in path.relative_to(ROOT).parts[:-1]:
        if part in SKIP_DIR_NAMES:
            return True
    return False


def priority(rel: str) -> str:
    if rel == "index.html":
        return "1.0"
    if rel in ("ai-academy/index.html", "ai-academy/courses.html"):
        return "0.9"
    if rel == "ai-news/index.html":
        return "0.8"
    if rel.startswith("ai-news/articles/"):
        return "0.7"
    if rel.startswith("ai-academy/modules/electives-hub"):
        return "0.8"
    parts = rel.split("/")
    if len(parts) > 3 and parts[2] in I18N:
        return "0.5"
    if rel.startswith("ai-academy/modules/"):
        return "0.8"
    if rel.startswith("ai-academy/"):
        return "0.7"
    if rel.startswith("about/") or rel.startswith("standards/"):
        return "0.6"
    if rel.startswith("policies/") or rel.startswith("review/") or rel.startswith("m/"):
        return "0.5"
    return "0.6"


def changefreq(rel: str) -> str:
    if rel == "ai-news/index.html":
        return "daily"
    if rel.startswith("ai-news/articles/"):
        return "yearly"
    return "monthly"


def lastmod(path: Path) -> str:
    return datetime.fromtimestamp(
        path.stat().st_mtime, tz=timezone.utc
    ).strftime("%Y-%m-%d")


def main() -> None:
    entries: list[tuple[str, str, str, str]] = []

    for path in sorted(ROOT.rglob("*.html")):
        if should_skip(path):
            continue
        rel = path.relative_to(ROOT).as_posix()
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
            if "</head>" not in text.lower():
                continue
        except OSError:
            continue
        entries.append((f"{BASE}/{rel}", lastmod(path), changefreq(rel), priority(rel)))

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for url, lm, freq, pri in entries:
        lines += [
            "  <url>",
            f"    <loc>{url}</loc>",
            f"    <lastmod>{lm}</lastmod>",
            f"    <changefreq>{freq}</changefreq>",
            f"    <priority>{pri}</priority>",
            "  </url>",
        ]
    lines.append("</urlset>")

    out = ROOT / "sitemap.xml"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Written {len(entries)} entries to sitemap.xml")


if __name__ == "__main__":
    main()
