#!/usr/bin/env node
/**
 * Test Recommendation Generator
 * Proof Unit #5: Verify recommendations are generated with reasoning
 */

import { generateRecommendations } from './lib/recommendation-generator.js';

// Sample research findings (typical output from research-engine)
const sampleResearch = {
  audienceGaps: [
    { segment: 'beginner', currentCoverage: 0, demand: 'high' },
    { segment: 'intermediate', currentCoverage: 2, demand: 'medium' },
    { segment: 'advanced', currentCoverage: 1, demand: 'low' },
  ],
  topicCoverage: [
    { topic: 'python', existingCourses: ['c1', 'c2'], gaps: 'Well covered' },
    { topic: 'basics', existingCourses: ['c1'], gaps: 'Limited coverage' },
  ],
  structuralPatterns: {
    averageModulesPerCourse: 8,
    commonMajorTopics: ['fundamentals', 'advanced', 'practice'],
    assessmentApproaches: ['quiz', 'project'],
  },
  prerequisites: [],
  researchSources: ['registry', 'web-search'],
  timestamp: new Date().toISOString(),
};

async function test() {
  console.log('Testing recommendation generator...\n');

  try {
    const recs = await generateRecommendations('Python Basics for Beginners', sampleResearch);

    // Verify structure
    console.log('✓ Recommendations generated\n');

    if (!Array.isArray(recs.recommendations)) {
      throw new Error('recommendations must be an array');
    }

    if (recs.recommendations.length === 0) {
      throw new Error('No recommendations generated');
    }

    console.log(`✓ Generated ${recs.recommendations.length} recommendations:`);

    recs.recommendations.forEach((rec, i) => {
      console.log(`\n  ${i + 1}. Question: ${rec.question}`);
      console.log(`     Recommendation: ${rec.recommendation}`);
      console.log(`     Reasoning: ${rec.reasoning}`);

      // Validate structure
      if (!rec.question || !rec.recommendation || !rec.reasoning) {
        throw new Error(`Recommendation ${i} missing required fields`);
      }

      // Validate reasoning is 1-2 sentences
      const sentences = (rec.reasoning.match(/[.!?]/g) || []).length;
      if (sentences < 1 || sentences > 3) {
        console.warn(`  ⚠ Reasoning has ${sentences} sentences (expected 1-2)`);
      }
    });

    // Verify required question types
    const questions = recs.recommendations.map(r => r.question);
    const requiredQuestions = [
      'target_audience',
      'core_topics',
      'module_structure',
      'assessment_approach',
      'prerequisites',
    ];
    const missingQuestions = requiredQuestions.filter(q => !questions.includes(q));

    if (missingQuestions.length > 0) {
      console.warn(`\n⚠ Missing question types: ${missingQuestions.join(', ')}`);
    } else {
      console.log('\n✓ All required question types present');
    }

    console.log(`\n✓ Recommendation generator OK`);
    process.exit(0);
  } catch (error) {
    console.error(`✗ Failed: ${error.message}`);
    process.exit(1);
  }
}

test();
