#!/usr/bin/env python3
"""
Generate standalone shareable HTML pages from ai-news JSON articles.
Run from repo root:  python3 ai-news/build-articles.py
"""
import json, os, html as ht

ARTICLES_DIR = os.path.join(os.path.dirname(__file__), 'articles')
OUTPUT_DIR   = ARTICLES_DIR  # HTML lives next to JSON
INDEX_HTML   = os.path.join(os.path.dirname(__file__), 'index.html')
INDEX_JSON   = os.path.join(os.path.dirname(__file__), 'articles-index.json')
FEED_START   = '<!-- SEO:STATIC-FEED-START -->'
FEED_END     = '<!-- SEO:STATIC-FEED-END -->'

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} &mdash; AESOP AI News</title>
<meta name="description" content="{subtitle}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://aesopacademy.org/ai-news/articles/{slug}.html">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon_16.png">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon_32.png">
<link rel="apple-touch-icon" sizes="512x512" href="/favicon_512.png">

<!-- Open Graph -->
<meta property="og:title" content="{title}">
<meta property="og:description" content="{subtitle}">
<meta property="og:url" content="https://aesopacademy.org/ai-news/articles/{slug}.html">
<meta property="og:site_name" content="AESOP AI Academy">
<meta property="og:type" content="article">
<meta property="og:image" content="https://aesopacademy.org/ai-news/og-news.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="article:published_time" content="{date}T12:00:00Z">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{subtitle}">
<meta name="twitter:image" content="https://aesopacademy.org/ai-news/og-news.jpg">

<!-- JSON-LD -->
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "NewsArticle",
  "headline": "{title_json}",
  "description": "{subtitle_json}",
  "datePublished": "{date}T12:00:00Z",
  "author": {{
    "@type": "Organization",
    "name": "AESOP AI Academy"
  }},
  "publisher": {{
    "@type": "Organization",
    "name": "AESOP AI Academy",
    "url": "https://aesopacademy.org"
  }},
  "mainEntityOfPage": "https://aesopacademy.org/ai-news/articles/{slug}.html"
}}
</script>

<!-- Firebase Analytics -->
<script type="module">
  import {{ initializeApp }} from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";
  import {{ getAnalytics }} from "https://www.gstatic.com/firebasejs/10.7.1/firebase-analytics.js";
  const app = initializeApp({{
    apiKey: "AIzaSyBvZQFNL-zThgCcpFuMEVXFd9G6MVQcVjo",
    authDomain: "playagame-f733d.firebaseapp.com",
    projectId: "playagame-f733d",
    storageBucket: "playagame-f733d.appspot.com",
    messagingSenderId: "610508714644",
    appId: "1:610508714644:web:63ca4374e5d5be1c81ba81",
    measurementId: "G-PYZX7EJ51J"
  }});
  getAnalytics(app);
</script>

<link rel="stylesheet" href="/academy-theme.css">
<link rel="stylesheet" href="/academy-dark-mode.css">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;0,900;1,400;1,600&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,300;1,9..40,400&display=swap" rel="stylesheet">

