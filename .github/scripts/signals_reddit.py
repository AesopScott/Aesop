"""
Multi-Source Community Signal Collector
Filename kept as signals_reddit.py for import compatibility.

Sources (all auth-free unless noted):
  - Hacker News      (Algolia search API)
  - GitHub           (repository search API, 60 req/hr unauthenticated)
  - Stack Overflow   (Stack Exchange API)
  - RSS feeds        (TechCrunch AI, VentureBeat, MIT Tech Review, The Verge AI)
  - Changelogs       (OpenAI, Google AI/Gemini, HuggingFace, Anthropic via Google News)
  - YouTube          (Data API v3 — requires YOUTUBE_API_KEY env var, optional)

Returns signal dicts identical in shape to the old Reddit signals so the
pipeline (aip_research_agent.py, ya_research_agent.py) needs no changes.
"""

import os
import re
import time
import requests
import xml.etree.ElementTree as ET

HEADERS = {
    "User-Agent": "AesopAcademy/1.0 (educational research bot; contact@aesopacademy.org)",
}

YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY", "").strip()

# ── HACKER NEWS ───────────────────────────────────────────────────────────────

HN_QUERIES = [
    "artificial intelligence",
    "machine learning",
    "large language model",
    "ChatGPT",
    "Claude AI",
    "AI agent",
    "prompt engineering",
    "RAG retrieval",
    "fine tuning LLM",
    "generative AI",
    "AI education",
    "LangChain",
    "open source AI",
    "AI automation workflow",
    "AI tools productivity",
]

# ── GITHUB TOPICS ─────────────────────────────────────────────────────────────

GITHUB_TOPICS = [
    "llm",
    "generative-ai",
    "artificial-intelligence",
    "langchain",
    "rag",
    "ai-agents",
    "prompt-engineering",
    "chatgpt",
    "machine-learning",
    "llm-applications",
]

# ── STACK OVERFLOW TAGS ───────────────────────────────────────────────────────

SO_TAGS = [
    "large-language-model",
    "langchain",
    "openai-api",
    "prompt-engineering",
    "chatgpt",
    "huggingface-transformers",
    "rag",
    "llm",
    "artificial-intelligence",
    "machine-learning",
]

# ── RSS FEEDS ─────────────────────────────────────────────────────────────────

RSS_FEEDS = [
    ("TechCrunch AI",   "https://techcrunch.com/category/artificial-intelligence/feed/"),
    ("VentureBeat AI",  "https://venturebeat.com/category/ai/feed/"),
    ("MIT Tech Review", "https://www.technologyreview.com/feed/"),
    ("The Verge AI",    "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml"),
]

# ── CHANGELOG / RELEASE FEEDS ─────────────────────────────────────────────────
# Direct RSS where available; Google News RSS for those without native feeds.

CHANGELOG_FEEDS = [
    # Native RSS feeds (verified working)
    ("OpenAI News",         "https://openai.com/news/rss.xml"),
    ("Google AI Blog",      "https://blog.google/technology/ai/rss/"),
    ("HuggingFace Blog",    "https://huggingface.co/blog/feed.xml"),
    # Google News RSS (captures Anthropic, Meta AI, Mistral, etc.)
    ("Anthropic News",      "https://news.google.com/rss/search?q=Anthropic+Claude+AI+announcement&hl=en-US&gl=US&ceid=US:en"),
    ("Meta AI News",        "https://news.google.com/rss/search?q=Meta+AI+Llama+release&hl=en-US&gl=US&ceid=US:en"),
    ("Mistral AI News",     "https://news.google.com/rss/search?q=Mistral+AI+model+release&hl=en-US&gl=US&ceid=US:en"),
    ("Microsoft Copilot",   "https://news.google.com/rss/search?q=Microsoft+Copilot+AI+update&hl=en-US&gl=US&ceid=US:en"),
]

# ── YOUTUBE SEARCH QUERIES ────────────────────────────────────────────────────
# Only used when YOUTUBE_API_KEY is set. Each query = 100 quota units.
# Free tier = 10,000 units/day → 100 searches/day. We use ~20/run.

YOUTUBE_QUERIES = [
    "how to use Claude AI tutorial",
    "ChatGPT tutorial for beginners 2025",
    "AI tools for work productivity",
    "LangChain tutorial 2025",
    "generative AI course free",
    "AI automation workflow tutorial",
    "prompt engineering course",
    "RAG tutorial large language model",
    "AI agent build tutorial",
    "Gemini AI tutorial Google",
    "GitHub Copilot tutorial",
    "AI for business professionals",
    "CrewAI tutorial multi agent",
    "n8n AI workflow automation",
    "Cursor AI coding tutorial",
    "Perplexity AI tutorial",
    "Microsoft Copilot tutorial",
    "Dify AI no code tutorial",
    "Flowise AI tutorial",
    "open source AI model tutorial",
]

# ── SCORING HELPERS ───────────────────────────────────────────────────────────

EDUCATION_SIGNALS = [
    "learn", "course", "tutorial", "how to", "beginner", "guide",
    "explain", "understand", "study", "career", "skill",
    "certification", "roadmap", "getting started", "introduction",
    "basics", "what is", "build", "create", "deploy", "implement",
]

