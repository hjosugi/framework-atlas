# Local implementation examples

## RAG and GraphQL: separate repositories

| Example | What to try |
|---|---|
| [rag-local](https://github.com/hjosugi/rag-local) | Embed Japanese documents locally, compare retrieval scores, filter old policies, inspect the prompt and PCA map. |
| [graphql-order](https://github.com/hjosugi/graphql-order) | Run a typed orders API and client, then compare DataLoader batching with the naive N+1 path. |

These examples are maintained in their own repositories. Each includes setup instructions and sample data.

## Comparable REST APIs

3例は `contracts/openapi.yaml` の同じ3 endpoint、成功shape、404/422 problem shapeを実装します。architectureの良し悪しではなく、routing、validation、DI/wiring、testの表現差を見る最小教材です。永続化・認証・telemetryは意図的に含めません。

| Endpoint | Behavior |
|---|---|
| `GET /healthz` | `{"status":"ok"}` |
| `GET /items/{item_id}` | memory storeから取得、なければ404 |
| `POST /items` | name/priceを検証し201 |

memory storeはprocess localでproduction用ではありません。benchmarkで複数workerを使うとstoreが共有されないため、POSTとGETの整合を測るscenarioでは外部storeへ置換してください。
