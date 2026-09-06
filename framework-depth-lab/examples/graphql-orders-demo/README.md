# graphql-orders-demo

A small but modern GraphQL setup. Code-first server, fully typed client,
JSON test data. It shows the classic GraphQL talking points as running
code: over-fetching, under-fetching, the type contract, deprecation,
and the N+1 problem with DataLoader.

## Stack (verified on npm, September 2026)

| Part            | Library                              | Why |
| --------------- | ------------------------------------ | --- |
| Schema          | Pothos v4 (code-first)               | TypeScript models are the source of truth. Wrong resolver = compile error. |
| HTTP server     | GraphQL Yoga v5                      | Small, spec-compliant, ships GraphiQL. |
| Batching        | dataloader v2                        | Fixes N+1. Per-request instances. |
| Client types    | GraphQL Code Generator v7 + client preset v6 | Exact types per document. `documentMode: "string"` = zero runtime deps. |
| Client runtime  | plain `fetch`                        | Shows exactly what goes over the wire. Swap for urql/Apollo later. |
| Monorepo        | npm workspaces                       | One install, shared lockfile, single graphql instance. |

The lockfile resolves one shared `graphql@16.14.2` for the server and client.
The package manifests allow compatible v16 updates with `^16.14.2`;
use `npm ci` to install the exact checked-in versions.
Two copies of graphql-js in one process can break type identity checks.
Check the resolved dependency tree with `npm ls graphql`.

## Architecture

```
server/ (code-first)                      client/ (typed)

src/db.ts        JSON files -> models     src/queries.ts   graphql(`...`) documents
     |           25ms fake latency             |
     v           logs every call               v
src/schema.ts    Pothos builder           npm run codegen
     |           checks resolvers              |  reads schema.graphql
     |           against the models            v
     v                                    src/generated/   exact result +
src/main.ts      Yoga on node:http            |            variable types
     |                                        v
     |  npm run schema                    src/execute.ts   typed fetch wrapper
     v                                        |
schema.graphql  <-------- the contract -------+
(generated SDL, committed)
```

The flow to remember: models -> Pothos -> SDL -> codegen -> client types.
One chain. Server and client cannot drift.

## Run it

Use Node.js 24 LTS and npm. Run these commands from this example directory.

```bash
npm ci

# Terminal 1: the server (GraphiQL at http://localhost:4000/graphql)
npm run dev

# Terminal 2: the typed client demo
npm run demo
```

After schema changes:

```bash
npm run codegen    # emit schema.graphql, regenerate client types
npm run typecheck  # both workspaces
```

## The four lessons in the demo

1. Over-fetching solved: `UserCard` asks for 2 fields, gets 2 fields.
2. Under-fetching solved: `user -> orders -> product` in one round trip.
3. N+1 and DataLoader: see below.
4. Typed mutation: `createOrder` with an input type.

Bonus in the schema: `gender` carries `@deprecated(reason: "Use
pronouns instead.")` — field-level evolution instead of `/v2` endpoints.

## The N+1 experiment (measured)

The same dashboard query, two server modes:

```
query { users(first: 5) { name orders { totalJpy product { name } } } }
```

```bash
npm run dev            # DataLoader mode
NAIVE=1 npm run dev    # batching off
```

Measured result with the bundled test data (11 orders):

| Mode       | db calls | What happens |
| ---------- | -------- | ------------ |
| DataLoader | 3        | users + orders IN (u1..u5) + products IN (p1..p5) |
| NAIVE=1    | 28       | 1 users + 5 orders + 22 product lookups |

Why 22 and not 11: `product` and `totalJpy` each resolve the product
separately, so every order loads its product twice. DataLoader fixes
this too — its per-request cache dedupes repeated keys, not just
batches them. The server terminal prints every simulated SQL call, so
you can watch both behaviors live.

## Where the type safety actually bites

- Add a field to a query that the schema does not have ->
  `npm run codegen` fails before anything runs.
- Typo a result field in `client/src/main.ts` -> `npm run typecheck` fails.
- Expose a field in Pothos that the TS model does not have ->
  the server does not compile.

Try each once. That is the "schema as contract" argument, executable.

## Test data

`server/data/*.json` — 6 users, 5 products, 12 orders with mixed
statuses. The fake db (`server/src/db.ts`) loads them into memory,
adds 25 ms latency per call, and logs each call. Mutations write to
memory only; restart resets the data.

## Things to try next

- Depth/cost limits: add `@escape.tech/graphql-armor` to block
  `friends { friends { friends ... } }` style queries.
- Persisted queries: Yoga has a plugin; pairs with CDN caching.
- Pagination: switch `users(first:)` to Relay connections
  (`@pothos/plugin-relay`).
- Swap the client runtime: keep the generated types, replace the
  fetch wrapper with urql or Apollo Client.
- Point `GRAPHQL_URL` at another endpoint to reuse the client shell.

## Official references

- [Pothos documentation](https://pothos-graphql.dev/)
- [GraphQL Yoga quick start](https://the-guild.dev/graphql/yoga-server/docs)
- [DataLoader](https://github.com/graphql/dataloader)
- [GraphQL Code Generator client preset](https://the-guild.dev/graphql/codegen/plugins/presets/preset-client)
