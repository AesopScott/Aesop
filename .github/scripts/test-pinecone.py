"""
Pinecone Diagnostic Test
Checks each layer independently so the exact failure point is visible in logs.
"""
import os
import sys
import requests

PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY", "")
PINECONE_HOST    = os.environ.get("PINECONE_HOST", "")
VOYAGE_API_KEY   = os.environ.get("VOYAGE_API_KEY", "")
PINECONE_INDEX   = "aesop-academy"

passed = 0
failed = 0

def ok(msg):
    global passed
    passed += 1
    print(f"  ✓ {msg}")

def fail(msg):
    global failed
    failed += 1
    print(f"  ✗ FAIL: {msg}", file=sys.stderr)

print("=== Pinecone Diagnostic Test ===\n")

# ── 1. Secrets present ────────────────────────────────────────────────────────
print("1. Checking secrets are populated...")
if PINECONE_API_KEY:
    ok(f"PINECONE_API_KEY present (length={len(PINECONE_API_KEY)}, prefix={PINECONE_API_KEY[:8]}...)")
else:
    fail("PINECONE_API_KEY is empty or not set")

if PINECONE_HOST:
    ok(f"PINECONE_HOST = {PINECONE_HOST}")
else:
    fail("PINECONE_HOST is empty or not set")

if VOYAGE_API_KEY:
    ok(f"VOYAGE_API_KEY present (length={len(VOYAGE_API_KEY)}, prefix={VOYAGE_API_KEY[:8]}...)")
else:
    fail("VOYAGE_API_KEY is empty or not set")

# ── 2. Pinecone package import ────────────────────────────────────────────────
print("\n2. Importing pinecone package...")
try:
    from pinecone import Pinecone
    import pinecone as _pc_mod
    version = getattr(_pc_mod, "__version__", "unknown")
    ok(f"pinecone imported OK (version={version})")
except ImportError as e:
    fail(f"Cannot import pinecone: {e}")
    sys.exit(1)

# ── 3. Pinecone client init ───────────────────────────────────────────────────
print("\n3. Initialising Pinecone client...")
try:
    pc = Pinecone(api_key=PINECONE_API_KEY)
    ok("Pinecone() constructor succeeded")
except Exception as e:
    fail(f"Pinecone() constructor raised: {type(e).__name__}: {e}")
    sys.exit(1)

# ── 4. List indexes (validates API key against control plane) ─────────────────
print("\n4. Listing indexes (validates API key)...")
index_obj = None
try:
    indexes = pc.list_indexes()
    names = [idx.name for idx in indexes] if hasattr(indexes, '__iter__') else str(indexes)
    ok(f"list_indexes() succeeded: {names}")
    if PINECONE_INDEX not in names:
        fail(f"Index '{PINECONE_INDEX}' not found in account — existing indexes: {names}")
    else:
        ok(f"Index '{PINECONE_INDEX}' exists in account")
except Exception as e:
    fail(f"list_indexes() raised: {type(e).__name__}: {e}")

# ── 5. Connect to named index via host ────────────────────────────────────────
print("\n5. Connecting to index via host URL...")
index = None
try:
    index = pc.Index(PINECONE_INDEX, host=PINECONE_HOST)
    ok("pc.Index() succeeded")
except Exception as e:
    fail(f"pc.Index() raised: {type(e).__name__}: {e}")
    sys.exit(1)

# ── 6. describe_index_stats (validates host reachability + data-plane auth) ───
print("\n6. describe_index_stats (data-plane connectivity)...")
vec = None
try:
    stats = index.describe_index_stats()
    total = stats.get("total_vector_count", stats.get("totalVectorCount", "?"))
    namespaces = list(stats.get("namespaces", {}).keys())
    ok(f"describe_index_stats() succeeded — vectors={total}, namespaces={namespaces}")
    if str(total) == "0":
        print("  ⚠ WARNING: index is empty (0 vectors) — corpus indexer may not have run")
except Exception as e:
    fail(f"describe_index_stats() raised: {type(e).__name__}: {e}")

# ── 7. Voyage-3 embedding ─────────────────────────────────────────────────────
print("\n7. Testing Voyage-3 embedding...")
if not VOYAGE_API_KEY:
    print("  (skipped — VOYAGE_API_KEY not set)")
else:
    try:
        res = requests.post(
            "https://api.voyageai.com/v1/embeddings",
            headers={"Authorization": f"Bearer {VOYAGE_API_KEY}", "content-type": "application/json"},
            json={"model": "voyage-3", "input": ["AI and education"], "input_type": "query"},
            timeout=30,
        )
        if res.status_code == 200:
            vec = res.json()["data"][0]["embedding"]
            ok(f"Voyage embedding OK — dimensions={len(vec)}")
        else:
            fail(f"Voyage API returned {res.status_code}: {res.text[:300]}")
    except Exception as e:
        fail(f"Voyage request raised: {type(e).__name__}: {e}")

# ── 8. End-to-end query ───────────────────────────────────────────────────────
print("\n8. End-to-end Pinecone query with real vector...")
if vec is not None and index is not None:
    try:
        result = index.query(vector=vec, top_k=3, include_metadata=True)
        matches = result.get("matches", [])
        ok(f"query() succeeded — {len(matches)} matches returned")
        for m in matches:
            score = m.get("score", "?")
            title = m.get("metadata", {}).get("title", m.get("metadata", {}).get("source", "no metadata"))
            print(f"       score={score:.3f}  {title}")
    except Exception as e:
        fail(f"index.query() raised: {type(e).__name__}: {e}")
else:
    print("  (skipped — Voyage embedding unavailable)")

# ── Summary ───────────────────────────────────────────────────────────────────
print(f"\n{'='*40}")
print(f"Results: {passed} passed, {failed} failed")
if failed:
    print("PINECONE IS NOT WORKING — see ✗ lines above for the exact failure point")
    sys.exit(1)
else:
    print("All checks passed — Pinecone is operational")
