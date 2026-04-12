"""
AIP Corpus Indexer — AESOP Intelligence Pipeline
Triggered by GitHub Actions on pushes to ai-academy/modules/**
Parses HTML module files, chunks text, embeds via Voyage-3,
and upserts vectors to Pinecone for RAG-based gap analysis.
"""

import os
import re
import hashlib
from pathlib import Path
import requests
from pinecone import Pinecone
from bs4 import BeautifulSoup

# ── CONFIG ────────────────────────────────────────────────────────────────────

ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
VOYAGE_API_KEY    = os.environ["VOYAGE_API_KEY"]
PINECONE_API_KEY  = os.environ["PINECONE_API_KEY"]
PINECONE_HOST     = os.environ["PINECONE_HOST"]
PINECONE_INDEX    = "aesop-academy"

MODULES_DIR       = Path("ai-academy/modules")
CHUNK_SIZE        = 500   # words per chunk
CHUNK_OVERLAP     = 50    # word overlap between chunks
EMBED_BATCH       = 5     # vectors per Voyage API call (keep small — chunks are large)
UPSERT_BATCH      = 50    # vectors per Pinecone upsert

# ── HTML PARSING ─────────────────────────────────────────────────────────────

def extract_text_from_html(filepath):
    """Parse an HTML module file and return cleaned text + metadata."""
    with open(filepath, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    # Remove scripts, styles, nav elements
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    # Extract title from first h1 or <title>
    title_tag = soup.find("h1") or soup.find("title")
    title = title_tag.get_text(strip=True) if title_tag else filepath.stem

    # Get all visible text
    text = soup.get_text(separator=" ", strip=True)
    # Collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return title, text


def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """Split text into overlapping word-based chunks."""
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        if chunk.strip():
            chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

# ── EMBEDDING ────────────────────────────────────────────────────────────────

def embed_texts(texts, retries=3):
    """Embed a batch of texts using Voyage-3 via VoyageAI REST API."""
    import time

    for attempt in range(retries):
        resp = requests.post(
            "https://api.voyageai.com/v1/embeddings",
            headers={
                "Authorization": f"Bearer {VOYAGE_API_KEY}",
                "content-type": "application/json",
            },
            json={
                "model": "voyage-3",
                "input": texts,
                "input_type": "document",
            },
            timeout=120,
        )

        if resp.status_code == 200:
            data = resp.json()["data"]
            return [item["embedding"] for item in data]

        if resp.status_code == 429 and attempt < retries - 1:
            wait = (attempt + 1) * 5
            print(f"    Rate limited, waiting {wait}s...")
            time.sleep(wait)
            continue

        print(f"    Voyage API error ({resp.status_code}): {resp.text[:500]}")
        raise RuntimeError(f"Voyage embedding failed ({resp.status_code}): {resp.text[:200]}")

    raise RuntimeError("Voyage embedding failed after all retries")

# ── MAIN PIPELINE ────────────────────────────────────────────────────────────

def main():
    print("=== AIP Corpus Indexer ===\n")

    # Connect to Pinecone
    print("Connecting to Pinecone...")
    pc = Pinecone(api_key=PINECONE_API_KEY)
    index = pc.Index(PINECONE_INDEX, host=PINECONE_HOST)
    stats = index.describe_index_stats()
    print(f"  Current vectors: {stats['total_vector_count']}\n")

    # Find all HTML module files
    html_files = sorted(MODULES_DIR.glob("**/*.html"))
    # Filter to actual module files (skip hubs, admin pages, etc.)
    module_files = [
        f for f in html_files
        if re.search(r"-m\d+\.html$", f.name)
    ]
    print(f"Found {len(module_files)} module files.\n")

    # Process each file
    all_vectors = []
    for filepath in module_files:
        rel_path = str(filepath.relative_to("."))
        title, text = extract_text_from_html(filepath)

        if len(text.split()) < 20:
            print(f"  Skipping (too short): {rel_path}")
            continue

        chunks = chunk_text(text)
        print(f"  {rel_path}: {len(chunks)} chunks from '{title}'")

        for i, chunk in enumerate(chunks):
            # Deterministic ID based on file path + chunk index
            vec_id = hashlib.md5(f"{rel_path}::{i}".encode()).hexdigest()
            all_vectors.append({
                "id": vec_id,
                "text": chunk,
                "metadata": {
                    "source": rel_path,
                    "title": title,
                    "chunk_index": i,
                    "total_chunks": len(chunks),
                },
            })

    print(f"\nTotal chunks to index: {len(all_vectors)}")

    if not all_vectors:
        print("No content to index.")
        return

    # Embed in batches
    print("\nEmbedding chunks...")
    for batch_start in range(0, len(all_vectors), EMBED_BATCH):
        batch = all_vectors[batch_start : batch_start + EMBED_BATCH]
        texts = [v["text"] for v in batch]
        embeddings = embed_texts(texts)

        for vec, emb in zip(batch, embeddings):
            vec["embedding"] = emb

        done = min(batch_start + EMBED_BATCH, len(all_vectors))
        print(f"  Embedded {done}/{len(all_vectors)}")

    # Upsert to Pinecone in batches
    print("\nUpserting to Pinecone...")
    for batch_start in range(0, len(all_vectors), UPSERT_BATCH):
        batch = all_vectors[batch_start : batch_start + UPSERT_BATCH]
        upsert_data = [
            (v["id"], v["embedding"], v["metadata"])
            for v in batch
        ]
        index.upsert(vectors=upsert_data)
        done = min(batch_start + UPSERT_BATCH, len(all_vectors))
        print(f"  Upserted {done}/{len(all_vectors)}")

    # Final stats
    stats = index.describe_index_stats()
    print(f"\nDone. Vectors now in index: {stats['total_vector_count']}")


if __name__ == "__main__":
    main()