<style>
.article-page {{
  max-width: clamp(600px, 66vw, 900px);
  margin: 0 auto;
  padding: 2.5rem 2rem 4rem;
}}
.article-back {{
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  font-family: var(--font-body);
  font-size: 0.82rem;
  font-weight: 500;
  color: var(--ink-muted);
  text-decoration: none;
  margin-bottom: 2rem;
  transition: color var(--transition);
}}
.article-back:hover {{ color: var(--gold); }}
.article-emoji {{
  font-size: 2.8rem;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 64px;
  height: 64px;
  background: var(--cream);
  border-radius: var(--radius-md);
  border: 1px solid var(--border-light);
}}
[data-theme="dark"] .article-emoji {{
  background: rgba(255,255,255,0.04);
  border-color: var(--border);
}}
.article-meta {{
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
  margin-bottom: 1rem;
}}
.article-category {{
  font-size: 0.72rem;
  font-weight: 600;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--teal-dark);
  background: rgba(61,214,192,0.1);
  padding: 0.2rem 0.6rem;
  border-radius: 100px;
}}
[data-theme="dark"] .article-category {{
  background: rgba(61,214,192,0.12);
  color: var(--teal);
}}
.article-date, .article-readtime {{
  font-size: 0.82rem;
  color: var(--ink-muted);
}}
.article-dot {{
  width: 3px; height: 3px;
  border-radius: 50%;
  background: var(--border);
}}
.article-page h1 {{
  font-family: var(--font-display);
  font-size: 2rem;
  font-weight: 700;
  color: var(--ink);
  line-height: 1.25;
  margin-bottom: 0.75rem;
}}
.article-subtitle {{
  font-size: 1.1rem;
  color: var(--ink-light);
  line-height: 1.55;
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid var(--border-light);
}}
[data-theme="dark"] .article-subtitle {{
  border-bottom-color: var(--border);
}}
.article-body p {{
  font-size: 1rem;
  color: var(--ink-mid);
  line-height: 1.8;
  margin-bottom: 1.25rem;
}}
.article-tags {{
  display: flex;
  gap: 0.4rem;
  flex-wrap: wrap;
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--border-light);
}}
[data-theme="dark"] .article-tags {{
  border-top-color: var(--border);
}}
.article-tag {{
  font-size: 0.72rem;
  font-weight: 500;
  color: var(--ink-muted);
  background: var(--cream);
  padding: 0.2rem 0.6rem;
  border-radius: 100px;
  border: 1px solid var(--border-light);
}}
[data-theme="dark"] .article-tag {{
  background: rgba(255,255,255,0.05);
  border-color: var(--border);
}}
.article-sources {{
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid var(--border-light);
}}
[data-theme="dark"] .article-sources {{
  border-top-color: var(--border);
}}
.article-sources-label {{
  font-size: 0.72rem;
  font-weight: 600;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--ink-muted);
  margin-bottom: 0.5rem;
}}
.article-source-link {{
  display: block;
  font-size: 0.85rem;
  color: var(--teal-dark);
  margin-bottom: 0.3rem;
  transition: color var(--transition);
}}
.article-source-link:hover {{ color: var(--gold); }}
[data-theme="dark"] .article-source-link {{ color: var(--teal); }}
[data-theme="dark"] .article-source-link:hover {{ color: var(--gold-light); }}
.article-share {{
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--border-light);
  display: flex;
  align-items: center;
  gap: 0.75rem;
}}
[data-theme="dark"] .article-share {{
  border-top-color: var(--border);
}}
.article-share-label {{
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--ink-muted);
}}
.article-share-btn {{
  font-family: var(--font-body);
  font-size: 0.78rem;
  font-weight: 500;
  padding: 0.35rem 0.85rem;
  border-radius: 100px;
  border: 1.5px solid var(--border);
  background: var(--white);
  color: var(--ink-light);
  cursor: pointer;
  transition: all var(--transition);
}}
.article-share-btn:hover {{
  border-color: var(--gold);
  color: var(--ink);
}}
.article-share-btn.copied {{
  border-color: var(--teal);
  color: var(--teal-dark);
}}
@media (max-width: 768px) {{
  .article-page {{ padding: 1.5rem 1.25rem 3rem; }}
  .article-page h1 {{ font-size: 1.5rem; }}
  .article-emoji {{ font-size: 2rem; width: 48px; height: 48px; }}
}}
</style>
</head>
<body>

<nav class="nav" role="navigation">
  <div class="nav-inner">
    <div class="nav-brand-group">
      <a href="https://aesopacademy.org" class="nav-brand-primary">AESOP AI Academy</a>
      <div class="nav-divider"></div>
      <a href="/ai-news/" class="nav-brand-secondary">AI News</a>
    </div>
    <button class="nav-hamburger" id="navHamburger" aria-label="Open menu" aria-expanded="false">&#9776;</button>
    <div class="nav-links" id="navLinks">
      <a href="/ai-academy/courses.html" class="nav-link">Courses</a>
      <a href="https://discord.gg/pKDa5ryX" target="_blank" rel="noopener" class="nav-btn nav-btn--forums">Forums</a>
      <button class="dark-mode-toggle" id="darkToggle" aria-label="Toggle dark mode">
        <span class="dark-mode-toggle__icon">&#9728;&#65039;</span>
        <span class="dark-mode-toggle__track"><span class="dark-mode-toggle__thumb"></span></span>
        <span class="dark-mode-toggle__icon">&#127769;</span>
      </button>
    </div>
  </div>
</nav>

