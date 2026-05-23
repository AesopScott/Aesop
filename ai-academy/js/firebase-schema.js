// Firebase Firestore schema for AESOP learner records
// Defines TypeScript-like interfaces for learner data structure

export const LearnerSchema = {
  // Core learner identification
  learnerId: 'string',      // UUID generated on first visit
  createdAt: 'timestamp',   // ISO string or Firestore timestamp
  lastActiveAt: 'timestamp',

  // Assessment results
  assessmentResults: {
    completed: 'boolean',           // Has learner completed assessment?
    completedAt: 'timestamp | null',
    conversationHistory: [
      {
        role: 'user | assistant',
        content: 'string',
        timestamp: 'timestamp'
      }
    ],
    aptitudeScore: 'number (0-100)',    // Inferred AI aptitude
    interestTags: ['string'],           // Tags: e.g., ['python', 'nlp', 'ethics']
    completionFlag: 'boolean',          // Assessment finished?
  },

  // Recommended pathway from assessment
  recommendedPathway: {
    generatedAt: 'timestamp | null',
    primaryCourse: {
      courseId: 'string',
      title: 'string',
      difficulty: 'beginner | intermediate | advanced',
      skillsFocused: ['string'],
    },
    followUpCourses: [
      {
        courseId: 'string',
        title: 'string',
        difficulty: 'string',
        skillsFocused: ['string'],
        reasoning: 'string',  // Why recommended for this learner
      }
    ],
    reasoningBrief: 'string',  // Summary of recommendation logic
  },

  // QR recovery mechanism
  qrRecoveryToken: {
    token: 'string',                   // Unique recovery token
    generatedAt: 'timestamp | null',
    qrCodeSvg: 'string (base64 | SVG)', // SVG string or base64-encoded PNG
    expiresAt: 'timestamp | null',     // Optional: token expiration
  },

  // Progress tracking
  progressData: {
    coursesStarted: ['string'],        // Array of course IDs started
    coursesCompleted: ['string'],      // Array of course IDs completed
    lastAccessedCourse: 'string | null',
    currentlyViewingCourse: 'string | null',
  }
};

// TypeScript-like type definitions for runtime validation
export const LearnerTypes = {
  Learner: {
    learnerId: 'string',
    createdAt: 'timestamp',
    lastActiveAt: 'timestamp',
    assessmentResults: 'object',
    recommendedPathway: 'object',
    qrRecoveryToken: 'object',
    progressData: 'object',
  },

  AssessmentResults: {
    completed: 'boolean',
    completedAt: 'timestamp|null',
    conversationHistory: 'array',
    aptitudeScore: 'number',
    interestTags: 'array',
    completionFlag: 'boolean',
  },

  RecommendedPathway: {
    generatedAt: 'timestamp|null',
    primaryCourse: 'object',
    followUpCourses: 'array',
    reasoningBrief: 'string',
  },

  QRRecoveryToken: {
    token: 'string',
    generatedAt: 'timestamp|null',
    qrCodeSvg: 'string',
    expiresAt: 'timestamp|null',
  }
};

// Helper to create empty assessment results
export const createEmptyAssessmentResults = () => ({
  completed: false,
  completedAt: null,
  conversationHistory: [],
  aptitudeScore: 0,
  interestTags: [],
  completionFlag: false,
});

// Helper to create empty pathway
export const createEmptyPathway = () => ({
  generatedAt: null,
  primaryCourse: null,
  followUpCourses: [],
  reasoningBrief: '',
});

// Helper to create empty QR recovery token
export const createEmptyQRRecoveryToken = () => ({
  token: '',
  generatedAt: null,
  qrCodeSvg: '',
  expiresAt: null,
});

// Helper to create new learner record
export const createNewLearnerRecord = (learnerId) => {
  const now = new Date().toISOString();
  return {
    learnerId,
    createdAt: now,
    lastActiveAt: now,
    assessmentResults: createEmptyAssessmentResults(),
    recommendedPathway: createEmptyPathway(),
    qrRecoveryToken: createEmptyQRRecoveryToken(),
    progressData: {
      coursesStarted: [],
      coursesCompleted: [],
      lastAccessedCourse: null,
      currentlyViewingCourse: null,
    }
  };
};
