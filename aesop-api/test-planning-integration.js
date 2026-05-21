#!/usr/bin/env node
/**
 * Test Planning Phase Integration
 * Proof Unit #7: Full research → recommendations → approval flow
 */

import {
  developCoursePlanning,
  processPlanningApprovals,
  displayRecommendations,
} from './lib/course-development-assistant.js';

async function test() {
  console.log('Testing planning phase integration...\n');

  try {
    // Step 1: Develop course planning (research + recommendations)
    console.log('Step 1: Developing course planning with research...\n');
    const planning = await developCoursePlanning('AI Ethics for High School');

    // Verify structure
    if (!planning.recommendations || !Array.isArray(planning.recommendations)) {
      throw new Error('Planning recommendations missing or not an array');
    }

    console.log(`✓ Planning package generated with ${planning.recommendations.length} recommendations\n`);

    // Step 2: Display recommendations
    console.log('Step 2: Displaying recommendations to user...\n');
    const display = displayRecommendations(planning);
    console.log(display);

    // Step 3: Simulate user approvals
    console.log('Step 3: Processing user approvals...\n');

    const userApprovals = [
      { approved: true }, // target_audience: approve
      { approved: false, userValue: 'AI Ethics, Decision Making, Governance, Policy' }, // core_topics: modify
      { approved: true }, // module_structure: approve
      { approved: true }, // assessment_approach: approve
      { approved: true }, // prerequisites: approve
    ];

    const finalParams = processPlanningApprovals(planning, userApprovals);

    console.log('✓ User approvals processed\n');
    console.log('Final approved planning parameters:');
    console.log(JSON.stringify(finalParams.parameters, null, 2));

    if (finalParams.approvalNotes.length > 0) {
      console.log('\nApproval notes:');
      finalParams.approvalNotes.forEach(note => console.log(`  ${note}`));
    }

    // Verify all parameters populated
    const requiredParams = [
      'target_audience',
      'core_topics',
      'module_structure',
      'assessment_approach',
      'prerequisites',
    ];
    const missingParams = requiredParams.filter(p => !(p in finalParams.parameters));

    if (missingParams.length > 0) {
      throw new Error(`Missing parameters: ${missingParams.join(', ')}`);
    }

    console.log('\n✓ All required parameters present');
    console.log('✓ Planning phase integration OK');
    process.exit(0);
  } catch (error) {
    console.error(`\n✗ Failed: ${error.message}`);
    process.exit(1);
  }
}

test();
