# AESOP AI Academy — Module Lesson File Standards
## Reference document for building Module 2 and beyond

---

## 1. File Naming Convention

Each lesson file follows: `m{MODULE}-age-{AGE_RANGE}-v{VERSION}.html`

- Module 1, Ages 9–10, version 3: `m1-age-9-10-v3.html`
- FTP to server as: `index.html` in the appropriate directory
- Versions are **per-file independent** — each file has its own version history
- **Bump the version on every delivery, no exceptions**

### Server directory structure
```
public_html/mobile/ai-academy/ai-curriculum/module-1/
  m1-age-5-6.html      (index.html)
  m1-age-7-8.html      (index.html)
  m1-age-9-10.html     (index.html)
  m1-age-11-12.html    (index.html)
  m1-age-13-15.html    (index.html)
  m1-age-16-18.html    (index.html)
```

---

## 2. Age Group Configuration

Each age group has a fixed color identity. **Never change these.**

| Age Group | Emoji | Accent Color | Accent RGB | Background |
|-----------|-------|-------------|------------|------------|
| 5–6       | 🌱    | #6ee7b7     | 110,231,183 | #0b0e08   |
| 7–8       | ⭐    | #fbbf24     | 251,191,36  | #0e1208   |
| 9–10      | 🚀    | #60a5fa     | 96,165,250  | #080c18   |
| 11–12     | 🔬    | #c084fc     | 192,132,252 | #0c0618   |
| 13–15     | 🔥    | #fb923c     | 251,146,60  | #110a04   |
| 16+       | 🎯    | #f43f5e     | 244,63,94   | #080810   |

Gold (universal): `#f0c040`

---

## 3. Page Architecture

### Concept Layer Stack (MANDATORY)

Each age group covers its own concept layer AND every layer below it, **rewritten completely for that age group's reader**. Same concept, different voice/vocabulary/depth.

| Page | Concept | 5-6 | 7-8 | 9-10 | 11-12 | 13-15 | 16+ |
|------|---------|-----|-----|------|-------|-------|-----|
| 1 | What Is AI? | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 2 | How AI Learns (Training Data) | — | ✅ | ✅ | ✅ | ✅ | ✅ |
| 3 | How AI Thinks (Tokens/Hallucination/Bias/RLHF) | — | — | ✅ | ✅ | ✅ | ✅ |
| 4 | LLMs, Transformers & Emergence | — | — | — | ✅ | ✅ | ✅ |
| 5 | AI History & Architecture | — | — | — | — | ✅ | ✅ |
| 6 | Scaling Laws, Alignment & AGI | — | — | — | — | — | ✅ |

**Critical rule:** Each page is written entirely for its age group's reader. A 16+ page covering "What Is AI?" is NOT the 5–6 version with additions — it is a university-level treatment of the same concept, written as if the reader has never seen prior lessons.

### Voice & Vocabulary by Age Group

| Age | Voice | Vocabulary | Sentence length | Story style |
|-----|-------|-----------|----------------|-------------|
| 5–6 | Wonder-first, warm | 1-2 syllable words wherever possible | Very short | Mia + ZIPP (simple narrative) |
| 7–8 | Curious explorer | Simple but expanding | Medium | Jordan + LIBREX (library discovery) |
| 9–10 | Investigative | Real terminology introduced carefully | Medium-long | Sam + Devon (project gone wrong) |
| 11–12 | Analytical | Technical terms with context | Long | Alex (debate/inquiry) |
| 13–15 | Developer-adjacent | Technical vocabulary expected | Long, complex | Priya (API builder) |
| 16+ | Peer/academic | Papers cited, no hand-holding | Dense | No story — case study framing |

---

## 4. Required HTML Structure (Every File)

