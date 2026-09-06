"""Tiny vector store on disk.

Three files inside index/:
- embeddings.npy : one matrix, one row per chunk (float32)
- chunks.jsonl   : text + metadata for each row, same order
- manifest.json  : which model made these vectors, and how

The manifest follows the checklist from the article. If you change the
model, the prefixes, or the chunking, old vectors are not compatible.
The manifest is how you notice that before you mix them.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

INDEX_DIR = Path(__file__).resolve().parent.parent / "index"


def save_index(embeddings, chunks, model_name, dimensions, chunking_config):
    INDEX_DIR.mkdir(exist_ok=True)

    np.save(INDEX_DIR / "embeddings.npy", embeddings.astype(np.float32))

    with open(INDEX_DIR / "chunks.jsonl", "w", encoding="utf-8", newline="\n") as f:
        for chunk in chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + "\n")

    manifest = {
        # The article says: record the model, the format, and the settings.
        "model_name": model_name,
        "dimensions": dimensions,
        "prefix_format": {"query": "query: ", "passage": "passage: "},
        "normalization": "l2",
        "similarity": "dot_product (== cosine because vectors are normalized)",
        "chunking": chunking_config,
        "num_chunks": len(chunks),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    with open(INDEX_DIR / "manifest.json", "w", encoding="utf-8", newline="\n") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    return manifest


def load_index():
    if not (INDEX_DIR / "embeddings.npy").exists():
        raise SystemExit("Index not found. Run: python 01_build_index.py")

    embeddings = np.load(INDEX_DIR / "embeddings.npy")
    chunks = []
    with open(INDEX_DIR / "chunks.jsonl", encoding="utf-8") as f:
        for line in f:
            chunks.append(json.loads(line))
    with open(INDEX_DIR / "manifest.json", encoding="utf-8") as f:
        manifest = json.load(f)
    return embeddings, chunks, manifest
