"""
K-12 AI Education Research Agent
Runs weekly via GitHub Actions (+ manual dispatch).

Equivalent to aip_research_agent.py but scoped exclusively to AI education
courses for learners aged 8-16. All drafts are tagged audience="youth".

Pipeline:
1. Collect signals from K-12 education communities (Reddit + Google Trends)
2. Use Claude to synthesize signals into youth-appropriate course topics
3. Check Pinecone corpus for existing coverage
4. Generate course proposals designed for 8-16 year old learners
5. Save drafts to aip/k12-drafts/ with full source attribution
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

sys.path.insert(0, str(Path(__file__).parent))
from signals_k12_education import collect_signals as collect_reddit_k12
from signals_k12_education import collect_trends_signals as collect_trends_k12

# ── CONFIG ─────────────────────────────────────────────────────────────────────

ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
VOYAGE_API_KEY    = os.environ.get("VOYAGE_API_KEY", "")
PINECONE_API_KEY  = os.environ.get("PINECONE_API_KEY", "")
PINECONE_HOST     = os.environ.get("PINECONE_HOST", "")
PINECONE_INDEX    = "aesop-academy"
DRAFTS_DIR        = Path("aip/k12-drafts")
DRAFTS_PER_RUN    = 20
GAP_THRESHOLD     = 0.72

AUDIENCE    = "youth"
AGE_RANGE   = "8-16"
CATEGORY    = "Youth"


# ── PHASE 1: COLLECT SIGNALS ──────────────────────────────────────────────────

def collect_all_signals():
    print("Phase 1: Collecting K-12 education signals\n")
    all_signals = []

    try:
        reddit = collect_reddit_k12(max_signals=30)
        all_signals.extend(reddit)
    except Exception as e:
        print(f"  WARNING: Reddit K-12 collection failed: {e}")

    try:
        trends = collect_trends_k12(max_signals=20)
        all_signals.extend(trends)
    except Exception as e:
        print(f"  WARNING: Google Trends K-12 collection failed: {e}")

    print(f"\n  Total raw signals collected: {len(all_signals)}")
    return all_signals


# ── PHASE 2: SYNTHESIZE WITH CLAUDE ───────────────────────────────────────────

def synthesize_topics(signals):
    print("\nPhase 2: Synthesizing signals into K-12 course topics\n")

    if not signals:
        print("  No signals — falling back to static topics.")
        return _fallback_topics()

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    signal_text = ""
    for s in signals[:50]:
        signal_text += f"- [{s['source']}] {s['topic']} (score: {s['score']})\n"

    prompt = f"""You are a curriculum analyst for AESOP AI Academy — a free AI literacy platform.

I've collected real-world signals from K-12 education communities (teachers, parents, students) showing what topics are most discussed and searched around AI education for young learners. Your job is to synthesize these into 25 distinct COURSE TOPIC CANDIDATES for an AI literacy curriculum aimed at students aged 8-16.

RAW SIGNALS:
{signal_text}

RULES:
- Each topic must be age-appropriate and meaningful for 8-16 year olds
- Topics should be genuinely educational — not just "AI is cool" but substantive skills and concepts
- Think in three age bands: 8-10 (foundational wonder), 11-13 (exploratory, creative), 14-16 (analytical, applied)
- Merge similar signals into a single coherent topic
- Include topics across: AI literacy, critical thinking about AI, creating with AI, AI ethics and safety, AI in everyday life, AI and careers, how AI works (age-appropriate), digital citizenship
- Avoid topics that are too advanced (transformer architecture, fine-tuning) or too vague ("AI for kids")
- For each topic, note which age band it fits best

Return a JSON array of 25 objects:
- "topic": clear course-worthy topic name (3-8 words)
- "age_band": "8-10", "11-13", or "14-16" — the primary target range
- "signals": array of the original signal texts that fed into this topic
- "signal_sources": array of source names
- "demand_score": 1-10 estimated demand based on signal strength
- "is_teacher_facing": true if the primary audience is teachers rather than students

