# Pinecone Integration Registry

Every Pinecone index and access point in this project. For each: what it stores, who produces/consumes it, and constraints.

---

## `aesop-academy` (Index)

Course content corpus for semantic search and gap analysis. Stores embeddings of course descriptions, topics, prerequisites, and audience data.

**Contents:** Course metadata and content vectors for the Aesop AI Academy course library (v1 and v2 courses)

**Producers** (who writes to index)
- `.github/scripts/index_aesop.py` — indexes course content into Pinecone via Voyage embeddings
- GitHub Actions: `index-corpus.yml` — runs index_aesop.py on schedule/post-deploy

**Consumers** (who reads from index)
- `.github/scripts/test-pinecone.py:12` — `PINECONE_INDEX = "aesop-academy"` (diagnostic queries)
- `.github/scripts/signals_*.py` — research agents may query for signal discovery (implied)
- Task #1 research module (planned) — queries for topic coverage, gaps, prerequisites

**Access method:** Pinecone Python SDK / HTTP API with `PINECONE_API_KEY` and `VOYAGE_API_KEY`

**Adjacent constraint:** Index must be kept in sync with courses-v2.html and courses.html (data source of truth); index_aesop.py maintains this

**Status:** ✓ Currently in production; Task #1 extends consumer usage

---

## Summary

| Index | Purpose | Producers | Consumers | Status |
|-------|---------|-----------|-----------|--------|
| `aesop-academy` | Course content corpus | index_aesop.py | test-pinecone.py, signals agents, Task #1 research (planned) | ✓ |

---

## Audit Trail — Proof of Registry Verification

**Last audit:** 2026-05-20 19:45 UTC (by /cross-boundary-audit, Task #1 planning)

**Boundaries checked:** Pinecone index names and access points

**Evidence recorded:**
- 1 entry with complete producer/consumer pairs ✓
- Index name consistent across all Python scripts
- Sync constraint documented (index ← index_aesop.py ← courses-v2.html)
- New identifiers introduced: None (existing index, new consumer planned)
- Registries match current code diff: Yes

**Gaps identified:** None — index properly named and maintained

**Status:** Audit complete — index ready for Task #1 skill queries
