"""
AIP Signal Collector — Google Trends
Queries Google Trends for rising AI-related topics.
Returns a list of signal dicts with topic, score, and source metadata.
"""

import time
from pytrends.request import TrendReq


# Seed queries — broad enough to catch emerging AI topics
SEED_QUERIES = [
    "AI education",
    "learn artificial intelligence",
    "AI skills",
    "AI tools",
    "AI course",
    "machine learning tutorial",
    "prompt engineering",
    "AI career",
    "AI certification",
    "generative AI",
]

# Model-specific seed queries — explicitly track demand around named models
MODEL_SEED_QUERIES = [
    "Claude AI",
    "ChatGPT",
    "GPT-4",
    "Gemini AI",
    "Llama AI",
    "Mistral AI",
    "how to use Claude",
    "how to use ChatGPT",
    "AI model comparison",
    "best AI model",
    "Claude vs ChatGPT",
    "open source AI models",
    "local AI model",
    "fine tuning AI model",
    "AI model for business",
    # Agentic frameworks — high demand, curriculum gap area
    "CrewAI tutorial",
    "LangGraph agent",
    "LangChain tutorial",
    "LlamaIndex RAG",
    "Flowise AI",
    "Dify AI platform",
    "n8n AI workflow",
    "AI agent framework",
    "OpenAI Agents SDK",
    "no code AI agent",
    "AI automation workflow",
    "Manus AI agent",
    "Semantic Kernel tutorial",
]

# Categories to scan for related rising queries
CATEGORY_SEEDS = [
    "artificial intelligence",
    "AI ethics",
    "AI healthcare",
    "AI business",
    "AI coding",
    "large language model",
    "AI model",
]


def collect_signals(max_signals=30):
    """Query Google Trends and return rising/trending AI topics."""
    print("  [Google Trends] Collecting signals...")
    pytrends = TrendReq(hl="en-US", tz=360, retries=3, backoff_factor=1.0)

    signals = []
    seen_topics = set()

    # Phase 1: Get related queries for each seed (general + model-specific)
    for seed in SEED_QUERIES + MODEL_SEED_QUERIES:
        try:
            pytrends.build_payload([seed], timeframe="today 3-m", geo="US")
            related = pytrends.related_queries()

            if seed in related:
                # Rising queries — these are the gold
                rising = related[seed].get("rising")
                if rising is not None and not rising.empty:
                    for _, row in rising.head(5).iterrows():
                        topic = row["query"].strip()
                        if topic.lower() not in seen_topics:
                            seen_topics.add(topic.lower())
                            signals.append({
                                "topic": topic,
                                "score": min(int(row.get("value", 0)), 10000),
                                "source": "google_trends",
                                "source_detail": f"rising query for '{seed}'",
                                "signal_type": "rising_query",
                            })

                # Top queries — popular but stable
                top = related[seed].get("top")
                if top is not None and not top.empty:
                    for _, row in top.head(3).iterrows():
                        topic = row["query"].strip()
                        if topic.lower() not in seen_topics:
                            seen_topics.add(topic.lower())
                            signals.append({
                                "topic": topic,
                                "score": int(row.get("value", 0)),
                                "source": "google_trends",
                                "source_detail": f"top query for '{seed}'",
                                "signal_type": "top_query",
                            })

            # Be polite — avoid rate limits
            time.sleep(2)

        except Exception as e:
            print(f"    Warning: seed '{seed}' failed: {e}")
            time.sleep(5)
            continue

    # Phase 2: Get related topics (broader concepts)
    for seed in CATEGORY_SEEDS:
        try:
            pytrends.build_payload([seed], timeframe="today 3-m", geo="US")
            related_topics = pytrends.related_topics()

            if seed in related_topics:
                rising = related_topics[seed].get("rising")
                if rising is not None and not rising.empty:
                    for _, row in rising.head(3).iterrows():
                        title = row.get("topic_title", "")
                        if title and title.lower() not in seen_topics:
                            seen_topics.add(title.lower())
                            signals.append({
                                "topic": title,
                                "score": min(int(row.get("value", 0)), 10000),
                                "source": "google_trends",
                                "source_detail": f"rising topic for '{seed}'",
                                "signal_type": "rising_topic",
                            })

            time.sleep(2)

        except Exception as e:
            print(f"    Warning: topic seed '{seed}' failed: {e}")
            time.sleep(5)
            continue

    # Sort by score descending, cap at max
    signals.sort(key=lambda x: x["score"], reverse=True)
    signals = signals[:max_signals]

    print(f"  [Google Trends] Collected {len(signals)} signals")
    return signals


if __name__ == "__main__":
    results = collect_signals()
    for s in results:
        print(f"  {s['score']:>6} | {s['topic']} ({s['signal_type']})")
