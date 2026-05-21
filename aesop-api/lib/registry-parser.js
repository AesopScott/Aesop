/**
 * Registry Parser — Extracts course metadata from courses-v2.html and courses.html
 * Used by research engine to identify course coverage, gaps, and patterns
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = path.join(__dirname, '../../');

/**
 * Parse courses-v2.html
 * Extracts: course title, slug, blurb, modules, assessment types
 */
export function parseCoursesV2() {
  const filePath = path.join(PROJECT_ROOT, 'ai-academy', 'courses-v2.html');

  if (!fs.existsSync(filePath)) {
    throw new Error(`courses-v2.html not found at ${filePath}`);
  }

  const html = fs.readFileSync(filePath, 'utf8');
  const courses = [];

  // Regex to extract each course block: <li>...course content...<li>
  const courseBlockRegex = /<li>\s*<button[^>]*>.*?<\/div>\s*<\/li>/gs;
  const blocks = html.match(courseBlockRegex) || [];

  blocks.forEach((block, index) => {
    // Extract course name
    const nameMatch = block.match(/<div class="cnav-name">([^<]+)<\/div>/);
    const name = nameMatch ? nameMatch[1].trim() : null;

    if (!name) return; // Skip if no name found

    // Extract blurb
    const blurbMatch = block.match(/<div class="cnav-blurb">([^<]+)<\/div>/);
    const blurb = blurbMatch ? blurbMatch[1].trim() : '';

    // Extract metadata (modules count, lab types)
    const metaMatch = block.match(/<div class="cnav-meta">([^<]+)<\/div>/);
    const meta = metaMatch ? metaMatch[1].trim() : '';

    // Parse meta for module count and lab types
    const moduleCountMatch = meta.match(/(\d+)\s+modules?/i);
    const moduleCount = moduleCountMatch ? parseInt(moduleCountMatch[1], 10) : 0;
    const hasDebate = /debate/i.test(meta);
    const hasSkill = /skill/i.test(meta);
    const hasBuild = /build/i.test(meta);

    // Extract course slug from module hrefs (e.g., /ai-academy/modules/v2/{slug}/m1.html)
    const slugMatch = block.match(/\/ai-academy\/modules\/v2\/([^\/]+)\//);
    const slug = slugMatch ? slugMatch[1] : null;

    // Extract module titles
    const modules = [];
    const moduleRegex = /<span class="cnav-mod-title">([^<]+)<\/span>/g;
    let moduleMatch;
    while ((moduleMatch = moduleRegex.exec(block)) !== null) {
      modules.push(moduleMatch[1].trim());
    }

    // Extract assessment types present
    const assessmentTypes = [];
    if (hasDebate) assessmentTypes.push('debate');
    if (hasSkill) assessmentTypes.push('skill');
    if (hasBuild) assessmentTypes.push('build');

    if (name && slug) {
      courses.push({
        id: `v2-${slug}`,
        version: 'v2',
        title: name,
        slug: slug,
        description: blurb,
        moduleCount: moduleCount,
        modules: modules,
        assessmentTypes: assessmentTypes,
        audience: extractAudience(blurb), // Infer from description
        topics: extractTopics(name, blurb), // Infer from title and description
      });
    }
  });

  return courses;
}

/**
 * Parse courses.html (v1 courses)
 * Simpler structure than v2; returns course metadata
 */
export function parseCoursesV1() {
  const filePath = path.join(PROJECT_ROOT, 'ai-academy', 'courses.html');

  if (!fs.existsSync(filePath)) {
    // v1 may not exist if project is v2-only
    return [];
  }

  const html = fs.readFileSync(filePath, 'utf8');
  const courses = [];

  // courses.html uses core-panel divs: <div class="core-panel" data-course="slug">
  const panelRegex = /<div class="core-panel"[^>]*data-course="([^"]+)"[^>]*>([\s\S]*?)(?=<div class="core-panel"|$)/g;
  let match;

  while ((match = panelRegex.exec(html)) !== null) {
    const slug = match[1];
    const block = match[2];

    const titleMatch = block.match(/<div class="core-panel__title">([^<]+)<\/div>/);
    const title = titleMatch ? titleMatch[1].trim() : slug;

    const descMatch = block.match(/<div class="core-panel__desc">([^<]+)<\/div>/);
    const description = descMatch ? descMatch[1].trim() : '';

    const modCountMatch = block.match(/<span class="core-badge-mods">(\d+)\s+Modules?<\/span>/i);
    const moduleCount = modCountMatch ? parseInt(modCountMatch[1], 10) : 0;

    const modules = [];
    const modTitleRegex = /<div class="core-mod__title">([^<]+)<\/div>/g;
    let modMatch;
    while ((modMatch = modTitleRegex.exec(block)) !== null) {
      modules.push(modMatch[1].trim());
    }

    courses.push({
      id: `v1-${slug}`,
      version: 'v1',
      title,
      slug,
      description,
      moduleCount,
      modules,
      assessmentTypes: [],
      audience: extractAudience(description),
      topics: extractTopics(title, description),
    });
  }

  return courses;
}

