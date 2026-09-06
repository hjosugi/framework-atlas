/* Fake database over the JSON files in ../data.
 *
 * Two tricks make it useful for learning:
 * 1. Every call waits LATENCY_MS. Slow calls make N+1 hurt for real.
 * 2. Every call is logged with a running number.
 *    Watch the server terminal to SEE how many "queries" one
 *    GraphQL request produces.
 */

import { readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

export interface UserModel {
  id: string;
  name: string;
  email: string;
  gender: string | null;
  pronouns: string | null;
  avatarUrl: string;
  createdAt: string;
}

export interface ProductModel {
  id: string;
  name: string;
  priceJpy: number;
}

export interface OrderModel {
  id: string;
  userId: string;
  productId: string;
  quantity: number;
  status: 'PENDING' | 'SHIPPED' | 'DELIVERED' | 'CANCELLED';
  orderedAt: string;
}

const DATA_DIR = join(dirname(fileURLToPath(import.meta.url)), '..', 'data');
const LATENCY_MS = 25;

function load<T>(name: string): T[] {
  return JSON.parse(readFileSync(join(DATA_DIR, name), 'utf-8')) as T[];
}

// In-memory tables. Mutations change these arrays, not the JSON files.
const users = load<UserModel>('users.json');
const products = load<ProductModel>('products.json');
const orders = load<OrderModel>('orders.json');

let callCount = 0;

async function simulate(sql: string): Promise<void> {
  callCount += 1;
  console.log(`  [db call ${String(callCount).padStart(2)}] ${sql}`);
  await new Promise((resolve) => setTimeout(resolve, LATENCY_MS));
}

export function resetCallCount(): number {
  const before = callCount;
  callCount = 0;
  return before;
}

export const db = {
  async getUsers(first: number): Promise<UserModel[]> {
    await simulate(`SELECT * FROM users LIMIT ${first}`);
    return users.slice(0, first);
  },

  async getUser(id: string): Promise<UserModel | null> {
    await simulate(`SELECT * FROM users WHERE id = '${id}'`);
    return users.find((u) => u.id === id) ?? null;
  },

  /** One call per user. This is the naive path that causes N+1. */
  async getOrdersByUserId(userId: string): Promise<OrderModel[]> {
    await simulate(`SELECT * FROM orders WHERE user_id = '${userId}'`);
    return orders.filter((o) => o.userId === userId);
  },

  /** One call for MANY users. This is what DataLoader batches into. */
  async getOrdersByUserIds(userIds: readonly string[]): Promise<OrderModel[][]> {
    await simulate(`SELECT * FROM orders WHERE user_id IN (${userIds.join(', ')})  -- batched`);
    return userIds.map((id) => orders.filter((o) => o.userId === id));
  },

  /** One call per product. Naive path. */
  async getProductById(id: string): Promise<ProductModel | null> {
    await simulate(`SELECT * FROM products WHERE id = '${id}'`);
    return products.find((p) => p.id === id) ?? null;
  },

  /** One call for MANY products. DataLoader path. */
  async getProductsByIds(ids: readonly string[]): Promise<(ProductModel | null)[]> {
    await simulate(`SELECT * FROM products WHERE id IN (${ids.join(', ')})  -- batched`);
    return ids.map((id) => products.find((p) => p.id === id) ?? null);
  },

  async insertOrder(input: { userId: string; productId: string; quantity: number }): Promise<OrderModel> {
    await simulate(`INSERT INTO orders (user_id, product_id, quantity) VALUES (...)`);
    const order: OrderModel = {
      id: `o${orders.length + 1}`,
      userId: input.userId,
      productId: input.productId,
      quantity: input.quantity,
      status: 'PENDING',
      orderedAt: new Date().toISOString(),
    };
    orders.push(order);
    return order;
  },
};
