/* GraphQL documents.
 *
 * graphql() comes from the generated code. It looks up each document
 * by its text and returns a TypedDocumentString with exact result and
 * variable types. Add a field that is not in the schema and
 * `npm run codegen` fails. Typo a field name after codegen and
 * `npm run typecheck` fails.
 */

import { graphql } from './generated/index.js';

// Lesson 1: the client decides the shape. Two fields, nothing else.
export const UserCardQuery = graphql(`
  query UserCard($id: ID!) {
    user(id: $id) {
      name
      avatarUrl
    }
  }
`);

// Lesson 2: one round trip for user -> orders -> product.
// With REST this is 1 + N + M sequential requests.
export const UserWithOrdersQuery = graphql(`
  query UserWithOrders($id: ID!, $status: OrderStatus) {
    user(id: $id) {
      name
      pronouns
      orders(status: $status) {
        id
        quantity
        status
        totalJpy
        product {
          name
          priceJpy
        }
      }
    }
  }
`);

// Lesson 3: the dashboard query that triggers N+1 on a naive server.
export const DashboardQuery = graphql(`
  query Dashboard($first: Int) {
    users(first: $first) {
      name
      orders {
        totalJpy
        product {
          name
        }
      }
    }
  }
`);

// Lesson 4: a typed mutation with an input type.
export const CreateOrderMutation = graphql(`
  mutation CreateOrder($input: CreateOrderInput!) {
    createOrder(input: $input) {
      id
      status
      quantity
      totalJpy
      product {
        name
      }
    }
  }
`);
