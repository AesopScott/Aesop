#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
apply_youth_six_categories.py — One-shot patch that expands Youth nav
from 3 sub-categories to 6, in lock-step across courses.html, the
autopatch script, the validator, the backfill, the K-12 research
prompt, and the 44 existing K-12 draft JSONs.

Idempotent. Safe to re-run.
"""

import re
import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def step(label):
    print(f"\n── {label} ──")


# ── 1. courses.html: insert 3 new Youth mega-group blocks ──────────────────
step("1. courses.html: insert 3 new Youth mega-group headers")

p = Path("ai-academy/courses.html")
html = p.read_text(encoding="utf-8")

new_blocks = (
    '        <div class="mega-group">\n'
    '          <div class="mega-cat">🛠️ AI Toolbox</div>\n'
    '        </div>\n'
    '        <div class="mega-group">\n'
    '          <div class="mega-cat">🎓 AI in School</div>\n'
    '        </div>\n'
    '        <div class="mega-group">\n'
    '          <div class="mega-cat">💻 Code with AI</div>\n'
    '        </div>\n'
)
marker = "</div><!-- /.youth-groups-row -->"
if "AI Toolbox</div>" in html:
    print("  already present, skipping")
elif marker not in html:
    raise SystemExit("Could not find /.youth-groups-row close marker")
else:
    html = html.replace(marker, new_blocks + "        " + marker, 1)
    p.write_text(html, encoding="utf-8")
    print("  inserted 3 new Youth mega-group headers")


# ── 2. aip_autopatch.py CAT_MARKERS ───────────────────────────────────────
step("2. aip_autopatch.py: extend CAT_MARKERS")

p = Path(".github/scripts/aip_autopatch.py")
ap = p.read_text(encoding="utf-8")
new_lines = (
    '        "AI Toolbox":     \'<div class="mega-cat">🛠️ AI Toolbox</div>\',\n'
    '        "AI in School":   \'<div class="mega-cat">🎓 AI in School</div>\',\n'
    '        "Code with AI":   \'<div class="mega-cat">💻 Code with AI</div>\',\n'
)
needle = '        "Truth & Safety":  \'<div class="mega-cat">🛡️ Truth &amp; Safety</div>\',\n'
if "AI Toolbox" in ap:
    print("  already extended, skipping")
elif needle not in ap:
    raise SystemExit("Could not find Truth & Safety entry in CAT_MARKERS")
else:
    ap = ap.replace(needle, needle + new_lines, 1)
    p.write_text(ap, encoding="utf-8")
    print("  added 3 new Youth labels to CAT_MARKERS")


# ── 3. validate_draft_schema.py ALLOWED_GROUPS["Youth"] ────────────────────
step('3. validate_draft_schema.py: extend ALLOWED_GROUPS["Youth"]')

p = Path(".github/scripts/validate_draft_schema.py")
vs = p.read_text(encoding="utf-8")
old = '    "Youth": [\n        "How AI Works", "Make & Create", "Truth & Safety",\n    ],'
new = ('    "Youth": [\n'
       '        "How AI Works", "Make & Create", "Truth & Safety",\n'
       '        "AI Toolbox", "AI in School", "Code with AI",\n'
       '    ],')
if "AI Toolbox" in vs:
    print("  already extended, skipping")
elif old not in vs:
    raise SystemExit("Could not find Youth entry in ALLOWED_GROUPS")
else:
    vs = vs.replace(old, new, 1)
    p.write_text(vs, encoding="utf-8")
    print("  extended Youth ALLOWED_GROUPS to 6 values")


# ── 4. backfill_drafts.py DRAFT_FOLDERS["aip/k12-drafts"] ──────────────────
step("4. backfill_drafts.py: extend Youth folder allowed list")

p = Path(".github/scripts/backfill_drafts.py")
bf = p.read_text(encoding="utf-8")
old = ('    "aip/k12-drafts":   ("Youth", [\n'
       '        "How AI Works", "Make & Create", "Truth & Safety",\n'
       '    ]),')
new = ('    "aip/k12-drafts":   ("Youth", [\n'
       '        "How AI Works", "Make & Create", "Truth & Safety",\n'
       '        "AI Toolbox", "AI in School", "Code with AI",\n'
       '    ]),')
if "AI Toolbox" in bf:
    print("  already extended, skipping")
elif old not in bf:
    raise SystemExit("Could not find Youth folder entry in DRAFT_FOLDERS")
else:
    bf = bf.replace(old, new, 1)
    p.write_text(bf, encoding="utf-8")
    print("  extended Youth folder allowed list to 6 values")


# ── 5. k12_research_agent.py prompt: extend mega_group description ────────
step("5. k12_research_agent.py: extend mega_group prompt to 6 Youth options")

p = Path(".github/scripts/k12_research_agent.py")
ka = p.read_text(encoding="utf-8")

# The prompt block is a multi-line string. Search for the 3-line block we
# wrote earlier and replace it with a 6-line block.
old_block = (
    '- "mega_group": which Youth nav section this course belongs in. Pick EXACTLY one of:\n'
    '    "How AI Works"   — how AI thinks, learns, and what it really is under the hood\n'
    '    "Make & Create"  — courses where the learner builds, designs, codes, or creates with AI\n'
    '    "Truth & Safety" — bias, misinformation, deepfakes, scams, ethics, privacy, digital citizenship\n'
)
new_block = (
    '- "mega_group": which Youth nav section this course belongs in. Pick EXACTLY one of:\n'
    '    "How AI Works"   — how AI thinks, learns, perceives, and communicates (mechanism / explanation)\n'
    '    "Make & Create"  — building, designing, no-code automation, or general creating with AI (excludes coding-as-skill)\n'
    '    "AI Toolbox"     — getting productive with specific named AI tools (ChatGPT, Claude, Gemini, etc.) and choosing between them\n'
    '    "AI in School"   — using AI in classroom contexts: tutoring, study skills, homework, teaching, school-specific risks\n'
    '    "Code with AI"   — programming/coding with AI assistants (Copilot, Cursor, Scratch-to-Python, etc.)\n'
    '    "Truth & Safety" — bias, misinformation, deepfakes, scams, ethics, privacy, digital citizenship, agentic-risk\n'
)
if "AI Toolbox" in ka:
    print("  prompt already extended, skipping")
elif old_block not in ka:
    raise SystemExit("Could not find Youth mega_group block in k12_research_agent.py prompt")
else:
    ka = ka.replace(old_block, new_block, 1)
    p.write_text(ka, encoding="utf-8")
    print("  extended mega_group prompt to 6 Youth options")


# ── 6. Re-classify the 44 K-12 drafts across the 6 buckets ─────────────────
step("6. Re-classify 44 K-12 drafts across the new 6-bucket scheme")

RECLASSIFY = {
    # How AI Works (12)
    "how-ai-actually-works":             "How AI Works",
    "robot-speak-talk-to-ai":            "How AI Works",
    "talking-to-ai-prompt-writing":      "How AI Works",
    "whats-really-inside-ai":            "How AI Works",
    "ai-lens-on-the-world":              "How AI Works",
    "how-chatbots-think":                "How AI Works",
    "how-machines-learn":                "How AI Works",
    "meet-your-ai-assistant":            "How AI Works",
    "smart-machines-learn-from-us":      "How AI Works",
    "what-is-ai-anyway":                 "How AI Works",
    "what-is-ai-really":                 "How AI Works",
    "your-first-ai-conversation":        "How AI Works",

    # Make & Create (5)
    "creating-with-ai-tools":            "Make & Create",
    "make-it-yours-creating-with-ai":    "Make & Create",
    "build-ai-workflows-no-code":        "Make & Create",
    "no-code-ai-builder":                "Make & Create",
    "talk-to-the-machine":               "Make & Create",

    # AI Toolbox (4)
    "chatgpt-unlocked":                  "AI Toolbox",
    "chatgpt-claude-gemini-showdown":    "AI Toolbox",
    "ai-tools-field-guide":              "AI Toolbox",
    "pick-the-right-ai-tool":            "AI Toolbox",

    # AI in School (8)
    "ai-tools-for-real-teaching":        "AI in School",
    "ai-risks-in-schools":               "AI in School",
    "ai-risks-decoded":                  "AI in School",
    "homework-and-ai-honestly":          "AI in School",
    "homework-and-the-ai-question":      "AI in School",
    "study-smarter-with-ai":             "AI in School",
    "ai-tutor-under-the-hood":           "AI in School",
    "how-ai-tutors-work":                "AI in School",

    # Code with AI (4)
    "code-smarter-with-ai":              "Code with AI",
    "code-with-ai-co-pilot":             "Code with AI",
    "code-your-first-idea":              "Code with AI",
    "your-first-ai-project":             "Code with AI",

    # Truth & Safety (11)
    "ai-and-fake-information":           "Truth & Safety",
    "ai-bias-and-fairness":              "Truth & Safety",
    "coded-unfair-ai-bias-exposed":      "Truth & Safety",
    "truth-detectives-ai-and-fake-info": "Truth & Safety",
    "ai-agents-in-the-wild":             "Truth & Safety",
    "digital-citizenship-and-ai":        "Truth & Safety",
    "is-ai-telling-you-the-truth":       "Truth & Safety",
    "is-the-robot-being-fair":           "Truth & Safety",
    "real-or-rendered":                  "Truth & Safety",
    "spot-the-fake-ai-content":          "Truth & Safety",
    "teen-privacy-and-ai":               "Truth & Safety",
}

from collections import Counter
print("  expected distribution:")
for cat, n in Counter(RECLASSIFY.values()).most_common():
    print(f"    {cat}: {n}")
print(f"    TOTAL: {len(RECLASSIFY)}")

changed = 0
for f in sorted(Path("aip/k12-drafts").glob("*.json")):
    if f.name == "index.json":
        continue
    try:
        d = json.loads(f.read_text(encoding="utf-8"))
    except Exception:
        continue
    if not isinstance(d, dict):
        continue
    sid = d.get("id")
    if sid in RECLASSIFY and d.get("mega_group") != RECLASSIFY[sid]:
        d["mega_group"] = RECLASSIFY[sid]
        f.write_text(
            json.dumps(d, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        changed += 1
print(f"  re-classified {changed} drafts")

print("\nAll six steps complete.")
