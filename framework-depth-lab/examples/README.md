# Local implementation examples

## RAG and GraphQL

| Example | What to try |
|---|---|
| [rag-local-demo](rag-local-demo/README.md) | Embed Japanese documents locally, compare retrieval scores, filter old policies, inspect the prompt and PCA map. |
| [graphql-orders-demo](graphql-orders-demo/README.md) | Run a typed orders API and client, then compare DataLoader batching with the naive N+1 path. |

Each example includes its own setup instructions and sample data. They run independently of the catalog site and the comparable REST APIs below.

## Comparable REST APIs

3例は `contracts/openapi.yaml` の同じ3 endpoint、成功shape、404/422 problem shapeを実装します。architectureの良し悪しではなく、routing、validation、DI/wiring、testの表現差を見る最小教材です。永続化・認証・telemetryは意図的に含めません。

| Endpoint | Behavior |
|---|---|
| `GET /healthz` | `{"status":"ok"}` |
| `GET /items/{item_id}` | memory storeから取得、なければ404 |
| `POST /items` | name/priceを検証し201 |

memory storeはprocess localでproduction用ではありません。benchmarkで複数workerを使うとstoreが共有されないため、POSTとGETの整合を測るscenarioでは外部storeへ置換してください。
