## Querying multiple product variants by ID in one request

I'm building a checkout/cart page on top of Saleor's GraphQL API. On the client side I keep a list of `ProductVariant` IDs (the line items the customer has added), and when the page loads I want to fetch the details (stock, price, related product info, etc.) for all of them at once so I can render the cart.

Looking at the schema, the only way I can find to fetch a variant is:

```graphql
query {
  productVariant(id: "...") {
    id
    name
    stockQuantity
    price { amount }
  }
}
```

This only accepts a single ID. So if my cart has 5 variants, my options are basically:

1. Fire 5 separate requests, one per variant — wasteful and slow.
2. Build one big query with 5 aliased copies of `productVariant`, which works but is awkward to assemble dynamically on the client and gets ugly as the cart grows.

Other list-style queries in the schema (like `products`, `categories`, etc.) are nice to work with because they return a proper paginated collection. It would be great to have something equivalent for variants — a query that accepts a list of variant IDs and returns the matching `ProductVariant` objects in one round trip, in the same connection-style shape as the other list queries.

Is there a way to do this today that I'm missing? If not, could batched lookup of variants by ID be exposed at the top level of `Query`? Something like `productVariants(ids: [...])` would feel natural alongside the existing `productVariant(id: ...)`.
