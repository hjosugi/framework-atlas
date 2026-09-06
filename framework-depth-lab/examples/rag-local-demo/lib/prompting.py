"""Prompt assembly. Shared by 05_ask.py and the debug UI."""

PROMPT_TEMPLATE = """あなたはカスタマーサポートのアシスタントです。
以下のコンテキストに書かれている情報だけを使って質問に答えてください。
コンテキストに答えが含まれていない場合は、「提供された情報からは分かりません」と答えてください。

# コンテキスト
{context}

# 質問
{question}

# 回答
"""


def build_prompt(query, results):
    """results is a list of (score, chunk) pairs from Retriever.search."""
    blocks = []
    for rank, (score, chunk) in enumerate(results, start=1):
        meta = chunk["meta"]
        source = f"{meta.get('title', chunk['doc'])} / {chunk['section']} (date: {meta.get('date', '-')})"
        blocks.append(f"[{rank}] {source}\n{chunk['text']}")
    return PROMPT_TEMPLATE.format(context="\n\n".join(blocks), question=query)
