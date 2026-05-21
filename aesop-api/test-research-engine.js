#!/usr/bin/env node
/**
 * Test Research Engine
 * Proof Unit #4: Verify research engine returns structured findings
 */

import { runResearch } from './lib/research-engine.js';

async function test() {
  console.log('Testing research engine...\n');

  try {
    // Run research on a sample course concept
    const findings = await runResearch('Python Basics for Beginners');

    // Verify structure
    console.log('✓ Research findings generated\n');

    const requiredFields = [
      'audienceGaps',
      'topicCoverage',
      'structuralPatterns',
      'prerequisites',
      'researchSources',
      'timestamp',
    ];

    const missing = requiredFields.filter(field => !(field in findings));

    if (missing.length > 0) {
      console.error(`✗ Missing fields: ${missing.join(', ')}`);
      process.exit(1);
    }

    console.log('✓ All required fields present:');
    console.log(`  - audienceGaps: ${findings.audienceGaps.length} segments`);
    console.log(`  - topicCoverage: ${findings.topicCoverage.length} topics`);
    console.log(`  - structuralPatterns: ${findings.structuralPatterns.averageModulesPerCourse} avg modules`);
    console.log(`  - prerequisites: ${findings.prerequisites.length} skills`);
    console.log(`  - researchSources: ${findings.researchSources.length} sources`);
    console.log(`  - timestamp: ${findings.timestamp}`);

    // Verify field types
    if (!Array.isArray(findings.audienceGaps)) {
      throw new Error('audienceGaps must be an array');
    }
    if (!Array.isArray(findings.topicCoverage)) {
      throw new Error('topicCoverage must be an array');
    }
    if (typeof findings.structuralPatterns !== 'object') {
      throw new Error('structuralPatterns must be an object');
    }

    console.log('\n✓ Research engine OK');
    process.exit(0);
  } catch (error) {
    console.error(`✗ Failed: ${error.message}`);
    process.exit(1);
  }
}

test();
