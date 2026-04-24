"""
Young Adult AIP Research Agent — AESOP Intelligence Pipeline
Runs weekly via GitHub Actions (+ manual dispatch).

Generates AI literacy course proposals for learners aged 17-25:
college students, first-job seekers, early-career professionals,
and curious young adults building skills outside the classroom.

Pipeline:
1. Collect signals from general trends (Google Trends + Reddit)
2. Claude synthesizes into YA-appropriate course topic candidates
3. Check Pinecone corpus for existing coverage
4. Generate full course proposals for genuine gaps
5. Save drafts to aip/ya-drafts/ with source attribution
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
from signals_google_trends import collect_signals as collect_trends
from signals_reddit import collect_signals as collect_reddit

# ── CONFIG ─────────────────────────────────────────────────────────────────────

ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
VOYAGE_API_KEY    = os.environ.get("VOYAGE_API_KEY", "")
PINECONE_API_KEY  = os.environ.get("PINECONE_API_KEY", "")
PINECONE_HOST     = os.environ.get("PINECONE_HOST", "")
PINECONE_INDEX    = "aesop-academy"
DRAFTS_DIR        = Path("aip/ya-drafts")
DRAFTS_PER_RUN    = 20
GAP_THRESHOLD     = 0.72

AUDIENCE    = "young-adult"
AGE_RANGE   = "17-25"
CATEGORY    = "Young Adult"


# ── PHASE 1: COLLECT SIGNALS ──────────────────────────────────────────────────

def collect_all_signals():
    print("Phase 1: Collecting signals for Young Adult pipeline\n")
    all_signals = []

    try:
        trends = collect_trends(max_signals=30)
        all_signals.extend(trends)
    except Exception as e:
        print(f"  WARNING: Google Trends collection failed: {e}")

    try:
        reddit = collect_reddit(max_signals=30)
        all_signals.extend(reddit)
    except Exception as e:
        print(f"  WARNING: Reddit collection failed: {e}")

    print(f"\n  Total raw signals collected: {len(all_signals)}")
    return all_signals


# ── PHASE 2: SYNTHESIZE WITH CLAUDE ───────────────────────────────────────────

def synthesize_topics(signals):
    print("\nPhase 2: Synthesizing signals into Young Adult course topics\n")

    if not signals:
        print("  No signals — falling back to static topics.")
        return _fallback_topics()

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    signal_text = ""
    for s in signals[:50]:
        source_tag = f"[{s['source']}]"
        signal_text += f"- {source_tag} {s['topic']} (score: {s['score']})\n"

    prompt = f"""You are a curriculum analyst for AESOP AI Academy — a free AI literacy platform.

I've collected real-world signals from Google Trends and Reddit showing what people are actively searching for and discussing about AI. Your job is to synthesize these into 25 COURSE TOPIC CANDIDATES specifically relevant to learners aged 17–25: college students, recent graduates, early-career workers, and young adults building skills independently.

RAW SIGNALS:
{signal_text}

LENS FOR YOUNG ADULTS (17-25):
Think about what THESE learners face:
- College coursework and studying with AI
- Internship and job hunting (AI for resumes, cover letters, interviews)
- Side hustles, freelancing, and making money with AI tools
- Creative work: music, art, writing, content creation
- Social media and the AI behind it
- First jobs — how AI is reshaping entry-level work
- Understanding and evaluating AI tools they use daily
- Building things without needing to code (no-code/AI tools)
- Privacy, data, and their digital footprint
- AI and relationships, social dynamics, identity online

RULES:
- Filter and reframe signals for a 17–25 audience — not corporate, not childlike
- Avoid purely enterprise/executive topics (those go in the Professional track)
- Avoid K-12-style topics (those go in the Youth track)
- Merge similar signals into a single coherent course topic
- Include high-demand model-specific topics (Claude, ChatGPT, etc.) framed for personal use
- For each topic, note which raw signals fed into it

