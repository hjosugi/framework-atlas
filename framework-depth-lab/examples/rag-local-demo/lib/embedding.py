"""Embedding model wrapper.

Model: intfloat/multilingual-e5-small
- Multilingual. Works for Japanese docs and Japanese queries.
- Output: 384 dimensions, L2-normalized.
- Trained for asymmetric retrieval (short query -> long passage).
  So it NEEDS prefixes: "query: " and "passage: ".
  If you drop the prefixes, retrieval quality drops. This is a real example
  of the "query and passage have different forms" point in the article.

First run downloads the model (about 470 MB) into the Hugging Face cache.
After that it runs fully offline.
"""

from sentence_transformers import SentenceTransformer

MODEL_NAME = "intfloat/multilingual-e5-small"
DIMENSIONS = 384

_model = None


def get_model():
    """Load the model once. Reuse it after that."""
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model


def embed_passages(texts):
    """Embed document chunks. E5 expects the "passage: " prefix here."""
    model = get_model()
    return model.encode(
        [f"passage: {t}" for t in texts],
        normalize_embeddings=True,  # unit vectors -> dot product == cosine
        show_progress_bar=False,
    )


def embed_query(text):
    """Embed one question. E5 expects the "query: " prefix here."""
    model = get_model()
    return model.encode([f"query: {text}"], normalize_embeddings=True)[0]


def embed_raw(texts):
    """Embed with no prefix. Used only for similarity experiments."""
    model = get_model()
    return model.encode(list(texts), normalize_embeddings=True, show_progress_bar=False)
