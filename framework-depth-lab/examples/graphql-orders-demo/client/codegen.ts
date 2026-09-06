/* GraphQL Code Generator config (client preset).
 *
 * Input : ../schema.graphql (emitted by the server, code-first)
 * Input : every graphql(`...`) document under src/
 * Output: src/generated/ with exact TypeScript types per document.
 *
 * documentMode "string" makes documents plain strings, so the client
 * needs no GraphQL runtime. fetch is enough.
 */

import type { CodegenConfig } from '@graphql-codegen/cli';

const config: CodegenConfig = {
  schema: '../schema.graphql',
  documents: ['src/**/*.ts'],
  ignoreNoDocuments: true,
  generates: {
    './src/generated/': {
      preset: 'client',
      config: {
        documentMode: 'string',
      },
    },
  },
};

export default config;
