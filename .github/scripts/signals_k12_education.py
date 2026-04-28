"""
K-12 Multi-Source Signal Collector
Collects AI education signals relevant to 8-16 year old learners, teachers,
and parents from open, auth-free sources:

  - Hacker News    (Algolia API — education/AI queries)
  - Stack Overflow (Stack Exchange API — CS education tags)
  - RSS feeds      (EdSurge, TechCrunch AI, MIT Tech Review)
  - Changelogs     (OpenAI, Google AI, Anthropic, etc. via RSS/Google News)
  - YouTube        (Data API v3 — requires YOUTUBE_API_KEY, optional)

Reddit replaced: Reddit now requires formal API approval.
Returns signal dicts with topic, score, and source metadata.
collect_trends_signals() (Google Trends) is unchanged below.
"""

import os
import re
import time
import requests
import xml.etree.ElementTree as ET

YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY", "").strip()

HEADERS = {
    "User-Agent": "AesopAcademy/1.0 (K-12 education research; contact@aesopacademy.org)",
}

HN_QUERIES_K12 = [
    "AI in schools",
    "AI education kids",
    "teaching artificial intelligence children",
    "ChatGPT students classroom",
    "AI literacy youth",
    "coding education AI",
    "K-12 AI curriculum",
    "EdTech AI tools",
    "AI ethics children",
    "digital citizenship AI",
]

SO_TAGS_K12 = [
    "computer-science-education",
    "scratch",
    "python-for-beginners",
    "teaching",
    "education",
    "machine-learning",
]

RSS_FEEDS_K12 = [
    ("EdSurge",         "https://edsurge.com/feed"),
    ("TechCrunch AI",   "https://techcrunch.com/category/artificial-intelligence/feed/"),
    ("MIT Tech Review", "https://www.technologyreview.com/feed/"),
]

# ── CHANGELOG / RELEASE FEEDS ────────────────────────────────────────────────
# AI company releases that affect tools kids/teachers actually use in classrooms

CHANGELOG_FEEDS_K12 = [
    ("OpenAI News",         "https://openai.com/news/rss.xml"),
    ("Google AI Blog",      "https://blog.google/technology/ai/rss/"),
    ("Khan Academy AI",     "https://news.google.com/rss/search?q=Khan+Academy+AI+Khanmigo+education&hl=en-US&gl=US&ceid=US:en"),
    ("Anthropic Education", "https://news.google.com/rss/search?q=Anthropic+Claude+education+students&hl=en-US&gl=US&ceid=US:en"),
    ("Google Classroom AI", "https://news.google.com/rss/search?q=Google+Classroom+AI+tools+teachers&hl=en-US&gl=US&ceid=US:en"),
    ("Microsoft Education", "https://news.google.com/rss/search?q=Microsoft+Copilot+education+students&hl=en-US&gl=US&ceid=US:en"),
    ("Scratch MIT News",    "https://news.google.com/rss/search?q=Scratch+MIT+coding+kids+AI&hl=en-US&gl=US&ceid=US:en"),
]

# ── YOUTUBE QUERIES (K-12 specific) ──────────────────────────────────────────
# Only used when YOUTUBE_API_KEY is set. Each query = 100 quota units.

YOUTUBE_QUERIES_K12 = [
    "AI for kids explained",
    "how does artificial intelligence work for children",
    "ChatGPT for students school",
    "coding for kids AI project",
    "teach AI to middle school students",
    "AI tools for teachers classroom",
    "machine learning kids tutorial",
    "Scratch AI coding kids",
    "digital citizenship AI teens",
    "AI ethics for high school",
    "how to use AI safely for students",
    "AI homework help students",
    "generative AI classroom activity",
    "AI bias explained kids",
    "computer science for beginners students",
]

# Education-specific signal words
EDUCATION_SIGNALS = [
    "student", "students", "school", "classroom", "teacher", "kids", "children",
    "learn", "course", "curriculum", "lesson", "middle school", "high school",
    "elementary", "youth", "teen", "teenager", "grade", "homework", "project",
    "age-appropriate", "parent", "k-12", "k12", "education", "literacy",
    "digital citizenship", "critical thinking", "creative", "activity",
]

