/* CLI demo. Start the server first:
 *   npm run dev            (in another terminal, repo root)
 * then:
 *   npm run demo
 *
 * Run the server with NAIVE=1 and run the demo again.
 * Compare the db call counts in the server terminal.
 */

import { execute } from './execute.js';
import {
  CreateOrderMutation,
  DashboardQuery,
  UserCardQuery,
  UserWithOrdersQuery,
} from './queries.js';

function section(title: string): void {
  console.log(`\n=== ${title} ${'='.repeat(Math.max(4, 56 - title.length))}`);
}

async function timed<T>(work: () => Promise<T>): Promise<[T, number]> {
  const start = performance.now();
  const result = await work();
  return [result, Math.round(performance.now() - start)];
}

async function main(): Promise<void> {
  section('Lesson 1: over-fetching solved');
  const [card, cardMs] = await timed(() => execute(UserCardQuery, { id: 'u1' }));
  // card.user is fully typed: { name: string; avatarUrl: string } | null
  console.log(`asked for 2 fields, got exactly 2 fields (${cardMs} ms)`);
  console.log(JSON.stringify(card, null, 2));

  section('Lesson 2: under-fetching solved (1 round trip)');
  const [nested, nestedMs] = await timed(() =>
    execute(UserWithOrdersQuery, { id: 'u1', status: null }),
  );
  const user = nested.user;
  if (user) {
    console.log(`user -> orders -> product in ONE request (${nestedMs} ms)`);
    for (const order of user.orders) {
      console.log(
        `  ${order.id}  ${order.product.name} x${order.quantity}  ` +
          `${order.totalJpy} JPY  [${order.status}]`,
      );
    }
  }

  section('Lesson 3: the N+1 query (watch the SERVER terminal)');
  const [dashboard, dashMs] = await timed(() => execute(DashboardQuery, { first: 5 }));
  const orderCount = dashboard.users.reduce((sum, u) => sum + u.orders.length, 0);
  console.log(`5 users, ${orderCount} orders, ${dashMs} ms on the client side`);
  console.log('server log, DataLoader mode : ~3 db calls (users + batched orders + batched products)');
  console.log('server log, NAIVE=1 mode    : 1 + 5 + one per order -> the N+1 problem');

  section('Lesson 4: typed mutation');
  const [created] = await timed(() =>
    execute(CreateOrderMutation, {
      input: { userId: 'u6', productId: 'p2', quantity: 1 },
    }),
  );
  const order = created.createOrder;
  console.log(
    `created ${order.id}: ${order.product.name} x${order.quantity} = ` +
      `${order.totalJpy} JPY [${order.status}]`,
  );

  const after = await execute(UserWithOrdersQuery, { id: 'u6', status: null });
  console.log(`u6 now has ${after.user?.orders.length ?? 0} orders`);
}

main().catch((error) => {
  console.error(`\ndemo failed: ${error instanceof Error ? error.message : error}`);
  console.error('Is the server running? Start it with: npm run dev');
  process.exit(1);
});
