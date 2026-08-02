# Framework Atlas 0.2.0

Release date: 2026-08-02

## この release の位置付け

v0.1.1 の厳密な evidence dataset・再現可能 ZIP・公開検証を保持しながら、祖先・転換点・派生を上から下へ追える broad catalog と「家系図」を一つの release に統合した版です。

世界中の全 framework を永久に完全収録したと断定するものではありません。現在の curated catalog と、GitHub Topics を継続的に再収集・分類・レビューする仕組みを一緒に公開します。

## 収録内容

- 380 framework / library / runtime / adjacent project records
- 15 family-tree views
- 37 deep Markdown profiles
- 53 architecture concepts
- 129 evidence-aware relationships
- 53 history events
- 16 organization/ecosystem maps
- 25 GitHub-ready research Issue drafts
- 124 GitHub Topic collection seeds
- versioned v1 evidence dataset と 47件の登録済み実装 Issue digest
- Spring Boot / FastAPI / Gin / modular-monolith の `framework-depth-lab`

## 家系図としての改善

巨大な一枚 graph は使わず、次の15系統へ分割しました。

1. Java / Spring
2. Rails / Laravel と MVC
3. Python Web
4. Go HTTP
5. JavaScript / Edge backend
6. React
7. Vue
8. 現代 UI framework
9. Terminal UI / Textualize
10. ORM / Data Model
11. HTML over the wire
12. Erlang/OTP / Elixir / Phoenix
13. Mobile / Desktop UI
14. AI / Agent framework
15. GitHub router topic の「同じ語の別系統」

線は次の3種類です。

- 実線: 一次資料で確認済み
- 破線: 設計上の応答・影響候補で追加 evidence が必要
- 点線: 直接の血縁ではなく、同じ問題領域・共通基盤・分類

## 公開サイト

`docs/` は外部 service や package install を必要としない static site です。

- framework 検索
- category / language / maturity / status filter
- 15の家系図
- node 詳細
- framework 比較
- 歴史 timeline
- research Issue の検索・Markdown 表示
- mobile layout

GitHub Pages 用 workflow は `.github/workflows/pages.yml` に含まれます。

## 統合した release gate

- broad catalog と versioned v1 dataset の個別 validation
- curated profile を生成処理が削除しない regression test
- unit test、JavaScript syntax、static-server smoke
- root / depth-lab checksum manifest
- release ZIP の byte-for-byte reproducibility と安全な path 検査
- main、tag、Pages、release asset の exact SHA / digest read-back

## 公開手順

```bash
make check
make zip VERSION=v0.2.0
```

release は main の exact SHA に tag を作り、ZIP、`SHA256SUMS`、`release-manifest.json` を添付した後、匿名 HTTP で再検証します。

詳細は `README.md` と `START_HERE.md` を参照してください。
