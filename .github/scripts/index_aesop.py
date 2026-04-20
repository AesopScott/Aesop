"""
AIP Corpus Indexer — AESOP Intelligence Pipeline
Triggered by GitHub Actions on pushes to ai-academy/modules/**
Supports delta mode (only changed files) and full re-index mode.

Delta mode (default on push): uses git diff to find changed module files,
  re-indexes only those, and removes vectors for deleted files.
Full mode (manual dispatch or FULL_REINDEX=true): re-indexes all modules.
"""

import os
import re
import sys
import time
import hashlib
import subprocess
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
EMBED_BATCH       = 8     # vectors per Voyage API call (keeps us ~40 RPM, under free-tier 100 RPM limit)
UPSERT_BATCH      = 50    # vectors per Pinecone upsert
EMBED_DELAY       = 1.5   # seconds between embedding batches
UPSERT_DELAY      = 2.0   # seconds between Pinecone upsert batches
UPSERT_RETRIES    = 6     # max retries per upsert batch on 429/5xx

MODULE_PATTERN    = re.compile(r"-m\d+\.html$")

# ── DELTA DETECTION ─────────────────────────────────────────────────────────

def get_changed_module_files():
    """Use git diff to find module files changed in the latest commit.
    Returns (changed_files, deleted_files) as lists of relative paths.
    """
    try:
        result = subprocess.run(
            ["git", "diff", "--name-status", "HEAD~1", "HEAD", "--", "ai-academy/modules/"],
            capture_output=True, text=True, check=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"  git diff failed: {e.stderr}")
        return None, None  # Fall back to full re-index

    changed = []
    deleted = []
    for line in result.stdout.strip().splitlines():
        if not line:
            continue
        parts = line.split("\t", 1)
        if len(parts) != 2:
            continue
        status, filepath = parts[0], parts[1]
        # Only care about module files (not hubs, admin pages, etc.)
        if not MODULE_PATTERN.search(filepath):
            continue
        if status.startswith("D"):
            deleted.append(filepath)
        else:
            # A (added), M (modified), R (renamed), C (copied)
            changed.append(filepath)

    return changed, deleted


def get_vector_ids_for_file(rel_path, max_chunks=100):
    """Generate all possible vector IDs for a given file path.
    Uses the same deterministic ID scheme as indexing.
    """
    ids = []
    for i in range(max_chunks):
        vec_id = hashlib.md5(f"{rel_path}::{i}".encode()).hexdigest()
        ids.append(vec_id)
    return ids

# ── HTML PARSING ─────────────────────────────────────────────────────────────

