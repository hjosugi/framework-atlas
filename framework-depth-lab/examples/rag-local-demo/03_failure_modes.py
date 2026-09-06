"""Step 03: Reproduce the failure modes from the article with real numbers.

"Related is not the same as correct."
Here we measure cosine similarity for the exact traps the article lists:
  1. negation           (can delete / cannot delete)
  2. numeric identifier (30 days / 60 days)
  3. same words, different entity (billing address / email address)
  4. similar topic, different question (eligibility / timing)

Run:
  python 03_failure_modes.py
"""

import numpy as np

from lib.embedding import embed_passages, embed_query, embed_raw


def show_pair(label, text_a, text_b):
    vec_a, vec_b = embed_raw([text_a, text_b])
    sim = float(np.dot(vec_a, vec_b))
    print(f"[{label}]  cosine = {sim:.4f}")
    print(f"  A: {text_a}")
    print(f"  B: {text_b}")
    print()


def main():
    print("=" * 60)
    print("Sentence pairs. High cosine, opposite or different meaning.")
    print("=" * 60)

    show_pair(
        "negation",
        "管理者はアーカイブ済みのプロジェクトを削除できます。",
        "管理者はアーカイブ済みのプロジェクトを削除できません。",
    )
    show_pair(
        "numeric",
        "年間サブスクリプションは30日以内であれば返金できます。",
        "年間サブスクリプションは60日以内であれば返金できます。",
    )
    show_pair(
        "entity",
        "請求先住所を変更する方法を説明します。",
        "メールアドレスを変更する方法を説明します。",
    )

    print("=" * 60)
    print("Query vs passages. Which passage actually answers the question?")
    print("=" * 60)

    query = "承認された返金が届くまでどのくらいかかりますか？"
    passages = [
        "年間サブスクリプションは、購入日から30日以内に申請した場合のみ返金できます。",  # eligibility
        "承認された返金は、5〜7営業日以内に元の支払い方法へ返金されます。",  # timing (the answer)
        "解約は次回の請求を止める操作です。解約しても自動的に返金は行われません。",  # cancellation
    ]
    labels = ["eligibility (related, no answer)", "timing (the real answer)", "cancellation (related topic)"]

    query_vec = embed_query(query)
    passage_vecs = embed_passages(passages)
    scores = passage_vecs @ query_vec

    print(f"query: {query}\n")
    order = np.argsort(-scores)
    for rank, i in enumerate(order, start=1):
        print(f"#{rank}  score={scores[i]:.4f}  {labels[i]}")
        print(f"    {passages[i]}")
    print()
    print("Lesson: all three scores are close. The model finds RELATED text.")
    print("It does not check if the text ANSWERS the question.")
    print("This is why we need eval sets, rerankers, and metadata filters.")


if __name__ == "__main__":
    main()