```html
<!DOCTYPE html>
<html lang="en">
<head>
  [meta + title + Google Fonts]
  <style>[CSS block — see Section 5]</style>
</head>
<body>
  <div class="stars" id="stars"></div>
  <div class="page-wrap">

    <!-- TOPBAR -->
    <div class="topbar">
      <span class="topbar-brand">AESOP AI Academy</span>
      <a href="/mobile/ai-academy/" class="back-btn">← Back</a>
    </div>

    <!-- UC BANNER -->
    <div class="uc-banner"><p>🚧 Module N Preview 🚧</p></div>

    <!-- LAYOUT: sidebar + main -->
    <div class="lesson-layout">
      <aside class="lesson-sidebar">
        <div class="sidebar-label">Module N</div>
        [sidebar-item buttons — one per page]
      </aside>
      <div class="lesson-main">

        <!-- PAGE 0 -->
        <div id="page-0">
          [lesson-hero]
          [page-nav-top]
          [content: story-scene, lesson-section blocks, story-lab, quiz-box]
          [page-nav-bottom]
        </div>

        <!-- PAGE 1 (hidden) -->
        <div id="page-1" style="display:none;">
          [same structure]
        </div>
        [... more pages ...]

      </div><!-- lesson-main -->
    </div><!-- lesson-layout -->

  </div><!-- page-wrap -->
  <script>[JS block — see Section 7]</script>
</body>
</html>
```

---

## 5. CSS Reference (Complete Standard Block)

Replace `{ACCENT_RGB}`, `{ACCENT_HEX}`, `{ACCENT2_HEX}`, `{BG}`, `{PANEL}`, `{BORDER}`, `{TEXT}`, `{MUTED}`, `{BG_TOP_RGB}` with age group values from Section 2.

