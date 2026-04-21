import json, re, shutil

# ── 1. ko/courses.html ────────────────────────────────────────────────────────
with open('ai-academy/modules/ko/courses.html', encoding='utf-8') as f:
    c = f.read()

c = c.replace('<html lang="ko">', '<html lang="ko">', 1)  # already correct

# Add KO to lang switcher
c = c.replace(
    '  <a href="#" data-lang="ar" title="العربية">AR</a>\n</div>',
    '  <a href="#" data-lang="ar" title="العربية">AR</a>\n  <div class="sep"></div>\n  <a href="#" data-lang="ko" title="한국어">KO</a>\n</div>',
    1
)
# Update LANGS array and regex
c = c.replace(
    "  var LANGS=['es','hi','ar'];\n  var EN_PATH='/ai-academy/courses.html';\n  var p=location.pathname, current='en';\n  // Detect current lang from path: /ai-academy/modules/{lang}/...\n  var m=p.match(/\\/ai-academy\\/modules\\/([a-z]{2})\\//);\n  if(m && LANGS.indexOf(m[1])!==-1) current=m[1];",
    "  var LANGS=['es','hi','ar','ko'];\n  var EN_PATH='/ai-academy/courses.html';\n  var p=location.pathname, current='en';\n  // Detect current lang from path: /ai-academy/modules/{lang}/...\n  var m=p.match(/\\/ai-academy\\/modules\\/([a-zA-Z-]+)\\//);\n  if(m && LANGS.indexOf(m[1])!==-1) current=m[1];",
    1
)

# Hero translations
c = c.replace('<h1>All <span>Literacy Courses</span></h1>', '<h1>모든 <span>과정</span></h1>', 1)
c = c.replace(
    '<p>Story-driven AI literacy for every learner. Start with the Foundations course and grow your skills one module at a time.</p>',
    '<p>모든 학습자를 위한 스토리 기반 AI 리터러시. 기초 과정에서 시작하여 모듈별로 실력을 키워보세요.</p>',
    1
)
c = c.replace('<span class="transcript-pill__label">My Progress</span>', '<span class="transcript-pill__label">나의 진도</span>', 1)
c = c.replace('<span class="transcript-pill__title">My Transcript</span>', '<span class="transcript-pill__title">학습 기록</span>', 1)
c = c.replace('<span class="transcript-pill__label">AI Curated Courses</span>', '<span class="transcript-pill__label">AI 큐레이션</span>', 1)
c = c.replace('<span class="transcript-pill__title">Pre-Approval</span>', '<span class="transcript-pill__title">사전 검토</span>', 1)

# Available Now
c = c.replace('        Available Now\n      </div>', '        현재 제공 중\n      </div>', 1)

# Badges
c = c.replace('<span class="badge badge--live"><span class="live-dot"></span> Live</span>', '<span class="badge badge--live"><span class="live-dot"></span> 진행 중</span>', 1)
c = c.replace('<span class="badge badge--gold">Start Here</span>', '<span class="badge badge--gold">여기서 시작</span>', 1)

# AI Foundations card
c = c.replace('<div class="course-card__sub">Course 1 — Foundations</div>', '<div class="course-card__sub">과정 1 — 기초</div>', 1)
c = c.replace('<h2>AI Foundations</h2>', '<h2>AI 기초</h2>', 1)
c = c.replace(
    'Your complete introduction to artificial intelligence. Learn what AI is, how it thinks, where it lives in the world, and how to use it safely — told through real stories and hands-on activities.',
    '인공지능에 대한 완벽한 입문 과정. 실제 이야기와 실습 활동을 통해 AI가 무엇인지, 어떻게 생각하는지, 세상에서 어떻게 활용되는지, 안전하게 사용하는 방법을 배웁니다.',
    1
)
c = c.replace('<strong>10 Modules</strong>', '<strong>10개 모듈</strong>', 1)
c = c.replace('<span class="course-card__cta course-card__cta--gold">Enter Course →</span>', '<span class="course-card__cta course-card__cta--gold">과정 입장 →</span>', 1)

