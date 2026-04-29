#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
backfill_drafts.py — One-shot backfill for legacy course drafts.

Walks all four draft folders:
  aip/drafts/         — Professional drafts
  aip/ya-drafts/      — Young Adult drafts
  aip/k12-drafts/     — Youth (K-12) drafts
  aip/cyber-drafts/   — Cybersecurity drafts

For each draft that is missing the new schema fields, calls the
Anthropic API once to produce:
  - mega_group         (one of the allowed nav-section keys)
  - modules            (objects with {title, sub, description})

The original module *titles* are preserved verbatim — the backfill only
adds the missing 'sub' and 'description' fields to each module object,
plus the missing top-level 'mega_group'.

Backwards-compatible: drafts that already have both fields are skipped.

Usage (local):
    export ANTHROPIC_API_KEY=sk-ant-...
    python .github/scripts/backfill_drafts.py             # dry run, prints planned writes
    python .github/scripts/backfill_drafts.py --apply     # actually write back

Cost: ~150 drafts at ~$0.005 each = ~$0.75. Tiny.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO  = Path(__file__).resolve().parents[2]

DRAFT_FOLDERS = {
    "aip/drafts":       ("Professional", [
        "AI Tools", "Strategy", "AI Models", "AI Frontier", "Development",
        "Society", "Applied", "Business", "Cybersecurity",
    ]),
    "aip/ya-drafts":    ("Young Adult", [
        "AI Tools", "Make & Create", "How AI Works", "Truth & Safety",
        "Strategy", "Society", "Business",
    ]),
    "aip/k12-drafts":   ("Youth", [
        "How AI Works", "Make & Create", "Truth & Safety",
    ]),
    "aip/cyber-drafts": ("Cybersecurity", [
        "Cybersecurity",
    ]),
}


def needs_backfill(draft: dict) -> bool:
    """Returns True iff this draft is missing mega_group OR any of its
    modules are still bare strings (legacy schema)."""
    if not draft.get("mega_group"):
        return True
    for m in draft.get("modules", []):
        if not isinstance(m, dict):
            return True
        if not (m.get("sub") or "").strip():
            return True
        if not (m.get("description") or "").strip():
            return True
    return False


def build_prompt(draft: dict, audience_label: str, allowed_groups: list[str]) -> str:
    title    = draft.get("title", "")
    synopsis = draft.get("synopsis", "")
    learning_outcome = draft.get("learning_outcome", "")
    age_band = draft.get("age_band", "")
    age_note = f"\nAge band: {age_band}" if age_band else ""
    raw_mods = draft.get("modules", [])
    # Normalise to a list of {title} for the prompt; preserve any existing sub/description
    mod_lines = []
    for i, m in enumerate(raw_mods, 1):
        if isinstance(m, dict):
            t = m.get("title", "") or ""
            s = m.get("sub", "") or ""
            d = m.get("description", "") or ""
            line = f'  M{i}: "{t}"'
            if s: line += f' (existing sub: "{s}")'
            if d: line += f' (existing desc: "{d[:80]}")'
            mod_lines.append(line)
        else:
            mod_lines.append(f'  M{i}: "{m}"')
    mods_block = "\n".join(mod_lines)

    allowed_block = "\n".join(f'    - "{g}"' for g in allowed_groups)

    return f"""You are backfilling missing metadata on an existing course draft for AESOP AI Academy.
The course is for the {audience_label} audience.{age_note}

Course title: {title}

Course synopsis: {synopsis}

Course learning outcome: {learning_outcome}

Course modules (in order — do not change titles):
{mods_block}

Your job is to produce two things:

1. mega_group — pick EXACTLY one of these labels for which nav section this course belongs in:
{allowed_block}

2. For EACH module, produce:
   - "sub":         a 6-12 word subtitle that frames what the module is about
   - "description": 2-3 sentences describing what the learner does, decides, or makes in that module

Return ONLY a JSON object with this exact shape (no markdown fences, no preamble):

{{
  "mega_group": "<one of the allowed labels above>",
  "modules": [
    {{"title": "<original module 1 title verbatim>", "sub": "<...>", "description": "<...>"}},
    {{"title": "<original module 2 title verbatim>", "sub": "<...>", "description": "<...>"}},
    ...
  ]
}}

The "title" for each module MUST match the original module title exactly. Only "sub" and "description" are new content."""


def call_claude(client, prompt: str) -> dict:
    for attempt in range(4):
        try:
            r = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=2500,
                messages=[{"role": "user", "content": prompt}],
            )
            break
        except Exception as e:
            if attempt == 3:
                raise
            time.sleep(8 * (attempt + 1))
    raw = r.content[0].text.strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    return json.loads(raw)


