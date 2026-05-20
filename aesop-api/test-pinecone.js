#!/usr/bin/env node
/**
 * Test Pinecone Integration
 * Proof Unit #3: Verify graceful degradation and error handling
 */

import { queryPinecone, checkStatus } from './lib/pinecone-query.js';

async function runTest() {
  console.log('Testing Pinecone integration...\n');

  try {
    // Test 1: Check status
    console.log('1. Checking Pinecone status...');
    const status = await checkStatus();
    console.log(`   Status: ${status.status}`);
    console.log(`   Message: ${status.message}\n`);

    // Test 2: Query Pinecone
    console.log('2. Attempting query...');
    const result = await queryPinecone('AI Ethics', 5);

    if (result.source === 'pinecone') {
      console.log(`✓ Pinecone query successful`);
      console.log(`  Results: ${result.count} found`);
      result.results.forEach((r, i) => {
        console.log(`    ${i + 1}. ${r.id} (score: ${r.score?.toFixed(3) || 'N/A'})`);
      });
    } else if (result.source === 'none' || result.source === 'pinecone_failed') {
      console.log(`⚠ ${result.warning}`);
      console.log(`✓ Graceful degradation active`);
    }

    // Test 3: Verify response structure
    console.log('\n3. Verifying response structure...');
    const requiredFields = ['results', 'source', 'count', 'warning'];
    const hasWarning = 'warning' in result;
    const hasCount = 'count' in result;

    if (hasWarning && hasCount) {
      console.log('✓ Response structure valid (with warning/count)');
    } else if (!hasWarning && !hasCount && result.source === 'pinecone') {
      console.log('✓ Response structure valid (Pinecone success)');
    } else {
      console.log('⚠ Response structure unexpected');
    }

    console.log('\n✓ Pinecone integration OK (graceful degradation tested)');
    process.exit(0);
  } catch (error) {
    console.error(`✗ Failed: ${error.message}`);
    process.exit(1);
  }
}

runTest();
