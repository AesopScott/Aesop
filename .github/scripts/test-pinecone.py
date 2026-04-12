"""
AIP Pinecone Connection Test
Run via GitHub Actions to verify Pinecone + embedding are working.
"""
import os
import requests
from pinecone import Pinecone

ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
VOYAGE_API_KEY    = os.environ["VOYAGE_API_KEY"]
PINECONE_API_KEY  = os.environ["PINECONE_API_KEY"]
PINECONE_HOST     = os.environ["PINECONE_HOST"]
PINECONE_INDEX    = "aesop-academy"

print("=== Pinecone Connection Test ===\n")

# Step 1: Connect to Pinecone
print("1. Connecting to Pinecone...")
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX, host=PINECONE_HOST)
stats = index.describe_index_stats()
print(f"   ✓ Connected. Vectors in index: {stats['total_vector_count']}")
print(f"   Namespaces: {list(stats.get('namespaces', {}).keys())}\n")

# Step 2: Test voyage-3 embedding via VoyageAI REST
print("2. Testing voyage-3 embedding...")
res = requests.post(
    "https://api.voyageai.com/v1/embeddings",
    headers={
        "Authorization": f"Bearer {VOYAGE_API_KEY}",
        "content-type": "application/json",
    },
    json={"model": "voyage-3", "input": ["AI and education"], "input_type": "query"},
    timeout=30
)
print(f"   Status: {res.status_code}")
if res.status_code == 200:
    vec = res.json()["data"][0]["embedding"]
    print(f"   ✓ Embedding OK. Dimensions: {len(vec)}\n")

    # Step 3: Query Pinecone with real vector
    print("3. Querying Pinecone with test vector...")
    result = index.query(vector=vec, top_k=3, include_metadata=True)
    matches = result.get("matches", [])
    print(f"   ✓ Got {len(matches)} matches")
    for m in matches:
        print(f"   score={m['score']:.3f} | {m.get('metadata', {}).get('source', 'no metadata')}")
else:
    print(f"   ✗ Embedding failed: {res.text}")

print("\nTest complete.")
