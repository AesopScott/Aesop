"""
AIP Research Agent — AESOP Intelligence Pipeline
Runs weekly via GitHub Actions (+ manual dispatch).

Pipeline:
1. Collect real-world signals from Google Trends + Reddit
2. Use Claude to synthesize signals into candidate topics
3. Check Pinecone corpus for existing coverage
4. Generate course proposals for genuine gaps
5. Save drafts with full source attribution

Every draft tracks WHERE the idea came from.
"""

import os
import sys
import json
import re
import time
from datetime import datetime
from pathlib import Path
import anthropic
import requests
from pinecone import Pinecone

# Add scripts dir to path for signal imports
sys.path.insert(0, str(Path(__file__).parent))
from signals_google_trends import collect_signals as collect_trends
from signals_reddit import collect_signals as collect_reddit

# ── CONFIG ────────────────────────────────────────────────────────────────────

ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
VOYAGE_API_KEY    = os.environ["VOYAGE_API_KEY"]
PINECONE_API_KEY  = os.environ["PINECONE_API_KEY"]
PINECONE_HOST     = os.environ["PINECONE_HOST"]
PINECONE_INDEX    = "aesop-academy"
DRAFTS_DIR        = Path("aip/drafts")
DRAFTS_PER_RUN    = 20
GAP_THRESHOLD     = 0.72


# ── PHASE 1: COLLECT SIGNALS ─────────────────────────────────────────────────

def collect_all_signals():
    """Gather signals from all sources."""
    print("Phase 1: Collecting real-world signals\n")

    all_signals = []

    # Google Trends
    try:
        trends = collect_trends(max_signals=30)
        all_signals.extend(trends)
    except Exception as e:
        print(f"  WARNING: Google Trends collection failed: {e}")

    # Reddit
    try:
        reddit = collect_reddit(max_signals=30)
        all_signals.extend(reddit)
    except Exception as e:
        print(f"  WARNING: Reddit collection failed: {e}")

    print(f"\n  Total raw signals collected: {len(all_signals)}")
    return all_signals


# ── PHASE 2: SYNTHESIZE WITH CLAUDE ──────────────────────────────────────────

