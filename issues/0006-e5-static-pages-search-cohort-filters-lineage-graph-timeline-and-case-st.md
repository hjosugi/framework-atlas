# #6 E5 static Pages: search, cohort filters, lineage graph, timeline, and case-study UX

- State: open
- Labels: none
- URL: https://github.com/hjosugi/framework-atlas/issues/6
- Updated: 2026-08-02T05:45:13Z

## Metadata
- State: ready
- Tracker role: execution lane
- Parent: [A0 #1](https://github.com/hjosugi/framework-atlas/issues/1)
- Blocked on: E1 data contract; UI shell can start with fixtures

## Outcome

追加サービス、backend、外部search、CDN依存なしで GitHub Pages 上に動作する Atlas を実装する。

## Artifacts

- `docs/index.html`
- `docs/app.js`
- `docs/style.css`
- generated `docs/atlas-data.json`
- `docs/.nojekyll`
- browser smoke script or deterministic DOM checks

## Required views

1. search + cohort/kind/language/profile/evidence filter
2. detail profile
3. directed lineage graph
4. generation timeline
5. comparison matrix
6. unresolved points
7. modular-monolith DDD case study and framework mappings
8. methodology/source drill-down

## Graph behavior

relation type、confidence、official/inference filterを持つ。arrow方向を表示し、edge選択で根拠URLと判断理由を出す。孤立nodeやquarantine候補も表示/非表示を選べる。

## Gates

- [ ] static file serverと `file://` 相当fixtureで主要機能を確認。
- [ ] keyboard操作、focus、semantic landmarks、reduced-motion、contrastを検証。
- [ ] mobile幅で検索、graph、tableが使用可能。
- [ ] JS無効時にも方法論とデータdownload linkが見える。
- [ ] user inputを `innerHTML` に入れない。
- [ ] URL queryで検索/filters/profileを再現可能。
- [ ] generated data driftをCIが拒否。

## Non-goals

ログイン、コメント、広告、analytics、server-side rendering、外部graph library。

## Children

- [ ] [#37](https://github.com/hjosugi/framework-atlas/issues/37) S1 site generation
- [ ] [#38](https://github.com/hjosugi/framework-atlas/issues/38) S2 search/filter/detail
- [ ] [#39](https://github.com/hjosugi/framework-atlas/issues/39) S3 lineage graph
- [ ] [#40](https://github.com/hjosugi/framework-atlas/issues/40) S4 timeline/matrices/case
- [ ] [#41](https://github.com/hjosugi/framework-atlas/issues/41) S5 accessibility/security/smoke
