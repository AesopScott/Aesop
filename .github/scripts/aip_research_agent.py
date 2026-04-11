"""
AIP Research Agent — AESOP Intelligence Pipeline
Runs weekly via GitHub Actions (+ manual dispatch).
1. Queries Pinecone corpus to find real coverage gaps
2. Uses Claude to generate course proposals for underserved topics
3. Saves draft JSON files to aip/drafts/
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path
import anthropic
import requests
from pinecone import Pinecone

# ── CONFIG ────────────────────────────────────────────────────────────────────

ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
PINECONE_API_KEY  = os.environ["PINECONE_API_KEY"]
PINECONE_HOST     = os.environ["PINECONE_HOST"]
PINECONE_INDEX    = "aesop-academy"
DRAFTS_DIR        = Path("aip/drafts")
DRAFTS_PER_RUN    = 3
GAP_THRESHOLD     = 0.72   # topics scoring below this are considered gaps

# Topics to scan for coverage gaps — the research frontier
SCAN_TOPICS = [
    "AI in healthcare diagnosis and treatment",
    "AI and climate change mitigation",
    "AI in criminal justice and policing",
    "AI for accessibility and disability support",
    "AI deepfakes and misinformation detection",
    "AI in personal finance and banking",
    "AI surveillance and facial recognition",
    "AI personalized learning and tutoring",
    "AI music and audio generation",
    "AI ethics for children and families",
    "Machine learning fundamentals for beginners",
    "AI and job displacement automation",
    "AI in government policy and regulation",
    "AI safety alignment and existential risk",
    "AI and data privacy protection",
    "Robotics and embodied AI systems",
    "AI in agriculture and food production",
    "AI mental health therapy and support",
    "Natural language processing and chatbots",
    "Computer vision everyday applications",
    "AI in game design and interactive media",
    "AI supply chain and logistics optimization",
    "AI in journalism and media production",
    "AI and intellectual property copyright",
    "AI in scientific research and discovery",
    "AI for small business and entrepreneurship",
    "AI in military and defense applications",
    "AI transparency and explainability",
    "AI in real estate and urban planning",
    "AI and human creativity collaboration",
]

# ── PINECONE GAP CHECK ───────────────────────────────────────────────────────

def embed_query(text):
    """Embed a single query using Voyage-3."""
    resp = requests.post(
        "https://api.voyageai.com/v1/embeddings",
        headers={
            "Authorization": f"Bearer {ANTHROPIC_API_KEY}",
            "content-type": "application/json",
        },
        json={
            "model": "voyage-3",
            "input": [text],
            "input_type": "query",
        },
        timeout=30,
    )
    if resp.status_code != 200:
        return None
    return resp.json()["data"][0]["embedding"]


def find_corpus_gaps():
    """Query Pinecone for each topic — return topics with thin coverage."""
    print("Connecting to Pinecone...")
    pc = Pinecone(api_key=PINECONE_API_KEY)
    index = pc.Index(PINECONE_INDEX, host=PINECONE_HOST)
    stats = index.describe_index_stats()
    total_vectors = stats["total_vector_count"]
    print(f"  Corpus size: {total_vectors} vectors\n")

    if total_vectors == 0:
        print("  WARNING: Corpus is empty! All topics are gaps.")
        return [{"topic": t, "score": 0.0, "nearest": "none"} for t in SCAN_TOPICS]

    print(f"Scanning {len(SCAN_TOPICS)} topics for coverage gaps...\n")
    gap_topics = []

    for topic in SCAN_TOPICS:
        vector = embed_query(topic)
        if vector is None:
            print(f"  {topic}: embedding failed, marking as gap")
            gap_topics.append({"topic": topic, "score": 0.0, "nearest": "error"})
            continue

        result = index.query(vector=vector, top_k=3, include_metadata=True)
        matches = result.get("matches", [])
        top_score = matches[0]["score"] if matches else 0.0
        nearest = matches[0].get("metadata", {}).get("title", "?") if matches else "none"

        status = "GAP" if top_score < GAP_THRESHOLD else "covered"
        print(f"  [{status}] {topic}: score={top_score:.3f} nearest='{nearest}'")

        if top_score < GAP_THRESHOLD:
            gap_topics.append({"topic": topic, "score": top_score, "nearest": nearest})

    gap_topics.sort(key=lambda x: x["score"])
    print(f"\nFound {len(gap_topics)} gap topics (threshold={GAP_THRESHOLD}).")
    return gap_topics


# ── LOAD EXISTING DRAFTS (avoid duplicates) ──────────────────────────────────

def load_existing_draft_ids():
    """Get IDs of all existing drafts to avoid re-proposing."""
    existing = set()
    if DRAFTS_DIR.exists():
        for f in DRAFTS_DIR.glob("*.json"):
            try:
                data = json.loads(f.read_text())
                existing.add(data.get("id", ""))
                # Also track the topic to avoid near-duplicates
                existing.add(data.get("title", "").lower())
            except Exception:
                continue
    return existing


# ── GENERATE PROPOSALS ───────────────────────────────────────────────────────

def generate_drafts(gap_topics):
    """Use Claude to generate course proposals for top gap topics."""
    if not gap_topics:
        print("No gaps found — skipping generation.")
        return []

    existing_ids = load_existing_draft_ids()
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    topics_to_draft = gap_topics[:DRAFTS_PER_RUN]
    topic_list = "\n".join(
        f"- {t['topic']} (corpus similarity: {t['score']:.2f}, nearest existing: '{t['nearest']}')"
        for t in topics_to_draft
    )
    existing_note = ", ".join(existing_ids) if existing_ids else "none yet"

    print(f"\nGenerating {len(topics_to_draft)} draft proposals...")

    prompt = f"""You are a curriculum designer for AESOP AI Academy — a free AI literacy platform for students, educators, and curious adults.

Generate {len(topics_to_draft)} course draft proposals for these topics that are UNDERREPRESENTED in our current curriculum:

{topic_list}

Avoid duplicating these existing draft IDs/titles: {existing_note}

For EACH topic, return a JSON object with exactly these fields:
- "id": kebab-case slug (e.g. "ai-in-healthcare")
- "title": short, compelling course title (max 6 words)
- "modules": array of 8 module names (each max 6 words) — design a full 8-module course
- "synopsis": 2-sentence course description for a general audience
- "tier": "Beginner", "Intermediate", or "Advanced"
- "rationale": 1 sentence on why this gap matters for AI literacy

Return ONLY a JSON array of objects. No preamble, no markdown fences."""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.content[0].text.strip()
    raw = re.sub(r"^```json\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)

    drafts = json.loads(raw)
    print(f"Generated {len(drafts)} proposals.")
    return drafts


# ── SAVE DRAFTS ──────────────────────────────────────────────────────────────

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

        if filepath.exists():
            print(f"  Skipping (exists): {filename}")
            continue

        with open(filepath, "w") as f:
            json.dump(draft, f, indent=2)

        print(f"  Saved: {filename}")
        saved.append(filename)

    return saved


# ── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    print("=== AIP Research Agent ===")
    print(f"Run date: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}\n")

    gap_topics = find_corpus_gaps()
    drafts = generate_drafts(gap_topics)

    if drafts:
        saved = save_drafts(drafts)
        print(f"\nDone. {len(saved)} new draft(s) saved to aip/drafts/")
    else:
        print("\nNo new drafts generated this run.")


if __name__ == "__main__":
    main()
