/**
 * Course Development Assistant
 * Orchestrates research → recommendations → approval flow for course building
 * Called by /aesop-course-builder skill during planning phase
 */

import { runResearch } from './research-engine.js';
import { generateRecommendations } from './recommendation-generator.js';

/**
 * Main orchestration: research + recommendations
 * @param {string} courseConcept - The course being developed
 * @returns {Promise<Object>} Course planning with recommendations ready for approval
 */
export async function developCoursePlanning(courseConcept) {
  console.log(`\n📚 Course Development Assistant\n`);
  console.log(`Developing planning recommendations for: "${courseConcept}"\n`);

  try {
    // Step 1: Run research
    console.log(`Step 1: Research...\n`);
    const researchFindings = await runResearch(courseConcept);

    // Step 2: Generate recommendations
    console.log(`Step 2: Recommendations...\n`);
    const recommendations = await generateRecommendations(
      courseConcept,
      researchFindings
    );

    // Step 3: Format for approval
    const planningPackage = formatForApproval(courseConcept, recommendations);

    return planningPackage;
  } catch (error) {
    console.error(`✗ Development assistant failed: ${error.message}`);
    throw error;
  }
}

/**
 * Format recommendations for user approval
 */
function formatForApproval(courseConcept, recommendations) {
  const formatted = {
    courseConcept,
    recommendations: recommendations.recommendations.map(rec => ({
      question: rec.question,
      recommendation: rec.recommendation,
      reasoning: rec.reasoning,
      approved: false, // User will set this
      modified: false, // User will set this if they change the recommendation
      userValue: null, // User can provide alternative value
    })),
    metadata: {
      generatedAt: recommendations.generatedAt,
      researchBacked: !recommendations.fallback,
      fallback: recommendations.fallback || false,
    },
  };

  return formatted;
}

/**
 * Process user approvals and build final planning parameters
 * @param {Object} planningPackage - Output from developCoursePlanning
 * @param {Array} userApprovals - User responses to recommendations
 * @returns {Object} Final approved planning parameters for course generation
 */
export function processPlanningApprovals(planningPackage, userApprovals) {
  const approved = {
    courseConcept: planningPackage.courseConcept,
    parameters: {},
    approvalNotes: [],
  };

  planningPackage.recommendations.forEach((rec, index) => {
    const userResponse = userApprovals[index];

    if (!userResponse) {
      // No response, use recommendation as-is
      approved.parameters[rec.question] = rec.recommendation;
      return;
    }

    if (userResponse.approved === false && !userResponse.userValue) {
      // User rejected without providing alternative — preserve original recommendation
      approved.parameters[rec.question] = rec.recommendation;
      approved.approvalNotes.push(
        `⚠ ${rec.question}: Rejected without alternative — using original recommendation`
      );
      return;
    }

    if (userResponse.userValue) {
      // User provided alternative value
      approved.parameters[rec.question] = userResponse.userValue;
      approved.approvalNotes.push(
        `✓ ${rec.question}: User provided alternative ("${userResponse.userValue}")`
      );
    } else {
      // User approved recommendation
      approved.parameters[rec.question] = rec.recommendation;
      approved.approvalNotes.push(`✓ ${rec.question}: Approved`);
    }
  });

  return approved;
}

/**
 * Format recommendations for display to user
 * Returns a human-readable format for CLI/UI display
 */
export function displayRecommendations(planningPackage) {
  let output = `\n${'='.repeat(70)}\n`;
  output += `COURSE PLANNING RECOMMENDATIONS: "${planningPackage.courseConcept}"\n`;
  output += `${'='.repeat(70)}\n\n`;

  planningPackage.recommendations.forEach((rec, index) => {
    output += `${index + 1}. ${formatQuestionLabel(rec.question)}\n`;
    output += `   Recommendation: ${rec.recommendation}\n`;
    output += `   Why: ${rec.reasoning}\n\n`;
    output += `   [ ] Approve   [ ] Modify   [ ] Reject\n\n`;
  });

  if (planningPackage.metadata.fallback) {
    output += `⚠ Note: Some recommendations are based on fallback logic (API unavailable)\n\n`;
  }

  output += `${'='.repeat(70)}\n`;

  return output;
}

/**
 * Helper: Format question label for display
 */
function formatQuestionLabel(question) {
  const labels = {
    target_audience: 'Target Audience',
    core_topics: 'Core Topics',
    module_structure: 'Module Structure',
    assessment_approach: 'Assessment Approach',
    prerequisites: 'Prerequisites',
  };

  return labels[question] || question;
}

export default {
  developCoursePlanning,
  processPlanningApprovals,
  displayRecommendations,
};