<main class="article-page">
  <a href="/ai-news/" class="article-back">&larr; All Articles</a>

  <div class="article-emoji">{heroEmoji}</div>

  <div class="article-meta">
    <span class="article-category">{category}</span>
    <span class="article-dot"></span>
    <span class="article-date">{date_display}</span>
    <span class="article-dot"></span>
    <span class="article-readtime">{readTime}</span>
  </div>

  <h1>{title}</h1>
  <p class="article-subtitle">{subtitle}</p>

  <div class="article-body">
    {body_html}
  </div>

  {tags_html}
  {sources_html}

  <div class="article-share">
    <span class="article-share-label">Share:</span>
    <button class="article-share-btn" onclick="copyLink(this)">Copy link</button>
    <a class="article-share-btn" href="https://twitter.com/intent/tweet?text={title_encoded}&url=https://aesopacademy.org/ai-news/articles/{slug}.html" target="_blank" rel="noopener">X / Twitter</a>
    <a class="article-share-btn" href="https://www.linkedin.com/sharing/share-offsite/?url=https://aesopacademy.org/ai-news/articles/{slug}.html" target="_blank" rel="noopener">LinkedIn</a>
  </div>
</main>

<footer class="news-footer" style="max-width:740px;margin:0 auto;padding:2rem;text-align:center;border-top:1px solid var(--border-light);">
  <p style="font-size:0.82rem;color:var(--ink-muted);line-height:1.6;">
    Articles are sourced from leading AI publications, then rewritten by AESOP's AI engine for clarity and accessibility. Original sources are always cited.<br>
    <a href="/ai-news/" style="color:var(--teal-dark);font-weight:500;">&larr; Back to AI News</a>
  </p>
</footer>

