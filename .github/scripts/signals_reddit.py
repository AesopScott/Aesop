"""
AIP Signal Collector — Reddit
Scrapes top/hot posts from AI-related subreddits using public JSON endpoints.
Returns a list of signal dicts with topic, score, and source metadata.
No API key required.
"""

import time
import re
import requests

# Subreddits to monitor — mix of learner, practitioner, and general interest
SUBREDDITS = [
    "artificial",
    "MachineLearning",
    "learnmachinelearning",
    "ChatGPT",
    "ClaudeAI",
    "LocalLLaMA",
    "singularity",
    "ArtificialInteligence",
    "deeplearning",
    "datascience",
]

# Timeframes: hot (trending now) + top of the month (sustained interest)
ENDPOINTS = [
    ("hot", ""),
    ("top", "?t=month"),
]

# Words that indicate educational/learning interest
EDUCATION_SIGNALS = [
    "learn", "course", "tutorial", "how to", "beginner", "guide",
    "explain", "understand", "study", "career", "job", "skill",
    "certification", "roadmap", "resource", "book", "free",
    "getting started", "introduction", "basics", "what is",
]

HEADERS = {
    "User-Agent": "AesopAcademy/1.0 (educational research bot; contact@aesopacademy.org)",
}


def _extract_ai_topics(title):
    """Check if a post title is relevant to AI education topics."""
    lower = title.lower()
    # Must mention AI/ML/LLM related terms
    ai_terms = ["ai", "artificial intelligence", "machine learning", "deep learning",
                 "llm", "gpt", "claude", "neural", "nlp", "computer vision",
                 "generative", "prompt", "model", "chatbot", "automation",
                 "transformer", "diffusion", "reinforcement learning"]
    has_ai = any(term in lower for term in ai_terms)
    if not has_ai:
        return None
    return title.strip()


def _score_educational_relevance(title):
    """Score how relevant a post is for educational content creation."""
    lower = title.lower()
    score = 0
    for signal in EDUCATION_SIGNALS:
        if signal in lower:
            score += 1
    return score


def collect_signals(max_signals=30):
    """Scrape Reddit for trending AI topics and questions."""
    print("  [Reddit] Collecting signals...")
    signals = []
    seen_titles = set()

    for subreddit in SUBREDDITS:
        for sort_type, params in ENDPOINTS:
            url = f"https://www.reddit.com/r/{subreddit}/{sort_type}.json{params}"
            if not params:
                url += "?limit=25"
            else:
                url += "&limit=25"

            try:
                resp = requests.get(url, headers=HEADERS, timeout=15)
                if resp.status_code != 200:
                    print(f"    Warning: r/{subreddit}/{sort_type} returned {resp.status_code}")
                    continue

                data = resp.json()
                posts = data.get("data", {}).get("children", [])

                for post in posts:
                    pdata = post.get("data", {})
                    title = pdata.get("title", "")
                    upvotes = pdata.get("ups", 0)
                    num_comments = pdata.get("num_comments", 0)
                    permalink = pdata.get("permalink", "")

                    # Filter for AI-relevant posts
                    topic = _extract_ai_topics(title)
                    if not topic:
                        continue

                    # Deduplicate
                    title_key = re.sub(r"[^a-z0-9]", "", title.lower())
                    if title_key in seen_titles:
                        continue
                    seen_titles.add(title_key)

                    # Score: engagement + educational relevance
                    engagement = upvotes + (num_comments * 3)
                    edu_bonus = _score_educational_relevance(title) * 50
                    total_score = engagement + edu_bonus

                    signals.append({
                        "topic": topic,
                        "score": total_score,
                        "source": "reddit",
                        "source_detail": f"r/{subreddit}/{sort_type}",
                        "signal_type": "community_discussion",
                        "metadata": {
                            "subreddit": subreddit,
                            "upvotes": upvotes,
                            "comments": num_comments,
                            "url": f"https://reddit.com{permalink}",
                        },
                    })

            except Exception as e:
                print(f"    Warning: r/{subreddit}/{sort_type} failed: {e}")
                continue

            # Be polite — Reddit rate limits unauthenticated requests
            time.sleep(2)

    # Sort by score descending, cap at max
    signals.sort(key=lambda x: x["score"], reverse=True)
    signals = signals[:max_signals]

    print(f"  [Reddit] Collected {len(signals)} signals")
    return signals


if __name__ == "__main__":
    results = collect_signals()
    for s in results:
        print(f"  {s['score']:>6} | {s['topic'][:80]} ({s['source_detail']})")