AI_TERMS = [
    "ai", "artificial intelligence", "machine learning", "deep learning",
    "llm", "gpt", "claude", "neural", "nlp", "generative",
    "prompt", "model", "chatbot", "automation", "transformer",
    "agent", "rag", "fine-tun", "langchain", "embedding", "openai",
    "diffusion", "multimodal", "copilot", "gemini", "mistral",
]


def _is_ai_relevant(title):
    lower = title.lower()
    return any(t in lower for t in AI_TERMS)


def _edu_score(title):
    lower = title.lower()
    return sum(1 for s in EDUCATION_SIGNALS if s in lower)


def _dedup_key(title):
    return re.sub(r"[^a-z0-9]", "", title.lower())[:60]


# ── SOURCE COLLECTORS ─────────────────────────────────────────────────────────

def _collect_hn(max_per_query=8):
    signals = []
    seen = set()
    for query in HN_QUERIES:
        try:
            resp = requests.get(
                "https://hn.algolia.com/api/v1/search",
                params={"query": query, "tags": "story",
                        "numericFilters": "points>15", "hitsPerPage": max_per_query},
                headers=HEADERS, timeout=15,
            )
            if resp.status_code != 200:
                continue
            for hit in resp.json().get("hits", []):
                title = (hit.get("title") or "").strip()
                if not title or not _is_ai_relevant(title):
                    continue
                key = _dedup_key(title)
                if key in seen:
                    continue
                seen.add(key)
                pts = hit.get("points", 0) or 0
                cmts = hit.get("num_comments", 0) or 0
                signals.append({
                    "topic": title,
                    "score": pts + cmts * 3 + _edu_score(title) * 50,
                    "source": "hacker_news",
                    "source_detail": f"HN: {query}",
                    "signal_type": "community_discussion",
                    "metadata": {"points": pts, "comments": cmts,
                                 "url": hit.get("url", "")},
                })
            time.sleep(0.4)
        except Exception as e:
            print(f"    [HN] warning ({query}): {e}")
    print(f"    [HN] {len(signals)} raw signals")
    return signals


