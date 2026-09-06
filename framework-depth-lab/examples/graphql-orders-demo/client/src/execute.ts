/* Minimal typed executor. Plain fetch, no client library.
 *
 * The generated TypedDocumentString carries two type parameters:
 * the result type and the variables type. So `execute` returns
 * fully typed data, and wrong variables fail at compile time.
 */

import type { TypedDocumentString } from './generated/graphql.js';

const ENDPOINT = process.env.GRAPHQL_URL ?? 'http://localhost:4000/graphql';

export async function execute<TResult, TVariables>(
  query: TypedDocumentString<TResult, TVariables>,
  ...[variables]: TVariables extends Record<string, never> ? [] : [TVariables]
): Promise<TResult> {
  const response = await fetch(ENDPOINT, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Accept: 'application/graphql-response+json, application/json',
    },
    body: JSON.stringify({ query: query.toString(), variables }),
  });

  if (!response.ok) {
    throw new Error(`HTTP ${response.status} from ${ENDPOINT}`);
  }

  const payload = (await response.json()) as {
    data?: TResult;
    errors?: { message: string }[];
  };

  // GraphQL reports errors in the body, usually with HTTP 200.
  if (payload.errors?.length) {
    throw new Error(payload.errors.map((e) => e.message).join('; '));
  }
  if (payload.data === undefined) {
    throw new Error('response has no data field');
  }
  return payload.data;
}