AI_EDUCATION_TERMS = [
    "ai", "artificial intelligence", "chatgpt", "claude", "chatbot",
    "machine learning", "algorithm", "data", "bias", "ethics",
    "prompt", "generative", "image generation", "coding", "programming",
    "robot", "automation", "deepfake", "misinformation", "digital",
    "computer science", "scratch", "block coding",
]


def _is_youth_education_relevant(title):
    lower = title.lower()
    return any(term in lower for term in AI_EDUCATION_TERMS)


def _score_youth_relevance(title):
    lower = title.lower()
    return sum(2 for s in EDUCATION_SIGNALS if s in lower)


def _dedup_key(title):
    return re.sub(r"[^a-z0-9]", "", title.lower())[:60]


def _collect_hn_k12():
    signals = []
    seen = set()
    for query in HN_QUERIES_K12:
        try:
            resp = requests.get(
                "https://hn.algolia.com/api/v1/search",
                params={"query": query, "tags": "story",
                        "numericFilters": "points>10", "hitsPerPage": 8},
                headers=HEADERS, timeout=15,
            )
            if resp.status_code != 200:
                continue
            for hit in resp.json().get("hits", []):
                title = (hit.get("title") or "").strip()
                if not title or not _is_youth_education_relevant(title):
                    continue
                key = _dedup_key(title)
                if key in seen:
                    continue
                seen.add(key)
                pts = hit.get("points", 0) or 0
                cmts = hit.get("num_comments", 0) or 0
                signals.append({
                    "topic": title,
                    "score": pts + cmts * 3 + _score_youth_relevance(title) * 75,
                    "source": "hacker_news_k12",
                    "source_detail": f"HN: {query}",
                    "signal_type": "k12_community_discussion",
                    "metadata": {"points": pts, "comments": cmts},
                })
            time.sleep(0.4)
        except Exception as e:
            print(f"    [HN K-12] warning ({query}): {e}")
    print(f"    [HN K-12] {len(signals)} raw signals")
    return signals