def merge_into_draft(draft: dict, llm_out: dict, allowed_groups: list[str]) -> dict:
    """Merge the model's output into the draft, preserving existing fields and
    enforcing that mega_group is one of the allowed values."""
    new = dict(draft)

    mg = (llm_out.get("mega_group") or "").strip()
    if mg in allowed_groups:
        new["mega_group"] = mg
    elif draft.get("mega_group"):
        new["mega_group"] = draft["mega_group"]
    else:
        # Default to the first allowed group as a last resort
        new["mega_group"] = allowed_groups[0]

    # Map original module titles → llm-produced sub/description by index,
    # then by exact title match as a fallback.
    raw_mods   = draft.get("modules", [])
    llm_mods   = llm_out.get("modules", []) or []
    llm_by_tit = {(m.get("title") or "").strip(): m for m in llm_mods if isinstance(m, dict)}

    new_mods = []
    for i, m in enumerate(raw_mods):
        orig_title = m.get("title") if isinstance(m, dict) else str(m)
        orig_sub   = m.get("sub", "") if isinstance(m, dict) else ""
        orig_desc  = m.get("description", "") if isinstance(m, dict) else ""

        llm_m = None
        if i < len(llm_mods) and isinstance(llm_mods[i], dict):
            llm_m = llm_mods[i]
        if not llm_m and orig_title and orig_title.strip() in llm_by_tit:
            llm_m = llm_by_tit[orig_title.strip()]

        sub  = orig_sub  or (llm_m.get("sub", "") if llm_m else "")
        desc = orig_desc or (llm_m.get("description", "") if llm_m else "")

        new_mods.append({
            "title":       (orig_title or "").strip(),
            "sub":         (sub or "").strip(),
            "description": (desc or "").strip(),
        })
    new["modules"] = new_mods
    return new


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true",
                    help="Actually write the updated drafts back. Without "
                         "this, runs as a dry-run with cost estimate only.")
    ap.add_argument("--limit", type=int, default=0,
                    help="Cap the number of drafts processed. 0 = no cap.")
    ap.add_argument("--folder", default="",
                    help="Restrict to one folder, e.g. aip/k12-drafts")
    args = ap.parse_args()

    candidates = []
    for folder, (audience, groups) in DRAFT_FOLDERS.items():
        if args.folder and folder != args.folder:
            continue
        d = REPO / folder
        if not d.exists():
            continue
        for p in sorted(d.glob("*.json")):
            # Skip the directory's index file if any
            if p.name in ("index.json",):
                continue
            try:
                draft = json.loads(p.read_text(encoding="utf-8"))
            except Exception:
                continue
            if not isinstance(draft, dict):
                continue   # skip lists, scalars, etc.
            if not draft.get("title") or not draft.get("modules"):
                continue   # not a course draft
            if needs_backfill(draft):
                candidates.append((p, draft, audience, groups))

    if args.limit:
        candidates = candidates[: args.limit]

    print(f"Drafts needing backfill: {len(candidates)}")
    if not candidates:
        return 0

    if not args.apply:
        for p, draft, audience, _ in candidates[:5]:
            print(f"  would update: {p.relative_to(REPO)}  ({audience}: {draft.get('title','')!r})")
        if len(candidates) > 5:
            print(f"  … and {len(candidates) - 5} more")
        print()
        print(f"Estimated cost: ~${0.005 * len(candidates):.2f} ({len(candidates)} Claude calls)")
        print("Re-run with --apply to actually write.")
        return 0

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY not set", file=sys.stderr)
        return 2
    import anthropic
    client = anthropic.Anthropic(api_key=api_key)

    written = 0
    failed  = 0
    for i, (p, draft, audience, groups) in enumerate(candidates, 1):
        print(f"[{i}/{len(candidates)}] {p.relative_to(REPO)}  ({audience})")
        try:
            prompt = build_prompt(draft, audience, groups)
            llm_out = call_claude(client, prompt)
            updated = merge_into_draft(draft, llm_out, groups)
            p.write_text(
                json.dumps(updated, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            written += 1
            print(f"  ok — mega_group={updated.get('mega_group')!r}, "
                  f"{sum(1 for m in updated['modules'] if m.get('sub'))} subs, "
                  f"{sum(1 for m in updated['modules'] if m.get('description'))} descriptions")
        except Exception as e:
            failed += 1
            print(f"  FAIL: {e}")

    print()
    print(f"Backfilled: {written}, failed: {failed}, total: {len(candidates)}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