# Foundations Advanced — LIVE for Korean
fa_card = '''
        <!-- FOUNDATIONS ADVANCED — LIVE -->
        <a href="/ai-academy/modules/ko/electives-hub.html" class="course-card course-card--live" aria-label="기초 심화 과정 입장">
          <div class="course-card__bar" style="background: linear-gradient(90deg, #2d5a8a, #4a7fb5);"></div>
          <div class="course-card__body">
            <div class="course-card__header">
              <span class="course-card__icon">🧠</span>
              <div class="course-card__badges">
                <span class="badge badge--live"><span class="live-dot"></span> 진행 중</span>
              </div>
            </div>
            <div class="course-card__sub">과정 2 — 기초 심화</div>
            <h2>기초 심화</h2>
            <p>AI 시스템의 핵심 개념을 깊이 탐구합니다. 모델 아키텍처, 학습 방법, 추론 기술과 실제 적용 사례를 다루며 고급 AI 리터러시의 토대를 마련합니다.</p>
          </div>
          <div class="course-card__footer">
            <div class="course-card__meta">
              <strong>10개 모듈</strong>
            </div>
            <span class="course-card__cta course-card__cta--gold">과정 입장 →</span>
          </div>
        </a>

'''
c = c.replace('        <!-- AI MASTERY CERTIFICATIONS -->', fa_card + '        <!-- AI MASTERY CERTIFICATIONS -->', 1)

# Certifications
c = c.replace('<h2>AI Mastery Certifications</h2>', '<h2>AI 전문 자격증</h2>', 1)
c = c.replace('<th>Credential</th>', '<th>자격</th>', 1)
c = c.replace('<th>Foundations</th>', '<th>기초</th>', 1)
c = c.replace('(Renewed Every 3 Years)', '（3년마다 갱신）', 1)
c = c.replace('(Renewed Every Year)', '（매년 갱신）', 1)
c = c.replace('<div class="cert-tier-name">Certified AI Professional</div>', '<div class="cert-tier-name">인증 AI 전문가</div>', 1)
c = c.replace('<td>Intro+</td>', '<td>입문+</td>', 1)
c = c.replace('<div class="cert-tier-name">Certified Advanced AI Professional</div>', '<div class="cert-tier-name">인증 고급 AI 전문가</div>', 1)
c = c.replace('<td>Basic+</td>', '<td>기초+</td>', 1)
c = c.replace('<div class="cert-tier-name">Certified Expert AI Professional</div>', '<div class="cert-tier-name">인증 전문 AI 전문가</div>', 1)
c = c.replace('<td>Advanced</td>', '<td>심화</td>', 1)
c = c.replace('Core Course Credits — valid 3 years', '핵심 과정 학점 — 3년 유효', 1)
c = c.replace('Active Course Credits — valid 1 year', '활성 과정 학점 — 1년 유효', 1)

# NOT AVAILABLE banner
c = c.replace(
    '<div class="not-available-banner">⚠ NOT AVAILABLE — These courses are not yet available in this language.</div>',
    '<div class="not-available-banner">⚠ 미제공 — 이 과정들은 아직 한국어로 제공되지 않습니다.</div>',
    1
)

