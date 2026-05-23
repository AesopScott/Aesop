// Pathway display — AESOP AI Academy
// Renders a recommended learning pathway on the student dashboard.
// Called from students.html after loading the learner's Firestore record.

const DIFFICULTY_LABEL = {
  beginner:     { text: 'Beginner',     color: '#2ba898' },
  intermediate: { text: 'Intermediate', color: '#9a5fb0' },
  advanced:     { text: 'Advanced',     color: '#c0384f' },
};

/**
 * Render pathway into a container element.
 *
 * @param {string}  containerId  - DOM element ID to render into
 * @param {Object}  pathway      - recommendedPathway from Firestore
 */
export function renderPathway(containerId, pathway) {
  const container = document.getElementById(containerId);
  if (!container) return;

  if (!pathway || !pathway.primaryCourse) {
    container.innerHTML = `
      <p style="color:var(--ink-muted,#718096);font-size:0.9rem;margin:0">
        No pathway yet. <a href="/ai-academy/assessment.html" style="color:var(--teal-dark,#2ba898)">Take the assessment</a> to get a personalized recommendation.
      </p>`;
    return;
  }

  const { primaryCourse, followUpCourses = [], reasoningBrief = '', aptitudeBand = '' } = pathway;

  const bandBadge = aptitudeBand
    ? `<span style="
        display:inline-block;padding:2px 10px;border-radius:12px;
        font-size:0.72rem;font-weight:700;letter-spacing:0.04em;
        background:var(--gold-pale,#f5e9d0);color:var(--ink-mid,#2c3e50);
        margin-left:0.5rem;vertical-align:middle;
      ">${aptitudeBand.charAt(0).toUpperCase() + aptitudeBand.slice(1)}</span>`
    : '';

  const primaryHTML = renderCourseCard(primaryCourse, true);
  const followUpHTML = followUpCourses.length > 0
    ? `<div style="margin-top:1rem">
        <div style="font-size:0.78rem;color:var(--ink-muted,#718096);font-weight:600;letter-spacing:0.06em;text-transform:uppercase;margin-bottom:0.6rem">
          Suggested Next
        </div>
        <div style="display:flex;flex-direction:column;gap:0.5rem">
          ${followUpCourses.map(c => renderCourseCard(c, false)).join('')}
        </div>
      </div>`
    : '';

  container.innerHTML = `
    <div>
      ${reasoningBrief
        ? `<p style="font-size:0.85rem;color:var(--ink-light,#4a5568);margin:0 0 1rem 0;line-height:1.6">
            ${reasoningBrief}${bandBadge}
           </p>`
        : ''}
      ${primaryHTML}
      ${followUpHTML}
      <div style="margin-top:1rem;padding-top:0.75rem;border-top:1px solid var(--border-light,#ede8df)">
        <a href="/ai-academy/assessment.html"
           style="font-size:0.8rem;color:var(--ink-muted,#718096);text-decoration:none">
          Retake assessment to update pathway →
        </a>
      </div>
    </div>`;
}

/** @private */
function renderCourseCard(course, isPrimary) {
  const diff = DIFFICULTY_LABEL[course.difficulty] || DIFFICULTY_LABEL.beginner;
  const skills = (course.skillsFocused || []).slice(0, 3);
  const skillPills = skills.map(s =>
    `<span style="
      display:inline-block;padding:1px 8px;border-radius:10px;font-size:0.72rem;
      background:rgba(61,214,192,0.1);color:var(--teal-dark,#2ba898);margin-right:4px
    ">${s}</span>`
  ).join('');

  const prereqs = (course.prerequisites || []);
  const prereqNote = prereqs.length > 0
    ? `<div style="font-size:0.75rem;color:var(--ink-muted,#718096);margin-top:0.3rem">
        Prereq: ${prereqs.join(', ')}
       </div>`
    : '';

  return `
    <a href="${course.path || '/ai-academy/courses.html'}"
       style="
         display:block;padding:${isPrimary ? '1rem' : '0.65rem 0.85rem'};
         background:${isPrimary ? 'var(--cream,#faf8f4)' : 'white'};
         border:${isPrimary ? '2px solid var(--teal-dark,#2ba898)' : '1px solid var(--border,#e2d9cc)'};
         border-radius:8px;text-decoration:none;
         transition:border-color 0.15s,box-shadow 0.15s;
       "
       onmouseover="this.style.boxShadow='0 2px 8px rgba(0,0,0,0.08)'"
       onmouseout="this.style.boxShadow=''"
    >
      <div style="display:flex;align-items:flex-start;justify-content:space-between;gap:0.5rem">
        <div style="font-weight:${isPrimary ? 700 : 600};font-size:${isPrimary ? '1rem' : '0.9rem'};color:var(--navy,#0d1b2a)">
          ${course.title}
        </div>
        <span style="
          flex-shrink:0;padding:2px 8px;border-radius:10px;font-size:0.7rem;font-weight:700;
          color:white;background:${diff.color}
        ">${diff.text}</span>
      </div>
      ${isPrimary && course.description
        ? `<div style="font-size:0.82rem;color:var(--ink-light,#4a5568);margin-top:0.35rem;line-height:1.55">
            ${course.description}
           </div>`
        : ''}
      ${skillPills ? `<div style="margin-top:0.5rem">${skillPills}</div>` : ''}
      ${prereqNote}
      ${isPrimary
        ? `<div style="margin-top:0.75rem;font-size:0.85rem;font-weight:700;color:var(--teal-dark,#2ba898)">
            Start Course →
           </div>`
        : ''}
    </a>`;
}

/**
 * Check localStorage for a completed assessment flag.
 * Returns true if the learner has taken the assessment.
 * Lightweight check for the homepage (no Firebase round-trip).
 *
 * @returns {boolean}
 */
export function hasCompletedAssessment() {
  try {
    return localStorage.getItem('aesop-assessment-complete') === '1';
  } catch (_) {
    return false;
  }
}

/**
 * Mark assessment as complete in localStorage.
 * Called from assessment-chat.js after handleAssessmentComplete.
 */
export function markAssessmentComplete() {
  try {
    localStorage.setItem('aesop-assessment-complete', '1');
  } catch (_) {}
}