Return a JSON array of 25 objects:
- "topic": clear course-worthy topic name (3-8 words)
- "signals": array of the original signal texts that fed into this topic
- "signal_sources": array of source names (e.g. ["google_trends", "reddit"])
- "demand_score": 1-10 estimated demand for this age group
- "is_model_topic": true if specifically about one or more named AI models

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
    return [
        {"topic": "AI for Your Job Search",        "signals": ["fallback"], "signal_sources": ["static"], "demand_score": 9, "is_model_topic": False},
        {"topic": "AI Tools for College Students",  "signals": ["fallback"], "signal_sources": ["static"], "demand_score": 8, "is_model_topic": False},
        {"topic": "Making Money With AI Side Hustles", "signals": ["fallback"], "signal_sources": ["static"], "demand_score": 8, "is_model_topic": False},
        {"topic": "AI and Your Creative Work",      "signals": ["fallback"], "signal_sources": ["static"], "demand_score": 7, "is_model_topic": False},
        {"topic": "What AI Really Knows About You", "signals": ["fallback"], "signal_sources": ["static"], "demand_score": 7, "is_model_topic": False},
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
        # Prepend YA context so embeddings reflect the audience framing
        vector = embed_query(f"Young adult AI literacy for ages {AGE_RANGE}: {topic}")

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
    print(f"\nPhase 4: Generating {min(len(gaps), DRAFTS_PER_RUN)} Young Adult course proposals\n")

    if not gaps:
        print("  No gaps found — skipping generation.")
        return []

    existing_ids = load_existing_draft_ids()
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    topics_to_draft = gaps[:DRAFTS_PER_RUN]
    topic_details = "\n".join(
        f"- {t['topic']} (demand: {t.get('demand_score','?')}/10, "
        f"corpus similarity: {t['corpus_score']:.2f}, "
        f"nearest existing: '{t['nearest_course']}', "
        f"signals from: {', '.join(t.get('signal_sources', ['unknown']))}"
        + (", ⚑ MODEL TOPIC" if t.get('is_model_topic') else "") + ")"
        for t in topics_to_draft
    )
    existing_note = ", ".join(list(existing_ids)[:20]) if existing_ids else "none yet"

    prompt = f"""You are a curriculum designer for AESOP AI Academy — a free AI literacy platform.

Generate {len(topics_to_draft)} course proposals for learners aged {AGE_RANGE}: college students, recent graduates, early-career workers, and young adults building skills on their own. These courses are UNDERREPRESENTED in the curriculum based on real demand signals.

{topic_details}

Avoid duplicating these existing draft IDs/titles: {existing_note}

DESIGN PRINCIPLES FOR YOUNG ADULT COURSES (17-25):
- Speak directly to the learner's actual situation: job searching, student life, side projects, creative work, first career steps
- Tone: smart and direct — not corporate, not childlike. Like a knowledgeable friend who tells you what you actually need to know
- Every course should answer: "What can I DO with this right now?"
- Include at least one module per course where learners apply the concept to their own life or work
- Avoid generic "AI overview" framing — be specific about the real skill or decision being taught
- Career and financial relevance is high for this audience — lean into it where appropriate

For EACH topic, return a JSON object with exactly these fields:
- "id": kebab-case slug (e.g. "ai-for-job-hunting")
- "title": short, compelling course title that a 20-year-old would want to click (max 6 words)
- "modules": array of 8 module names (each max 6 words) — design a full 8-module arc
- "synopsis": 2-sentence description written for the learner directly (use "you")
- "tier": "Beginner", "Intermediate", or "Advanced"
- "rationale": 1 sentence on why this gap matters for young adults' AI literacy
- "learning_outcome": 1 sentence — what can the learner DO after this course?

For topics marked ⚑ MODEL TOPIC, design courses around actually using the model to accomplish real goals — job search, creative work, studying, building things.

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
        draft["is_model_topic"]  = gap.get("is_model_topic", False) or draft.get("is_model_topic", False)

    return drafts


# ── PHASE 5: SAVE DRAFTS ──────────────────────────────────────────────────────

def save_drafts(drafts):
    DRAFTS_DIR.mkdir(parents=True, exist_ok=True)
    date_str = datetime.utcnow().strftime("%Y-%m-%d")
    saved = []

    for draft in drafts:
        draft["generated"]        = date_str
        draft["status"]           = "pending"
        draft["pipeline_version"] = "1.0-ya"
        draft["audience"]         = AUDIENCE     # "young-adult"
        draft["age_range"]        = AGE_RANGE    # "17-25"
        draft["category"]         = CATEGORY     # "Young Adult"

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
    print("Young Adult AIP Research Agent v1.0")
    print(f"Audience: Young Adults (ages {AGE_RANGE})")
    print("=" * 60)
    print(f"Run date: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}\n")

    signals    = collect_all_signals()
    candidates = synthesize_topics(signals)
    gaps       = check_gaps(candidates)
    drafts     = generate_drafts(gaps)

    if drafts:
        saved = save_drafts(drafts)
        print(f"\nDone. {len(saved)} new Young Adult draft(s) saved to {DRAFTS_DIR}/")
        print("\nDraft summary:")
        for d in drafts:
            sources = ", ".join(d.get("source_names", ["unknown"]))
            print(f"  {d['title']} | demand={d.get('demand_score','?')}/10 | src=[{sources}]")
    else:
        print("\nNo new Young Adult drafts generated this run.")


if __name__ == "__main__":
    main()
