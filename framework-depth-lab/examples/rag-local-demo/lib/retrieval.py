"""Retrieval core. Shared by the CLI (02, 05) and the debug UI (06).

One code path for scoring means: what you debug in the UI is exactly
what the CLI does. No drift between the two.
"""

from lib.embedding import embed_query
from lib.store import load_index


def parse_filters(pairs):
    """Turn ["status=current"] into {"status": "current"}."""
    filters = {}
    for pair in pairs or []:
        key, value = pair.split("=", 1)
        filters[key] = value
    return filters


class Retriever:
    """Loads the index once. Scores queries against every chunk."""

    def __init__(self):
        self.embeddings, self.chunks, self.manifest = load_index()

    def score_all(self, query):
        """Return (scores for every chunk, query vector).

        Vectors are L2-normalized, so dot product == cosine similarity.
        We return ALL scores, not only top-k. Seeing the full score
        distribution is the main debugging tool.
        """
        query_vec = embed_query(query)
        return self.embeddings @ query_vec, query_vec

    @staticmethod
    def passes(chunk, filters):
        """True if the chunk matches every metadata filter."""
        if not filters:
            return True
        return all(chunk["meta"].get(key) == value for key, value in filters.items())

    def search(self, query, k=5, filters=None):
        """Filter first, then rank. Returns a list of (score, chunk)."""
        scores, _ = self.score_all(query)
        candidates = [
            (float(scores[i]), chunk)
            for i, chunk in enumerate(self.chunks)
            if self.passes(chunk, filters)
        ]
        candidates.sort(key=lambda pair: pair[0], reverse=True)
        return candidates[:k]
