# Environment Variables Registry

Every environment variable referenced in this project. For each: where it's set, where it's read, and what it controls.

---

## `AESOP_ANTHROPIC_API_KEY`

Anthropic API key for lab chat proxy endpoint. Server-side only; not exposed to client.

**Schema:** String (API key, sensitive)

**Producers** (where set)
- Environment/deployment: `.cpanel.yml` or hosting provider secrets (not in code)
- `secrets.php` — referenced as `aesop_secret('AESOP_ANTHROPIC_API_KEY', '')`

**Consumers** (where read)
- `aesop-api/proxy.php:15` — `$API_KEY = aesop_secret('AESOP_ANTHROPIC_API_KEY', '')`
- Used to authenticate requests to Anthropic Messages API

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

**Last audit:** 2026-05-20 19:45 UTC (by /cross-boundary-audit, Task #1 planning)

**Boundaries checked:** Environment variables used across codebase

**Evidence recorded:**
- 4 entries with complete producer/consumer pairs ✓
- All secrets gated through environment (not in code)
- All consumers have fallback handling (empty string defaults)
- New identifiers introduced: None (Task #1 reuses existing env vars)
- Registries match current code diff: Yes

**Gaps identified:** None — all env vars properly gated

**Status:** Audit complete — env vars ready for Task #1 skill usage
