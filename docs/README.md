# Framework Atlas

Framework の名前を並べるだけではなく、**何を解決するために生まれ、どの設計を受け継ぎ、次の世代が何を改善しようとしたか**を、家系図・歴史・比較表で調べるための公開データベースです。

GitHub Pages だけで公開できます。検索、分類、家系図、比較、timeline、調査 Issue はすべて静的 HTML / CSS / JavaScript で動き、外部 SaaS、database、CDN package は必要ありません。

- 公開サイト: https://hjosugi.github.io/framework-atlas/
- 最新 release: https://github.com/hjosugi/framework-atlas/releases/tag/v0.2.0
- versioned schema: [`schema/`](schema/) / [`data/*.v1.json`](data/)

![Rails / Laravel 家系図のプレビュー](docs/assets/family-tree-preview.png)

## 最初に見る場所

1. `docs/index.html` — 公開サイト本体
2. `data/families.json` — 読みやすく整理した15の家系図
3. `data/frameworks.json` — framework / library / runtime / adjacent project の catalog
4. `data/relations.json` — evidence-aware な影響・依存関係
5. `research/issues/` — 追加調査を GitHub Issue にできる Markdown

## 二つのデータ層

- `data/frameworks.json` などは、380件を検索・家系図・比較へ使う broad catalog です。
- `data/*.v1.json` は、根拠種別、確度、未測定、Kofun 実装対応を厳密に検証する versioned dataset です。

両者は同じ release に含まれます。broad catalog の自動更新が v1 の curated claim や profile を削除・上書きしないことを build と test で検証します。詳細調査の原資料と共通 API sample は [`framework-depth-lab/`](framework-depth-lab/) にあります。

## 現在の収録内容

- 380 framework / project records
- 15 family-tree views
- 37 deep profiles
- 53 architecture concepts
- 129 global relationship edges
- 53 historical events
- 25 structured research gaps
- Web、frontend、backend、router、ORM、TUI、mobile/desktop、testing、AI/data、game、runtime など

収録件数は `make build` のたびに `data/stats.json` へ再計算されます。

## 家系図の読み方

家系図は上から下へ読みます。

- **実線**: 公式文書または一次資料で確認できた関係
- **破線**: 設計上の影響・応答として有力だが、追加 evidence が必要
- **点線**: 直接の血縁ではなく、同じ問題領域、共通基盤、topic 分類

巨大な一枚 graph は作りません。Spring、Rails/Laravel、Python Web、Go HTTP、React、Vue、Textualize、ORM などを別々の家系図にし、各 node をクリックすると「何を解決するか」「設計の核」「歴史」「強みと tradeoff」「つながる線の理由」が開きます。

## ローカルで確認

Python 3.11 以上だけで動きます。

```bash
make check
make zip
make serve
```

`make check` は二つの dataset、生成 drift、unit test、JavaScript 構文、静的 server smoke、checksum manifest、ZIP 再現性をまとめて検証します。

次を開きます。

```text
http://localhost:8000
```

`docs/index.html` を直接開いても、`docs/data/atlas.js` を使うため基本機能は動作します。

## GitHub Pages で公開

1. `make check` を通す
2. main branch へ pushする
3. `.github/workflows/pages.yml` の成功を確認する
4. tag と release asset を同じ main commit から作る
5. Pages、tag、ZIP、checksum を匿名 HTTP で読み戻す

CI が green でも Pages や release asset の公開完了とは見なしません。`scripts/verify_public_release.py` が公開 URL と digest を個別に照合します。

## 追加調査を Issue に登録

まず dry run で確認します。

```bash
python scripts/create_issues.py --repo hjosugi/framework-atlas --dry-run
```

問題なければ `--dry-run` を外します。

```bash
python scripts/create_issues.py --repo hjosugi/framework-atlas
```

同じ title の Issue は既定で重複作成しません。必要な label も作成します。

## GitHub Topics を再収集

GitHub Search API の一 query 1,000件制限を避けるため、作成日、stars、size で再帰分割します。Python standard library のみを使用します。

```bash
export GITHUB_TOKEN=...
python scripts/collect_github_topics.py --scope core --dry-run
python scripts/collect_github_topics.py --scope core --resume
python scripts/merge_discovered.py --min-confidence 0.85 --max-new 500
make check
```

自動発見された候補は、curated explanation や family tree を上書きしません。

## データ構造

```text
framework-atlas/
├── data/
│   ├── frameworks.json          # canonical catalog
│   ├── concepts.json            # MVC、DI、ASGI、VDOM など
│   ├── relations.json           # global evidence-aware graph
│   ├── families.json            # 読みやすい家系図 editorial layer
│   ├── timeline.json            # historical events
│   ├── ecosystems.json          # organization/ecosystem grouping
│   ├── research-gaps.json       # Issue source data
│   └── *.v1.json                # strict evidence / implementation dataset
├── docs/
│   ├── index.html
│   ├── app.js
│   ├── styles.css
│   └── data/                    # GitHub Pages bundle
├── research/issues/             # GitHub-ready Markdown
├── framework-depth-lab/         # deep research, examples, benchmark protocol
├── scripts/                     # collect/build/validate/publish tools
├── tests/
└── .github/workflows/
```

## 「すべて網羅」の扱い

世界中の全 framework が永久に完全であることは証明できません。GitHub topic はユーザー付与で、private repository、GitHub 外の project、rename、archive、同名 project、誤分類があります。

そのため本 project は completeness を次の process として管理します。

- dated snapshot を残す
- deep / standard / seed を分ける
- framework、library、runtime、application、network product、security tool を分離する
- 未検証の影響を事実として表示しない
- 不足を Markdown Issue として追跡する
- collector と public contribution で更新し続ける

詳細は [METHODOLOGY.md](METHODOLOGY.md) と [LIMITATIONS.md](LIMITATIONS.md) を参照してください。

## License

Code and original structured content are provided under the MIT License. Linked project names, trademarks, documentation, and source material remain the property of their respective owners. Summaries are paraphrases; source URLs are retained for verification.
