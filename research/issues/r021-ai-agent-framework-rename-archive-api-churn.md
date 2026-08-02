---
title: "AI/agent framework の rename・archive・API churn を追跡する"
labels: "research,ai-agents,maintenance,priority/p2"
---

# AI/agent framework の rename・archive・API churn を追跡する

## 背景

LangChain、LangGraph、LlamaIndex、Haystack、Semantic Kernel、AutoGen、CrewAI、DSPy、OpenAI Agents SDK の scope と current API/guidance を quarterly に確認する。

## 完了条件

- [ ] official docs/release/repository を quarterly snapshot
- [ ] framework と hosted service を分離
- [ ] provider-neutrality を根拠付きで評価

## Evidence rule

- 直接影響は公式文書・作者発言・package/source dependency がある場合だけ確定する。
- 類似だけの場合は `needs-evidence` または `design-relative` のままにする。
- 変更した relation には confidence、verification、source URL を付ける。

## 主な変更対象

- `data/frameworks.json`
- `data/relations.json` または `data/families.json`
- `profiles/`、`history/`、`research/`

<!-- framework-atlas-gap:R021 -->
