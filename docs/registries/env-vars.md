# Environment Variables Registry

Every environment variable referenced in this project. For each: where it's set, where it's read, and what it controls.

---

## `AESOP_ANTHROPIC_API_KEY`

Anthropic API key for lab chat proxy endpoint (PHP server-side). Not exposed to client.

**Schema:** String (API key, sensitive)

**Producers** (where set)
- Environment/deployment: cPanel secrets / hosting provider (not in code)
- `secrets.php` — referenced as `aesop_secret('AESOP_ANTHROPIC_API_KEY', '')`

**Consumers** (where read)
- `aesop-api/proxy.php:15` — `$API_KEY = aesop_secret('AESOP_ANTHROPIC_API_KEY', '')`

**Note:** This is the PHP-layer credential. Node.js research modules use `ANTHROPIC_API_KEY` (see below) — two separate env vars for the same upstream service.

---

## `ANTHROPIC_API_KEY`

Anthropic API key for Node.js research modules (research engine, recommendation generator). Separate from `AESOP_ANTHROPIC_API_KEY` used by PHP proxy.

**Schema:** String (API key, sensitive)

**Producers** (where set)
- Environment/deployment: must be set in the Node.js execution environment (shell, CI, or skill runner)

**Consumers** (where read)
- `aesop-api/lib/research-engine.js:15` — `apiKey: process.env.ANTHROPIC_API_KEY`
- `aesop-api/lib/recommendation-generator.js:10` — `apiKey: process.env.ANTHROPIC_API_KEY`
- `aesop-api/test-claude-sonnet.js:7` — `const ANTHROPIC_API_KEY = process.env.ANTHROPIC_API_KEY`

**Adjacent constraint:** Must be set before invoking `/aesop-course-builder` research phase. Missing key causes graceful fallback to registry-only recommendations.

**Status:** ✓ Properly gated; missing key triggers fallback, not crash

**Adjacent constraint:** Must be present at runtime; missing key returns 500 error (proxy.php:34-37)

**Status:** ✓ Properly gated and validated

---

## `PINECONE_API_KEY`

Pinecone vector database API key for course corpus queries.

**Schema:** String (API key, sensitive)

**Producers** (where set)
- Environment/deployment: cPanel secrets or GitHub Actions secrets (not in code)

**Consumers** (where read)
- `.github/scripts/test-pinecone.py:9` — `PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY", "")`
- `.github/scripts/index_aesop.py` — implied (Pinecone query operations)
- Task #1 research module (planned) — will read for corpus queries

**Adjacent constraint:** Missing key causes diagnostic failure (test-pinecone.py checks presence)

**Status:** ✓ Currently used; Task #1 extends usage to skill

---

## `PINECONE_HOST`

Pinecone API host endpoint.

**Schema:** String (URL)

**Producers** (where set)
- Environment/deployment: cPanel secrets or GitHub Actions secrets

**Consumers** (where read)
- `.github/scripts/test-pinecone.py:10` — `PINECONE_HOST = os.environ.get("PINECONE_HOST", "")`
- Task #1 research module (planned) — will read for API connectivity

**Adjacent constraint:** Must be paired with `PINECONE_API_KEY` for auth

**Status:** ✓ Currently used; Task #1 extends usage

---

## `VOYAGE_API_KEY`

Voyage AI embeddings API key (for semantic search in Pinecone).

**Schema:** String (API key, sensitive)

**Producers** (where set)
- Environment/deployment: cPanel secrets or GitHub Actions secrets

**Consumers** (where read)
- `.github/scripts/test-pinecone.py:11` — `VOYAGE_API_KEY = os.environ.get("VOYAGE_API_KEY", "")`
- Pinecone index operations that need embeddings

**Adjacent constraint:** Used alongside `PINECONE_API_KEY` for semantic queries

**Status:** ✓ Currently used; Task #1 may extend usage for research

---

## Summary

| Variable | Type | Producers | Consumers | Status |
|----------|------|-----------|-----------|--------|
| `AESOP_ANTHROPIC_API_KEY` | Secret | cPanel secrets | proxy.php | ✓ |
| `PINECONE_API_KEY` | Secret | cPanel secrets | test-pinecone.py, index_aesop.py, Task #1 research (planned) | ✓ |
| `PINECONE_HOST` | Config | cPanel secrets | test-pinecone.py, Task #1 research (planned) | ✓ |
| `VOYAGE_API_KEY` | Secret | cPanel secrets | Pinecone operations, Task #1 (planned) | ✓ |

---

## Audit Trail — Proof of Registry Verification

**Last audit:** 2026-05-20 22:00 UTC (by /cross-boundary-audit, Task #1 build complete)

**Boundaries checked:** Environment variables used across codebase

**Evidence recorded:**
- 5 entries with complete producer/consumer pairs ✓ (added ANTHROPIC_API_KEY for Node.js layer)
- All secrets gated through environment (not in code)
- All consumers have fallback handling
- New identifiers introduced: `ANTHROPIC_API_KEY` (Task #1 Node.js research modules)
- Registries match current code diff: Yes

**Gaps identified:**
- `AESOP_ANTHROPIC_API_KEY` (PHP proxy) and `ANTHROPIC_API_KEY` (Node.js libs) are two separate env vars for the same upstream Anthropic service. Intentional split by runtime layer; document where each must be set.

**Status:** Audit complete
