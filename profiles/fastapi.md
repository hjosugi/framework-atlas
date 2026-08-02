# FastAPI — 一つのtyped declarationを複数artifactへ

確認日: 2026-08-02。観測version: 0.141.1（GitHub release, 2026-07-29）。

## 核心

FastAPIはPythonの標準type annotation、Pydantic、Starletteを接続し、handler signatureからrequest parsing、validation、editor support、OpenAPI/JSON Schema、interactive documentationを派生する。dependency declarationも階層として解決され、同じschema/contractに統合される。

重要なのはsyntaxの短さではなく、情報を重複させずruntime artifactへ変換する経路である。annotationは静的hintだが、Pydantic validationはruntimeで入力をparse/検査するため、その境界を同一視しない。失敗はvalidation errorとしてHTTP境界で構造化される。一方で、Python annotationはdomain ownershipやtransaction boundaryを自動的には作らない。Pydantic request modelをORM row/domain entityへそのまま渡すと短いが、transport/data/domainの変更が結合する。route dependencyへbusiness ruleを積み過ぎると、便利な宣言面が暗黙のapplication layerになる。

dependency overrideはtest seamとして有効だが、実DB transactionやqueue semanticsを証明しない。yield dependencyとASGI lifespanはresource scopeを可視化する。response後のBackgroundTasksはprocess crashを越えるdurable queueではない。detached async taskへrequest-scoped sessionを渡さない。

## 強みと代償

| 軸 | 強み | 代償 |
|---|---|---|
| contract | type、validation、OpenAPI、docsが近い | Python runtime semanticsとschema表現の差を理解する必要 |
| async | ASGI/Starlette ecosystemを利用 | blocking libraryを混ぜるとevent loopを阻害 |
| DI | function signatureで小さく宣言 | lifecycle、cache scope、overrideの追跡が必要 |
| testing | dependency overrideとTestClient/ASGI transport | overrideだけではreal DB/queue差を証明しない |
| domain | plain Python objectへ分離しやすい | framework自体はmodule architectureを強制しない |

## kofun-bootへの抽出

route、validator、OpenAPI、typed clientを一つのADTから派生し、それぞれを別generatorの権威にしない。dependency graphはeffect capability graphとして静的に可視化し、resource scopeを型と実行時の両方で検証する。HTTP errorはclosed sum typeからadapterで変換する。FastAPIの「宣言情報を捨てず複数artifactに使う」点を採用し、Python固有のreflectionには依存しない。

## Sources

- https://fastapi.tiangolo.com/features/
- https://fastapi.tiangolo.com/tutorial/dependencies/
- https://fastapi.tiangolo.com/async/
- https://github.com/fastapi/fastapi
- https://github.com/fastapi/fastapi/releases/tag/0.141.1
