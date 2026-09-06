"""Step 02: Search the index.

This is the "retrieval phase" from the article:
  embed the query -> compare vectors -> return top-k chunks.

Run:
  python 02_search.py "45日前に買った年間サブスクは返金できますか？"
  python 02_search.py "返金はいつ届きますか？" --k 3
  python 02_search.py "返金の条件" --filter status=current
  python 02_search.py "返金の条件" --json          # machine-readable output

Note the filter example. Without the filter, the deprecated 60-day policy
can rank high. Embeddings cannot tell "old" from "new" by meaning alone.
Metadata filters fix that. This is the "versions and dates" failure mode.

For a visual version of this script, run: python 06_debug_ui.py
"""

import argparse
import json

from lib.retrieval import Retriever, parse_filters


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    parser.add_argument("--k", type=int, default=5)
    parser.add_argument("--filter", action="append", help="metadata filter, e.g. status=current")
    parser.add_argument("--json", action="store_true", help="print results as JSON")
    args = parser.parse_args()

    filters = parse_filters(args.filter)
    retriever = Retriever()
    results = retriever.search(args.query, k=args.k, filters=filters)

    if args.json:
        payload = [
            {"rank": rank, "score": round(score, 4), "chunk_id": chunk["chunk_id"],
             "section": chunk["section"], "meta": chunk["meta"], "text": chunk["text"]}
            for rank, (score, chunk) in enumerate(results, start=1)
        ]
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return

    print(f"query : {args.query}")
    print(f"model : {retriever.manifest['model_name']}")
    if filters:
        print(f"filter: {filters}")
    print()

    for rank, (score, chunk) in enumerate(results, start=1):
        meta = chunk["meta"]
        print(f"#{rank}  score={score:.4f}  {chunk['chunk_id']}  "
              f"(status={meta.get('status', '-')}, date={meta.get('date', '-')})")
        print(f"    section: {chunk['section']}")
        for line in chunk["text"].splitlines():
            print(f"    | {line}")
        print()


if __name__ == "__main__":
    main()