# Core section UI
c = c.replace('Select Course <span class="arrow">▾</span>', '과정 선택 <span class="arrow">▾</span>', 1)
c = c.replace('<div class="core-panel__num">74 Courses Available</div>', '<div class="core-panel__num">74개 과정 선택 가능</div>', 1)
c = c.replace('<div class="core-panel__title">Welcome to the Course Catalog</div>', '<div class="core-panel__title">과정 목록에 오신 것을 환영합니다</div>', 1)
c = c.replace('<div class="core-panel__desc">Choose a course from the dropdown above to see its modules, progress, and details. Courses marked with a green dot are live and ready to start.</div>', '<div class="core-panel__desc">위 드롭다운에서 과정을 선택하여 모듈, 진도 및 세부 정보를 확인하세요. 녹색 점이 표시된 과정은 현재 진행 중입니다.</div>', 1)
c = c.replace('<div class="core-modules-label">Getting started</div>', '<div class="core-modules-label">시작하기</div>', 1)
c = c.replace('<div class="core-mod__title">Select a Course</div>', '<div class="core-mod__title">과정 선택</div>', 1)
c = c.replace('<div class="core-mod__sub">Use the dropdown above to browse all available courses by category</div>', '<div class="core-mod__sub">위 드롭다운으로 카테고리별 과정을 탐색하세요</div>', 1)
c = c.replace('<div class="core-mod__title">Explore Modules</div>', '<div class="core-mod__title">모듈 탐색</div>', 1)
c = c.replace('<div class="core-mod__sub">Each course contains story-driven modules with lessons, quizzes, and hands-on labs</div>', '<div class="core-mod__sub">각 과정에는 수업, 퀴즈, 실습이 포함된 스토리 기반 모듈이 있습니다</div>', 1)
c = c.replace('<div class="core-mod__title">Start Learning</div>', '<div class="core-mod__title">학습 시작</div>', 1)
c = c.replace('<div class="core-mod__sub">Click any live module to begin — your progress is tracked automatically</div>', '<div class="core-mod__sub">진행 중인 모듈을 클릭하여 시작하세요 — 진도가 자동으로 기록됩니다</div>', 1)

with open('ai-academy/modules/ko/courses.html', 'w', encoding='utf-8') as f:
    f.write(c)
print('ko/courses.html done')

# ── 2. ko/electives-hub.html ──────────────────────────────────────────────────
shutil.copy('ai-academy/modules/electives-hub.html', 'ai-academy/modules/ko/electives-hub.html')
with open('ai-academy/modules/ko/electives-hub.html', encoding='utf-8') as f:
    h = f.read()
h = h.replace('<html lang="en">', '<html lang="ko">', 1)
h = h.replace('<title>AI Electives — AESOP AI Academy</title>', '<title>AI 선택 과정 — AESOP AI 아카데미</title>', 1)
h = h.replace(
    '<a class="hdr-back" href="/ai-academy/courses.html">← All Courses</a>',
    '<a class="hdr-back" href="/ai-academy/modules/ko/courses.html">← 모든 과정</a>',
    1
)
h = h.replace('◈ Forums - Discord', '◈ 포럼 - Discord', 1)
h = h.replace(
    '<!-- Language switcher intentionally omitted from electives pages;\n     electives are English-only. Foundations pages retain siteLangSwitch. -->',
    '<!-- 한국어 선택 과정 페이지 -->',
    1
)
with open('ai-academy/modules/ko/electives-hub.html', 'w', encoding='utf-8') as f:
    f.write(h)
print('ko/electives-hub.html done')

# ── 3. course-registry.json ───────────────────────────────────────────────────
with open('ai-academy/modules/course-registry.json', encoding='utf-8') as f:
    raw = f.read().rstrip()
raw = raw[:raw.rfind('}')+1]
reg = json.loads(raw)

# Add ko to _meta.languages
meta = reg.get('_meta', {})
langs = meta.get('languages', [])
if not any(l.get('code') == 'ko' for l in langs):
    langs.append({
        "code": "ko",
        "name": "Korean",
        "nativeName": "한국어",
        "flag": "🇰🇷",
        "urlPrefix": "/ai-academy/modules/ko",
        "dir": "ltr"
    })
meta['languages'] = langs
reg['_meta'] = meta

# Add ko to foundations-advanced languages and langUrls
fa = reg.get('foundations-advanced', {})
fa_langs = fa.get('languages', [])
if 'ko' not in fa_langs:
    fa_langs.append('ko')
fa['languages'] = fa_langs
lang_urls = fa.get('langUrls', {})
lang_urls['ko'] = '/ai-academy/modules/ko/module-{n}/advanced-m{n}.html'
fa['langUrls'] = lang_urls
reg['foundations-advanced'] = fa

with open('ai-academy/modules/course-registry.json', 'w', encoding='utf-8') as f:
    json.dump(reg, f, ensure_ascii=False, indent=2)
print('course-registry.json done')

print('All done.')
