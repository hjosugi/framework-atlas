# Framework Depth Lab

Spring Boot 4.1.0、FastAPI 0.141.1、Gin 1.12.0を、同じ物差しで分解するための研究リポジトリです。さらに `kgrzybek/modular-monolith-with-ddd` を、本番級アプリケーション構造のケーススタディとして分析します。

調査基準日: 2026-08-02 (JST)

## 最初に読む順番

1. [Executive Summary](EXECUTIVE_SUMMARY.md)
2. [3フレームワーク横断比較](docs/04-comparison.md)
3. [request lifecycleと内部構造](docs/06-request-lifecycle.md)
4. [Modular Monolith with DDDケーススタディ](docs/13-modular-monolith-case-study.md)
5. [新しいframeworkを設計するときの原則](docs/12-framework-design-lessons.md)

## 重要な結論

3者は同じカテゴリではありません。

| 対象 | 主な責任 | 意図的に持たないもの |
|---|---|---|
| Spring Boot | Springベースのアプリケーション全体を起動・自動構成・運用可能にする | ドメイン設計そのもの |
| FastAPI | Pythonの型宣言から検証・DI・OpenAPIを統合したAPIを作る | ORM、ジョブ基盤、完全な運用プラットフォーム |
| Gin | Go `net/http` 上に高速routing、middleware、binding、renderingを足す | DI container、ORM、OpenAPI自動生成、アプリ構造 |

したがって、単純な「どれが一番速いか」ではなく、`frameworkが代わりに引き受ける責任 / 利用者に残す責任 / そのために払う実行時・学習・運用コスト`を比較します。

## 内容

- `docs/`: 歴史、内部構造、data model、concurrency、security、testing、operations、migration、設計原則
- `data/`: 機械可読な比較表、影響関係edge、一次情報registry
- `examples/`: 同一API contractのSpring Boot / FastAPI / Gin実装
- `contracts/`: 3実装共通のOpenAPI contract
- `benchmarks/`: 公平な計測を行うための実験計画とk6 scenario
- `issues/`: 追加調査・実装課題。1ファイルを1 GitHub Issueとして登録可能
- `site/`: dependency-freeのGitHub Pages用ダッシュボード
- `scripts/validate.py`: repository全体の静的検証
- `scripts/create-issues.sh`: `issues/*.md` をGitHub Issueとして登録する補助script

## GitHub Pages

Actionsを有効にして、このリポジトリをGitHubへpushすると `.github/workflows/pages.yml` が `site/` を公開します。ローカル確認は次です。

```bash
python3 -m http.server 8000 -d site
```

その後 `http://localhost:8000` を開きます。外部CDNやbuild toolは不要です。

## サンプルの起動

各例は `/healthz`、`GET /items/{item_id}`、`POST /items` を実装します。依存versionは調査対象に固定しています。

```bash
# Spring Boot: Java 17+ / Maven 3.6.3+
cd examples/spring-boot && mvn spring-boot:run

# FastAPI: Python 3.10+
cd examples/fastapi && python -m pip install -e '.[test]' && fastapi dev app/main.py

# Gin: Go 1.25+
cd examples/gin && go run .
```

## 検証

```bash
python3 scripts/validate.py
```

実行環境にMavenまたはGoがない場合でも、repository構造、JSON/CSV、Markdown link、Issue metadata、Python構文、site assetを検証します。実際に行っていないcompileやload testは `RESEARCH_STATUS.md` に明記しています。

## 引用方針

事実は公式documentation、release note、tag固定のsource code、対象repositoryのADRを優先しました。影響関係は `official`、`direct-dependency`、`inferred` に分け、推測を事実として扱いません。詳細は [Research Method](RESEARCH_METHOD.md) と [Sources](docs/15-sources.md) を参照してください。

## License

独自の文章・データ・サンプルコードはMIT Licenseです。リンク先および引用元の著作権・licenseは各projectに帰属します。