def synthesize_topics(signals):
    """Use Claude to distill raw signals into candidate course topics."""
    print("\nPhase 2: Synthesizing signals into candidate topics\n")

    if not signals:
        print("  No signals to synthesize — falling back to static topics.")
        return _fallback_topics()

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    # Format signals for Claude
    signal_text = ""
    for s in signals[:50]:  # Cap context size
        source_tag = f"[{s['source']}]"
        signal_text += f"- {source_tag} {s['topic']} (score: {s['score']})\n"

    prompt = f"""You are a curriculum analyst for AESOP AI Academy — a free AI literacy platform.

I've collected real-world signals from Google Trends and Reddit showing what people are actively searching for and discussing about AI. Your job is to synthesize these into 25 distinct COURSE TOPIC CANDIDATES for an AI literacy curriculum.

RAW SIGNALS:
{signal_text}

RULES:
- Merge similar signals into a single coherent topic (e.g. "learn AI for business" + "AI tools for small business" → "AI for Small Business")
- Each topic should be specific enough for a focused course (not just "AI" or "machine learning")
- Topics should be educational/literacy focused — things a general audience would take a course on
- For each topic, list which signals it came from
- PAY SPECIAL ATTENTION to signals about specific AI models (Claude, GPT-4, Gemini, Llama, Mistral, Copilot, DeepSeek, Perplexity, etc.) — these are high-demand gaps. Propose model-specific or model-comparison courses when you see them (e.g. "Choosing the Right AI Model", "Getting the Most from Claude", "Open-Source AI Models Explained", "AI Model Benchmarks Demystified").

Return a JSON array of 25 objects:
- "topic": clear course-worthy topic name (3-8 words)
- "signals": array of the original signal texts that fed into this topic
- "signal_sources": array of source names (e.g. ["google_trends", "reddit"])
- "demand_score": 1-10 estimated demand based on signal strength
- "is_model_topic": true if this topic is specifically about one or more named AI models, false otherwise

Return ONLY the JSON array. No preamble, no markdown fences."""

    for attempt in range(4):
        try:
            response = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=4000,
                messages=[{"role": "user", "content": prompt}]
            )
            break
        except anthropic.APIStatusError as e:
            if e.status_code in (529, 500, 503):
                wait = 30 * (attempt + 1)
                print(f"  Anthropic API error {e.status_code} — retrying in {wait}s (attempt {attempt+1}/4)...")
                time.sleep(wait)
            else:
                raise
    else:
        raise RuntimeError("Anthropic API unavailable after 4 attempts — try again later.")

    raw = response.content[0].text.strip()
    raw = re.sub(r"^```json\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)

    candidates = json.loads(raw)
    print(f"  Synthesized {len(candidates)} candidate topics")
    return candidates


def _fallback_topics():
    """Static fallback if all signal sources fail."""
    return [
        {"topic": "AI in Healthcare", "signals": ["fallback"], "signal_sources": ["static"], "demand_score": 7},
        {"topic": "AI Ethics for Beginners", "signals": ["fallback"], "signal_sources": ["static"], "demand_score": 7},
        {"topic": "AI and Job Automation", "signals": ["fallback"], "signal_sources": ["static"], "demand_score": 6},
        {"topic": "AI Safety and Alignment", "signals": ["fallback"], "signal_sources": ["static"], "demand_score": 6},
        {"topic": "AI for Small Business", "signals": ["fallback"], "signal_sources": ["static"], "demand_score": 5},
    ]


# ── PHASE 3: CHECK PINECONE FOR GAPS ────────────────────────────────────────

def embed_query(text):
    """Embed a single query using Voyage-3."""
    resp = requests.post(
        "https://api.voyageai.com/v1/embeddings",
        headers={
            "Authorization": f"Bearer {VOYAGE_API_KEY}",
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
        print(f"    Embedding failed ({resp.status_code}): {resp.text[:200]}")
        return None
    return resp.json()["data"][0]["embedding"]


def check_gaps(candidates):
    """Check each candidate against Pinecone corpus — return real gaps."""
    print("\nPhase 3: Checking corpus coverage via Pinecone\n")

    pc = Pinecone(api_key=PINECONE_API_KEY)
    index = pc.Index(PINECONE_INDEX, host=PINECONE_HOST)
    stats = index.describe_index_stats()
    total_vectors = stats["total_vector_count"]
    print(f"  Corpus size: {total_vectors} vectors")

    if total_vectors == 0:
        print("  WARNING: Corpus is empty — all candidates are gaps by default")
        for c in candidates:
            c["corpus_score"] = 0.0
            c["nearest_course"] = "none (empty corpus)"
        return candidates

    gaps = []
    for c in candidates:
        topic = c["topic"]
        vector = embed_query(topic)

        if vector is None:
            c["corpus_score"] = 0.0
            c["nearest_course"] = "embedding_error"
            gaps.append(c)
            continue

        result = index.query(vector=vector, top_k=3, include_metadata=True)
        matches = result.get("matches", [])
        top_score = matches[0]["score"] if matches else 0.0
        nearest = matches[0].get("metadata", {}).get("title", "?") if matches else "none"

        c["corpus_score"] = round(top_score, 3)
        c["nearest_course"] = nearest

        status = "GAP" if top_score < GAP_THRESHOLD else "COVERED"
        print(f"  [{status}] {topic}: score={top_score:.3f} → '{nearest}'")

        if top_score < GAP_THRESHOLD:
            gaps.append(c)

    # Sort by demand (high) then corpus score (low = bigger gap)
    gaps.sort(key=lambda x: (-x.get("demand_score", 0), x["corpus_score"]))
    print(f"\n  Found {len(gaps)} gaps out of {len(candidates)} candidates")
    return gaps


# ── PHASE 4: GENERATE PROPOSALS ──────────────────────────────────────────────

def load_existing_draft_ids():
    """Get IDs of all existing drafts to avoid duplicates."""
    existing = set()
    if DRAFTS_DIR.exists():
        for f in DRAFTS_DIR.glob("*.json"):
            try:
                data = json.loads(f.read_text())
                existing.add(data.get("id", ""))
                existing.add(data.get("title", "").lower())
            except Exception:
                continue
    return existing


def generate_drafts(gaps):
    """Use Claude to generate full course proposals for top gaps."""
    print(f"\nPhase 4: Generating {min(len(gaps), DRAFTS_PER_RUN)} course proposals\n")

    if not gaps:
        print("  No gaps found — skipping generation.")
        return []

    existing_ids = load_existing_draft_ids()
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    topics_to_draft = gaps[:DRAFTS_PER_RUN]
    topic_details = "\n".join(
        f"- {t['topic']} (demand: {t.get('demand_score', '?')}/10, "
        f"corpus similarity: {t['corpus_score']:.2f}, "
        f"nearest existing: '{t['nearest_course']}', "
        f"signals from: {', '.join(t.get('signal_sources', ['unknown']))}"
        + (", ⚑ MODEL TOPIC" if t.get('is_model_topic') else "") + ")"
        for t in topics_to_draft
    )
    existing_note = ", ".join(list(existing_ids)[:20]) if existing_ids else "none yet"

    prompt = f"""You are a curriculum designer for AESOP AI Academy — a free AI literacy platform for students, educators, and curious adults.

Generate {len(topics_to_draft)} course proposals for these topics that are UNDERREPRESENTED in our curriculum, based on real-world demand signals:

{topic_details}

Avoid duplicating these existing draft IDs/titles: {existing_note}

For EACH topic, return a JSON object with exactly these fields:
- "id": kebab-case slug (e.g. "ai-in-healthcare")
- "title": short, compelling course title (max 6 words)
- "modules": array of 8 module names (each max 6 words) — design a full 8-module course
- "synopsis": 2-sentence course description for a general audience
- "tier": "Beginner", "Intermediate", or "Advanced"
- "rationale": 1 sentence on why this gap matters for AI literacy, referencing the demand signals
- "is_model_topic": true if the course is specifically about one or more named AI models or model selection/comparison

For topics marked ⚑ MODEL TOPIC, design courses that help learners understand, choose, and use specific AI models effectively — these are extremely high-demand right now.

Return ONLY a JSON array of objects. No preamble, no markdown fences."""

    for attempt in range(4):
        try:
            response = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=4000,
                messages=[{"role": "user", "content": prompt}]
            )
            break
        except anthropic.APIStatusError as e:
            if e.status_code in (529, 500, 503):
                wait = 30 * (attempt + 1)
                print(f"  Anthropic API error {e.status_code} — retrying in {wait}s (attempt {attempt+1}/4)...")
                time.sleep(wait)
            else:
                raise
    else:
        raise RuntimeError("Anthropic API unavailable after 4 attempts — try again later.")

    raw = response.content[0].text.strip()
    raw = re.sub(r"^```json\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)

    drafts = json.loads(raw)
    print(f"  Generated {len(drafts)} proposals")

    # Attach source tracking to each draft
    for draft, gap in zip(drafts, topics_to_draft):
        draft["source_signals"] = gap.get("signals", [])
        draft["source_names"] = gap.get("signal_sources", [])
        draft["demand_score"] = gap.get("demand_score", 0)
        draft["corpus_score"] = gap.get("corpus_score", 0)
        draft["nearest_existing"] = gap.get("nearest_course", "unknown")
        draft["is_model_topic"] = gap.get("is_model_topic", False) or draft.get("is_model_topic", False)

    return drafts


# ── PHASE 5: SAVE DRAFTS ────────────────────────────────────────────────────

def save_drafts(drafts):
    """Save each draft as a JSON file with full provenance."""
    DRAFTS_DIR.mkdir(parents=True, exist_ok=True)
    date_str = datetime.utcnow().strftime("%Y-%m-%d")
    saved = []

    for draft in drafts:
        draft["generated"] = date_str
        draft["status"] = "pending"
        draft["pipeline_version"] = "2.0"

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
    print("=" * 60)
    print("AIP Research Agent v2.0 — Signal-Driven Pipeline")
    print("=" * 60)
    print(f"Run date: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}\n")

    # 1. Collect real-world signals
    signals = collect_all_signals()

    # 2. Synthesize into candidate topics
    candidates = synthesize_topics(signals)

    # 3. Check Pinecone for coverage gaps
    gaps = check_gaps(candidates)

    # 4. Generate course proposals for real gaps
    drafts = generate_drafts(gaps)

    # 5. Save with source tracking
    if drafts:
        saved = save_drafts(drafts)
        print(f"\nDone. {len(saved)} new draft(s) saved to aip/drafts/")
        print("\nDraft source attribution:")
        for d in drafts:
            sources = ", ".join(d.get("source_names", ["unknown"]))
            print(f"  {d['title']}: sources=[{sources}], demand={d.get('demand_score', '?')}/10")
    else:
        print("\nNo new drafts generated this run.")


if __name__ == "__main__":
    main()
