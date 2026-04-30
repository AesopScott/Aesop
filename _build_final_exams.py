#!/usr/bin/env python3
"""
Generate {slug}-final.html for every live course that doesn't already have one.

Extracts module-test questions from each module's HTML (the mt-area questions
that use mtAnswer()), pools them, samples up to MAX_QUESTIONS, and writes a
styled standalone final exam page.

Also patches course-registry.json to add a "final" key to each live entry.

Usage:
    python3 _build_final_exams.py [--dry-run]
"""

import json, os, re, random, sys
from pathlib import Path
from bs4 import BeautifulSoup

REPO     = Path("C:/Users/scott/Code/Aesop")
MODULES  = REPO / "ai-academy" / "modules"
REG_PATH = MODULES / "course-registry.json"

MAX_QUESTIONS = 20
RANDOM_SEED   = 42   # reproducible shuffle

# Foundations course IDs — no test-out allowed (enforced in UI, flagged in registry)
FOUNDATIONS_IDS = {
    "foundations-intro",
    "foundations-basic",
    "foundations-advanced",
    "ai-foundations-intro",
    "ai-foundations-basic",
    "ai-foundations-advanced",
}

# ------------------------------------------------------------------
def load_registry():
    with open(REG_PATH, encoding="utf-8") as f:
        return json.load(f)

def save_registry(reg):
    with open(REG_PATH, "w", encoding="utf-8", newline="\n") as f:
        json.dump(reg, f, indent=2, ensure_ascii=False)
    print("  ✓ course-registry.json updated")

# ------------------------------------------------------------------
def extract_mt_questions(html_path: Path):
    """Return list of dicts: {q, opts, correct_idx, fb_right, fb_wrong}
    Handles two module-test formats:
      New: div.quiz-box > div.quiz-q / div.quiz-opts > button.quiz-opt
           onclick="mtAnswer(this,'correct'|'wrong','mt1')"
      Old: div.mt-question > div.mt-q / div.mt-opts > button.mt-opt
           onclick="mtAnswer(this, true|false, 'mt-q1')"
    """
    try:
        soup = BeautifulSoup(
            html_path.read_text(encoding="utf-8", errors="replace"),
            "html.parser"
        )
    except Exception as e:
        print(f"    parse error {html_path.name}: {e}")
        return []

    mt_page = soup.find("div", {"id": "p-mt"})
    if not mt_page:
        return []

    questions = []

    # ── NEW FORMAT: div.quiz-box ────────────────────────────────────
    for box in mt_page.find_all("div", class_="quiz-box"):
        q_el = box.find("div", class_="quiz-q")
        if not q_el:
            continue
        q_text = re.sub(r"^\d+\.\s*", "", q_el.get_text(" ", strip=True))

        opts_el = box.find("div", class_="quiz-opts")
        if not opts_el:
            continue

        opts, correct_idx = [], 0
        # Support both button.quiz-opt and button.mt-opt inside quiz-box
        btns = opts_el.find_all("button", class_=re.compile(r"quiz-opt|mt-opt"))
        for i, btn in enumerate(btns):
            onclick = btn.get("onclick", "")
            opts.append(btn.get_text(" ", strip=True))
            # New style: 'correct' string; Old style: true boolean
            if "'correct'" in onclick or '"correct"' in onclick:
                correct_idx = i
            elif re.search(r"mtAnswer\s*\(\s*this\s*,\s*true", onclick):
                correct_idx = i

        if len(opts) < 2:
            continue

        fb_right = fb_wrong = ""
        for fb in box.find_all(["div"], class_=re.compile(r"quiz-feedback|mt-feedback")):
            cls = " ".join(fb.get("class", []))
            txt = fb.get_text(" ", strip=True)
            if "right" in cls:   fb_right = txt
            elif "wrong" in cls: fb_wrong = txt

        questions.append({"q": q_text, "opts": opts, "correct_idx": correct_idx,
                          "fb_right": fb_right, "fb_wrong": fb_wrong})

    if questions:
        return questions

    # ── OLD FORMAT: div.mt-question (or bare mt-q siblings) ────────
    # Questions may be direct children or inside div.mt-question wrappers
    wrappers = mt_page.find_all("div", class_="mt-question")
    if not wrappers:
        # Fallback: find all mt-q divs and treat each as a question root
        wrappers = mt_page.find_all("div", class_="mt-q")

    for wrap in wrappers:
        # If this IS the mt-q div itself, grab siblings; else find child mt-q
        if "mt-q" in wrap.get("class", []):
            q_el = wrap
        else:
            q_el = wrap.find("div", class_="mt-q")
        if not q_el:
            continue
        q_text = re.sub(r"^\d+\.\s*", "", q_el.get_text(" ", strip=True))

        # opts may be in wrap or sibling
        opts_el = wrap.find("div", class_="mt-opts") if "mt-q" not in wrap.get("class",[]) else None
        if not opts_el:
            # try next sibling pattern
            nxt = q_el.find_next_sibling("div", class_="mt-opts")
            if nxt:
                opts_el = nxt

        if not opts_el:
            continue

        opts, correct_idx = [], 0
        for i, btn in enumerate(opts_el.find_all("button", class_="mt-opt")):
            onclick = btn.get("onclick", "")
            opts.append(btn.get_text(" ", strip=True))
            # old format: mtAnswer(this, true, ...) or mtAnswer(this,true,...)
            if re.search(r"mtAnswer\s*\(\s*this\s*,\s*true", onclick):
                correct_idx = i

        if len(opts) < 2:
            continue

        fb_right = fb_wrong = ""
        parent = wrap.parent if "mt-q" in wrap.get("class",[]) else wrap
        for fb in parent.find_all("div", class_=re.compile(r"mt-feedback")):
            cls = " ".join(fb.get("class", []))
            txt = fb.get_text(" ", strip=True)
            if "right" in cls:   fb_right = txt or "Correct."
            elif "wrong" in cls: fb_wrong = txt or "Incorrect."

        questions.append({"q": q_text, "opts": opts, "correct_idx": correct_idx,
                          "fb_right": fb_right or "Correct.",
                          "fb_wrong": fb_wrong or "Incorrect — review the module for more information."})

    return questions

