
"""
AESOP Academy — Pinecone Corpus Indexer
Runs inside GitHub Actions. Reads lesson files from the repo,
chunks them, embeds with Anthropic, and upserts into Pinecone.
"""

import os
import re
import time
import anthropic
from pathlib import Path
from bs4 import BeautifulSoup
from pinecone import Pinecone

ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
PINECONE_API_KEY  = os.environ["PINECONE_API_KEY"]
PINECONE_HOST     = "https://aesop-academy-sqe0vz2.svc.aped-4627-b74a.pinecone.io"
EMBED_MODEL       = "voyage-3"
CHUNK_SIZE        = 500
CHUNK_OVERLAP     = 50

def extract_text(html):
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "nav", "header", "footer"]):
        tag.decompose()
    text = soup.get_text(separator=" ", strip=True)
    return re.sub(r'\s+', ' ', text).strip()

def chunk_text(text):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + CHUNK_SIZE
        chunk = " ".join(words[start:end])
        if chunk.strip():
            chunks.append(chunk)
        start = end - CHUNK_OVERLAP
        if start >= len(words):
            break
    return chunks

def get_embedding(client, text):
    response = client.embeddings.create(model=EMBED_MODEL, input=text)
    return response.embeddings[0].values

def age_label(filename):
    name = Path(filename).stem
    return name.replace("age-", "").replace("plus", "+")

def main():
    print("AESOP Academy — Pinecone Indexer")
    print("=" * 50)

    anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    pc = Pinecone(api_key=PINECONE_API_KEY)
    index = pc.Index(host=PINECONE_HOST)

    modules_path = Path("ai-academy/modules")
    if not modules_path.exists():
        print("No modules folder found — nothing to index.")
        return

    total_vectors = 0
    total_files = 0

    for module_dir in sorted(modules_path.iterdir()):
        if not module_dir.is_dir():
            continue
        module_num = module_dir.name.replace("module-", "")
        print(f"\nModule {module_num}")

        for html_file in sorted(module_dir.glob("*.html")):
            print(f"  {html_file.name}...")
            html = html_file.read_text(encoding="utf-8", errors="ignore")
            text = extract_text(html)
            if len(text.split()) < 50:
                print(f"  Too short, skipping")
                continue
            chunks = chunk_text(text)
            print(f"  {len(chunks)} chunks")
            vectors = []
            for i, chunk in enumerate(chunks):
                try:
                    embedding = get_embedding(anthropic_client, chunk)
                    vectors.append({
                        "id": f"m{module_num}-{html_file.stem}-chunk{i}",
                        "values": embedding,
                        "metadata": {
                            "module": module_num,
                            "age_group": age_label(html_file.name),
                            "chunk_index": i,
                            "source": str(html_file),
                            "text": chunk[:500],
                        }
                    })
                    time.sleep(0.1)
                except Exception as e:
                    print(f"  Embedding error chunk {i}: {e}")
                    continue
            if vectors:
                for b in range(0, len(vectors), 100):
                    index.upsert(vectors=vectors[b:b+100])
                print(f"  Upserted {len(vectors)} vectors")
                total_vectors += len(vectors)
                total_files += 1

    print("\n" + "=" * 50)
    print(f"Done. Files: {total_files} | Vectors: {total_vectors}")

if __name__ == "__main__":
    main()