```css
:root{
  --bg:{BG};--panel:{PANEL};--border:{BORDER};
  --accent:{ACCENT_HEX};--accent2:{ACCENT2_HEX};
  --gold:#f0c040;--text:{TEXT};
  --accent-rgb:{ACCENT_RGB};--muted:{MUTED};
}
*{margin:0;padding:0;box-sizing:border-box;}
body{background:var(--bg);color:var(--text);font-family:'Nunito',sans-serif;min-height:100vh;}

/* TOPBAR */
.topbar{background:rgba({BG_TOP_RGB},0.97);border-bottom:1px solid var(--border);padding:10px 24px;display:flex;align-items:center;justify-content:space-between;position:sticky;top:0;z-index:100;}
.topbar-brand{font-family:'Cinzel',serif;font-size:1.61rem;color:var(--gold);letter-spacing:0.08em;}
.back-btn{background:rgba({ACCENT_RGB},0.1);border:1px solid var(--accent);color:var(--accent);padding:6px 14px;border-radius:20px;font-size:1.52rem;font-weight:700;text-decoration:none;}

/* UC BANNER */
.uc-banner{background:repeating-linear-gradient(45deg,#1a1200,#1a1200 10px,#2a1e00 10px,#2a1e00 20px);border-top:3px solid var(--gold);border-bottom:3px solid var(--gold);padding:14px 24px;text-align:center;}
.uc-banner p{font-size:1.61rem;font-weight:800;letter-spacing:0.15em;text-transform:uppercase;color:var(--gold);}

/* HERO */
.lesson-hero{padding:48px 32px 40px;text-align:center;border-bottom:1px solid var(--border);position:relative;overflow:hidden;}
.lesson-hero::before{content:'';position:absolute;inset:0;background:radial-gradient(ellipse 60% 80% at 50% 30%,rgba({ACCENT_RGB},0.08) 0%,transparent 70%);}
.age-chip{display:inline-block;background:rgba({ACCENT_RGB},0.12);border:1px solid var(--accent);color:var(--accent);font-size:1.42rem;font-weight:700;letter-spacing:0.18em;text-transform:uppercase;padding:5px 14px;border-radius:20px;margin-bottom:16px;}
.page-chip{display:inline-block;background:rgba(240,192,64,0.1);border:1px solid rgba(240,192,64,0.3);color:var(--gold);font-size:1.23rem;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;padding:4px 12px;border-radius:20px;margin-left:8px;}
.lesson-hero h1{font-family:'Cinzel',serif;font-size:clamp(1.4rem,5vw,2.2rem);font-weight:900;color:#fff;margin-bottom:12px;line-height:1.2;position:relative;}
.lesson-hero .tagline{font-size:1.9rem;color:var(--muted);max-width:600px;margin:0 auto;line-height:1.65;position:relative;}

/* TOP NAV */
.page-nav-top{margin:16px 24px 0;padding:0 24px;display:flex;align-items:center;justify-content:space-between;gap:12px;}
.page-nav-top .pnt-info{font-family:'Cinzel',serif;font-size:1.23rem;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;color:var(--muted);text-align:center;flex:1;}
.page-nav-top .pnt-info span{color:var(--accent);}
.pnt-btn{padding:10px 20px;border-radius:10px;font-family:'Cinzel',serif;font-size:1.33rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;cursor:pointer;border:1.5px solid var(--accent);color:var(--accent);background:rgba({ACCENT_RGB},0.08);transition:all 0.2s;white-space:nowrap;text-decoration:none;}
.pnt-btn:hover{background:rgba({ACCENT_RGB},0.18);}
.pnt-btn.disabled{opacity:0.25;pointer-events:none;}

/* BOTTOM NAV */
.page-nav-bottom{margin:32px 24px 60px;padding:0 24px;display:flex;gap:12px;}
.pnb-btn{flex:1;padding:18px 20px;border-radius:14px;font-family:'Cinzel',serif;font-size:1.52rem;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;cursor:pointer;text-align:center;text-decoration:none;transition:all 0.2s;border:2px solid var(--border);color:var(--muted);background:rgba(255,255,255,0.03);display:flex;flex-direction:column;align-items:center;gap:4px;}
.pnb-btn:hover{border-color:var(--accent);color:var(--accent);}
.pnb-btn.primary{background:rgba({ACCENT_RGB},0.12);border-color:var(--accent);color:var(--accent);}
.pnb-btn.disabled{opacity:0.25;pointer-events:none;}
.pnb-arrow{font-size:2.66rem;line-height:1;}
.pnb-label{font-size:1.18rem;opacity:0.7;}

/* STORY SCENE */
.story-scene{background:var(--panel);border:1px solid var(--border);border-radius:20px;padding:40px 48px;margin:48px 24px;position:relative;}
.story-scene[data-label]::before{content:attr(data-label);position:absolute;top:-14px;left:32px;background:var(--panel);padding:0 14px;font-size:1.1rem;font-weight:800;letter-spacing:0.2em;color:var(--accent);border:1px solid var(--accent);border-radius:12px;}
.story-text{font-size:1.94rem;line-height:2.1;color:var(--text);}
.story-text em{color:var(--accent);font-style:normal;font-weight:800;}
.story-text .char{color:var(--gold);font-weight:800;}

/* SECTIONS */
.lesson-section{margin:0 0 56px;padding:0 32px;}
.section-heading{font-family:'Cinzel',serif;font-size:2.1rem;font-weight:700;color:var(--accent);margin-bottom:24px;padding-bottom:14px;border-bottom:2px solid var(--border);letter-spacing:0.03em;}
.section-body{font-size:1.9rem;line-height:2.05;color:var(--text);}
.section-body p+p{margin-top:28px;}

/* CALLOUTS */
.callout{background:rgba({ACCENT_RGB},0.07);border-left:5px solid var(--accent);border-radius:0 14px 14px 0;padding:24px 28px;margin:32px 0;}
.callout-label{font-size:1.15rem;font-weight:800;letter-spacing:0.2em;text-transform:uppercase;color:var(--accent);margin-bottom:12px;}
.callout p{font-size:1.9rem;line-height:1.9;color:var(--text);}
.callout p+p{margin-top:16px;}

.gold-callout{background:rgba(240,192,64,0.07);border-left:5px solid var(--gold);border-radius:0 14px 14px 0;padding:24px 28px;margin:32px 0;}
.gold-callout .callout-label{color:var(--gold);}
.gold-callout p{font-size:1.9rem;line-height:1.9;color:var(--text);}
.gold-callout p+p{margin-top:16px;}

.warn-callout{background:rgba(239,68,68,0.07);border-left:5px solid #ef4444;border-radius:0 14px 14px 0;padding:24px 28px;margin:32px 0;}
.warn-callout .callout-label{color:#ef4444;}
.warn-callout p{font-size:1.9rem;line-height:1.9;color:var(--text);}
.warn-callout p+p{margin-top:16px;}

/* STORY LAB */
.story-lab{background:linear-gradient(135deg,rgba({ACCENT_RGB},0.09),rgba({ACCENT_RGB},0.04));border:2px solid rgba({ACCENT_RGB},0.35);border-radius:20px;padding:40px 40px 36px;margin:48px 24px;position:relative;}
.story-lab::before{content:'{EMOJI} AESOP STORY LAB';position:absolute;top:-14px;left:28px;background:var(--bg);padding:0 14px;font-size:1.1rem;font-weight:800;letter-spacing:0.22em;color:var(--accent);border:1px solid rgba({ACCENT_RGB},0.4);border-radius:12px;}
.story-lab h4{font-family:'Cinzel',serif;font-size:1.9rem;color:#fff;margin-bottom:18px;}
.story-lab p,.story-lab ol li{font-size:1.9rem;line-height:2.0;color:var(--text);}
.story-lab ol{padding-left:1.8rem;margin-top:16px;}
.story-lab ol li{margin-bottom:18px;}
.story-lab .prompt{background:rgba({ACCENT_RGB},0.09);border:1px solid rgba({ACCENT_RGB},0.25);border-radius:12px;padding:20px 24px;margin-top:24px;font-size:1.8rem;font-style:italic;color:var(--accent);line-height:1.85;}

/* QUIZ */
.quiz-box{background:rgba({ACCENT_RGB},0.04);border:1px solid rgba({ACCENT_RGB},0.2);border-radius:18px;padding:36px 40px;margin:48px 24px;}
.quiz-q{font-weight:800;font-size:2rem;color:#fff;margin-bottom:24px;line-height:1.55;}
.quiz-opts{display:flex;flex-direction:column;gap:14px;}
.quiz-opt{background:rgba(255,255,255,0.04);border:1px solid var(--border);color:var(--text);padding:18px 24px;border-radius:12px;font-family:'Nunito',sans-serif;font-size:1.9rem;cursor:pointer;text-align:left;transition:all 0.2s;font-weight:600;}
.quiz-opt:hover:not(:disabled){border-color:var(--accent);background:rgba({ACCENT_RGB},0.08);color:#fff;}
.quiz-opt.correct{border-color:#22c55e;background:rgba(34,197,94,0.12);color:#86efac;}
.quiz-opt.wrong{border-color:#ef4444;background:rgba(239,68,68,0.1);color:#fca5a5;}
.quiz-feedback{margin-top:20px;font-size:1.8rem;line-height:1.75;padding:18px 22px;border-radius:12px;display:none;}
.quiz-feedback.show{display:block;}
.quiz-feedback.right{background:rgba(34,197,94,0.1);border:1px solid rgba(34,197,94,0.3);color:#86efac;}
.quiz-feedback.wrong{background:rgba(239,68,68,0.08);border:1px solid rgba(239,68,68,0.25);color:#fca5a5;}

/* SECTION DIVIDER */
.section-divider{height:1px;background:linear-gradient(90deg,transparent,var(--border),transparent);margin:8px 32px 56px;}

/* SIDEBAR */
.lesson-layout{display:grid;grid-template-columns:220px 1fr;max-width:100%;margin:0 auto;min-height:calc(100vh - 120px);gap:0;}
.lesson-sidebar{border-right:1px solid var(--border);background:rgba(0,0,0,0.25);padding:24px 16px;position:sticky;top:52px;height:calc(100vh - 52px);overflow-y:auto;}
.sidebar-label{font-family:'Cinzel',serif;font-size:1.1rem;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;color:var(--muted);margin-bottom:16px;padding-bottom:10px;border-bottom:1px solid var(--border);}
.sidebar-item{display:flex;align-items:center;gap:10px;width:100%;padding:10px 12px;border-radius:10px;border:1px solid transparent;background:transparent;color:var(--muted);font-family:'Nunito',sans-serif;font-size:1.3rem;font-weight:700;cursor:pointer;text-align:left;transition:all 0.2s;margin-bottom:4px;}
.sidebar-item:hover{background:rgba(255,255,255,0.05);color:var(--text);}
.sidebar-item.active{background:rgba({ACCENT_RGB},0.12);border-color:var(--accent);color:var(--accent);}
.sidebar-item.done{color:rgba({ACCENT_RGB},0.45);}
.sidebar-item.done::before{content:'✓ ';}
.sidebar-dot{width:8px;height:8px;border-radius:50%;background:currentColor;flex-shrink:0;opacity:0.6;}
.sidebar-item.active .sidebar-dot{opacity:1;}
.lesson-main{min-width:0;padding:0 8px;}

/* RESPONSIVE */
@media(max-width:700px){.lesson-layout{grid-template-columns:1fr;}.lesson-sidebar{display:none;}}
@media(max-width:600px){
  .lesson-hero{padding:32px 16px 28px;}
  .story-scene{padding:20px 16px;margin:20px 16px;}
  .lesson-section{padding:0 16px;}
  .story-lab,.quiz-box{padding:18px 16px;margin:20px 16px;}
  .page-nav-top,.page-nav-bottom{padding:0 16px;}
  .page-nav-bottom{margin-bottom:40px;}
  .pnb-btn{padding:16px 12px;}
  .topbar-brand{font-size:1.37rem;}
  .back-btn{font-size:1.37rem;padding:5px 10px;}
}

/* STARS */
.stars{position:fixed;inset:0;pointer-events:none;z-index:0;overflow:hidden;}
.star{position:absolute;border-radius:50%;background:#fff;animation:twinkle var(--dur) ease-in-out infinite;}
@keyframes twinkle{0%,100%{opacity:0.1}50%{opacity:var(--max-op)}}
.page-wrap{position:relative;z-index:1;}
```

