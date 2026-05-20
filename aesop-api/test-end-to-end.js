#!/usr/bin/env node
/**
 * End-to-End Test
 * Proof Unit #8: Full course development workflow
 * research → recommendations → approval → ready for course generation
 */

import { developCoursePlanning, processPlanningApprovals } from './lib/course-development-assistant.js';

async function test() {
  console.log('\n' + '='.repeat(70));
  console.log('END-TO-END COURSE DEVELOPMENT TEST');
  console.log('='.repeat(70) + '\n');

  try {
    // Test 1: Develop planning for a real course concept
    console.log('TEST 1: Course Development (Research + Recommendations)\n');

    const courseConcept = 'Cybersecurity Fundamentals for Beginners';
    console.log(`Concept: "${courseConcept}"\n`);

    const planning = await developCoursePlanning(courseConcept);

    console.log(`✓ Planning developed with ${planning.recommendations.length} recommendations\n`);

    // Test 2: Simulate user approvals
    console.log('TEST 2: User Approval Flow\n');

    const userApprovals = [
      { approved: true },
      { approved: true },
      { approved: false, userValue: '8 modules: Intro, Security Basics, Threats, Defense, Cryptography, Networks, Tools, Labs' },
      { approved: true },
      { approved: true },
    ];

    const finalParams = processPlanningApprovals(planning, userApprovals);

    console.log('Approval summary:');
    finalParams.approvalNotes.forEach(note => console.log(`  ${note}`));

    // Test 3: Verify readiness for course generation
    console.log('\nTEST 3: Readiness for Course Generation\n');

    const requiredParams = [
      'target_audience',
      'core_topics',
      'module_structure',
      'assessment_approach',
      'prerequisites',
    ];

    let readyForGeneration = true;
    requiredParams.forEach(param => {
      const hasValue = param in finalParams.parameters && finalParams.parameters[param];
      const status = hasValue ? '✓' : '✗';
      console.log(`  ${status} ${param}: ${hasValue ? 'present' : 'MISSING'}`);
      if (!hasValue) readyForGeneration = false;
    });

    if (!readyForGeneration) {
      throw new Error('Not all parameters present for course generation');
    }

    console.log('\n✓ Ready for course generation\n');

    // Test 4: Simulate course generation call
    console.log('TEST 4: Course Generation Parameters\n');

    const generationPayload = {
      courseConcept: finalParams.courseConcept,
      parameters: finalParams.parameters,
      generatedAt: new Date().toISOString(),
    };

    console.log('Payload for course builder:');
    console.log(JSON.stringify(generationPayload, null, 2));

    console.log('\n' + '='.repeat(70));
    console.log('✓ END-TO-END WORKFLOW COMPLETE');
    console.log('='.repeat(70));
    console.log('\nWorkflow Summary:');
    console.log('  1. Research identified existing courses and gaps');
    console.log('  2. Recommendations generated for 5 planning areas');
    console.log('  3. User reviewed and approved/modified recommendations');
    console.log('  4. Final parameters assembled for course generation');
    console.log('  5. Ready to pass to /aesop-course-builder for HTML generation\n');

    process.exit(0);
  } catch (error) {
    console.error(`\n✗ End-to-end test failed: ${error.message}\n`);
    process.exit(1);
  }
}

test();