def _collect_github(max_per_topic=5):
    signals = []
    seen = set()
    for topic in GITHUB_TOPICS:
        try:
            resp = requests.get(
                "https://api.github.com/search/repositories",
                params={"q": f"topic:{topic} pushed:>2025-01-01",
                        "sort": "stars", "order": "desc", "per_page": max_per_topic},
                headers={**HEADERS, "Accept": "application/vnd.github+json"},
                timeout=15,
            )
            if resp.status_code != 200:
                continue
            for repo in resp.json().get("items", []):
                name = (repo.get("name") or "").replace("-", " ").replace("_", " ")
                desc = (repo.get("description") or "").strip()
                title = f"{name} — {desc}"[:120] if desc else name
                if not title or not _is_ai_relevant(title):
                    continue
                key = _dedup_key(name)
                if key in seen:
                    continue
                seen.add(key)
                stars = repo.get("stargazers_count", 0) or 0
                signals.append({
                    "topic": title,
                    "score": min(stars // 10, 500) + _edu_score(title) * 30,
                    "source": "github",
                    "source_detail": f"GitHub topic: {topic}",
                    "signal_type": "tool_adoption",
                    "metadata": {"stars": stars, "url": repo.get("html_url", "")},
                })
            time.sleep(1.2)  # unauthenticated: 60 req/hr
        except Exception as e:
            print(f"    [GitHub] warning ({topic}): {e}")
    print(f"    [GitHub] {len(signals)} raw signals")
    return signals


def _collect_stackoverflow(max_per_tag=10):
    signals = []
    seen = set()
    for tag in SO_TAGS:
        try:
            resp = requests.get(
                "https://api.stackexchange.com/2.3/questions",
                params={"order": "desc", "sort": "hot", "tagged": tag,
                        "site": "stackoverflow", "pagesize": max_per_tag},
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
                    "score": score * 5 + answers * 10 + min(views // 100, 200) + _edu_score(title) * 40,
                    "source": "stackoverflow",
                    "source_detail": f"SO tag: {tag}",
                    "signal_type": "learning_gap",
                    "metadata": {"score": score, "answers": answers, "views": views},
                })
            time.sleep(0.5)
        except Exception as e:
            print(f"    [SO] warning ({tag}): {e}")
    print(f"    [StackOverflow] {len(signals)} raw signals")
    return signals


def _collect_rss(max_per_feed=15):
    signals = []
    seen = set()
    for source_name, url in RSS_FEEDS:
        try:
            resp = requests.get(url, headers=HEADERS, timeout=15)
            if resp.status_code != 200:
                print(f"    [RSS] {source_name} returned {resp.status_code}")
                continue
            root = ET.fromstring(resp.content)
            items = root.findall(".//item")  # RSS 2.0
            if not items:
                ns = {"a": "http://www.w3.org/2005/Atom"}
                items = root.findall(".//a:entry", ns)  # Atom
            for item in items[:max_per_feed]:
                el = item.find("title")
                title = (el.text or "").strip() if el is not None else ""
                if not title or not _is_ai_relevant(title):
                    continue
                key = _dedup_key(title)
                if key in seen:
                    continue
                seen.add(key)
                signals.append({
                    "topic": title,
                    "score": 120 + _edu_score(title) * 40,
                    "source": "rss",
                    "source_detail": source_name,
                    "signal_type": "news",
                    "metadata": {"feed": source_name},
                })
        except Exception as e:
            print(f"    [RSS] {source_name} warning: {e}")
    print(f"    [RSS] {len(signals)} raw signals")
    return signals


# ── CHANGELOG COLLECTOR ───────────────────────────────────────────────────────

def _collect_changelogs(max_per_feed=20):
    """Collect signals from AI company release feeds and changelogs."""
    signals = []
    seen = set()
    for source_name, url in CHANGELOG_FEEDS:
        try:
            resp = requests.get(url, headers=HEADERS, timeout=15)
            if resp.status_code != 200:
                print(f"    [Changelog] {source_name} returned {resp.status_code}")
                continue
            root = ET.fromstring(resp.content)
            items = root.findall(".//item")
            if not items:
                ns = {"a": "http://www.w3.org/2005/Atom"}
                items = root.findall(".//a:entry", ns)
            for item in items[:max_per_feed]:
                el = item.find("title")
                title = (el.text or "").strip() if el is not None else ""
                if not title or not _is_ai_relevant(title):
                    continue
                key = _dedup_key(title)
                if key in seen:
                    continue
                seen.add(key)
                signals.append({
                    "topic": title,
                    "score": 200 + _edu_score(title) * 50,  # changelogs = high priority
                    "source": "changelog",
                    "source_detail": source_name,
                    "signal_type": "product_release",
                    "metadata": {"feed": source_name},
                })
        except Exception as e:
            print(f"    [Changelog] {source_name} warning: {e}")
    print(f"    [Changelog] {len(signals)} raw signals")
    return signals


# ── YOUTUBE COLLECTOR ─────────────────────────────────────────────────────────

def _collect_youtube(max_per_query=5):
    """
    Collect signals from YouTube tutorial searches via Data API v3.
    Skipped silently if YOUTUBE_API_KEY is not set.
    Each search query costs 100 quota units (10,000 free/day).
    """
    if not YOUTUBE_API_KEY:
        print("    [YouTube] YOUTUBE_API_KEY not set — skipping")
        return []

    signals = []
    seen = set()
    for query in YOUTUBE_QUERIES:
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
                    "maxResults": max_per_query,
                    "key": YOUTUBE_API_KEY,
                },
                timeout=15,
            )
            if resp.status_code != 200:
                print(f"    [YouTube] search '{query}' returned {resp.status_code}: {resp.text[:100]}")
                continue
            for item in resp.json().get("items", []):
                title = (item.get("snippet", {}).get("title") or "").strip()
                if not title or not _is_ai_relevant(title):
                    continue
                key = _dedup_key(title)
                if key in seen:
                    continue
                seen.add(key)
                signals.append({
                    "topic": title,
                    "score": 250 + _edu_score(title) * 60,  # YouTube = very high intent signal
                    "source": "youtube",
                    "source_detail": f"YouTube search: {query}",
                    "signal_type": "tutorial_demand",
                    "metadata": {
                        "video_id": item.get("id", {}).get("videoId", ""),
                        "channel": item.get("snippet", {}).get("channelTitle", ""),
                    },
                })
            time.sleep(0.3)
        except Exception as e:
            print(f"    [YouTube] warning ({query}): {e}")
    print(f"    [YouTube] {len(signals)} raw signals")
    return signals


# ── PUBLIC INTERFACE (unchanged from Reddit version) ─────────────────────────

def collect_signals(max_signals=30):
    """
    Collect AI community signals from HN, GitHub, Stack Overflow, and RSS.
    Drop-in replacement for the old Reddit collect_signals().
    """
    print("  [Multi-source] Collecting signals (HN + GitHub + SO + RSS + Changelogs + YouTube)...")

    all_signals = []
    all_signals.extend(_collect_hn())
    all_signals.extend(_collect_github())
    all_signals.extend(_collect_stackoverflow())
    all_signals.extend(_collect_rss())
    all_signals.extend(_collect_changelogs())
    all_signals.extend(_collect_youtube())

    # Global dedup across sources
    seen = set()
    deduped = []
    for s in all_signals:
        key = _dedup_key(s["topic"])
        if key not in seen:
            seen.add(key)
            deduped.append(s)

    deduped.sort(key=lambda x: x["score"], reverse=True)
    result = deduped[:max_signals]

    sources = {}
    for s in result:
        sources[s["source"]] = sources.get(s["source"], 0) + 1
    breakdown = ", ".join(f"{k}={v}" for k, v in sources.items())
    print(f"  [Multi-source] {len(result)} signals collected ({breakdown})")
    return result


if __name__ == "__main__":
    results = collect_signals(max_signals=50)
    for s in results:
        print(f"  {s['score']:>6} | {s['topic'][:80]} ({s['source_detail']})")
