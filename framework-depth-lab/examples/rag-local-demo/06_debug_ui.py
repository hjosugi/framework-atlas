"""Step 06: Visual debug UI.

A local instrument panel for the retriever. It shows, live:
- every chunk's score for a query (not only top-k)
- the vector space as a 2D map (PCA), with the query position
- what a metadata filter removes
- the exact prompt the LLM would receive
- a two-sentence cosine lab for the failure modes

Only the standard library + numpy. No web framework.

Run:
  python 06_debug_ui.py            # http://localhost:8765
  python 06_debug_ui.py --port 9000
"""

import argparse
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import numpy as np

from lib.embedding import embed_raw
from lib.prompting import build_prompt
from lib.retrieval import Retriever

WEB_DIR = Path(__file__).resolve().parent / "web"

STATIC_ROUTES = {
    "/": ("index.html", "text/html; charset=utf-8"),
    "/app.js": ("app.js", "text/javascript; charset=utf-8"),
    "/style.css": ("style.css", "text/css; charset=utf-8"),
}


class DebugState:
    """Index + a fixed 2D projection of the vector space.

    PCA keeps the two directions with the most variance. 384 dims -> 2 dims
    loses a lot, so the map shows neighborhoods, not exact distances.
    Trust the cosine scores. Use the map for intuition.
    """

    def __init__(self):
        self.retriever = Retriever()
        embeddings = self.retriever.embeddings
        self.mean = embeddings.mean(axis=0)
        centered = embeddings - self.mean
        _, _, vt = np.linalg.svd(centered, full_matrices=False)
        self.components = vt[:2]  # top-2 principal directions
        self.coords = centered @ self.components.T

    def project(self, vector):
        """Put a new vector (the query) on the same 2D map."""
        return (vector - self.mean) @ self.components.T


def chunk_payload(state):
    """Chunks + 2D coordinates, ready for the frontend."""
    items = []
    for i, chunk in enumerate(state.retriever.chunks):
        items.append({
            "i": i,
            "chunk_id": chunk["chunk_id"],
            "doc": chunk["doc"],
            "section": chunk["section"],
            "text": chunk["text"],
            "embed_text": chunk["embed_text"],
            "content_hash": chunk["content_hash"],
            "meta": chunk["meta"],
            "x": float(state.coords[i, 0]),
            "y": float(state.coords[i, 1]),
        })
    return items


def handle_state(state, _params):
    return {
        "manifest": state.retriever.manifest,
        "chunks": chunk_payload(state),
    }


def handle_search(state, params):
    query = params.get("q", [""])[0].strip()
    if not query:
        return {"error": "empty query"}
    k = max(1, min(int(params.get("k", ["3"])[0]), len(state.retriever.chunks)))
    filters = {}
    for pair in params.get("filter", []):
        if "=" in pair:
            key, value = pair.split("=", 1)
            filters[key] = value

    scores, query_vec = state.retriever.score_all(query)

    # Rank ALL chunks. Mark which ones the filter removes.
    order = list(np.argsort(-scores))
    passes = [state.retriever.passes(c, filters) for c in state.retriever.chunks]
    top_ids = [i for i in order if passes[i]][:k]

    query_xy = state.project(query_vec)
    results = [(float(scores[i]), state.retriever.chunks[i]) for i in top_ids]

    return {
        "query": query,
        "k": k,
        "filters": filters,
        "scores": [round(float(s), 4) for s in scores],
        "order": [int(i) for i in order],
        "passes": passes,
        "top_ids": [int(i) for i in top_ids],
        "query_xy": [float(query_xy[0]), float(query_xy[1])],
        "prompt": build_prompt(query, results),
    }


def handle_pair(_state, params):
    text_a = params.get("a", [""])[0].strip()
    text_b = params.get("b", [""])[0].strip()
    if not text_a or not text_b:
        return {"error": "both texts are required"}
    vec_a, vec_b = embed_raw([text_a, text_b])
    return {"a": text_a, "b": text_b, "cosine": round(float(np.dot(vec_a, vec_b)), 4)}


API_ROUTES = {
    "/api/state": handle_state,
    "/api/search": handle_search,
    "/api/pair": handle_pair,
}


def make_handler(state):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            parsed = urlparse(self.path)

            if parsed.path in API_ROUTES:
                payload = API_ROUTES[parsed.path](state, parse_qs(parsed.query))
                body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
                self._send(200, "application/json; charset=utf-8", body)
                return

            if parsed.path in STATIC_ROUTES:
                filename, content_type = STATIC_ROUTES[parsed.path]
                body = (WEB_DIR / filename).read_bytes()
                self._send(200, content_type, body)
                return

            self._send(404, "text/plain; charset=utf-8", b"not found")

        def _send(self, status, content_type, body):
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")  # always fresh while debugging
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, fmt, *args):
            # Keep the terminal readable. Comment this out to see every request.
            pass

    return Handler


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()

    print("loading index and model...")
    state = DebugState()
    print(f"{len(state.retriever.chunks)} chunks / model: {state.retriever.manifest['model_name']}")
    print(f"open http://localhost:{args.port}  (Ctrl+C to stop)")

    server = HTTPServer(("localhost", args.port), make_handler(state))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")


if __name__ == "__main__":
    main()
