# Framework Atlas

Framework Atlas は、Webフレームワークと周辺技術の設計史・系譜・トレードオフを、根拠と確度を失わず比較する公開データセット兼静的サイトです。目的は人気順位を作ることではなく、`kofun-boot` の実装判断に再利用できる設計材料を作ることです。

- 公開サイト: https://hjosugi.github.io/framework-atlas/
- versioned ZIP: https://github.com/hjosugi/framework-atlas/releases/tag/v0.1.1
- methodology: [データの読み方](#データの読み方) / [`schema/`](schema/) / [`data/`](data/)

## 収録するもの

- Spring Boot、FastAPI、Ginを中心とする詳細プロファイル
- Rails、Laravel、Django、React、Vueと現代のWebフレームワーク群
- router、ORM、UI、desktop/mobile、TUI、AI/dataなどの周辺カテゴリ
- 公式な影響関係と、根拠付きの推定類似を分離した有向グラフ
- modular-monolith-with-ddd から抽出したDDD、CQRS、Outbox/Inbox、Event Sourcing、テスト戦略
- Spring Boot／FastAPI／Gin／Kofunへの実装対応表
- 追加サービス不要のGitHub Pagesサイトと再現可能な配布ZIP

## ローカル検証

Python 3.11以降だけを使います。外部パッケージは不要です。

```sh
make check
make site
make zip
```

`make check` はスキーマ間整合性、根拠、分類、収集器の境界条件、静的サイト、ZIP再現性を検証します。`make site` は `docs/atlas-data.json` を決定的に再生成します。

## データの読み方

- `data/entities.v1.json`: 比較対象と隔離候補
- `data/relations.v1.json`: 向き・関係種別・確度・根拠を持つ辺
- `data/claims.v1.json`: 比較表や説明の根拠
- `data/unresolved.v1.json`: 未測定・未決・検証待ち
- `data/case-studies/`: 本番級アーキテクチャのケース抽出と実装対応
- `profiles/`: 人間向けの詳細調査
- `issues/`: GitHub Issueから生成する実装索引

`official` は公式文書が明示した関係、`primary-code` は一次コードから確認できる構成、`inference` は複数の設計特性が似るという推定です。推定を公式な影響として表示しません。性能値は同一条件の測定がない限り `unmeasured` です。

## 更新

```sh
GITHUB_TOKEN=... python3 scripts/collect_github.py --topic framework --output data/snapshots/framework.json
python3 scripts/normalize_snapshot.py data/snapshots/framework.json
python3 scripts/export_issues.py --repo hjosugi/framework-atlas
```

収集器はGitHub Search APIの1000件上限を作成日区間の再帰分割で回避し、ページ単位のチェックポイントを残します。トークン、レスポンスヘッダー、生の個人情報は保存しません。

## ライセンス

コードと編集物はMIT Licenseです。リンク先プロジェクトの名称・文書・コードは各権利者と各ライセンスに従います。
