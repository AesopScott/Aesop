# AESOP AI Academy — Electives Module Standards
> For modules loaded by `electives-hub.html` via content injection (fetch + inject).
> Version 1.0.0 | April 2026

---

## How the Hub Loads Modules

The electives hub fetches the module HTML file and extracts three things:
1. All `<style>` blocks → injected into `<head>` once
2. `.tab-strip` div → injected as the lesson tab bar
3. `.content-area` div → injected as the lesson content
4. All `<script>` blocks → re-executed in global scope

The hub provides its own outer chrome: header bar, sidebar, back button, font sizer.

**The module file must NOT include:**
- `<!DOCTYPE html>`, `<html>`, `<head>`, `<body>` — hub ignores these but keep them for standalone testing
- A topbar / nav bar — hub renders its own
- External `<link>` stylesheets — hub already loads `academy-theme.css` and `academy-dark-mode.css`
- Academy-wide fonts — already loaded by hub

**The module file MUST include:**
- `.tab-strip` div
- `.content-area` div containing all `.page` divs
- One `<script>` block with all JS
- Its own `<style>` block for module-specific CSS only

---

## File Naming Convention

```
Local staging name:   {course}-m{N}-v{X}_{Y}_{Z}.html
Server deploy name:   {course}-m{N}.html
```

**Examples:**
```
ai-governance-m1-v1_0_0.html  →  ai-governance-m1.html
ai-governance-m2-v1_0_2.html  →  ai-governance-m2.html
```

**Server path:** `aesop-academy/ai-academy/modules/ai-governance/`

---

## Required JS Variables

Every module file must declare these variables at the top of its `<script>` block:

```javascript
var COURSE_ID  = 'governance';   // matches hub COURSES data id
var MODULE_ID  = 'gov-m1';       // matches hub module id
var PROXY_URL  = '/aesop-api/proxy.php';
var currentPageId = 'p-l1';      // first page id
var lessonSignaled = {}, quizSignaled = {}, labSignaled = {};
var PAGE_TO_LESSON = {
  'p-l1':'l1', 'p-l2':'l2', 'p-l3':'l3', 'p-l4':'l4'
};
```

**COURSE_ID values:**

| Course | COURSE_ID |
|--------|-----------|
| AI Governance | `governance` |
| AI in Society | `society` |
| AI & Creativity | `creativity` |
| AI Ethics | `ethics` |
| Building with AI | `building` |
| AI Careers | `careers` |

**MODULE_ID format:** `{coursePrefix}-m{N}`

| Course | Prefix | Example |
|--------|--------|---------|
| governance | gov | `gov-m1` |
| society | soc | `soc-m1` |
| creativity | cre | `cre-m1` |
| ethics | eth | `eth-m1` |
| building | bld | `bld-m1` |
| careers | car | `car-m1` |

---

## Required JS Functions

### goPage(id)
Navigates between pages. Signals lesson complete when leaving a lesson page.

```javascript
function goPage(id){
  var prev = document.getElementById(currentPageId);
  var next = document.getElementById(id);
  if(!next) return;
  // Signal lesson complete on navigation away
  var pl = PAGE_TO_LESSON[currentPageId];
  if(pl && !lessonSignaled[pl]){
    lessonSignaled[pl] = true;
    window.parent.postMessage({
      type:'lessonComplete',
      courseId: COURSE_ID,
      moduleId: MODULE_ID,
      lessonId: pl
    }, '*');
  }
  if(prev) prev.classList.remove('active');
  next.classList.add('active');
  currentPageId = id;
  updateTabs();
  window.scrollTo(0,0);
}
```

### updateTabs()
Syncs active state on the tab strip.

```javascript
function updateTabs(){
  document.querySelectorAll('.tab-lesson,.tab-sub,.tab-test').forEach(function(el){
    el.classList.toggle('active', el.dataset.page === currentPageId);
  });
}
```

### adjustSize(delta) + applySize(val)
Font sizer — hub topbar calls these directly.

```javascript
function applySize(val){
  document.querySelector('.content-area').style.fontSize = val + 'px';
}
function adjustSize(delta){
  var r = document.getElementById('sizerRange');
  if(!r) return;
  r.value = Math.min(22, Math.max(12, parseInt(r.value) + delta));
  applySize(r.value);
}
```