Return ONLY the JSON array. No preamble, no markdown fences."""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.content[0].text.strip()
    raw = re.sub(r"^```json\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)

    candidates = json.loads(raw)
    print(f"  Synthesized {len(candidates)} candidate topics")
    return candidates


def _fallback_topics():
    return [
        {"topic": "How AI Actually Works", "age_band": "11-13", "signals": ["fallback"], "signal_sources": ["static"], "demand_score": 8},
        {"topic": "AI and Fake Information", "age_band": "11-13", "signals": ["fallback"], "signal_sources": ["static"], "demand_score": 8},
        {"topic": "Creating with AI Tools", "age_band": "14-16", "signals": ["fallback"], "signal_sources": ["static"], "demand_score": 7},
        {"topic": "AI Bias and Fairness", "age_band": "14-16", "signals": ["fallback"], "signal_sources": ["static"], "demand_score": 7},
        {"topic": "Talking to AI: Prompt Writing", "age_band": "8-10", "signals": ["fallback"], "signal_sources": ["static"], "demand_score": 7},
    ]


# ── PHASE 3: CHECK PINECONE FOR GAPS ──────────────────────────────────────────

def embed_query(text):
    if not VOYAGE_API_KEY:
        return None
    resp = requests.post(
        "https://api.voyageai.com/v1/embeddings",
        headers={"Authorization": f"Bearer {VOYAGE_API_KEY}", "content-type": "application/json"},
        json={"model": "voyage-3", "input": [text], "input_type": "query"},
        timeout=30,
    )
    if resp.status_code != 200:
        return None
    return resp.json()["data"][0]["embedding"]


def check_gaps(candidates):
    print("\nPhase 3: Checking corpus coverage via Pinecone\n")

    if not PINECONE_API_KEY or not PINECONE_HOST:
        print("  Pinecone not configured — treating all candidates as gaps")
        for c in candidates:
            c["corpus_score"] = 0.0
            c["nearest_course"] = "corpus_unavailable"
        return candidates

    pc = Pinecone(api_key=PINECONE_API_KEY)
    index = pc.Index(PINECONE_INDEX, host=PINECONE_HOST)
    stats = index.describe_index_stats()
    total_vectors = stats["total_vector_count"]
    print(f"  Corpus size: {total_vectors} vectors")

    if total_vectors == 0:
        for c in candidates:
            c["corpus_score"] = 0.0
            c["nearest_course"] = "none (empty corpus)"
        return candidates

    gaps = []
    for c in candidates:
        topic = c["topic"]
        # Prepend youth context so embeddings reflect the age-appropriate framing
        vector = embed_query(f"K-12 AI education for students ages {AGE_RANGE}: {topic}")

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
        print(f"  [{status}] {topic} ({c.get('age_band','?')}): score={top_score:.3f} → '{nearest}'")

        if top_score < GAP_THRESHOLD:
            gaps.append(c)

    gaps.sort(key=lambda x: (-x.get("demand_score", 0), x["corpus_score"]))
    print(f"\n  Found {len(gaps)} gaps out of {len(candidates)} candidates")
    return gaps


# ── PHASE 4: GENERATE PROPOSALS ───────────────────────────────────────────────

def load_existing_draft_ids():
    existing = set()
    if DRAFTS_DIR.exists():
        for f in DRAFTS_DIR.glob("*.json"):
            try:
                data = json.loads(f.read_text())
                if isinstance(data, dict):
                    existing.add(data.get("id", ""))
                    existing.add(data.get("title", "").lower())
            except Exception:
                continue
    return existing


def generate_drafts(gaps):
    print(f"\nPhase 4: Generating {min(len(gaps), DRAFTS_PER_RUN)} K-12 course proposals\n")

    if not gaps:
        print("  No gaps found — skipping generation.")
        return []

    existing_ids = load_existing_draft_ids()
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    topics_to_draft = gaps[:DRAFTS_PER_RUN]
    topic_details = "\n".join(
        f"- {t['topic']} (age band: {t.get('age_band','?')}, demand: {t.get('demand_score','?')}/10, "
        f"corpus similarity: {t['corpus_score']:.2f}, nearest existing: '{t['nearest_course']}')"
        for t in topics_to_draft
    )
    existing_note = ", ".join(list(existing_ids)[:20]) if existing_ids else "none yet"

    prompt = f"""You are a curriculum designer for AESOP AI Academy — a free AI literacy platform.

