---
title: "Frontend meta-framework の server/client boundary を比較する"
labels: "research,frontend,meta-framework,priority/p1"
---

# Frontend meta-framework の server/client boundary を比較する

## 背景

Next.js、React Router、Nuxt、SvelteKit、SolidStart、Qwik City、Astro、Analog の data loading、server function、cache、streaming、hydration/resume を比較する。

## 完了条件

- [ ] route unit と cache unit を記録
- [ ] static/server/edge deployment 差を記録
- [ ] vendor hosting と portable output を区別

## Evidence rule

- 直接影響は公式文書・作者発言・package/source dependency がある場合だけ確定する。
- 類似だけの場合は `needs-evidence` または `design-relative` のままにする。
- 変更した relation には confidence、verification、source URL を付ける。

## 主な変更対象

- `data/frameworks.json`
- `data/relations.json` または `data/families.json`
- `profiles/`、`history/`、`research/`

<!-- framework-atlas-gap:R013 -->
