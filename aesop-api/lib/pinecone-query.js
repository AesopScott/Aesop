/**
 * Pinecone Query Wrapper
 * Queries the aesop-academy index for course-related semantic searches.
 * Requires PINECONE_API_KEY + VOYAGE_API_KEY for real queries.
 * Gracefully degrades when either credential is absent.
 */

import { Pinecone } from '@pinecone-database/pinecone';

const PINECONE_INDEX = 'aesop-academy';
const VOYAGE_EMBED_URL = 'https://api.voyageai.com/v1/embeddings';
const VOYAGE_MODEL = 'voyage-3'; // 1024-dimensional, matches index

let client = null;
let isAvailable = false;

async function initialize() {
  if (client !== null) return isAvailable;

  const apiKey = process.env.PINECONE_API_KEY;
  const voyageKey = process.env.VOYAGE_API_KEY;

  if (!apiKey) {
    console.warn('⚠ Pinecone unavailable: PINECONE_API_KEY not set');
    return false;
  }
  if (!voyageKey) {
    console.warn('⚠ Pinecone unavailable: VOYAGE_API_KEY not set (required for embeddings)');
    return false;
  }

  try {
    client = new Pinecone({ apiKey });
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
 * Generate embeddings via Voyage AI API.
 * Throws if VOYAGE_API_KEY is missing or the API call fails.
 */
async function generateEmbedding(text) {
  const voyageKey = process.env.VOYAGE_API_KEY;
  if (!voyageKey) throw new Error('VOYAGE_API_KEY not set');

  const response = await fetch(VOYAGE_EMBED_URL, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${voyageKey}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      model: VOYAGE_MODEL,
      input: [text],
      input_type: 'query',
    }),
  });

  if (!response.ok) {
    const body = await response.text();
    throw new Error(`Voyage AI error ${response.status}: ${body}`);
  }

  const data = await response.json();
  return data.data[0].embedding;
}

/**
 * Query Pinecone for courses semantically matching a concept.
 * Returns graceful degradation object when Pinecone / embeddings unavailable.
 */
export async function queryPinecone(concept, limit = 10) {
  const initialized = await initialize();

  if (!initialized) {
    return {
      results: [],
      source: 'none',
      warning: '⚠ Pinecone unavailable — using web search + course registry only.',
    };
  }

  try {
    const embedding = await generateEmbedding(concept);
    const index = client.Index(PINECONE_INDEX);
    const queryResponse = await index.query({
      vector: embedding,
      topK: limit,
      includeMetadata: true,
    });

    const results = queryResponse.matches?.map(match => ({
      id: match.id,
      score: match.score,
      metadata: match.metadata,
    })) || [];

    return { results, source: 'pinecone', queryText: concept, count: results.length };
  } catch (error) {
    console.warn(`⚠ Pinecone query failed: ${error.message}. Falling back.`);
    return {
      results: [],
      source: 'pinecone_failed',
      warning: '⚠ Pinecone query error — continuing with web search + course registry.',
    };
  }
}

export async function checkStatus() {
  const initialized = await initialize();
  return initialized
    ? { status: 'OK', message: `Pinecone index "${PINECONE_INDEX}" is available` }
    : { status: 'UNAVAILABLE', message: 'Pinecone unavailable — graceful degradation enabled.' };
}

export default { queryPinecone, checkStatus };
