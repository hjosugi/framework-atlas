"""Step 05: Full RAG answer.

retrieve top-k -> build a grounded prompt -> (optional) call a local LLM.

The LLM part is optional on purpose. The article's point: if retrieval
fails, no LLM can fix it. So first LOOK at the retrieved chunks and the
prompt. That is what this script prints.

Run (prompt only):
  python 05_ask.py "45日前に買った年間サブスクは返金できますか？"

Run with a local LLM via Ollama (https://ollama.com):
  ollama pull qwen3:4b
  python 05_ask.py "45日前に買った年間サブスクは返金できますか？" --ollama-model qwen3:4b
"""

import argparse
import json
import urllib.error
import urllib.request

from lib.prompting import build_prompt
from lib.retrieval import Retriever, parse_filters


def call_ollama(model, prompt):
    """Call a local Ollama server with the standard /api/generate endpoint."""
    payload = json.dumps({"model": model, "prompt": prompt, "stream": False}).encode("utf-8")
    request = urllib.request.Request(
        "http://localhost:11434/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=300) as response:
        return json.loads(response.read())["response"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    parser.add_argument("--k", type=int, default=3)
    parser.add_argument("--filter", action="append", default=["status=current"],
                        help="metadata filter (default: status=current)")
    parser.add_argument("--no-filter", action="store_true", help="disable all filters")
    parser.add_argument("--ollama-model", help="e.g. qwen3:4b. If not set, only print the prompt.")
    args = parser.parse_args()

    filters = {} if args.no_filter else parse_filters(args.filter)
    retriever = Retriever()
    results = retriever.search(args.query, k=args.k, filters=filters)

    print("--- retrieved chunks " + "-" * 39)
    for rank, (score, chunk) in enumerate(results, start=1):
        print(f"#{rank} score={score:.4f} {chunk['chunk_id']} ({chunk['meta'].get('status', '-')})")
    print()

    prompt = build_prompt(args.query, results)
    print("--- prompt sent to the LLM " + "-" * 33)
    print(prompt)

    if not args.ollama_model:
        print("(no --ollama-model given, so only the prompt is shown)")
        return

    print("--- LLM answer " + "-" * 45)
    try:
        print(call_ollama(args.ollama_model, prompt).strip())
    except (urllib.error.URLError, OSError) as error:
        print(f"Could not reach Ollama at localhost:11434 ({error}).")
        print("Install Ollama, run `ollama pull <model>`, then retry.")


if __name__ == "__main__":
    main()