### answer(btn, result, qId)
Handles quiz answer selection.

```javascript
function answer(btn, result, qId){
  var box = document.getElementById(qId);
  box.querySelectorAll('.quiz-opt').forEach(function(b){ b.disabled = true; });
  btn.classList.add(result);
  box.querySelectorAll('.quiz-feedback').forEach(function(fb){ fb.classList.remove('show'); });
  box.querySelector('.quiz-feedback.' + (result==='correct' ? 'right' : 'wrong')).classList.add('show');
  if(result === 'correct'){
    var lm = qId.match(/q\d+-l(\d+)/);
    if(lm){
      var lid = MODULE_ID + '-l' + lm[1];
      if(!quizSignaled[lid]){
        quizSignaled[lid] = true;
        window.parent.postMessage({
          type:'quizComplete',
          courseId: COURSE_ID,
          moduleId: MODULE_ID,
          lessonId: 'l' + lm[1]
        }, '*');
      }
    }
  }
}
```

### chatSend(labId)
AI lab chat — calls the proxy.

```javascript
var chatHistories = { l1:[], l2:[], l3:[], l4:[] };

async function chatSend(labId){
  var inp = document.getElementById('inp-' + labId);
  if(!inp) return;
  var text = inp.value.trim();
  if(!text) return;
  inp.value = '';
  chatAppend(labId, 'user', text);
  chatHistories[labId].push({role:'user', content:text});
  chatSetLoading(labId, true);
  try{
    var res = await fetch(PROXY_URL, {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({
        messages: chatHistories[labId],
        system_prompt: ACADEMY_GUARDRAIL + (LAB_SYSTEM_PROMPTS[labId] || ''),
        max_tokens: 1024
      })
    });
    if(!res.ok) throw new Error('Server error ' + res.status);
    var data = await res.json();
    var reply = (data.content && data.content[0] && data.content[0].text) || data.reply || '(No response)';
    chatHistories[labId].push({role:'assistant', content:reply});
    chatAppend(labId, 'ai', reply);
  } catch(err){
    chatAppend(labId, 'error', '⚠ ' + err.message);
    chatHistories[labId].pop();
  }
  chatSetLoading(labId, false);
}
```

---

## HTML Structure

### Full File Shell

```html
<!DOCTYPE html>
<!-- {course}-m{N}-v{X}.{Y}.{Z} -->
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{Module Title} — AI Governance M{N} | AESOP AI Academy</title>
<style>
  /* Module-specific styles only — see CSS section below */
</style>
</head>
<body>

<!-- TAB STRIP — required, extracted by hub -->
<div class="tab-strip">
  <!-- see Tab Strip section -->
</div>

<!-- CONTENT AREA — required, extracted by hub -->
<div class="content-area">
  <!-- all .page divs go here -->
</div>

<script>
// All JS — see JS section above
</script>
</body>
</html>
```

---

### Tab Strip

One `.tab-group` per lesson. Each group has a lesson tab + quiz + lab sub-tabs.
Module test tab goes at the end.

```html
<div class="tab-strip">
  <div class="tab-group">
    <div class="tab-lesson active" data-page="p-l1" onclick="goPage('p-l1')">L1</div>
    <div class="tab-subs">
      <span class="tab-sep">·</span>
      <div class="tab-sub" data-page="p-q1" onclick="goPage('p-q1')">Quiz</div>
      <span class="tab-sep">·</span>
      <div class="tab-sub" data-page="p-lab1" onclick="goPage('p-lab1')">Lab</div>
    </div>
  </div>
  <div class="tab-group">
    <div class="tab-lesson" data-page="p-l2" onclick="goPage('p-l2')">L2</div>
    <div class="tab-subs">
      <span class="tab-sep">·</span>
      <div class="tab-sub" data-page="p-q2" onclick="goPage('p-q2')">Quiz</div>
      <span class="tab-sep">·</span>
      <div class="tab-sub" data-page="p-lab2" onclick="goPage('p-lab2')">Lab</div>
    </div>
  </div>
  <!-- repeat for L3, L4 -->
  <div class="tab-test" data-page="p-mt" onclick="goPage('p-mt')">Module Test</div>
</div>
```

