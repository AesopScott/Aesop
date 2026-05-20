#!/usr/bin/env node
/**
 * Test Claude Sonnet API Connection
 * Proof Unit #1: Verify Anthropic SDK can make synchronous API calls
 */

const ANTHROPIC_API_KEY = process.env.ANTHROPIC_API_KEY;

if (!ANTHROPIC_API_KEY) {
  console.error('✗ Failed: ANTHROPIC_API_KEY not set');
  process.exit(1);
}

// Dynamically import the Anthropic SDK
(async () => {
  try {
    const { Anthropic } = await import('@anthropic-ai/sdk');
    const client = new Anthropic({ apiKey: ANTHROPIC_API_KEY });

    // Test: Make a simple API call to Sonnet
    const response = await client.messages.create({
      model: 'claude-sonnet-4-6',
      max_tokens: 100,
      messages: [
        {
          role: 'user',
          content: 'Say "Connection OK" if you receive this.',
        },
      ],
    });

    // Verify response structure
    if (response && response.content && response.content.length > 0) {
      console.log('✓ Connection OK');
      console.log(`✓ Response received from ${response.model}`);
      process.exit(0);
    } else {
      console.error('✗ Failed: Unexpected response structure');
      process.exit(1);
    }
  } catch (error) {
    console.error(`✗ Failed: ${error.message}`);
    process.exit(1);
  }
})();
