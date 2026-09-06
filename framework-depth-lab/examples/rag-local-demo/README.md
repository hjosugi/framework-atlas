# rag-local-demo

A small local RAG pipeline. No API keys. No vector database.
It shows the ideas from the ByteByteGo article
"Why your RAG system depends on the embedding model" with running code.

## What you need

- Python 3.10+
- About 2 GB of disk (CPU-only PyTorch + one small model)
- Internet for the first run only (model download, about 470 MB)

## Setup

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# CPU-only torch first. It is much smaller than the CUDA build.
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
```

Embedding model: `intfloat/multilingual-e5-small`.
It is multilingual, so Japanese docs and Japanese queries work.
It uses `query: ` / `passage: ` prefixes. This is asymmetric retrieval:
a short question must match a long answer passage.

## Pipeline

```
INDEXING (run once)                      RETRIEVAL (every question)

data/docs/*.md                           "45日前に買った年間サブスクは..."
     |                                        |
     v                                        v
[chunking.py]  split + metadata          [embedding.py]  "query: ..." -> vector
     |                                        |
     v                                        v
[embedding.py] "passage: ..." -> vectors [02_search.py]  dot product vs all rows
     |                                        |
     v                                        v
index/embeddings.npy                     top-k chunks (+ metadata filter)
index/chunks.jsonl                            |
index/manifest.json                           v
                                         [05_ask.py]  prompt -> (optional) LLM
```

## Run the steps in order

```bash
# 1. Build the index. Chunk -> embed -> store.
python 01_build_index.py

# 2. Search. The article's main example: 45 days > 30-day limit.
python 02_search.py "45日前に買った年間サブスクは返金できますか？"

# The version trap: the deprecated 60-day policy also ranks high.
python 02_search.py "返金の条件を教えて"
# Fix it with a metadata filter:
python 02_search.py "返金の条件を教えて" --filter status=current

# 3. Failure modes with real cosine scores.
#    negation / numbers / entities / related-but-not-answering.
python 03_failure_modes.py

# 4. Matryoshka idea: truncate 384 dims to 128 and 64 and compare.
python 04_matryoshka.py

# 5. Full RAG: build the grounded prompt. LLM call is optional.
python 05_ask.py "45日前に買った年間サブスクは返金できますか？"
python 05_ask.py "..." --ollama-model qwen3:4b   # needs Ollama running

# 6. Visual debug UI. Open http://localhost:8765 in a browser.
python 06_debug_ui.py
```

## Debug UI (06_debug_ui.py)

A local instrument panel. The HTTP server uses the Python standard library;
retrieval also requires NumPy, sentence-transformers, and PyTorch. Install the
dependencies and download the model first. To avoid model update checks when
working offline, set `HF_HUB_OFFLINE=1` after the first successful run.

```
+--------------------------------------------------------------+
| RAG 検索デバッグ盤    model / dims / chunks                    |
| [ query....................... ] [k] [x] status=current  検索 |
| verdict: #1 ... / gap to #2 / warning if deprecated in top-k  |
+---------------------------+----------------------------------+
| score bars (ALL chunks)   |  vector space map (PCA 2D)       |
|  1 v2-000 ############    |     .   .    +query              |
|  . v1-000 #######~~~ dep  |   .    (1)--(2)   .              |
|  excluded shown, striped  |     deprecated marked in red     |
+---------------------------+----------------------------------+
| chunk inspector | prompt preview + copy | 2-sentence cosine lab|
+--------------------------------------------------------------+
```

What it makes visible:

- All scores, not only top-k. You see how close the wrong chunks are.
- What a metadata filter removes. Excluded chunks stay on screen, striped.
- A red warning when a deprecated chunk lands in top-k.
- The exact prompt the LLM would receive. Copy it with one click.
- A pair lab with presets for the article's traps (negation, numbers,
  entities, related-but-not-answering).
- The query's position in the vector space, with lines to its top-k.

The map is a PCA projection from 384 to 2 dims. It shows neighborhoods,
not exact distances. Trust the scores; use the map for intuition.

## Map to the article

| Article section                        | Where in this repo                          |
| -------------------------------------- | ------------------------------------------- |
| Indexing phase                         | `01_build_index.py`, `lib/chunking.py`      |
| Retrieval phase, top-k                 | `02_search.py`                              |
| Asymmetric search (query vs passage)   | prefixes in `lib/embedding.py`              |
| "Related is not correct" failure modes | `03_failure_modes.py`                       |
| Versions and dates                     | `--filter status=current` in `02_search.py` |
| Embedding record checklist             | `index/manifest.json` (`lib/store.py`)      |
| Content hash per chunk                 | `content_hash` in `lib/chunking.py`         |
| Why a better LLM cannot fix retrieval  | `05_ask.py` prints chunks BEFORE the LLM    |
| Matryoshka embeddings                  | `04_matryoshka.py`                          |
| Test and debug retrieval first         | `06_debug_ui.py` (visual inspector)         |

## Why no vector database?

At this size, a NumPy matrix and one dot product per query is exact
and fast. `embeddings @ query_vec` scores every chunk at once.
A vector DB (FAISS, Qdrant, pgvector) adds approximate search (ANN)
for millions of vectors, plus filtering and persistence at scale.
The concepts stay the same.

## Things to try next

- Break the prefixes. Remove `passage: ` in `lib/embedding.py`,
  rebuild, and watch scores drop. Cheap and very convincing.
- Swap the model. Change `MODEL_NAME`, run `01_build_index.py`,
  and note that a FULL rebuild is required. Old vectors are useless.
  This is the "changing the embedding model is expensive" section.
- Add a reranker. Retrieve top-20 with vectors, then rescore with a
  cross-encoder (for example `hotchpotch/japanese-reranker-*` or
  `cross-encoder/mmarco-mMiniLMv2-L12-H384-v1`) and keep top-3.
- Use `02_search.py --json` to pipe results into your own checks.
- Build a tiny eval set. 10 questions with expected chunk ids.
  Measure recall@k before and after any change. The article's main
  advice: debug retrieval first, not the prompt.

## Official references

- [multilingual-e5-small model card](https://huggingface.co/intfloat/multilingual-e5-small)
- [Sentence Transformers documentation](https://sbert.net/)
- [Ollama generate API](https://docs.ollama.com/api/generate)
