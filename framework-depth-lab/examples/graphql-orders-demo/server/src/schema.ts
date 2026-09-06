/* Code-first schema with Pothos.
 *
 * The TypeScript models in db.ts are the source of truth.
 * Pothos checks every resolver against them at compile time:
 * expose a field that does not exist on the model -> compile error.
 *
 * emit-schema.ts prints this schema to ../schema.graphql.
 * The client runs GraphQL Code Generator against that file.
 * So server types and client types can never drift apart.
 */

import SchemaBuilder from '@pothos/core';
import type { AppContext } from './context.js';
import { db, type OrderModel, type ProductModel, type UserModel } from './db.js';

const builder = new SchemaBuilder<{
  Context: AppContext;
  DefaultFieldNullability: false;
  Objects: {
    User: UserModel;
    Order: OrderModel;
    Product: ProductModel;
  };
}>({
  // Non-null by default. Nullable is the exception and must be explicit.
  // This matches how you want a contract to read: String! unless stated.
  defaultFieldNullability: false,
});

const OrderStatus = builder.enumType('OrderStatus', {
  values: ['PENDING', 'SHIPPED', 'DELIVERED', 'CANCELLED'] as const,
});

builder.objectType('Product', {
  fields: (t) => ({
    id: t.exposeID('id'),
    name: t.exposeString('name'),
    priceJpy: t.exposeInt('priceJpy'),
  }),
});

builder.objectType('Order', {
  fields: (t) => ({
    id: t.exposeID('id'),
    quantity: t.exposeInt('quantity'),
    status: t.field({ type: OrderStatus, resolve: (order) => order.status }),
    orderedAt: t.exposeString('orderedAt'),

    // Order -> Product is the second N+1 spot (after User -> orders).
    product: t.field({
      type: 'Product',
      resolve: async (order, _args, ctx) => {
        const product = ctx.naive
          ? await db.getProductById(order.productId)
          : await ctx.loaders.productById.load(order.productId);
        if (!product) throw new Error(`Product ${order.productId} not found`);
        return product;
      },
    }),

    // A computed field. It does not exist in the JSON at all.
    totalJpy: t.int({
      resolve: async (order, _args, ctx) => {
        const product = ctx.naive
          ? await db.getProductById(order.productId)
          : await ctx.loaders.productById.load(order.productId);
        if (!product) throw new Error(`Product ${order.productId} not found`);
        return product.priceJpy * order.quantity;
      },
    }),
  }),
});

builder.objectType('User', {
  fields: (t) => ({
    id: t.exposeID('id'),
    name: t.exposeString('name'),
    email: t.exposeString('email'),
    avatarUrl: t.exposeString('avatarUrl'),
    createdAt: t.exposeString('createdAt'),

    // Field-level evolution instead of /v2 endpoints.
    gender: t.exposeString('gender', {
      nullable: true,
      deprecationReason: 'Use pronouns instead.',
    }),
    pronouns: t.exposeString('pronouns', { nullable: true }),

    orders: t.field({
      type: ['Order'],
      args: {
        status: t.arg({ type: OrderStatus, required: false }),
      },
      resolve: async (user, args, ctx) => {
        const orders = ctx.naive
          ? await db.getOrdersByUserId(user.id)
          : await ctx.loaders.ordersByUser.load(user.id);
        return args.status ? orders.filter((o) => o.status === args.status) : orders;
      },
    }),
  }),
});

builder.queryType({
  fields: (t) => ({
    user: t.field({
      type: 'User',
      nullable: true,
      args: { id: t.arg.id({ required: true }) },
      resolve: (_root, args) => db.getUser(String(args.id)),
    }),
    users: t.field({
      type: ['User'],
      args: { first: t.arg.int({ defaultValue: 5 }) },
      resolve: (_root, args) => db.getUsers(args.first ?? 5),
    }),
  }),
});

const CreateOrderInput = builder.inputType('CreateOrderInput', {
  fields: (t) => ({
    userId: t.id({ required: true }),
    productId: t.id({ required: true }),
    quantity: t.int({ required: true }),
  }),
});

builder.mutationType({
  fields: (t) => ({
    createOrder: t.field({
      type: 'Order',
      args: { input: t.arg({ type: CreateOrderInput, required: true }) },
      resolve: async (_root, args) => {
        const { userId, productId, quantity } = args.input;
        if (quantity < 1) throw new Error('quantity must be at least 1');
        const user = await db.getUser(String(userId));
        if (!user) throw new Error(`User ${userId} not found`);
        const product = await db.getProductById(String(productId));
        if (!product) throw new Error(`Product ${productId} not found`);
        return db.insertOrder({ userId: String(userId), productId: String(productId), quantity });
      },
    }),
  }),
});

export const schema = builder.toSchema();
