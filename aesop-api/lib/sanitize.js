/**
 * Shared input sanitization for research pipeline.
 * Prevents prompt injection via user-supplied course concept strings.
 */

export function sanitizeConcept(concept) {
  return concept
    .replace(/[\x00-\x1f\x7f]/g, '')       // control characters
    .replace(/```|<\/?[a-z]+>|---/gi, ' ')  // markdown/HTML delimiters
    .slice(0, 200)
    .trim();
}