<script>
(function() {{
  'use strict';
  const toggle = document.getElementById('darkToggle');
  const html = document.documentElement;
  const saved = localStorage.getItem('aesop-theme');
  if (saved === 'dark' || (!saved && window.matchMedia('(prefers-color-scheme: dark)').matches)) {{
    html.setAttribute('data-theme', 'dark');
  }}
  if (toggle) {{
    toggle.addEventListener('click', () => {{
      const next = html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      html.setAttribute('data-theme', next);
      localStorage.setItem('aesop-theme', next);
    }});
  }}
  const hamburger = document.getElementById('navHamburger');
  const navLinks = document.getElementById('navLinks');
  if (hamburger && navLinks) {{
    hamburger.addEventListener('click', () => {{
      const open = navLinks.classList.toggle('nav-open');
      hamburger.setAttribute('aria-expanded', open);
    }});
  }}
}})();
function copyLink(btn) {{
  navigator.clipboard.writeText(window.location.href).then(() => {{
    btn.textContent = 'Copied!';
    btn.classList.add('copied');
    setTimeout(() => {{ btn.textContent = 'Copy link'; btn.classList.remove('copied'); }}, 2000);
  }});
}}
</script>
</body>
</html>"""

def esc(s):
    return ht.escape(str(s))

def format_date_long(date_str):
    from datetime import datetime
    d = datetime.strptime(date_str, '%Y-%m-%d')
    return d.strftime('%A, %B ') + str(d.day) + d.strftime(', %Y')

def build_card_html(article):
    slug = article['id']
    article_url = f'/ai-news/articles/{slug}.html'
    body_html = ''.join(f'<p>{esc(p)}</p>' for p in article.get('body', []))
    tags = article.get('tags', [])
    tags_html = ''
    if tags:
        tags_html = '<div class="news-card-tags">' + ''.join(f'<span class="news-card-tag">{esc(t)}</span>' for t in tags) + '</div>'
    sources = article.get('sources', [])
    sources_html = ''
    if sources:
        links = ''.join(f'<a href="{esc(s["url"])}" target="_blank" rel="noopener" class="news-card-source-link">{esc(s["title"])}</a>' for s in sources)
        sources_html = f'<div class="news-card-sources"><div class="news-card-sources-label">Sources</div>{links}</div>'
    return (
        f'<article class="news-card" data-id="{slug}">'
        f'<div class="news-card-header">'
        f'<div class="news-card-emoji">{article.get("heroEmoji", "📰")}</div>'
        f'<div>'
        f'<div class="news-card-meta">'
        f'<span class="news-card-category">{esc(article.get("category", "General"))}</span>'
        f'<span class="news-card-dot"></span>'
        f'<span class="news-card-readtime">{esc(article.get("readTime", "3 min read"))}</span>'
        f'</div>'
        f'<h2>{esc(article.get("title", "Untitled"))}</h2>'
        f'<p class="news-card-subtitle">{esc(article.get("subtitle", ""))}</p>'
        f'</div>'
        f'</div>'
        f'<div class="news-card-expand">'
        f'<span class="expand-text">Read full article</span>'
        f'<span class="collapse-text">Collapse</span>'
        f'<span class="news-card-expand-arrow">▾</span>'
        f'<a href="{article_url}" class="news-card-share" title="Open shareable link">Share ↗</a>'
        f'</div>'
        f'<div class="news-card-body">{body_html}{tags_html}{sources_html}</div>'
        f'</article>'
    )

def build_index():
    if not os.path.exists(INDEX_JSON):
        print('  WARNING: articles-index.json not found, skipping index build.')
        return
    with open(INDEX_JSON, 'r', encoding='utf-8') as f:
        index = json.load(f)

    base = os.path.dirname(__file__)
    articles = []
    for rel_path in index.get('articles', []):
        json_path = os.path.join(base, rel_path)
        if not os.path.exists(json_path):
            continue
        with open(json_path, 'r', encoding='utf-8') as f:
            articles.append(json.load(f))

    articles.sort(key=lambda a: a.get('date', ''), reverse=True)

    by_date = {}
    for article in articles:
        by_date.setdefault(article.get('date', 'unknown'), []).append(article)

    html_parts = ['\n']
    for date in sorted(by_date.keys(), reverse=True):
        items = by_date[date]
        count_label = f'{len(items)} article' if len(items) == 1 else f'{len(items)} articles'
        cards = ''.join(build_card_html(a) for a in items)
        html_parts.append(
            f'<section class="news-day">'
            f'<div class="news-day-header">'
            f'<span class="news-day-header-date">{format_date_long(date)}</span>'
            f'<span class="news-day-header-count">{count_label}</span>'
            f'</div>'
            f'<div class="news-day-row">{cards}</div>'
            f'</section>\n'
        )
    html_parts.append('')

    with open(INDEX_HTML, 'r', encoding='utf-8') as f:
        content = f.read()

    if FEED_START not in content or FEED_END not in content:
        print('  ERROR: SEO feed markers not found in index.html — skipping.')
        return

    before = content[:content.index(FEED_START) + len(FEED_START)]
    after  = content[content.index(FEED_END):]
    with open(INDEX_HTML, 'w', encoding='utf-8') as f:
        f.write(before + ''.join(html_parts) + after)

    print(f'  Pre-rendered {len(articles)} articles across {len(by_date)} days into index.html.')

def url_encode(s):
    import urllib.parse
    return urllib.parse.quote(str(s), safe='')

def format_date(date_str):
    from datetime import datetime
    d = datetime.strptime(date_str, '%Y-%m-%d')
    return d.strftime('%B %d, %Y')

def build_article(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        article = json.load(f)

    slug = article['id']
    body_html = '\n    '.join(f'<p>{esc(p)}</p>' for p in article.get('body', []))

    tags = article.get('tags', [])
    tags_html = ''
    if tags:
        tag_spans = ''.join(f'<span class="article-tag">{esc(t)}</span>' for t in tags)
        tags_html = f'<div class="article-tags">{tag_spans}</div>'

    sources = article.get('sources', [])
    sources_html = ''
    if sources:
        links = ''.join(
            f'<a href="{esc(s["url"])}" target="_blank" rel="noopener" class="article-source-link">&rarr; {esc(s["title"])}</a>'
            for s in sources
        )
        sources_html = f'<div class="article-sources"><div class="article-sources-label">Sources</div>{links}</div>'

    page = TEMPLATE.format(
        title=esc(article.get('title', 'Untitled')),
        title_json=esc(article.get('title', 'Untitled')).replace('"', '\\"'),
        title_encoded=url_encode(article.get('title', '')),
        subtitle=esc(article.get('subtitle', '')),
        subtitle_json=esc(article.get('subtitle', '')).replace('"', '\\"'),
        date=article.get('date', ''),
        date_display=format_date(article.get('date', '2026-01-01')),
        slug=slug,
        heroEmoji=article.get('heroEmoji', '\U0001F4F0'),
        category=esc(article.get('category', 'General')),
        readTime=esc(article.get('readTime', '3 min read')),
        body_html=body_html,
        tags_html=tags_html,
        sources_html=sources_html,
    )

    out_path = os.path.join(OUTPUT_DIR, f'{slug}.html')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(page)
    return out_path

def main():
    json_files = sorted(f for f in os.listdir(ARTICLES_DIR) if f.endswith('.json'))
    print(f'Found {len(json_files)} JSON articles')
    count = 0
    for jf in json_files:
        path = os.path.join(ARTICLES_DIR, jf)
        out = build_article(path)
        count += 1
        print(f'  Built: {os.path.basename(out)}')
    print(f'\nDone -- {count} HTML pages generated.')
    print('\nPre-rendering news index...')
    build_index()

if __name__ == '__main__':
    main()