---

## 6. HTML Patterns — Required Per-Page Elements

### Lesson Hero
```html
<div class="lesson-hero">
  <div class="age-chip">{EMOJI} {AGE_LABEL}</div>
  <span class="page-chip">Page {N} of {TOTAL}</span>
  <h1>{PAGE TITLE}</h1>
  <p class="tagline">{1-2 sentence hook for this page}</p>
</div>
```

### Top Navigation (required at top of every page, immediately after hero)
```html
<div class="page-nav-top">
  <button class="pnt-btn [disabled]" [onclick="goPage(N-1)"]>← Previous</button>
  <div class="pnt-info">Page <span>{N}</span> of <span>{TOTAL}</span> — {Title}</div>
  <button class="pnt-btn [disabled]" [onclick="goPage(N+1)"]>Next →</button>
</div>
```
- Add `disabled` class and remove onclick on first page Previous button
- Add `disabled` class and remove onclick on last page Next button

### Bottom Navigation (required at bottom of every page)
```html
<div class="page-nav-bottom">
  <!-- Left: Back to Curriculum (page 1) OR Previous page button -->
  <a href="/mobile/ai-academy/ai-curriculum/" class="pnb-btn">
    <span class="pnb-arrow">←</span>
    <span class="pnb-label">Back to Curriculum</span>
  </a>
  <!-- OR -->
  <button class="pnb-btn" onclick="goPage(N-1)">
    <span class="pnb-arrow">←</span>
    <span class="pnb-label">Back: {Prev Page Title}</span>
  </button>

  <!-- Right: Next page (primary) OR Academy Home (last page) -->
  <button class="pnb-btn primary" onclick="goPage(N+1)">
    <span class="pnb-arrow">→</span>
    <span class="pnb-label">Next: {Next Page Title}</span>
  </button>
  <!-- OR -->
  <a href="/mobile/ai-academy/" class="pnb-btn primary">
    <span class="pnb-arrow">🏠</span>
    <span class="pnb-label">Academy Home</span>
  </a>
</div>
```

