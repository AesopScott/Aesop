#!/usr/bin/env node
/**
 * CLI wrapper for the course development research pipeline.
 * Usage: node aesop-api/run-research.js "AI Ethics for High School"
 * Called by the /aesop-course-builder skill during Stage 0.
 */

import { developCoursePlanning, displayRecommendations } from './lib/course-development-assistant.js';

const concept = process.argv.slice(2).join(' ').trim();

if (!concept) {
  console.error('Usage: node run-research.js "<course concept>"');
  process.exit(1);
}

if (!process.env.ANTHROPIC_API_KEY) {
  console.error('✗ ANTHROPIC_API_KEY not set. Research requires the Anthropic API.');
  process.exit(1);
}

(async () => {
  try {
    const planningPackage = await developCoursePlanning(concept);
    console.log(displayRecommendations(planningPackage));

    // Also emit machine-readable JSON to stdout for skill consumption
    const jsonOutput = JSON.stringify(planningPackage, null, 2);
    // Write to a temp file the skill can read
    const { writeFile } = await import('fs/promises');
    await writeFile('/tmp/aesop-research-output.json', jsonOutput, 'utf8');
    console.log('\n[Research output saved to /tmp/aesop-research-output.json]\n');
  } catch (error) {
    console.error(`✗ Research failed: ${error.message}`);
    process.exit(1);
  }
})();