def _collect_so_k12():
    signals = []
    seen = set()
    for tag in SO_TAGS_K12:
        try:
            resp = requests.get(
                "https://api.stackexchange.com/2.3/questions",
                params={"order": "desc", "sort": "hot", "tagged": tag,
                        "site": "stackoverflow", "pagesize": 10},
                headers=HEADERS, timeout=15,
            )
            if resp.status_code != 200:
                continue
            for q in resp.json().get("items", []):
                title = (q.get("title") or "").strip()
                if not title:
                    continue
                key = _dedup_key(title)
                if key in seen:
                    continue
                seen.add(key)
                score = q.get("score", 0) or 0
                answers = q.get("answer_count", 0) or 0
                views = q.get("view_count", 0) or 0
                signals.append({
                    "topic": title,
                    "score": score * 5 + answers * 10 + min(views // 100, 200) + _score_youth_relevance(title) * 40,
                    "source": "stackoverflow_k12",
                    "source_detail": f"SO tag: {tag}",
                    "signal_type": "k12_learning_gap",
                    "metadata": {"score": score, "answers": answers, "views": views},
                })
            time.sleep(0.5)
        except Exception as e:
            print(f"    [SO K-12] warning ({tag}): {e}")
    print(f"    [SO K-12] {len(signals)} raw signals")
    return signals


def _collect_rss_k12():
    signals = []
    seen = set()
    for source_name, url in RSS_FEEDS_K12:
        try:
            resp = requests.get(url, headers=HEADERS, timeout=15)
            if resp.status_code != 200:
                continue
            root = ET.fromstring(resp.content)
            items = root.findall(".//item")
            if not items:
                ns = {"a": "http://www.w3.org/2005/Atom"}
                items = root.findall(".//a:entry", ns)
            for item in items[:15]:
                el = item.find("title")
                title = (el.text or "").strip() if el is not None else ""
                if not title or not _is_youth_education_relevant(title):
                    continue
                key = _dedup_key(title)
                if key in seen:
                    continue
                seen.add(key)
                signals.append({
                    "topic": title,
                    "score": 120 + _score_youth_relevance(title) * 50,
                    "source": "rss_k12",
                    "source_detail": source_name,
                    "signal_type": "k12_news",
                    "metadata": {"feed": source_name},
                })
        except Exception as e:
            print(f"    [RSS K-12] {source_name} warning: {e}")
    print(f"    [RSS K-12] {len(signals)} raw signals")
    return signals


def _collect_changelogs_k12():
    """Collect K-12-relevant AI product releases from changelog/news RSS feeds."""
    signals = []
    seen = set()
    for source_name, url in CHANGELOG_FEEDS_K12:
        try:
            resp = requests.get(url, headers=HEADERS, timeout=15)
            if resp.status_code != 200:
                print(f"    [Changelog K-12] {source_name} returned {resp.status_code}")
                continue
            root = ET.fromstring(resp.content)
            items = root.findall(".//item")
            if not items:
                ns = {"a": "http://www.w3.org/2005/Atom"}
                items = root.findall(".//a:entry", ns)
            for item in items[:20]:
                el = item.find("title")
                title = (el.text or "").strip() if el is not None else ""
                if not title or not _is_youth_education_relevant(title):
                    continue
                key = _dedup_key(title)
                if key in seen:
                    continue
                seen.add(key)
                signals.append({
                    "topic": title,
                    "score": 200 + _score_youth_relevance(title) * 50,
                    "source": "changelog_k12",
                    "source_detail": source_name,
                    "signal_type": "k12_product_release",
                    "metadata": {"feed": source_name},
                })
        except Exception as e:
            print(f"    [Changelog K-12] {source_name} warning: {e}")
    print(f"    [Changelog K-12] {len(signals)} raw signals")
    return signals


def _collect_youtube_k12():
    """
    Collect K-12 AI education signals from YouTube tutorial searches.
    Skipped silently if YOUTUBE_API_KEY is not set.
    Each search query costs 100 quota units (10,000 free/day).
    """
    if not YOUTUBE_API_KEY:
        print("    [YouTube K-12] YOUTUBE_API_KEY not set — skipping")
        return []

    signals = []
    seen = set()
    for query in YOUTUBE_QUERIES_K12:
        try:
            resp = requests.get(
                "https://www.googleapis.com/youtube/v3/search",
                params={
                    "part": "snippet",
                    "q": query,
                    "type": "video",
                    "order": "viewCount",
                    "relevanceLanguage": "en",
                    "publishedAfter": "2024-01-01T00:00:00Z",
                    "maxResults": 5,
                    "key": YOUTUBE_API_KEY,
                },
                timeout=15,
            )
            if resp.status_code != 200:
                print(f"    [YouTube K-12] search '{query}' returned {resp.status_code}: {resp.text[:100]}")
                continue
            for item in resp.json().get("items", []):
                title = (item.get("snippet", {}).get("title") or "").strip()
                if not title or not _is_youth_education_relevant(title):
                    continue
                key = _dedup_key(title)
                if key in seen:
                    continue
                seen.add(key)
                signals.append({
                    "topic": title,
                    "score": 250 + _score_youth_relevance(title) * 60,
                    "source": "youtube_k12",
                    "source_detail": f"YouTube search: {query}",
                    "signal_type": "k12_tutorial_demand",
                    "metadata": {
                        "video_id": item.get("id", {}).get("videoId", ""),
                        "channel": item.get("snippet", {}).get("channelTitle", ""),
                    },
                })
            time.sleep(0.3)
        except Exception as e:
            print(f"    [YouTube K-12] warning ({query}): {e}")
    print(f"    [YouTube K-12] {len(signals)} raw signals")
    return signals


def collect_signals(max_signals=30):
    """Collect K-12 AI education signals from HN, Stack Overflow, RSS, Changelogs, and YouTube."""
    print("  [Multi-source K-12] Collecting signals (HN + SO + RSS + Changelogs + YouTube)...")

    all_signals = []
    all_signals.extend(_collect_hn_k12())
    all_signals.extend(_collect_so_k12())
    all_signals.extend(_collect_rss_k12())
    all_signals.extend(_collect_changelogs_k12())
    all_signals.extend(_collect_youtube_k12())

    seen = set()
    deduped = []
    for s in all_signals:
        key = _dedup_key(s["topic"])
        if key not in seen:
            seen.add(key)
            deduped.append(s)

    deduped.sort(key=lambda x: x["score"], reverse=True)
    result = deduped[:max_signals]
    print(f"  [Multi-source K-12] {len(result)} signals collected")
    return result


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
