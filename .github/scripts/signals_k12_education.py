"""
K-12 Education Signal Collector
Scrapes Reddit communities and Google Trends for AI education signals
specifically relevant to 8-16 year old learners and their teachers/parents.
Returns signal dicts with topic, score, and source metadata.
No API key required.
"""

import time
import re
import requests

# Education communities — teachers, parents, school technologists
SUBREDDITS = [
    "Teachers",
    "education",
    "EdTech",
    "CSEducation",
    "Parenting",
    "Homeschool",
    "ChatGPT",            # filter for school/kids posts
    "ArtificialIntelligence",  # filter for education posts
    "learnprogramming",   # school-age learners
    "teenagers",          # direct youth signal
    "Coding",
    "technology",
]

ENDPOINTS = [
    ("hot", ""),
    ("top", "?t=month"),
]

# Education-specific signal words
EDUCATION_SIGNALS = [
    "student", "students", "school", "classroom", "teacher", "kids", "children",
    "learn", "course", "curriculum", "lesson", "middle school", "high school",
    "elementary", "youth", "teen", "teenager", "grade", "homework", "project",
    "age-appropriate", "parent", "k-12", "k12", "education", "literacy",
    "digital citizenship", "critical thinking", "creative", "activity",
]

# AI topics appropriate for young learners
AI_EDUCATION_TERMS = [
    "ai", "artificial intelligence", "chatgpt", "claude", "chatbot",
    "machine learning", "algorithm", "data", "bias", "ethics",
    "prompt", "generative", "image generation", "coding", "programming",
    "robot", "automation", "deepfake", "misinformation", "digital",
]

HEADERS = {
    "User-Agent": "AesopAcademy/1.0 (K-12 education research; contact@aesopacademy.org)",
}


def _is_youth_education_relevant(title):
    """Check if a post is relevant to AI education for young learners."""
    lower = title.lower()
    has_ai = any(term in lower for term in AI_EDUCATION_TERMS)
    if not has_ai:
        return None
    return title.strip()


def _score_youth_relevance(title):
    """Score how relevant a post is for K-12 AI curriculum development."""
    lower = title.lower()
    score = 0
    for signal in EDUCATION_SIGNALS:
        if signal in lower:
            score += 2  # Education signals weighted higher than general pipeline
    return score


def collect_signals(max_signals=30):
    """Scrape Reddit for trending AI topics relevant to K-12 education."""
    print("  [Reddit K-12] Collecting signals...")
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

                    topic = _is_youth_education_relevant(title)
                    if not topic:
                        continue

                    title_key = re.sub(r"[^a-z0-9]", "", title.lower())
                    if title_key in seen_titles:
                        continue
                    seen_titles.add(title_key)

                    engagement = upvotes + (num_comments * 3)
                    edu_bonus = _score_youth_relevance(title) * 75  # higher weight than general pipeline
                    total_score = engagement + edu_bonus

                    signals.append({
                        "topic": topic,
                        "score": total_score,
                        "source": "reddit_k12",
                        "source_detail": f"r/{subreddit}/{sort_type}",
                        "signal_type": "k12_community_discussion",
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

            time.sleep(2)

    signals.sort(key=lambda x: x["score"], reverse=True)
    signals = signals[:max_signals]
    print(f"  [Reddit K-12] Collected {len(signals)} signals")
    return signals


def collect_trends_signals(max_signals=20):
    """Query Google Trends for K-12 AI education topics."""
    print("  [Google Trends K-12] Collecting signals...")
    try:
        from pytrends.request import TrendReq
    except ImportError:
        print("  [Google Trends K-12] pytrends not installed — skipping")
        return []

    SEED_QUERIES = [
        "AI for kids",
        "AI in schools",
        "teaching artificial intelligence",
        "AI curriculum K-12",
        "ChatGPT for students",
        "AI literacy children",
        "coding for kids AI",
        "digital citizenship AI",
        "AI ethics for teens",
        "AI tools for teachers",
        "AI middle school",
        "generative AI classroom",
    ]

    pytrends = TrendReq(hl="en-US", tz=360, retries=3, backoff_factor=1.0)
    signals = []
    seen = set()

    for seed in SEED_QUERIES:
        try:
            pytrends.build_payload([seed], timeframe="today 3-m", geo="US")
            related = pytrends.related_queries()

            if seed in related:
                rising = related[seed].get("rising")
                if rising is not None and not rising.empty:
                    for _, row in rising.head(5).iterrows():
                        topic = row["query"].strip()
                        if topic.lower() not in seen:
                            seen.add(topic.lower())
                            signals.append({
                                "topic": topic,
                                "score": min(int(row.get("value", 0)), 10000),
                                "source": "google_trends_k12",
                                "source_detail": f"rising query for '{seed}'",
                                "signal_type": "rising_k12_query",
                            })

            time.sleep(2)
        except Exception as e:
            print(f"    Warning: seed '{seed}' failed: {e}")
            time.sleep(5)
            continue

    signals.sort(key=lambda x: x["score"], reverse=True)
    signals = signals[:max_signals]
    print(f"  [Google Trends K-12] Collected {len(signals)} signals")
    return signals


if __name__ == "__main__":
    results = collect_signals()
    for s in results:
        print(f"  {s['score']:>6} | {s['topic'][:80]} ({s['source_detail']})")
