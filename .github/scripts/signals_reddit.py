"""
Multi-Source Community Signal Collector
Filename kept as signals_reddit.py for import compatibility.

Reddit now requires formal API approval for programmatic access.
This module replaces Reddit with four open, auth-free alternatives:

  - Hacker News    (Algolia search API — no auth, no rate limits)
  - GitHub         (repository search API — no auth, 60 req/hr)
  - Stack Overflow (Stack Exchange API — no auth, generous free tier)
  - RSS feeds      (TechCrunch AI, VentureBeat, MIT Tech Review, The Verge AI)

Returns signal dicts identical in shape to the old Reddit signals so the
pipeline (aip_research_agent.py, ya_research_agent.py) needs no changes.
"""

import re
import time
import requests
import xml.etree.ElementTree as ET

HEADERS = {
    "User-Agent": "AesopAcademy/1.0 (educational research bot; contact@aesopacademy.org)",
}

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


# ── PUBLIC INTERFACE (unchanged from Reddit version) ─────────────────────────

def collect_signals(max_signals=30):
    """
    Collect AI community signals from HN, GitHub, Stack Overflow, and RSS.
    Drop-in replacement for the old Reddit collect_signals().
    """
    print("  [Multi-source] Collecting signals (HN + GitHub + SO + RSS)...")

    all_signals = []
    all_signals.extend(_collect_hn())
    all_signals.extend(_collect_github())
    all_signals.extend(_collect_stackoverflow())
    all_signals.extend(_collect_rss())

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