### Section Divider (between every lesson-section)
```html
<div class="section-divider"></div>
```

### Story Scene
```html
<div class="story-scene" data-label="📖 STORY TIME">
  <p class="story-text">
    <span class="char">CharacterName</span> narrative text...
    <em>emphasized key term</em>
  </p>
</div>
```

### Callout Types
```html
<!-- Standard accent callout -->
<div class="callout">
  <p class="callout-label">🔑 Label Text</p>
  <p>Body text.</p>
</div>

<!-- Gold callout (positive/summary) -->
<div class="gold-callout">
  <p class="callout-label">🌟 Label Text</p>
  <p>Body text.</p>
</div>

<!-- Warning callout (caution/important) -->
<div class="warn-callout">
  <p class="callout-label">⚠️ Label Text</p>
  <p>Body text.</p>
</div>
```

### Story Lab
```html
<div class="story-lab">
  <h4>Lab Title</h4>
  <p>Intro sentence.</p>
  <ol>
    <li>Step 1</li>
    <li>Step 2</li>
    <li>Step 3</li>
  </ol>
  <div class="prompt">Closing insight in italic accent color.</div>
</div>
```

### Quiz Box
```html
<div class="quiz-box" id="q{N}p{PAGE}">
  <p class="quiz-q">🧪 Question text?</p>
  <div class="quiz-opts">
    <button class="quiz-opt" onclick="answer(this,'wrong','q{N}p{PAGE}')">Wrong answer</button>
    <button class="quiz-opt" onclick="answer(this,'correct','q{N}p{PAGE}')">Correct answer</button>
    <button class="quiz-opt" onclick="answer(this,'wrong','q{N}p{PAGE}')">Wrong answer</button>
  </div>
  <div class="quiz-feedback right">✅ Correct feedback text.</div>
  <div class="quiz-feedback wrong">Incorrect feedback — what the right answer is.</div>
</div>
```