**Page ID naming:**

| Page | ID |
|------|----|
| Lesson N | `p-l{N}` |
| Quiz N | `p-q{N}` |
| Lab N | `p-lab{N}` |
| Module Test | `p-mt` |

---

### Content Area & Pages

```html
<div class="content-area">

  <!-- LESSON 1 -->
  <div class="page active" id="p-l1">
    <div class="lesson-hero">
      <div class="lesson-kicker">AI Governance · Module 1 · Lesson 1</div>
      <h1>{Lesson Title}</h1>
      <p class="tagline">{One-sentence hook}</p>
    </div>
    <!-- lesson body — see Content Blocks section -->
    <div class="page-nav">
      <button class="pnav-btn" onclick="goPage('p-q1')">Lesson Quiz →</button>
      <button class="pnav-btn primary" onclick="goPage('p-lab1')">Lab 1 →</button>
    </div>
  </div>

  <!-- QUIZ 1 -->
  <div class="page" id="p-q1">
    <!-- see Quiz section -->
    <div class="page-nav">
      <button class="pnav-btn" onclick="goPage('p-l1')">← Lesson 1</button>
      <button class="pnav-btn primary" onclick="goPage('p-lab1')">Lab 1 →</button>
    </div>
  </div>

  <!-- LAB 1 -->
  <div class="page" id="p-lab1">
    <!-- see Lab section -->
    <div class="page-nav">
      <button class="pnav-btn" onclick="goPage('p-q1')">← Quiz</button>
      <button class="pnav-btn primary" onclick="goPage('p-l2')">Lesson 2 →</button>
    </div>
  </div>

  <!-- repeat for L2, L3, L4 -->

  <!-- MODULE TEST -->
  <div class="page" id="p-mt">
    <!-- see Module Test section -->
  </div>

</div>
```

---

## Content Blocks

### Story Scene
```html
<div class="story-scene" data-label="SCENE LABEL">
  <p class="story-text"><span class="char">CharacterName</span> narrative text here.</p>
  <p class="story-text">Continue the scene...</p>
</div>
```

### Lesson Section
```html
<div class="lesson-section">
  <p class="section-heading">Section Title</p>
  <div class="section-body">
    <p>Body text...</p>
    <div class="callout">
      <p class="callout-label">Callout Title</p>
      <p>Callout body.</p>
    </div>
  </div>
</div>
<div class="section-divider"></div>
```

### Gold Callout (emphasis)
```html
<div class="gold-callout">
  <p class="callout-label">Title</p>
  <p>Important takeaway text.</p>
</div>
```

### Key Term
```html
<div class="key-term">
  <span class="kt-term">Term</span>
  <span class="kt-def">Definition of the term in plain language.</span>
</div>
```

---

## Quiz Block

One quiz per lesson. ID format: `q{N}-l{N}` (e.g. `q1-l1` = quiz 1, lesson 1).

```html
<div class="quiz-block" id="q1-l1">
  <div class="quiz-question">Question text here?</div>
  <div class="quiz-opts">
    <button class="quiz-opt" onclick="answer(this,'wrong','q1-l1')">Wrong answer A</button>
    <button class="quiz-opt" onclick="answer(this,'correct','q1-l1')">Correct answer</button>
    <button class="quiz-opt" onclick="answer(this,'wrong','q1-l1')">Wrong answer B</button>
    <button class="quiz-opt" onclick="answer(this,'wrong','q1-l1')">Wrong answer C</button>
  </div>
  <div class="quiz-feedback right">✓ Correct! Explanation of why this is right.</div>
  <div class="quiz-feedback wrong">✗ Not quite. Explanation of why this is wrong.</div>
</div>
```

- Always 4 options, 1 correct
- Correct answer position should vary across questions
- Feedback divs: `.right` shown on correct, `.wrong` shown on incorrect

---

## Lab Block

AI chat lab — one per lesson. `labId` matches lesson number: `l1`, `l2`, etc.

