"""Step 01: Build the index.

This is the "indexing phase" from the article:
  collect docs -> extract -> chunk -> embed -> store vectors + metadata.

Run:
  python 01_build_index.py
"""

from pathlib import Path

from lib.chunking import make_chunks
from lib.embedding import DIMENSIONS, MODEL_NAME, embed_passages
from lib.store import save_index

DOCS_DIR = Path(__file__).resolve().parent / "data" / "docs"
MAX_CHARS = 300


def main():
    # 1) Collect documents and split them into chunks.
    chunks = []
    for doc_path in sorted(DOCS_DIR.glob("*.md")):
        chunks.extend(make_chunks(doc_path, max_chars=MAX_CHARS))
    print(f"docs: {len(list(DOCS_DIR.glob('*.md')))}  chunks: {len(chunks)}")

    # 2) Embed every chunk with the SAME model we will use for queries.
    print(f"embedding with {MODEL_NAME} ({DIMENSIONS} dims)...")
    embeddings = embed_passages([c["embed_text"] for c in chunks])

    # 3) Store vectors, chunk text, and the manifest.
    manifest = save_index(
        embeddings,
        chunks,
        model_name=MODEL_NAME,
        dimensions=DIMENSIONS,
        chunking_config={"strategy": "heading + paragraph merge", "max_chars": MAX_CHARS, "version": 1},
    )

    print(f"saved {manifest['num_chunks']} vectors to index/")
    print("\nchunk list:")
    for chunk in chunks:
        status = chunk["meta"].get("status", "-")
        print(f"  [{status:10s}] {chunk['chunk_id']:24s} {chunk['section']}")


if __name__ == "__main__":
    main()
