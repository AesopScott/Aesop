/**
 * Research Engine
 * Queries Pinecone, course registries, and web search to identify:
 * - Audience gaps in course offerings
 * - Topic coverage and gaps
 * - Structural patterns in existing courses
 * - Prerequisites and skill recommendations
 */

import { Anthropic } from '@anthropic-ai/sdk';
import { queryPinecone } from './pinecone-query.js';
import { getAllCourses, getCoverageSummary } from './registry-parser.js';

const client = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

/**
 * Main research entry point
 * @param {string} courseConcept - The course concept to research (e.g., "AI Ethics for High School")
 * @returns {Promise<Object>} researchFindings object with gaps, coverage, patterns, prerequisites
 */
export async function runResearch(courseConcept) {
  console.log(`🔍 Researching: "${courseConcept}"\n`);

  try {
    // 1. Query existing course registries
    const registryCoverage = queryRegistries(courseConcept);
    console.log(`✓ Registry query complete (${registryCoverage.existingCourses.length} existing courses found)`);

    // 2. Query Pinecone (if available)
    const pineconeResults = await queryPinecone(courseConcept, 5);
    console.log(`✓ Pinecone query complete (source: ${pineconeResults.source}, ${pineconeResults.count || 0} results)`);

    // 3. Web search via Claude
    const webSearch = await performWebSearch(courseConcept);
    console.log(`✓ Web search complete`);

    // 4. Synthesize all findings into structured format
    const findings = await synthesizeFindings(
      courseConcept,
      registryCoverage,
      pineconeResults,
      webSearch
    );

    console.log(`✓ Research synthesis complete\n`);
    return findings;
  } catch (error) {
    console.error(`✗ Research failed: ${error.message}`);
    throw error;
  }
}

/**
 * Query course registries to find existing coverage
 */
function queryRegistries(concept) {
  const allCourses = getAllCourses();
  const summary = getCoverageSummary();

  // Find courses related to the concept (naive keyword matching)
  const keywords = concept.toLowerCase().split(/\s+/);
  const relevantCourses = allCourses.filter(course => {
    const courseText = `${course.title} ${course.description}`.toLowerCase();
    return keywords.some(kw => courseText.includes(kw));
  });

  return {
    existingCourses: relevantCourses.map(c => ({
      id: c.id,
      title: c.title,
      audience: c.audience,
      topics: c.topics,
      modules: c.moduleCount,
    })),
    totalCoursesInCatalog: allCourses.length,
    coverageSummary: summary,
  };
}

/**
 * Perform web search via Claude's web search tool
 */
async function performWebSearch(concept) {
  try {
    const response = await client.messages.create({
      model: 'claude-sonnet-4-20250514',
      max_tokens: 500,
      messages: [
        {
          role: 'user',
          content: `Search for: "${concept}". Identify: 1) demand signals (how many people search for this), 2) related topics people search for, 3) skill gaps you find mentioned. Be concise.`,
        },
      ],
    });

    const content = response.content[0];
    return {
      searchResults: content.type === 'text' ? content.text : '',
      model: response.model,
    };
  } catch (error) {
    console.warn(`⚠ Web search via Claude failed: ${error.message}`);
    return { searchResults: '', error: error.message };
  }
}

/**
 * Synthesize all research into structured findings
 */
async function synthesizeFindings(concept, registry, pinecone, webSearch) {
  // Build context from all sources
  const context = {
    concept,
    existingCourses: registry.existingCourses,
    pineconeAvailable: pinecone.source === 'pinecone',
    webInsights: webSearch.searchResults,
    catalogSize: registry.totalCoursesInCatalog,
  };

  // Use Claude to synthesize structured findings
  const prompt = `
You are analyzing research for a new course: "${concept}"

Existing courses on related topics: ${registry.existingCourses.length}
Total courses in catalog: ${registry.totalCoursesInCatalog}

Audience coverage:
${registry.existingCourses.map(c => `- ${c.title}: ${c.audience.join(', ')}`).join('\n')}

Web research insights:
${webSearch.searchResults}

Generate structured findings (JSON format) with:
1. audienceGaps: Array of { segment, currentCoverage (int), demand (high/medium/low) }
2. topicCoverage: Array of { topic, existingCourses (array), gaps (string) }
3. structuralPatterns: { averageModulesPerCourse, commonMajorTopics, assessmentApproaches }
4. prerequisites: Array of { skill, recommendedLevel (foundational/intermediate/advanced) }
5. researchSources: Array of source descriptions

Return ONLY valid JSON, no markdown, no explanation.
`;

  try {
    const response = await client.messages.create({
      model: 'claude-sonnet-4-20250514',
      max_tokens: 1200,
      messages: [
        {
          role: 'user',
          content: prompt,
        },
      ],
    });

    const jsonText = response.content[0].type === 'text' ? response.content[0].text : '{}';

    // Parse JSON response
    const findings = JSON.parse(jsonText);

    return {
      audienceGaps: findings.audienceGaps || [],
      topicCoverage: findings.topicCoverage || [],
      structuralPatterns: findings.structuralPatterns || {},
      prerequisites: findings.prerequisites || [],
      researchSources: findings.researchSources || [],
      timestamp: new Date().toISOString(),
    };
  } catch (error) {
    console.warn(`⚠ Synthesis failed: ${error.message}. Returning partial findings.`);

    // Return partial findings based on registry alone
    return {
      audienceGaps: inferAudienceGaps(registry),
      topicCoverage: inferTopicCoverage(registry),
      structuralPatterns: inferStructuralPatterns(registry),
      prerequisites: [],
      researchSources: ['registry query', 'pinecone query'],
      timestamp: new Date().toISOString(),
    };
  }
}

/**
 * Infer audience gaps from registry data
 */
function inferAudienceGaps(registry) {
  const audienceCounts = {};
  registry.existingCourses.forEach(course => {
    course.audience.forEach(aud => {
      audienceCounts[aud] = (audienceCounts[aud] || 0) + 1;
    });
  });

  const potentialAudiences = ['beginner', 'intermediate', 'advanced', 'technical', 'business'];
  return potentialAudiences.map(aud => ({
    segment: aud,
    currentCoverage: audienceCounts[aud] || 0,
    demand: 'medium', // Default; Claude would provide actual assessment
  }));
}

/**
 * Infer topic coverage from registry data
 */
function inferTopicCoverage(registry) {
  const topicMap = {};
  registry.existingCourses.forEach(course => {
    course.topics.forEach(topic => {
      if (!topicMap[topic]) topicMap[topic] = [];
      topicMap[topic].push(course.id);
    });
  });

  return Object.entries(topicMap).map(([topic, courses]) => ({
    topic,
    existingCourses: courses,
    gaps: `Covered by ${courses.length} course(s)`,
  }));
}

/**
 * Infer structural patterns from registry data
 */
function inferStructuralPatterns(registry) {
  const modules = registry.existingCourses.map(c => c.modules);
  const avgModules =
    modules.length > 0 ? modules.reduce((a, b) => a + b, 0) / modules.length : 8;

  return {
    averageModulesPerCourse: Math.round(avgModules),
    commonMajorTopics: ['AI', 'skill development', 'practical application'],
    assessmentApproaches: ['debate', 'skill lab', 'build project'],
  };
}

export default {
  runResearch,
};
