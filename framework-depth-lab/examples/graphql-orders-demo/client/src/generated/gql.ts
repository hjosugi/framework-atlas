/* eslint-disable */
import * as types from './graphql';



/**
 * Map of all GraphQL operations in the project.
 *
 * This map has several performance disadvantages:
 * 1. It is not tree-shakeable, so it will include all operations in the project.
 * 2. It is not minifiable, so the string of a GraphQL query will be multiple times inside the bundle.
 * 3. It does not support dead code elimination, so it will add unused operations.
 *
 * Therefore it is highly recommended to use the babel or swc plugin for production.
 * Learn more about it here: https://the-guild.dev/graphql/codegen/plugins/presets/preset-client#reducing-bundle-size
 */
type Documents = {
    "\n  query UserCard($id: ID!) {\n    user(id: $id) {\n      name\n      avatarUrl\n    }\n  }\n": typeof types.UserCardDocument,
    "\n  query UserWithOrders($id: ID!, $status: OrderStatus) {\n    user(id: $id) {\n      name\n      pronouns\n      orders(status: $status) {\n        id\n        quantity\n        status\n        totalJpy\n        product {\n          name\n          priceJpy\n        }\n      }\n    }\n  }\n": typeof types.UserWithOrdersDocument,
    "\n  query Dashboard($first: Int) {\n    users(first: $first) {\n      name\n      orders {\n        totalJpy\n        product {\n          name\n        }\n      }\n    }\n  }\n": typeof types.DashboardDocument,
    "\n  mutation CreateOrder($input: CreateOrderInput!) {\n    createOrder(input: $input) {\n      id\n      status\n      quantity\n      totalJpy\n      product {\n        name\n      }\n    }\n  }\n": typeof types.CreateOrderDocument,
};
const documents: Documents = {
    "\n  query UserCard($id: ID!) {\n    user(id: $id) {\n      name\n      avatarUrl\n    }\n  }\n": types.UserCardDocument,
    "\n  query UserWithOrders($id: ID!, $status: OrderStatus) {\n    user(id: $id) {\n      name\n      pronouns\n      orders(status: $status) {\n        id\n        quantity\n        status\n        totalJpy\n        product {\n          name\n          priceJpy\n        }\n      }\n    }\n  }\n": types.UserWithOrdersDocument,
    "\n  query Dashboard($first: Int) {\n    users(first: $first) {\n      name\n      orders {\n        totalJpy\n        product {\n          name\n        }\n      }\n    }\n  }\n": types.DashboardDocument,
    "\n  mutation CreateOrder($input: CreateOrderInput!) {\n    createOrder(input: $input) {\n      id\n      status\n      quantity\n      totalJpy\n      product {\n        name\n      }\n    }\n  }\n": types.CreateOrderDocument,
};

/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  query UserCard($id: ID!) {\n    user(id: $id) {\n      name\n      avatarUrl\n    }\n  }\n"): typeof import('./graphql').UserCardDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  query UserWithOrders($id: ID!, $status: OrderStatus) {\n    user(id: $id) {\n      name\n      pronouns\n      orders(status: $status) {\n        id\n        quantity\n        status\n        totalJpy\n        product {\n          name\n          priceJpy\n        }\n      }\n    }\n  }\n"): typeof import('./graphql').UserWithOrdersDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  query Dashboard($first: Int) {\n    users(first: $first) {\n      name\n      orders {\n        totalJpy\n        product {\n          name\n        }\n      }\n    }\n  }\n"): typeof import('./graphql').DashboardDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "\n  mutation CreateOrder($input: CreateOrderInput!) {\n    createOrder(input: $input) {\n      id\n      status\n      quantity\n      totalJpy\n      product {\n        name\n      }\n    }\n  }\n"): typeof import('./graphql').CreateOrderDocument;


export function graphql(source: string) {
  return (documents as any)[source] ?? {};
}