def extract_text_from_html(filepath):
    """Parse an HTML module file and return cleaned text + metadata."""
    with open(filepath, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    title_tag = soup.find("h1") or soup.find("title")
    title = title_tag.get_text(strip=True) if title_tag else filepath.stem
    if len(title) > 120:
        title = title[:120].rsplit(" ", 1)[0] + "…"

    text = soup.get_text(separator=" ", strip=True)
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

def embed_texts(texts, retries=5):
    """Embed a batch of texts using Voyage-3 via VoyageAI REST API."""
    for attempt in range(retries):
        try:
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
        except requests.exceptions.RequestException as e:
            if attempt < retries - 1:
                wait = min(5 * 2 ** attempt, 120)
                print(f"    Network error, retrying in {wait}s... ({e})")
                time.sleep(wait)
                continue
            raise RuntimeError(f"Voyage network error after {retries} retries: {e}")

        if resp.status_code == 200:
            data = resp.json()["data"]
            return [item["embedding"] for item in data]

        if resp.status_code == 429 and attempt < retries - 1:
            wait = min(5 * 2 ** attempt, 120)
            print(f"    Rate limited, waiting {wait}s...")
            time.sleep(wait)
            continue

        if resp.status_code >= 500 and attempt < retries - 1:
            wait = min(5 * 2 ** attempt, 120)
            print(f"    Server error ({resp.status_code}), retrying in {wait}s...")
            time.sleep(wait)
            continue

        print(f"    Voyage API error ({resp.status_code}): {resp.text[:500]}")
        raise RuntimeError(f"Voyage embedding failed ({resp.status_code}): {resp.text[:200]}")

    raise RuntimeError("Voyage embedding failed after all retries")

# ── UPSERT WITH RETRY ───────────────────────────────────────────────────────

def upsert_with_retry(index, vectors):
    """Upsert vectors to Pinecone in batches with retry on rate limits."""
    print(f"\nUpserting {len(vectors)} vectors to Pinecone...")
    for batch_start in range(0, len(vectors), UPSERT_BATCH):
        batch = vectors[batch_start : batch_start + UPSERT_BATCH]
        upsert_data = [
            (v["id"], v["embedding"], v["metadata"])
            for v in batch
        ]

        for attempt in range(UPSERT_RETRIES):
            try:
                index.upsert(vectors=upsert_data)
                break
            except Exception as e:
                err_str = str(e)
                is_retryable = ("429" in err_str or "Too Many Requests" in err_str
                                or "500" in err_str or "503" in err_str)
                if is_retryable and attempt < UPSERT_RETRIES - 1:
                    wait = min(3 * 2 ** attempt, 120)
                    print(f"    Pinecone rate limited, retrying in {wait}s... (attempt {attempt + 1})")
                    time.sleep(wait)
                    continue
                raise

        done = min(batch_start + UPSERT_BATCH, len(vectors))
        print(f"  Upserted {done}/{len(vectors)}")
        time.sleep(UPSERT_DELAY)

# ── PROCESS FILES ───────────────────────────────────────────────────────────

def process_files(file_list):
    """Parse, chunk, and prepare vectors for a list of module files."""
    all_vectors = []
    for filepath in file_list:
        if isinstance(filepath, str):
            filepath = Path(filepath)
        rel_path = str(filepath.relative_to(".")) if filepath.is_absolute() else str(filepath)

        if not filepath.exists():
            print(f"  Skipping (not found): {rel_path}")
            continue

        title, text = extract_text_from_html(filepath)

        if len(text.split()) < 20:
            print(f"  Skipping (too short): {rel_path}")
            continue

        chunks = chunk_text(text)
        print(f"  {rel_path}: {len(chunks)} chunks from '{title}'")

        for i, chunk in enumerate(chunks):
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

    return all_vectors


def embed_vectors(all_vectors):
    """Embed all vectors' text using Voyage-3."""
    if not all_vectors:
        return all_vectors

    print(f"\nEmbedding {len(all_vectors)} chunks...")
    embed_start = time.time()
    for batch_start in range(0, len(all_vectors), EMBED_BATCH):
        batch = all_vectors[batch_start : batch_start + EMBED_BATCH]
        texts = [v["text"] for v in batch]
        embeddings = embed_texts(texts)

        for vec, emb in zip(batch, embeddings):
            vec["embedding"] = emb

        done = min(batch_start + EMBED_BATCH, len(all_vectors))
        elapsed = time.time() - embed_start
        if (done // EMBED_BATCH) % 10 == 0 or done >= len(all_vectors):
            print(f"  Embedded {done}/{len(all_vectors)} ({elapsed:.0f}s)")

        time.sleep(EMBED_DELAY)

    print(f"  Embedding complete in {time.time() - embed_start:.0f}s")
    return all_vectors

# ── MAIN PIPELINE ────────────────────────────────────────────────────────────

def main():
    full_reindex = os.environ.get("FULL_REINDEX", "").lower() == "true"

    print("=== AIP Corpus Indexer ===")
    print(f"Mode: {'FULL re-index' if full_reindex else 'DELTA (changed files only)'}\n")

    # Connect to Pinecone
    print("Connecting to Pinecone...")
    pc = Pinecone(api_key=PINECONE_API_KEY)
    index = pc.Index(PINECONE_INDEX, host=PINECONE_HOST)
    stats = index.describe_index_stats()
    print(f"  Current vectors: {stats['total_vector_count']}\n")

    if full_reindex:
        # ── FULL RE-INDEX ────────────────────────────────────────────────
        html_files = sorted(MODULES_DIR.glob("**/*.html"))
        module_files = [f for f in html_files if MODULE_PATTERN.search(f.name)]
        print(f"Found {len(module_files)} module files.\n")

        # Process and upsert in file-batches to avoid overwhelming rate limits
        FILE_BATCH = 30  # files per round during full re-index
        for i in range(0, len(module_files), FILE_BATCH):
            batch_files = module_files[i:i + FILE_BATCH]
            print(f"\n── File batch {i // FILE_BATCH + 1} / {-(-len(module_files) // FILE_BATCH)}"
                  f" ({len(batch_files)} files) ──")
            batch_vectors = process_files(batch_files)
            if not batch_vectors:
                continue
            batch_vectors = embed_vectors(batch_vectors)
            upsert_with_retry(index, batch_vectors)
            if i + FILE_BATCH < len(module_files):
                print("  Cooling down 10s before next file batch...")
                time.sleep(10)

    else:
        # ── DELTA MODE ───────────────────────────────────────────────────
        changed_files, deleted_files = get_changed_module_files()

        if changed_files is None:
            print("  Could not determine changed files, falling back to full re-index.")
            os.environ["FULL_REINDEX"] = "true"
            return main()

        print(f"Changed/added module files: {len(changed_files)}")
        print(f"Deleted module files: {len(deleted_files)}")

        if not changed_files and not deleted_files:
            print("\nNo module files changed. Nothing to do.")
            return

        # Handle deletions: remove vectors for deleted files
        if deleted_files:
            print(f"\nRemoving vectors for {len(deleted_files)} deleted files...")
            for del_path in deleted_files:
                ids_to_delete = get_vector_ids_for_file(del_path)
                # Delete in batches of 100 (Pinecone limit)
                for i in range(0, len(ids_to_delete), 100):
                    batch = ids_to_delete[i:i+100]
                    try:
                        index.delete(ids=batch)
                    except Exception as e:
                        print(f"    Warning: delete failed for {del_path}: {e}")
                print(f"  Removed vectors for: {del_path}")

        # Handle changed/added files
        if changed_files:
            print(f"\nIndexing {len(changed_files)} changed files...")
            file_paths = [Path(f) for f in changed_files]
            all_vectors = process_files(file_paths)

            if all_vectors:
                print(f"\nTotal chunks to index: {len(all_vectors)}")
                all_vectors = embed_vectors(all_vectors)
                upsert_with_retry(index, all_vectors)
            else:
                print("No indexable content in changed files.")

    # Final stats
    stats = index.describe_index_stats()
    print(f"\nDone. Vectors now in index: {stats['total_vector_count']}")


if __name__ == "__main__":
    main()
