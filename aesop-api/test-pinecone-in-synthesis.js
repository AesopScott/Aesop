#!/usr/bin/env node
/**
 * Test that Pinecone results appear in the synthesis prompt sent to Claude.
 * Proof Unit #2 (extended): Pinecone coverage data flows through to researchFindings.
 *
 * Uses buildSynthesisPrompt (exported for testing) with fake Pinecone data
 * to verify the prompt includes match titles and scores — without needing
 * live Pinecone or Claude API credentials.
 */

import { buildSynthesisPrompt } from './lib/research-engine.js';

function test() {
  console.log('Testing Pinecone coverage in synthesis prompt...\n');

  const fakeRegistry = {
    existingCourses: [
      { title: 'Intro to AI', audience: ['beginner'], topics: ['ai'] },
    ],
    totalCoursesInCatalog: 150,
    coverageSummary: {},
  };

  const fakePinecone = {
    results: [
      { id: 'course-ai-ethics', score: 0.923, metadata: { title: 'AI Ethics & Decision Making' } },
      { id: 'course-ai-basics',  score: 0.871, metadata: { title: 'AI Fundamentals' } },
    ],
    source: 'pinecone',
    count: 2,
  };

  const fakeWebSearch = { searchResults: 'Demand for Python courses is high.', realSearch: true };

  const prompt = buildSynthesisPrompt('Python Basics', fakeRegistry, fakePinecone, fakeWebSearch);

  // Assert: Pinecone match titles appear in the prompt
  const titleA = 'AI Ethics & Decision Making';
  const titleB = 'AI Fundamentals';
  if (!prompt.includes(titleA)) {
    console.error(`✗ Pinecone title missing from prompt: "${titleA}"`);
    process.exit(1);
  }
  if (!prompt.includes(titleB)) {
    console.error(`✗ Pinecone title missing from prompt: "${titleB}"`);
    process.exit(1);
  }

  // Assert: scores appear in the prompt
  if (!prompt.includes('0.923')) {
    console.error('✗ Pinecone score 0.923 missing from prompt');
    process.exit(1);
  }

  // Assert: section header present
  if (!prompt.includes('Semantically similar courses from vector index')) {
    console.error('✗ Pinecone section header missing from prompt');
    process.exit(1);
  }

  console.log('✓ Pinecone match titles appear in synthesis prompt');
  console.log('✓ Pinecone scores appear in synthesis prompt');
  console.log('✓ Pinecone section header present');

  // Also verify the (none) fallback when results is empty
  const emptyPinecone = { results: [], source: 'none' };
  const emptyPrompt = buildSynthesisPrompt('Python Basics', fakeRegistry, emptyPinecone, fakeWebSearch);
  if (!emptyPrompt.includes('(none)')) {
    console.error('✗ Fallback "(none)" missing when Pinecone has no results');
    process.exit(1);
  }
  console.log('✓ Fallback "(none)" shown when Pinecone results are empty');

  console.log('\n✓ Pinecone-in-synthesis test OK');
  process.exit(0);
}

test();
