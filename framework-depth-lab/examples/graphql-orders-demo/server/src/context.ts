/* Per-request context.
 *
 * DataLoader batches all .load(key) calls that happen in the same
 * event loop tick into ONE batch function call. So 5 resolvers asking
 * for orders of 5 different users become 1 db call.
 *
 * Loaders MUST be created per request. A shared loader would leak its
 * cache across requests and serve stale data to other users.
 */

import DataLoader from 'dataloader';
import { db, type OrderModel, type ProductModel } from './db.js';

export interface AppContext {
  naive: boolean; // NAIVE=1 turns DataLoader off to show the N+1 problem
  loaders: {
    ordersByUser: DataLoader<string, OrderModel[]>;
    productById: DataLoader<string, ProductModel | null>;
  };
}

export function createContext(): AppContext {
  const naive = process.env.NAIVE === '1';
  console.log(`\n[request] new GraphQL request (mode: ${naive ? 'NAIVE, no batching' : 'DataLoader'})`);
  return {
    naive,
    loaders: {
      ordersByUser: new DataLoader((userIds) => db.getOrdersByUserIds(userIds)),
      productById: new DataLoader((productIds) => db.getProductsByIds(productIds)),
    },
  };
}