### Sidebar (in lesson-layout)
```html
<aside class="lesson-sidebar">
  <div class="sidebar-label">Module {N}</div>
  <button class="sidebar-item active" id="sbi-0" onclick="goPage(0)">
    <span class="sidebar-dot"></span>1. Page Title
  </button>
  <button class="sidebar-item" id="sbi-1" onclick="goPage(1)">
    <span class="sidebar-dot"></span>2. Page Title
  </button>
  <!-- etc. -->
</aside>
```

---

## 7. JavaScript Block (Complete — Required in Every File)

Replace `{NUM_PAGES}` with the actual number of pages.

```javascript
function answer(btn, result, qId) {
  const box = document.getElementById(qId);
  box.querySelectorAll('.quiz-opt').forEach(b => { b.disabled = true; });
  btn.classList.add(result);
  box.querySelectorAll('.quiz-feedback').forEach(f => f.classList.remove('show'));
  box.querySelector('.quiz-feedback.' + (result === 'correct' ? 'right' : 'wrong')).classList.add('show');
}

const PAGES = ['page-0', 'page-1', /* ... 'page-N' */];
let currentPage = 0;
const completedPages = new Set([0]);

function goPage(n) {
  document.getElementById(PAGES[currentPage]).style.display = 'none';
  currentPage = n;
  completedPages.add(n);
  document.getElementById(PAGES[currentPage]).style.display = '';
  for (let i = 0; i < {NUM_PAGES}; i++) {
    const sbi = document.getElementById('sbi-' + i);
    if (!sbi) continue;
    sbi.classList.toggle('active', i === n);
    sbi.classList.toggle('done', completedPages.has(i) && i !== n);
  }
  window.scrollTo(0, 0);
}

// Stars
const s = document.getElementById('stars');
for (let i = 0; i < 60; i++) {
  const el = document.createElement('div');
  el.className = 'star';
  const sz = Math.random() * 2 + 0.5;
  el.style.cssText = `width:${sz}px;height:${sz}px;top:${Math.random()*100}%;left:${Math.random()*100}%;--dur:${2+Math.random()*4}s;--max-op:${0.2+Math.random()*0.4}`;
  s.appendChild(el);
}
```

