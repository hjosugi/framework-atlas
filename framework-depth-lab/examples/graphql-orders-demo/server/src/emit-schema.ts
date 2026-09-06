/* Print the code-first schema to ../../schema.graphql (SDL).
 * The client codegen reads that file. Run this after schema changes:
 *   npm run schema   (from the repo root)
 */

import { writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { lexicographicSortSchema, printSchema } from 'graphql';
import { schema } from './schema.js';

const out = join(dirname(fileURLToPath(import.meta.url)), '..', '..', 'schema.graphql');
writeFileSync(out, printSchema(lexicographicSortSchema(schema)), 'utf-8');
console.log(`schema written to ${out}`);
