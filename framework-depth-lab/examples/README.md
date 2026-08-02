# Comparable API examples

3例は `contracts/openapi.yaml` の同じ3 endpoint、成功shape、404/422 problem shapeを実装します。architectureの良し悪しではなく、routing、validation、DI/wiring、testの表現差を見る最小教材です。永続化・認証・telemetryは意図的に含めません。

| Endpoint | Behavior |
|---|---|
| `GET /healthz` | `{"status":"ok"}` |
| `GET /items/{item_id}` | memory storeから取得、なければ404 |
| `POST /items` | name/priceを検証し201 |

memory storeはprocess localでproduction用ではありません。benchmarkで複数workerを使うとstoreが共有されないため、POSTとGETの整合を測るscenarioでは外部storeへ置換してください。