**CRITICAL:** `completedPages` MUST be declared before `goPage` is called. All three variables (`PAGES`, `currentPage`, `completedPages`) must be in the same script block. Never split them across multiple script tags.

---

## 8. Content Rules

### What each page MUST contain
- Lesson hero with age chip, page chip (Page N of Total), h1, tagline
- Top nav (immediately after hero, before first content)
- At least one story scene OR a case study opening on page 1
- At least 2 lesson sections with section headings
- At least 1 callout per section
- Section dividers between sections
- Story lab on the final page of each file
- At least 1 quiz per page
- Bottom nav

### What each file MUST NOT contain
- `max-width` constraints on `.lesson-section`, `.story-scene`, `.quiz-box`, `.story-lab` — these should fill the content column
- The `progress-bar` / `progress-fill` / `progress-track` elements (removed)
- The `.page-tabs` element (removed — replaced by sidebar)
- `completedPages` declared after `goPage` is defined
- Multiple `<script>` tags
- `progressFill` references anywhere in JS

### Writing voice by age (enforce strictly)
- **5–6:** Max 2-syllable words. Max 10 words per sentence. No jargon. Dialogue-heavy.
- **7–8:** Simple vocabulary. Analogies required for every technical concept. Story-led.
- **9–10:** Technical terms introduced with immediate plain-language definition. Investigative tone.
- **11–12:** Technical vocabulary expected. Precise language. Philosophical questions welcome.
- **13–15:** Developer-adjacent. Papers and tools referenced. Technical accuracy required.
- **16+:** Academic/peer level. Papers cited by author. No simplification. Dense.

---

## 9. Link Paths

| Link destination | Path |
|-----------------|------|
| Back to Academy | `/mobile/ai-academy/` |
| Back to Curriculum | `/mobile/ai-academy/ai-curriculum/` |
| Module 1 lessons | `/mobile/ai-academy/ai-curriculum/module-1/` |
| Module 2 lessons | `/mobile/ai-academy/ai-curriculum/module-2/` |

Desktop Academy (AI-Academy.html) storyUrl paths use:
`/aesop-academy/ai-academy/ai-curriculum/module-{N}/m{N}-age-{RANGE}.html`

---

## 10. Quality Checklist (Before Delivery)

- [ ] Version number bumped from previous delivery
- [ ] File named correctly: `mN-age-XX-XX-vN.html`
- [ ] All accent colors correct for this age group
- [ ] No `max-width:760px` on content elements
- [ ] No `progress-bar` elements
- [ ] `completedPages` declared before `goPage`
- [ ] Single `<script>` block only
- [ ] Top nav on every page
- [ ] Bottom nav on every page
- [ ] First page Previous button disabled
- [ ] Last page Next button disabled / replaced with Academy Home
- [ ] Sidebar items match pages exactly (count and labels)
- [ ] Story lab on final page
- [ ] At least 1 quiz per page
- [ ] Section dividers between all sections
- [ ] Back links point to `/mobile/ai-academy/` (not `/aesop-edu/`)
- [ ] Writing voice appropriate for the age group
- [ ] Concept layer matches the page/age matrix in Section 3
