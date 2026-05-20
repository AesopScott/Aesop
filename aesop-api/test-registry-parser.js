#!/usr/bin/env node
/**
 * Test Registry Parser
 * Proof Unit #2: Verify course parsing works correctly
 */

import { parseCoursesV2, getCoverageSummary } from './lib/registry-parser.js';

try {
  console.log('Testing courses-v2.html parser...\n');

  const courses = parseCoursesV2();
  console.log(`✓ Parsed ${courses.length} courses from courses-v2.html`);

  if (courses.length < 5) {
    console.error(`✗ Expected at least 5 courses, got ${courses.length}`);
    process.exit(1);
  }

  // Verify course structure
  const course = courses[0];
  const requiredFields = ['id', 'title', 'slug', 'description', 'modules', 'audience', 'topics'];
  const missing = requiredFields.filter(field => !(field in course));

  if (missing.length > 0) {
    console.error(`✗ Missing fields: ${missing.join(', ')}`);
    process.exit(1);
  }

  console.log(`✓ Course structure valid`);
  console.log(`  - Sample course: "${courses[0].title}"`);
  console.log(`  - Modules: ${courses[0].modules.length}`);
  console.log(`  - Audience: ${courses[0].audience.join(', ')}`);
  console.log(`  - Topics: ${courses[0].topics.join(', ')}`);

  // Get summary
  const summary = getCoverageSummary();
  console.log(`\n✓ Coverage summary generated`);
  console.log(`  - Total courses: ${summary.totalCourses}`);
  console.log(`  - By version: v1=${summary.byVersion.v1}, v2=${summary.byVersion.v2}`);
  console.log(`  - Topic coverage: ${Object.keys(summary.byTopic).length} distinct topics`);

  console.log('\n✓ Registry parser OK');
  process.exit(0);
} catch (error) {
  console.error(`✗ Failed: ${error.message}`);
  process.exit(1);
}
