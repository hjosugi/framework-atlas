/* eslint-disable */
/** Internal type. DO NOT USE DIRECTLY. */
type Exact<T extends { [key: string]: unknown }> = { [K in keyof T]: T[K] };
/** Internal type. DO NOT USE DIRECTLY. */
export type Incremental<T> = T | { [P in keyof T]?: P extends ' $fragmentName' | '__typename' ? T[P] : never };
import { DocumentTypeDecoration } from '@graphql-typed-document-node/core';
export type CreateOrderInput = {
  productId: string | number;
  quantity: number;
  userId: string | number;
};

export type OrderStatus =
  | 'CANCELLED'
  | 'DELIVERED'
  | 'PENDING'
  | 'SHIPPED';

export type UserCardQueryVariables = Exact<{
  id: string | number;
}>;


export type UserCardQuery = { user: { name: string, avatarUrl: string } | null };

export type UserWithOrdersQueryVariables = Exact<{
  id: string | number;
  status?: OrderStatus | null | undefined;
}>;


export type UserWithOrdersQuery = { user: { name: string, pronouns: string | null, orders: Array<{ id: string, quantity: number, status: OrderStatus, totalJpy: number, product: { name: string, priceJpy: number } }> } | null };

export type DashboardQueryVariables = Exact<{
  first?: number | null | undefined;
}>;


export type DashboardQuery = { users: Array<{ name: string, orders: Array<{ totalJpy: number, product: { name: string } }> }> };

export type CreateOrderMutationVariables = Exact<{
  input: CreateOrderInput;
}>;


export type CreateOrderMutation = { createOrder: { id: string, status: OrderStatus, quantity: number, totalJpy: number, product: { name: string } } };

export class TypedDocumentString<TResult, TVariables>
  extends String
  implements DocumentTypeDecoration<TResult, TVariables>
{
  __apiType?: NonNullable<DocumentTypeDecoration<TResult, TVariables>['__apiType']>;
  private value: string;
  public __meta__?: Record<string, any> | undefined;

  constructor(value: string, __meta__?: Record<string, any> | undefined) {
    super(value);
    this.value = value;
    this.__meta__ = __meta__;
  }

  override toString(): string & DocumentTypeDecoration<TResult, TVariables> {
    return this.value;
  }
}

export const UserCardDocument = new TypedDocumentString(`
    query UserCard($id: ID!) {
  user(id: $id) {
    name
    avatarUrl
  }
}
    `) as unknown as TypedDocumentString<UserCardQuery, UserCardQueryVariables>;
export const UserWithOrdersDocument = new TypedDocumentString(`
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
    `) as unknown as TypedDocumentString<UserWithOrdersQuery, UserWithOrdersQueryVariables>;
export const DashboardDocument = new TypedDocumentString(`
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
    `) as unknown as TypedDocumentString<DashboardQuery, DashboardQueryVariables>;
export const CreateOrderDocument = new TypedDocumentString(`
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
    `) as unknown as TypedDocumentString<CreateOrderMutation, CreateOrderMutationVariables>;