# ------------------------------------------------------------------
def esc(s):
    return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"','&quot;')

def build_questions_html(questions):
    parts = []
    for i, q in enumerate(questions, 1):
        qid = f"fe{i}"
        opts_html = ""
        for j, opt in enumerate(q["opts"]):
            marker = "correct" if j == q["correct_idx"] else "wrong"
            opts_html += f'        <button class="quiz-opt" onclick="feAnswer(this,\'{marker}\',\'{qid}\')">{esc(opt)}</button>\n'

        parts.append(f'''
    <div class="quiz-box" id="{qid}">
      <div class="quiz-q">{i}. {esc(q["q"])}</div>
      <div class="quiz-opts">
{opts_html.rstrip()}
      </div>
      <div class="quiz-feedback right">{esc(q["fb_right"])}</div>
      <div class="quiz-feedback wrong">{esc(q["fb_wrong"])}</div>
    </div>''')
    return "\n".join(parts)

# ------------------------------------------------------------------
HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__ — Final Exam</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Crimson+Pro:ital,wght@0,400;0,600;1,400&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root{
  --bg:#0d1117;--surface:#161b22;--border-dark:#21262d;
  --accent:#c9a05a;--accent-rgb:201,160,90;
  --muted:#8b949e;--text:#e6edf3;
  --green:#4fcf8a;--red:#f07070;--blue:#38bdf8;
}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--text);font-family:Inter,sans-serif;min-height:100vh;display:flex;flex-direction:column}
.exam-header{background:var(--surface);border-bottom:1px solid var(--border-dark);padding:1.5rem 2rem;text-align:center}
.exam-header h1{font-family:'Crimson Pro',Georgia,serif;font-size:1.6rem;font-weight:600;color:#fff;font-style:italic;margin-bottom:0.25rem}
.exam-header .tagline{font-size:0.8rem;color:var(--muted)}
.exam-header .course-name{font-size:0.9rem;color:var(--accent);font-weight:600;margin-bottom:0.5rem}
.exam-body{width:90%;max-width:860px;margin:0 auto;padding:1.5rem 0 3rem;flex:1}
.quiz-box{background:rgba(var(--accent-rgb),0.02);border:1px solid var(--border-dark);border-radius:6px;padding:1.25rem 1.5rem;margin-bottom:1rem}
.quiz-q{font-family:'Crimson Pro',Georgia,serif;font-size:1rem;font-weight:600;color:#fff;margin-bottom:0.85rem;line-height:1.45}
.quiz-opts{display:flex;flex-direction:column;gap:0.5rem}
.quiz-opt{background:transparent;border:1px solid var(--border-dark);color:#6e6861;padding:0.65rem 1rem;border-radius:4px;font-family:inherit;font-size:0.82rem;cursor:pointer;text-align:left;transition:all 0.15s;font-weight:500}
.quiz-opt:hover:not(:disabled){border-color:var(--accent);color:#e8e3db;background:rgba(var(--accent-rgb),0.04)}
.quiz-opt.correct{border-color:#4fcf8a;background:rgba(79,207,138,0.06);color:#4fcf8a}
.quiz-opt.wrong{border-color:#f07070;background:rgba(240,112,112,0.05);color:#f07070}
.quiz-feedback{margin-top:0.75rem;font-size:0.8rem;line-height:1.6;padding:0.65rem 0.85rem;border-radius:4px;display:none!important}
.quiz-feedback.show{display:block!important}
.quiz-feedback.right{background:rgba(56,189,248,0.08);border:1px solid rgba(56,189,248,0.25);color:#38bdf8}
.quiz-feedback.wrong{background:rgba(240,112,112,0.05);border:1px solid rgba(240,112,112,0.15);color:#f07070}
.submit-row{text-align:center;margin:2rem 0 1rem}
.submit-btn{background:var(--accent);color:#0d1117;border:none;padding:0.85rem 2.5rem;border-radius:6px;font-family:inherit;font-size:0.95rem;font-weight:600;cursor:pointer;transition:opacity 0.2s}
.submit-btn:hover{opacity:0.85}
.submit-btn:disabled{opacity:0.4;cursor:not-allowed}
.result-panel{display:none;background:var(--surface);border:1px solid var(--border-dark);border-radius:8px;padding:2rem;text-align:center;margin:2rem 0}
.result-panel.show{display:block}
.result-score{font-size:3rem;font-weight:700;margin-bottom:0.5rem}
.result-score.pass{color:var(--green)}
.result-score.fail{color:var(--red)}
.result-label{font-family:'Crimson Pro',Georgia,serif;font-size:1.3rem;color:#fff;margin-bottom:0.75rem}
.result-msg{font-size:0.88rem;color:var(--muted);line-height:1.6;max-width:520px;margin:0 auto}
.progress-bar{height:6px;background:var(--border-dark);border-radius:3px;margin:1rem 0 0.5rem;overflow:hidden}
.progress-fill{height:100%;background:var(--accent);border-radius:3px;transition:width 0.3s}
.progress-label{font-size:0.75rem;color:var(--muted);text-align:right}
@media(max-width:600px){.exam-body{padding:1rem 1.25rem 2rem}}
</style>
</head>
<body>
<div class="exam-header">
  <div class="course-name">__TITLE__</div>
  <h1 id="examTitle">Final Exam</h1>
  <div class="tagline" id="examTagline">__QCOUNT__ questions &middot; <span id="threshDisplay">70</span>% to pass</div>
</div>

<div class="exam-body">
  <div class="progress-bar"><div class="progress-fill" id="progressFill" style="width:0%"></div></div>
  <div class="progress-label" id="progressLabel">0 of __QCOUNT__ answered</div>

__QUESTIONS__

  <div class="submit-row">
    <button class="submit-btn" id="submitBtn" onclick="submitExam()" disabled>Submit Exam</button>
  </div>

  <div class="result-panel" id="resultPanel">
    <div class="result-score" id="resultScore"></div>
    <div class="result-label" id="resultLabel"></div>
    <div class="result-msg"   id="resultMsg"></div>
  </div>
</div>

<script>
var COURSE_ID = '__CID__';
var Q_COUNT   = __QCOUNT__;
var STANDARD_THRESH = 70;
var TESTOUT_THRESH  = 80;

var params     = new URLSearchParams(window.location.search);
var IS_TESTOUT = params.get('mode') === 'testout';
var THRESH     = IS_TESTOUT ? TESTOUT_THRESH : STANDARD_THRESH;

// Guard: test-out is one-shot — if already attempted, lock immediately
if (IS_TESTOUT) {
  var _existing = null;
  try { _existing = JSON.parse(localStorage.getItem('aesop-final-' + COURSE_ID)); } catch(e) {}
  if (_existing && _existing.path === 'testout' && _existing.attempted) {
    document.getElementById('examTitle').textContent  = 'Bypass Exam — Already Attempted';
    document.getElementById('examTagline').textContent = 'You have already used your one bypass attempt for this course.';
    document.getElementById('submitBtn').disabled = true;
    document.querySelectorAll('.quiz-opt').forEach(function(b){ b.disabled = true; });
  }
}

if (IS_TESTOUT) {
  document.getElementById('examTitle').textContent = 'Bypass Exam';
  document.getElementById('threshDisplay').textContent = '80';
  document.getElementById('examTagline').innerHTML =
    Q_COUNT + ' questions · 80% to pass · One attempt only';
}

var answered = {};

function feAnswer(btn, result, qid) {
  var box = document.getElementById(qid);
  if (box.dataset.done) return;
  box.dataset.done = '1';
  box.querySelectorAll('.quiz-opt').forEach(function(b) {
    b.disabled = true;
    if (b === btn) b.classList.add(result === 'correct' ? 'correct' : 'wrong');
  });
  box.querySelectorAll('.quiz-feedback').forEach(function(fb) {
    if ((result === 'correct' && fb.classList.contains('right')) ||
        (result !== 'correct' && fb.classList.contains('wrong'))) {
      fb.classList.add('show');
    }
  });
  answered[qid] = result;
  updateProgress();
}

function updateProgress() {
  var count = Object.keys(answered).length;
  var pct   = Math.round(count / Q_COUNT * 100);
  document.getElementById('progressFill').style.width  = pct + '%';
  document.getElementById('progressLabel').textContent = count + ' of ' + Q_COUNT + ' answered';
  document.getElementById('submitBtn').disabled = (count < Q_COUNT);
}

function submitExam() {
  var correct = Object.values(answered).filter(function(v){ return v === 'correct'; }).length;
  var score   = Math.round(correct / Q_COUNT * 100);
  var passed  = score >= THRESH;
  var key     = 'aesop-final-' + COURSE_ID;

  var record = {
    attempted:   true,
    passed:      passed,
    score:       score,
    correct:     correct,
    total:       Q_COUNT,
    path:        IS_TESTOUT ? 'testout' : 'standard',
    completedAt: new Date().toISOString()
  };
  localStorage.setItem(key, JSON.stringify(record));

  window.parent.postMessage({
    type:     passed ? 'finalExamPassed' : 'finalExamFailed',
    courseId: COURSE_ID,
    score:    score,
    passed:   passed,
    path:     IS_TESTOUT ? 'testout' : 'standard'
  }, '*');

  showResult(score, passed);
}

function showResult(score, passed) {
  document.getElementById('submitBtn').style.display = 'none';
  var scoreEl = document.getElementById('resultScore');
  var labelEl = document.getElementById('resultLabel');
  var msgEl   = document.getElementById('resultMsg');
  scoreEl.textContent = score + '%';
  scoreEl.className   = 'result-score ' + (passed ? 'pass' : 'fail');
  if (passed) {
    if (IS_TESTOUT) {
      labelEl.textContent = 'Bypass Complete';
      msgEl.textContent   = 'You passed the bypass exam at ' + score + '%. Course credit has been applied at 50% of the standard point value. The full course remains available if you want to go deeper.';
    } else {
      labelEl.textContent = 'Exam Passed — Course Complete';
      msgEl.textContent   = 'You scored ' + score + '% and have earned full course credit. Congratulations on completing the course.';
    }
  } else {
    if (IS_TESTOUT) {
      labelEl.textContent = 'Bypass Attempt Failed';
      msgEl.textContent   = 'You scored ' + score + '% — the bypass threshold is 80%. This was your one bypass attempt. Begin the course from Module 1 to earn full credit.';
    } else {
      labelEl.textContent = 'Not Quite — Review and Retry';
      msgEl.textContent   = 'You scored ' + score + '%. You need ' + THRESH + '% to pass. Review the modules and try the exam again when you\'re ready.';
    }
  }
  document.getElementById('resultPanel').classList.add('show');
  document.getElementById('resultPanel').scrollIntoView({behavior:'smooth', block:'center'});
}
</script>
</body>
</html>
"""

# ------------------------------------------------------------------
def build_final_exam(slug: str, title: str, module_paths: list, dry_run: bool) -> bool:
    rng = random.Random(RANDOM_SEED)

    all_questions = []
    for mp in module_paths:
        qs = extract_mt_questions(mp)
        all_questions.extend(qs)

    if not all_questions:
        print(f"  ✗ {slug}: no MT questions found in {len(module_paths)} module(s)")
        return False

    rng.shuffle(all_questions)
    questions = all_questions[:MAX_QUESTIONS]
    q_count   = len(questions)

    questions_html = build_questions_html(questions)

    html = (HTML_TEMPLATE
        .replace("__TITLE__",  esc(title))
        .replace("__CID__",    slug)
        .replace("__QCOUNT__", str(q_count))
        .replace("__QUESTIONS__", questions_html)
    )

    out_path = MODULES / slug / f"{slug}-final.html"
    if not dry_run:
        out_path.write_text(html, encoding="utf-8", newline="\n")
    print(f"  {'[dry] ' if dry_run else ''}✓ {slug}-final.html  ({q_count}q / {len(all_questions)} available, {len(module_paths)} modules)")
    return True

# ------------------------------------------------------------------
def main():
    dry_run = "--dry-run" in sys.argv

    reg  = load_registry()
    live = [(slug, v) for slug, v in reg.items() if v.get("status") == "live"]
    print(f"Live courses: {len(live)}")
    if dry_run:
        print("DRY RUN — no files written\n")

    built        = 0
    skipped      = 0
    no_questions = 0

    for slug, entry in sorted(live):
        title      = entry.get("title", slug)
        module_ids = entry.get("modules", [])
        course_dir = MODULES / slug

        if not course_dir.exists():
            print(f"  ✗ {slug}: directory missing")
            skipped += 1
            continue

        final_path = course_dir / f"{slug}-final.html"
        if final_path.exists():
            skipped += 1
            continue  # already built — silent skip

        # Resolve module HTML paths
        module_paths = []
        for mid in module_ids:
            mp = course_dir / f"{mid}.html"
            if mp.exists():
                module_paths.append(mp)

        if not module_paths:
            module_paths = sorted(course_dir.glob(f"{slug}-m*.html"))

        if not module_paths:
            print(f"  ✗ {slug}: no module HTML files")
            skipped += 1
            continue

        ok = build_final_exam(slug, title, module_paths, dry_run)
        if ok:
            built += 1
            if not dry_run:
                reg[slug]["final"]       = f"{slug}-final"
                reg[slug]["noTestout"]   = slug in FOUNDATIONS_IDS
        else:
            no_questions += 1

    print(f"\n{'DRY RUN ' if dry_run else ''}Results:")
    print(f"  Built:        {built}")
    print(f"  Skipped:      {skipped}  (already exist or no files)")
    print(f"  No MT data:   {no_questions}")

    if not dry_run and built > 0:
        save_registry(reg)
        print(f"\nNext: git add ai-academy/modules && git commit -m 'feat: generate final exams for {built} courses'")

if __name__ == "__main__":
    main()
