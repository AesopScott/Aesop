"""
AIP Research Agent — AESOP Intelligence Pipeline
Runs weekly via GitHub Actions.
Queries Pinecone for corpus gaps, generates course draft proposals,
saves them as JSON to aip/drafts/.
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path
import anthropic
from pinecone import Pinecone, ServerlessSpec

# ── CONFIG ────────────────────────────────────────────────────────────────────

ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
PINECONE_API_KEY  = os.environ["PINECONE_API_KEY"]
PINECONE_HOST     = os.environ["PINECONE_HOST"]
PINECONE_INDEX    = "aesop-academy"
DRAFTS_DIR        = Path("aip/drafts")
DRAFTS_PER_RUN    = 3   # proposals generated per weekly run

EDTECH_TOPICS = [
    "AI in healthcare and medicine",
    "AI and climate change",
    "AI in criminal justice",
    "AI for accessibility and disability",
    "AI and misinformation / deepfakes",
    "AI in financial systems",
    "AI and surveillance",
    "AI in education and personalized learning",
    "AI and creative arts",
    "AI ethics for beginners",
    "Machine learning basics",
    "AI and job automation",
    "AI in government and policy",
    "AI safety and alignment",
    "AI and privacy",
    "Robotics and physical AI",
    "AI in agriculture",
    "AI and mental health",
    "Natural language processing",
    "Computer vision in everyday life",
]

# ── PINECONE: CHECK CORPUS COVERAGE ──────────────────────────────────────────

def check_corpus_coverage():
    """Query Pinecone for each topic — return topics with thin coverage."""
    print("Checking corpus coverage via Pinecone...")
    pc = Pinecone(api_key=PINECONE_API_KEY)
    index = pc.Index(PINECONE_INDEX, host=PINECONE_HOST)

    import requests
    gap_topics = []

    for topic in EDTECH_TOPICS:
        # Embed via Anthropic voyage-3 REST directly
        embed_res = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": "voyage-3",
                "input": [topic],
                "input_type": "query",
            }
        )

        # Fallback: if voyage endpoint unavailable, use zero vector + skip scoring
        if embed_res.status_code != 200:
            print(f"  {topic}: embedding unavailable, marking as gap")
            gap_topics.append({"topic": topic, "score": 0.0})
            continue

        vector = embed_res.json()["embeddings"][0]["values"]

        # Query Pinecone
        result = index.query(vector=vector, top_k=3, include_metadata=True)
        matches = result.get("matches", [])
        top_score = matches[0]["score"] if matches else 0.0
        print(f"  {topic}: top score={top_score:.3f}")

        if top_score < 0.75:
            gap_topics.append({"topic": topic, "score": top_score})

    gap_topics.sort(key=lambda x: x["score"])
    print(f"\nFound {len(gap_topics)} gap topics.")
    return gap_topics

# ── ANTHROPIC: GENERATE DRAFT PROPOSALS ──────────────────────────────────────

def generate_drafts(gap_topics):
    """Generate course draft proposals for the top gap topics."""
    if not gap_topics:
        print("No gaps found — skipping generation.")
        return []

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    topics_to_draft = gap_topics[:DRAFTS_PER_RUN]
    topic_list = "\n".join(f"- {t['topic']}" for t in topics_to_draft)

    print(f"\nGenerating {len(topics_to_draft)} draft proposals...")

    prompt = f"""You are a curriculum designer for AESOP AI Academy — an AI literacy platform for learners of all ages.

Generate {len(topics_to_draft)} course draft proposals for these underrepresented topics in our curriculum:

{topic_list}

For EACH topic, return a JSON object with exactly these fields:
- "id": kebab-case slug (e.g. "ai-in-healthcare")
- "title": short, compelling course title (max 6 words)
- "modules": array of 4 module names (each max 5 words)
- "synopsis": 2-sentence course description for a general audience

Return ONLY a JSON array of objects. No preamble, no markdown fences."""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.content[0].text.strip()

    # Strip markdown fences if present
    raw = re.sub(r"^```json\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)

    drafts = json.loads(raw)
    print(f"Generated {len(drafts)} proposals.")
    return drafts

# ── SAVE DRAFTS ───────────────────────────────────────────────────────────────

def save_drafts(drafts):
    """Save each draft as a JSON file in aip/drafts/."""
    DRAFTS_DIR.mkdir(parents=True, exist_ok=True)
    date_str = datetime.utcnow().strftime("%Y-%m-%d")
    saved = []

    for draft in drafts:
        draft["generated"] = date_str
        draft["status"] = "pending"

        filename = f"{date_str}-{draft['id']}.json"
        filepath = DRAFTS_DIR / filename

        # Don't overwrite an existing draft with same ID
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

    gap_topics = check_corpus_coverage()
    drafts = generate_drafts(gap_topics)

    if drafts:
        saved = save_drafts(drafts)
        print(f"\nDone. {len(saved)} new draft(s) committed to aip/drafts/")
    else:
        print("\nNo new drafts generated this run.")

if __name__ == "__main__":
    main()