```html
<div class="lab-block" id="lab-l1">
  <div class="lab-header">
    <span class="lab-tag">AI LAB</span>
    <span class="lab-title">Lab Title</span>
  </div>
  <div class="lab-prompt">
    <p>Instructions for the student. What should they explore or practice?</p>
    <p>Give a specific starting prompt suggestion in <strong>bold</strong>.</p>
  </div>
  <div class="chat-window" id="chat-l1">
    <div class="chat-msgs" id="msgs-l1"></div>
    <div class="chat-input-row">
      <textarea class="chat-inp" id="inp-l1" rows="2"
        placeholder="Type your response..."
        onkeydown="if(event.key==='Enter'&&!event.shiftKey){event.preventDefault();chatSend('l1');}"></textarea>
      <button class="chat-send" onclick="chatSend('l1')">Send</button>
    </div>
  </div>
</div>
```

**LAB_SYSTEM_PROMPTS** — define in `<script>` block:

```javascript
var LAB_SYSTEM_PROMPTS = {
  l1: 'You are a tutor helping students understand [topic]. Keep answers focused on [scope]. If asked off-topic questions, redirect back.',
  l2: 'You are a debate partner helping students practice [skill]...',
  l3: '...',
  l4: '...'
};
```

---

## Module Test

15 questions minimum, auto-scored. One question per lesson (minimum 3–4 per lesson).

```html
<div class="page" id="p-mt">
  <div class="lesson-hero">
    <div class="lesson-kicker">Module Test</div>
    <h1>{Module Title}</h1>
    <p class="tagline">Answer all questions to complete this module.</p>
  </div>
  <div class="mt-progress">
    <span id="mt-score">0</span> / <span id="mt-total">15</span> correct
  </div>
  <div id="mt-questions">
    <!-- question blocks -->
    <div class="mt-q" id="mtq-1">
      <div class="mt-q-text">1. Question text?</div>
      <div class="mt-opts">
        <button class="mt-opt" onclick="mtAnswer(this,false,1)">Option A</button>
        <button class="mt-opt" onclick="mtAnswer(this,true,1)">Correct Option</button>
        <button class="mt-opt" onclick="mtAnswer(this,false,1)">Option C</button>
        <button class="mt-opt" onclick="mtAnswer(this,false,1)">Option D</button>
      </div>
    </div>
    <!-- repeat for all 15 questions -->
  </div>
  <div class="mt-result" id="mt-result" style="display:none;">
    <div class="mt-result-score" id="mt-result-score"></div>
    <div class="mt-result-msg" id="mt-result-msg"></div>
    <button class="pnav-btn primary" onclick="goPage('p-l1')">Review Lessons</button>
  </div>
</div>
```

**Module test JS** — add to `<script>` block:

```javascript
var mtTotal = 15, mtCorrect = 0, mtAnswered = 0;

function mtAnswer(btn, correct, qNum){
  var box = document.getElementById('mtq-' + qNum);
  if(box.classList.contains('answered')) return;
  box.classList.add('answered');
  box.querySelectorAll('.mt-opt').forEach(function(b){ b.disabled = true; });
  btn.classList.add(correct ? 'correct' : 'wrong');
  if(correct) mtCorrect++;
  mtAnswered++;
  document.getElementById('mt-score').textContent = mtCorrect;
  if(mtAnswered >= mtTotal){
    var pct = Math.round((mtCorrect / mtTotal) * 100);
    var passed = pct >= 70;
    document.getElementById('mt-result').style.display = 'block';
    document.getElementById('mt-result-score').textContent = pct + '%';
    document.getElementById('mt-result-msg').textContent = passed
      ? 'Module complete! Well done.'
      : 'Score below 70% — review lessons and retake.';
    if(passed){
      window.parent.postMessage({
        type: 'modTestPassed',
        courseId: COURSE_ID,
        moduleId: MODULE_ID
      }, '*');
    }
  }
}
```

---

## Module-Specific CSS

Only include styles the hub doesn't already provide. The hub loads `academy-theme.css` and `academy-dark-mode.css`. Module CSS handles:

- Tab strip appearance
- Page layout
- Lesson hero, story scenes, callouts
- Quiz and lab blocks
- Module test blocks

**Key CSS variables available from hub:**
```css
var(--gold)          /* #c9a05a */
var(--gold-light)    /* #dbb87a */
var(--teal)          /* #3dd6c0 */
var(--ink)           /* body text */
var(--ink-light)     /* secondary text */
var(--cream)         /* page background */
var(--white)         /* card background */
var(--border)        /* border color */
var(--navy)          /* dark navy */
```

