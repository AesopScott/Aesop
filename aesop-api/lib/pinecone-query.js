/**
 * Pinecone Query Wrapper
 * Queries the aesop-academy index for course-related semantic searches
 * Gracefully degrades if Pinecone unavailable (warns user, continues with web search)
 */

import { Pinecone } from '@pinecone-database/pinecone';

const PINECONE_INDEX = 'aesop-academy';
const PINECONE_API_KEY = process.env.PINECONE_API_KEY;
const PINECONE_HOST = process.env.PINECONE_HOST;

let client = null;
let isAvailable = false;

/**
 * Initialize Pinecone client
 * Returns: true if initialization successful, false otherwise
 */
async function initialize() {
  if (client !== null) {
    return isAvailable; // Already initialized
  }

  try {
    if (!PINECONE_API_KEY || !PINECONE_HOST) {
      console.warn('⚠ Pinecone credentials missing (PINECONE_API_KEY, PINECONE_HOST)');
      isAvailable = false;
      return false;
    }

    client = new Pinecone({
      apiKey: PINECONE_API_KEY,
    });

    // Test connectivity by listing indexes
    const indexes = await client.listIndexes();
    const indexExists = indexes.indexes?.some(idx => idx.name === PINECONE_INDEX);

    if (!indexExists) {
      console.warn(`⚠ Pinecone index "${PINECONE_INDEX}" not found`);
      isAvailable = false;
      return false;
    }

    isAvailable = true;
    return true;
  } catch (error) {
    console.warn(`⚠ Pinecone initialization failed: ${error.message}`);
    isAvailable = false;
    client = null;
    return false;
  }
}

/**
 * Query Pinecone for courses matching a concept
 * Returns: { results: [...], source: 'pinecone', queryText: concept }
 * Or graceful degradation: { results: [], source: 'none', warning: '...' }
 */
export async function queryPinecone(concept, limit = 10) {
  const initialized = await initialize();

  if (!initialized) {
    return {
      results: [],
      source: 'none',
      warning: `⚠ Pinecone unavailable. Using web search + course registry only.`,
    };
  }

  try {
    // Query the index
    const index = client.Index(PINECONE_INDEX);
    const queryResponse = await index.query({
      vector: await generateEmbedding(concept),
      topK: limit,
      includeMetadata: true,
    });

    const results = queryResponse.matches?.map(match => ({
      id: match.id,
      score: match.score,
      metadata: match.metadata,
    })) || [];

    return {
      results,
      source: 'pinecone',
      queryText: concept,
      count: results.length,
    };
  } catch (error) {
    console.warn(`⚠ Pinecone query failed: ${error.message}. Falling back to web search.`);
    return {
      results: [],
      source: 'pinecone_failed',
      warning: `⚠ Pinecone query error. Continuing with web search + course registry.`,
    };
  }
}

/**
 * Generate embeddings for a text query
 * Uses Voyage AI (separate from Anthropic)
 * For now, returns a dummy vector (placeholder for actual embedding)
 */
async function generateEmbedding(text) {
  // Placeholder: In production, use Voyage AI embeddings
  // For testing, return a random vector
  const dimension = 1024; // Adjust to match Pinecone index dimension
  return Array(dimension)
    .fill(0)
    .map(() => Math.random());
}

/**
 * Check Pinecone status
 */
export async function checkStatus() {
  const initialized = await initialize();

  if (initialized) {
    return { status: 'OK', message: `Pinecone index "${PINECONE_INDEX}" is available` };
  } else {
    return {
      status: 'UNAVAILABLE',
      message: 'Pinecone is not available. Graceful degradation enabled.',
    };
  }
}

export default {
  queryPinecone,
  checkStatus,
};
