"""Step 04: Dimension truncation experiment (Matryoshka idea).

The article: Matryoshka models pack a rough meaning into the first
dimensions and details into the later ones. So you can cut the vector
short and still search.

Here we truncate our 384-dim vectors to 128 and 64 dims and compare
top-3 results against the full vectors.

IMPORTANT: multilingual-e5-small is NOT trained as a Matryoshka model.
So truncation may hurt more than it would with a real MRL model
(for example nomic-embed-text-v1.5 or OpenAI text-embedding-3).
That contrast is the point of this experiment.

Run:
  python 04_matryoshka.py
"""

import numpy as np

from lib.embedding import embed_query
from lib.store import load_index

QUERIES = [
    "45日前に買った年間サブスクは返金できますか？",
    "返金はいつ届きますか？",
    "メールアドレスを変えたい",
]


def normalize_rows(matrix):
    """Re-normalize after truncation. Otherwise dot product is not cosine."""
    norms = np.linalg.norm(matrix, axis=-1, keepdims=True)
    return matrix / np.clip(norms, 1e-12, None)


def top_k(embeddings, query_vec, k=3):
    scores = embeddings @ query_vec
    order = np.argsort(-scores)[:k]
    return [(int(i), float(scores[i])) for i in order]


def main():
    embeddings, chunks, manifest = load_index()
    full_dims = embeddings.shape[1]

    for query in QUERIES:
        query_vec = embed_query(query)
        print("=" * 60)
        print(f"query: {query}")

        baseline = top_k(embeddings, query_vec)
        baseline_ids = [i for i, _ in baseline]

        for dims in (full_dims, 128, 64):
            # Keep only the first `dims` values, then re-normalize.
            emb_cut = normalize_rows(embeddings[:, :dims])
            q_cut = normalize_rows(query_vec[:dims][None, :])[0]
            results = top_k(emb_cut, q_cut)

            overlap = len(set(i for i, _ in results) & set(baseline_ids))
            marker = "baseline" if dims == full_dims else f"overlap with baseline: {overlap}/3"
            print(f"\n  dims={dims:3d}  ({marker})")
            for rank, (i, score) in enumerate(results, start=1):
                print(f"    #{rank} score={score:.4f}  {chunks[i]['chunk_id']}  {chunks[i]['section']}")
        print()

    print("Storage math (float32):")
    for dims in (full_dims, 128, 64):
        print(f"  {dims:3d} dims -> {dims * 4:4d} bytes/vector "
              f"-> {dims * 4 * 1_000_000 / 1e9:.2f} GB per 1M chunks")


if __name__ == "__main__":
    main()