**Tab strip (required CSS):**
```css
.tab-strip{background:#060e18;border-bottom:1px solid #1a2738;padding:0 1.5rem;display:flex;gap:0;overflow-x:auto;flex-shrink:0;scrollbar-width:none;}
.tab-strip::-webkit-scrollbar{display:none;}
.tab-group{display:flex;align-items:stretch;flex-shrink:0;}
.tab-lesson{font-size:0.88rem;color:rgba(201,160,90,0.25);padding:0.65rem 1rem;cursor:pointer;border-bottom:2px solid transparent;transition:all 0.15s;white-space:nowrap;}
.tab-lesson:hover{color:rgba(201,160,90,0.55);}
.tab-lesson.active{color:var(--gold);border-bottom-color:var(--gold);}
.tab-subs{display:flex;align-items:center;padding:0 0.25rem;}
.tab-sep{color:rgba(201,160,90,0.1);font-size:0.7rem;padding:0 0.1rem;}
.tab-sub{font-size:0.7rem;color:rgba(201,160,90,0.18);padding:0.65rem 0.45rem;cursor:pointer;transition:color 0.15s;white-space:nowrap;}
.tab-sub:hover{color:rgba(201,160,90,0.45);}
.tab-sub.active{color:var(--gold);}
.tab-test{font-size:0.6rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:rgba(201,160,90,0.2);padding:0.65rem 1rem;margin-left:auto;cursor:pointer;border-bottom:2px solid transparent;transition:all 0.15s;}
.tab-test:hover{color:rgba(201,160,90,0.5);}
.tab-test.active{color:var(--gold);border-bottom-color:var(--gold);}
```

**Page visibility (required CSS):**
```css
.content-area{flex:1;display:flex;flex-direction:column;}
.page{display:none;flex:1;flex-direction:column;padding:2rem;}
.page.active{display:flex;}
```

---

## PostMessage Events (Hub Communication)

The hub listens for these events from injected module scripts:

| Event type | Payload | When to fire |
|------------|---------|--------------|
| `lessonComplete` | `{courseId, moduleId, lessonId}` | On navigating away from a lesson page |
| `quizComplete` | `{courseId, moduleId, lessonId}` | On correct quiz answer |
| `labComplete` | `{courseId, moduleId, lessonId, exchangeCount}` | After N AI exchanges in lab |
| `modTestPassed` | `{courseId, moduleId}` | On module test score ≥ 70% |

All fire via:
```javascript
window.parent.postMessage({ type: '...', courseId: COURSE_ID, moduleId: MODULE_ID, ... }, '*');
```

---

## QA Checklist

Before FTPing a module file:

- [ ] `COURSE_ID` and `MODULE_ID` match values in hub `COURSES` data
- [ ] All page IDs unique: `p-l1`, `p-q1`, `p-lab1`, `p-l2`, `p-q2`, `p-lab2`, `p-l3`, `p-q3`, `p-lab3`, `p-l4`, `p-q4`, `p-lab4`, `p-mt`
- [ ] First page has `class="page active"`
- [ ] `PAGE_TO_LESSON` maps all lesson page IDs
- [ ] All `data-page` attributes on tabs match a page `id`
- [ ] Quiz IDs follow format `q{N}-l{N}`
- [ ] Lab IDs follow format `l{N}` (`inp-l1`, `chat-l1`, `msgs-l1`)
- [ ] `LAB_SYSTEM_PROMPTS` defined for all lab IDs
- [ ] Module test has 15 questions, `mtTotal = 15`
- [ ] `mtAnswer()` function present with `modTestPassed` postMessage
- [ ] No external `<link>` stylesheets (hub loads them)
- [ ] No topbar HTML (hub renders it)
- [ ] Server filename: `{course}-m{N}.html`

---

## Lesson Count by Module

All elective modules follow this structure:

| Tier | Lessons | Quizzes | Labs | Module Test | Total Pages |
|------|---------|---------|------|-------------|-------------|
| All electives | 4 | 4 | 4 | 1 | 13 |

---

*AESOP-ELECTIVES-MODULE-STANDARDS.md — maintained alongside electives-hub.html*
*Last updated: 2026-04-09*
