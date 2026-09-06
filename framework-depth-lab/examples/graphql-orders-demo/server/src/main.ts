/* HTTP server. GraphQL Yoga on plain node:http.
 *
 * Run:
 *   npm run dev          # DataLoader mode
 *   NAIVE=1 npm run dev  # no batching, watch the N+1 in the logs
 *
 * GraphiQL (interactive playground) at http://localhost:4000/graphql
 */

import { createServer } from 'node:http';
import { createYoga } from 'graphql-yoga';
import { createContext } from './context.js';
import { schema } from './schema.js';

const PORT = Number(process.env.PORT ?? 4000);

const yoga = createYoga({
  schema,
  // The context factory runs once per request. Fresh loaders every time.
  context: () => createContext(),
});

const server = createServer(yoga);

server.listen(PORT, () => {
  const mode = process.env.NAIVE === '1' ? 'NAIVE (N+1 visible)' : 'DataLoader (batched)';
  console.log(`GraphQL server on http://localhost:${PORT}/graphql`);
  console.log(`mode: ${mode}`);
  console.log('Open the URL in a browser for GraphiQL.');
});