Your task: design {len(topics_to_draft)} complete course proposals for AI education aimed at students aged {AGE_RANGE}. These courses will be delivered through AESOP's story-driven engine, where learners make choices inside a narrative that teaches AI concepts through consequence and judgment — not just reading or watching.

TOPICS TO DEVELOP (with age bands and demand signals):
{topic_details}

Avoid duplicating these existing draft IDs/titles: {existing_note}

DESIGN PRINCIPLES FOR YOUTH COURSES:
- Learning happens through story, choice, and creation — not lecture
- Every module should include at least one moment where the learner decides something
- Age 8-10: concrete, playful, wonder-driven — "What is this thing? How does it help me?"
- Age 11-13: exploratory, questioning — "How does it really work? What can I make?"
- Age 14-16: analytical, critical, applied — "What are its limits? What are the risks? How do I use it well?"
- Each course exits with a creation or judgment artifact — something made or decided, not just learned
- Course titles should be direct and compelling for a young person, not academic-sounding

For EACH topic, return a JSON object with exactly these fields:
- "id": kebab-case slug (e.g. "ai-and-fake-news")
- "title": short, compelling title a student would want to click (max 6 words)
- "modules": array of 6 module names (each max 6 words) — design a focused 6-module arc
- "synopsis": 2-sentence description written for a student or their teacher
- "tier": "Beginner", "Intermediate", or "Advanced"
- "age_band": "8-10", "11-13", or "14-16"
- "rationale": 1 sentence on why this gap matters for youth AI literacy
- "learning_outcome": 1 sentence — what can the student DO after completing this course?

Return ONLY a JSON array of objects. No preamble, no markdown fences."""

    for attempt in range(4):
        try:
            response = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=5000,
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

    for draft, gap in zip(drafts, topics_to_draft):
        draft["source_signals"]  = gap.get("signals", [])
        draft["source_names"]    = gap.get("signal_sources", [])
        draft["demand_score"]    = gap.get("demand_score", 0)
        draft["corpus_score"]    = gap.get("corpus_score", 0)
        draft["nearest_existing"] = gap.get("nearest_course", "unknown")

    return drafts


# ── PHASE 5: SAVE DRAFTS ──────────────────────────────────────────────────────

def save_drafts(drafts):
    DRAFTS_DIR.mkdir(parents=True, exist_ok=True)
    date_str = datetime.utcnow().strftime("%Y-%m-%d")
    saved = []

    for draft in drafts:
        draft["generated"]        = date_str
        draft["status"]           = "pending"
        draft["pipeline_version"] = "1.0-k12"
        draft["audience"]         = AUDIENCE     # "youth"
        draft["age_range"]        = AGE_RANGE    # "8-16"
        draft["category"]         = CATEGORY     # "Youth"

        filename = f"{date_str}-{draft['id']}.json"
        filepath = DRAFTS_DIR / filename

        if filepath.exists():
            print(f"  Skipping (exists): {filename}")
            continue

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(draft, f, indent=2, ensure_ascii=False)

        print(f"  Saved: {filename}")
        saved.append(filename)

    return saved


# ── MAIN ──────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("K-12 AI Education Research Agent v1.0")
    print("Audience: Youth (ages 8-16)")
    print("=" * 60)
    print(f"Run date: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}\n")

    signals   = collect_all_signals()
    candidates = synthesize_topics(signals)
    gaps       = check_gaps(candidates)
    drafts     = generate_drafts(gaps)

    if drafts:
        saved = save_drafts(drafts)
        print(f"\nDone. {len(saved)} new K-12 draft(s) saved to {DRAFTS_DIR}/")
        print("\nDraft summary:")
        for d in drafts:
            sources = ", ".join(d.get("source_names", ["unknown"]))
            print(f"  [{d.get('age_band','?')}] {d['title']} | demand={d.get('demand_score','?')}/10 | src=[{sources}]")
    else:
        print("\nNo new K-12 drafts generated this run.")


if __name__ == "__main__":
    main()
