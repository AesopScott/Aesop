#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audit_drift.py — Read-only drift report against disk truth.

Source of truth: `ai-academy/modules/<slug>/<slug>-m1.html`. A course
exists if that file exists. Every other surface (course-registry.json,
courses.html mega-menu + panels, dashboard.html COURSES array,
stats.json, i18n/courses.*.json) is checked against the disk slug set
and discrepancies are reported.

This script **never writes**. It produces a markdown report for human
review, saved to aip/drift-report.md.

Usage:
    python .github/scripts/audit_drift.py
"""

from __future__ import annotations

import html as _html_mod
import json
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO         = Path(__file__).resolve().parents[2]
MODULES_DIR  = REPO / "ai-academy" / "modules"
COURSES_HTML = REPO / "ai-academy" / "courses.html"
DASHBOARD    = REPO / "ai-academy" / "dashboard.html"
REGISTRY     = MODULES_DIR / "course-registry.json"
STATS_JSON   = REPO / "stats.json"
I18N_DIR     = REPO / "i18n"
REPORT       = REPO / "aip" / "drift-report.md"


# ── Disk truth ────────────────────────────────────────────────────────────────

def disk_courses() -> dict[str, dict]:
    """Return {slug: {n_modules: int, title_guess: str}} for every folder
    under ai-academy/modules/ that has <slug>-m1.html."""
    out: dict[str, dict] = {}
    for d in sorted(MODULES_DIR.iterdir()):
        if not d.is_dir() or d.name.startswith("."):
            continue
        m1 = d / f"{d.name}-m1.html"
        if not m1.exists():
            continue
        modules = sorted(d.glob(f"{d.name}-m*.html"))
        # Best-effort title from the kicker line — may be garbage for some
        # courses (e.g. returns "🎯 Advanced" or "Lesson 1" when the HTML
        # doesn't follow the usual template); report it as-is for human
        # review rather than silently fixing.
        title_guess = ""
        try:
            text = m1.read_text(encoding="utf-8", errors="replace")
            m = re.search(r'class="lesson-kicker">([^·<]+)', text)
            if m:
                title_guess = _html_mod.unescape(m.group(1).strip())
        except Exception:
            pass
        out[d.name] = {"n_modules": len(modules), "title_guess": title_guess}
    return out


# ── Registry ──────────────────────────────────────────────────────────────────

def registry_slugs() -> tuple[dict[str, str], list[dict]]:
    """Return ({slug: status}, raw_entries). Slug comes from the URL field
    (e.g. '/ai-academy/modules/ai-governance/' → 'ai-governance'). Entries
    with no URL are returned separately as 'sluggable-unknowns'."""
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    by_slug: dict[str, str] = {}
    orphans: list[dict] = []  # entries with no usable slug
    for key, entry in data.items():
        if not isinstance(entry, dict):
            continue
        url = entry.get("url") or ""
        m = re.search(r"/modules/([^/]+)/", url)
        if m:
            slug = m.group(1)
            # If multiple registry entries hit the same slug, prefer 'live'
            existing = by_slug.get(slug)
            status = entry.get("status") or "coming-soon"
            if existing is None or (existing != "live" and status == "live"):
                by_slug[slug] = status
        else:
            orphans.append({
                "key":    key,
                "title":  entry.get("title"),
                "status": entry.get("status"),
            })
    return by_slug, orphans


# ── courses.html ──────────────────────────────────────────────────────────────

def mega_menu_buttons(html: str) -> list[dict]:
    """Return [{classes, panel, name, resolved_slug_or_None}] per button."""
    # Build dv-N → slug by scanning panels and their CTAs
    dv_to_slug: dict[str, str] = {}
    panel_pat = re.compile(
        r'<div\s+class="core-panel"\s+id="(dv-\d+)"(.*?)</div>\s*</div>',
        re.DOTALL,
    )
    course_pat = re.compile(r"course=([A-Za-z0-9_\-]+)")
    for m in panel_pat.finditer(html):
        cm = course_pat.search(m.group(2))
        if cm:
            dv_to_slug[m.group(1)] = cm.group(1)

    btns: list[dict] = []
    btn_pat = re.compile(
        r'<button\s+class="([^"]+)"[^>]*data-panel="([^"]+)"[^>]*>([^<]+)</button>'
    )
    for m in btn_pat.finditer(html):
        classes = m.group(1)
        if "mega-link" not in classes:
            continue
        panel = m.group(2)
        name = _html_mod.unescape(m.group(3).strip())
        resolved = None
        if panel.startswith("aip-"):
            resolved = panel[4:]
        elif panel.startswith("dv-"):
            resolved = dv_to_slug.get(panel)
        btns.append({
            "classes":  classes,
            "panel":    panel,
            "name":     name,
            "resolved": resolved,
            "is_live":  "mega-link--live" in classes,
        })
    return btns


def panel_summary(html: str) -> dict:
    """Panels are inline blocks with `id="dv-N"` and a title in
    `core-panel__title`. They don't carry a course slug, so we can't
    auto-match them to disk folders — we just count them."""
    # Count distinct panel ids
    dv_ids = set(re.findall(r'<div\s+class="core-panel"\s+id="(dv-\d+)"', html))
    # Count live badges (each panel may have a badge block)
    live_badges = len(re.findall(r"core-badge-live", html))
    # Pull titles from each panel for the report
    titles = []
    for m in re.finditer(
        r'<div\s+class="core-panel"\s+id="(dv-\d+)"(.*?)(?=<div\s+class="core-panel"\s+id="dv-\d+"|\Z)',
        html, re.DOTALL,
    ):
        dv_id = m.group(1)
        body = m.group(2)
        tm = re.search(r'class="core-panel__title">([^<]+)</div>', body)
        has_live = "core-badge-live" in body
        titles.append({
            "dv_id":  dv_id,
            "title":  _html_mod.unescape(tm.group(1).strip()) if tm else "",
            "is_live": has_live,
        })
    return {
        "n_ids":       len(dv_ids),
        "n_live":      live_badges,
        "titles":      titles,
    }


# ── dashboard.html ────────────────────────────────────────────────────────────

def dashboard_entries(html: str) -> list[str]:
    m = re.search(r"const\s+COURSES\s*=\s*\[(.*?)\];", html, re.DOTALL)
    if not m:
        return []
    body = m.group(1)
    return re.findall(r"id:\s*'([^']+)'", body)


# ── i18n ──────────────────────────────────────────────────────────────────────

def i18n_course_titles() -> dict[str, set[str]]:
    """Return {filename: {course_title, ...}}."""
    out = {}
    for f in sorted(I18N_DIR.glob("courses.*.json")):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        # i18n files are {english_title: translated_title} maps
        out[f.name] = set(data.keys()) if isinstance(data, dict) else set()
    return out


# ── Report ────────────────────────────────────────────────────────────────────

def render(disk: dict[str, dict],
           reg: dict[str, str],
           reg_orphans: list[dict],
           btns: list[dict],
           panels: dict,
           dash: list[str],
           stats: dict,
           i18n: dict[str, set[str]]) -> str:
    disk_slugs = set(disk.keys())
    reg_slugs = set(reg.keys())
    reg_live = {s for s, st in reg.items() if st == "live"}

    live_btns = [b for b in btns if b["is_live"]]
    resolved_live = {b["resolved"] for b in live_btns if b["resolved"]}

    panel_n_ids  = panels["n_ids"]
    panel_n_live = panels["n_live"]

    dash_set = set(dash)
    stats_live = stats.get("coursesLive")

    def mdlist(items, limit=None):
        items = sorted(items)
        if limit and len(items) > limit:
            return "\n".join(f"- `{x}`" for x in items[:limit]) + f"\n- … and {len(items)-limit} more"
        return "\n".join(f"- `{x}`" for x in items) or "- _(none)_"

    L = []
    L.append("# Course Drift Report")
    L.append("")
    L.append("**Source of truth for this report:** course folders with `<slug>-m1.html`")
    L.append("under `ai-academy/modules/` in the **local working copy of this repo**.")
    L.append("This is not necessarily the same as:")
    L.append("")
    L.append("- **GitHub `origin/main`** — usually identical if this worktree is synced, but")
    L.append("  could differ if commits are pending push or if `main` advanced during this run.")
    L.append("- **Production web server (aesopacademy.org)** — reflects whatever was last")
    L.append("  deployed; may lag behind or differ from GitHub `main` depending on deploy state.")
    L.append("")
    L.append("This script is read-only — nothing was modified.")
    L.append("")
    L.append(f"- Disk (truth): **{len(disk_slugs)}** courses")
    L.append(f"- Registry live: **{len(reg_live)}** courses  ({len(reg_slugs)} with a URL)")
    L.append(f"- courses.html `--live` buttons: **{len(live_btns)}**  (total mega-links: {len(btns)})")
    L.append(f"- courses.html panels (unique `dv-N` ids): **{panel_n_ids}**  (with `core-badge-live`: {panel_n_live})")
    L.append(f"- dashboard.html COURSES array: **{len(dash_set)}** entries")
    L.append(f"- stats.json coursesLive: **{stats_live}**")
    L.append("")

    # --- Registry ---
    L.append("## Registry vs Disk")
    L.append("")
    missing = disk_slugs - reg_slugs
    extra = reg_slugs - disk_slugs
    wrong_status = {s for s in disk_slugs & reg_slugs if reg[s] != "live"}
    L.append(f"**{len(missing)} on disk, missing from registry:**")
    L.append(mdlist(missing))
    L.append("")
    L.append(f"**{len(extra)} in registry, no folder on disk:**")
    L.append(mdlist(extra))
    L.append("")
    L.append(f"**{len(wrong_status)} in registry but not marked `live` (though folder exists):**")
    L.append(mdlist(wrong_status))
    L.append("")
    if reg_orphans:
        L.append(f"**{len(reg_orphans)} registry entries with no URL (unusable for matching):**")
        for o in sorted(reg_orphans, key=lambda x: x["key"] or ""):
            L.append(f"- key=`{o['key']}`  title={o['title']!r}  status={o['status']}")
        L.append("")

    # --- courses.html mega-menu ---
    L.append("## courses.html Mega-Menu vs Disk")
    L.append("")
    unresolved = [b for b in live_btns if not b["resolved"]]
    resolved_not_on_disk = {b["resolved"] for b in live_btns if b["resolved"] and b["resolved"] not in disk_slugs}
    disk_not_live_in_nav = disk_slugs - resolved_live
    L.append(f"**{len(unresolved)} `--live` buttons whose slug could not be auto-resolved**")
    L.append("(manual lookup needed — no slug in data-panel and CTA not inspected):")
    for b in sorted(unresolved, key=lambda x: x["panel"]):
        L.append(f"- panel=`{b['panel']}`  name=`{b['name']}`")
    L.append("")
    L.append(f"**{len(resolved_not_on_disk)} `--live` buttons resolved to a slug not found on disk:**")
    L.append(mdlist(resolved_not_on_disk))
    L.append("")
    L.append(f"**{len(disk_not_live_in_nav)} disk courses not represented by an auto-resolvable `--live` button:**")
    L.append("(some may have a button whose panel id couldn't be traced to a slug — cross-check against the unresolved list above)")
    L.append(mdlist(disk_not_live_in_nav))
    L.append("")

    # --- Panels ---
    L.append("## courses.html Panels")
    L.append("")
    L.append(f"Total panels (by `dv-N` id): **{panel_n_ids}**, with `core-badge-live`: **{panel_n_live}**.")
    L.append("")
    L.append("_Panels don't encode a course slug, so direct panel↔disk matching isn't implemented in this audit._")
    L.append("_Titles in each panel are listed below for human cross-reference with the nav and disk lists above._")
    L.append("")
    live_title_rows = [p for p in panels["titles"] if p["is_live"]]
    soon_title_rows = [p for p in panels["titles"] if not p["is_live"]]
    L.append(f"### {len(live_title_rows)} panels with live badge")
    for p in live_title_rows:
        L.append(f"- `{p['dv_id']}`  {p['title']!r}")
    L.append("")
    L.append(f"### {len(soon_title_rows)} panels without live badge")
    for p in soon_title_rows:
        L.append(f"- `{p['dv_id']}`  {p['title']!r}")
    L.append("")

    # --- Dashboard ---
    L.append("## dashboard.html vs Disk")
    L.append("")
    dash_missing = disk_slugs - dash_set
    dash_extra   = dash_set - disk_slugs
    L.append(f"**{len(dash_missing)} disk courses missing from dashboard COURSES array:**")
    L.append(mdlist(dash_missing))
    L.append("")
    L.append(f"**{len(dash_extra)} dashboard entries with no disk folder:**")
    L.append(mdlist(dash_extra))
    L.append("")

    # --- Stats ---
    L.append("## stats.json vs Disk")
    L.append("")
    delta = (stats_live or 0) - len(disk_slugs)
    L.append(f"stats.json reports **{stats_live}** live; disk has **{len(disk_slugs)}**.  Delta: **{delta:+d}**")
    L.append("")

    # --- i18n ---
    L.append("## i18n Course Files")
    L.append("")
    disk_titles = {d["title_guess"] for d in disk.values() if d["title_guess"]}
    for fname, titles in sorted(i18n.items()):
        missing_titles = disk_titles - titles if disk_titles else set()
        L.append(f"- `{fname}`: {len(titles)} titles " +
                 (f"(disk title-guesses missing: {len(missing_titles)})" if missing_titles else "(no gap vs disk title-guesses)"))
    L.append("")
    L.append("_(i18n comparison uses extracted title guesses from m1.html; some titles are garbage strings like '🎯 Advanced' — human review needed.)_")
    L.append("")

    # --- Disk title-extraction issues ---
    bad_titles = {slug: d["title_guess"] for slug, d in disk.items()
                  if not d["title_guess"]
                  or d["title_guess"].lower().startswith("lesson ")
                  or d["title_guess"].startswith(("🎯", "🧠", "🔬", "💡"))}
    if bad_titles:
        L.append("## Disk Courses With Bad Title Extraction")
        L.append("")
        L.append("These folders have m1.html but the lesson-kicker regex returned a non-title string.")
        L.append("Canonical title will need to be set elsewhere (registry, or a manual list).")
        L.append("")
        for slug, guess in sorted(bad_titles.items()):
            L.append(f"- `{slug}` → {guess!r}")
        L.append("")

    return "\n".join(L)


def main() -> None:
    disk = disk_courses()
    reg, reg_orphans = registry_slugs()
    html = COURSES_HTML.read_text(encoding="utf-8")
    btns = mega_menu_buttons(html)
    panels = panel_summary(html)
    dash = dashboard_entries(DASHBOARD.read_text(encoding="utf-8"))
    stats = json.loads(STATS_JSON.read_text(encoding="utf-8"))
    i18n = i18n_course_titles()

    md = render(disk, reg, reg_orphans, btns, panels, dash, stats, i18n)
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(md, encoding="utf-8")

    # Short console summary
    disk_slugs = set(disk.keys())
    reg_live = {s for s, st in reg.items() if st == "live"}
    live_btns = sum(1 for b in btns if b["is_live"])
    print(f"Disk:          {len(disk_slugs)} courses")
    print(f"Registry live: {len(reg_live)}")
    print(f"Nav --live:    {live_btns}")
    print(f"Dashboard:     {len(set(dash))}")
    print(f"stats.json:    {stats.get('coursesLive')}")
    print()
    print(f"Wrote {REPORT.relative_to(REPO)}")


if __name__ == "__main__":
    main()