/**
 * Infer audience from course description
 */
function extractAudience(description) {
  const audiences = [];

  if (/student|learner|beginner|introductory|basic|foundational/i.test(description)) {
    audiences.push('beginner');
  }
  if (/intermediate|advanced|professional|expert|practitioner/i.test(description)) {
    audiences.push('intermediate');
  }
  if (/advanced|expert|specialized|deep|architecture/i.test(description)) {
    audiences.push('advanced');
  }
  if (/developer|engineer|architect|builder|technical/i.test(description)) {
    audiences.push('technical');
  }
  if (/business|manager|leader|stakeholder|decision/i.test(description)) {
    audiences.push('business');
  }

  return audiences.length > 0 ? audiences : ['general'];
}

/**
 * Extract topic keywords from course title and description
 */
function extractTopics(title, description) {
  const keywords = [];
  const fullText = `${title} ${description}`.toLowerCase();

  // Common AI/course topics
  const topics = [
    'ai', 'agent', 'ethics', 'building', 'brainstorming', 'rag',
    'pipeline', 'governance', 'command center', 'prompt', 'models',
    'evaluation', 'testing', 'security', 'creativity', 'careers',
    'society', 'decision', 'policy', 'oversight', 'reasoning',
    'healthcare', 'education', 'finance', 'media', 'leadership',
  ];

  topics.forEach(topic => {
    if (fullText.includes(topic)) {
      keywords.push(topic);
    }
  });

  return keywords.length > 0 ? keywords : [];
}

/**
 * Get all courses from both v1 and v2
 */
export function getAllCourses() {
  const v1 = parseCoursesV1();
  const v2 = parseCoursesV2();
  return [...v1, ...v2];
}

/**
 * Build course coverage map: { topic: [courseIds], audience: [courseIds], ... }
 */
export function getCoverageSummary() {
  const courses = getAllCourses();
  const summary = {
    totalCourses: courses.length,
    byVersion: { v1: 0, v2: 0 },
    byAudience: {},
    byTopic: {},
    byAssessmentType: {},
  };

  courses.forEach(course => {
    // Count by version
    if (course.version === 'v1') summary.byVersion.v1++;
    else summary.byVersion.v2++;

    // Count by audience
    course.audience.forEach(aud => {
      if (!summary.byAudience[aud]) summary.byAudience[aud] = [];
      summary.byAudience[aud].push(course.id);
    });

    // Count by topic
    course.topics.forEach(topic => {
      if (!summary.byTopic[topic]) summary.byTopic[topic] = [];
      summary.byTopic[topic].push(course.id);
    });

    // Count by assessment type
    course.assessmentTypes.forEach(type => {
      if (!summary.byAssessmentType[type]) summary.byAssessmentType[type] = [];
      summary.byAssessmentType[type].push(course.id);
    });
  });

  return summary;
}

export default {
  parseCoursesV2,
  parseCoursesV1,
  getAllCourses,
  getCoverageSummary,
};
