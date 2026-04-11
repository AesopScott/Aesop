"""
AIP Research Agent — AESOP Intelligence Pipeline
Runs weekly via GitHub Actions.
Uses Claude to identify EdTech content gaps and generate course proposals.
Saves draft JSON files to aip/drafts/.
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path
import anthropic

# ── CONFIG ────────────────────────────────────────────────────────────────────

ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
DRAFTS_DIR        = Path("aip/drafts")
DRAFTS_PER_RUN    = 3

# ── EXISTING COURSES (keep updated as courses launch) ─────────────────────────

EXISTING_COURSES = [
    "Building with AI — AI foundations course",
    "AI Electives — supplementary AI topics",
]

# ── GENERATE GAP ANALYSIS + PROPOSALS IN ONE CALL ────────────────────────────

def generate_drafts():
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    existing = "\n".join(f"- {c}" for c in EXISTING_COURSES)

    print(f"Calling Claude to identify gaps and generate {DRAFTS_PER_RUN} proposals...")

    prompt = f"""You are a curriculum designer for AESOP AI Academy — an AI literacy platform for learners of all ages.

Our existing courses cover:
{existing}

Identify {DRAFTS_PER_RUN} high-value AI literacy topics NOT yet covered by these courses that would benefit a general audience (students, educators, curious adults).

For EACH topic, return a JSON object with exactly these fields:
- "id": kebab-case slug (e.g. "ai-in-healthcare")
- "title": short, compelling course title (max 6 words)
- "modules": array of 4 module names (each max 5 words)
- "synopsis": 2-sentence course description for a general audience

Return ONLY a JSON array of {DRAFTS_PER_RUN} objects. No preamble, no markdown fences."""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.content[0].text.strip()
    raw = re.sub(r"^```json\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)

    drafts = json.loads(raw)
    print(f"Generated {len(drafts)} proposals.")
    return drafts

# ── SAVE DRAFTS ───────────────────────────────────────────────────────────────

def save_drafts(drafts):
    DRAFTS_DIR.mkdir(parents=True, exist_ok=True)
    date_str = datetime.utcnow().strftime("%Y-%m-%d")
    saved = []

    for draft in drafts:
        draft["generated"] = date_str
        draft["status"] = "pending"
        filename = f"{date_str}-{draft['id']}.json"
        filepath = DRAFTS_DIR / filename

        if filepath.exists():
            print(f"  Skipping (exists): {filename}")
            continue

        with open(filepath, "w") as f:
            json.dump(draft, f, indent=2)

        print(f"  Saved: {filename}")
        saved.append(filename)

    return saved

# ── MAIN ──────────────────────────────────────────────────────────────────────

def main():
    print("=== AIP Research Agent ===")
    print(f"Run date: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}\n")

    drafts = generate_drafts()

    if drafts:
        saved = save_drafts(drafts)
        print(f"\nDone. {len(saved)} new draft(s) saved to aip/drafts/")
    else:
        print("\nNo drafts generated this run.")

if __name__ == "__main__":
    main()
