# Flesh out order management on the Trading API client

Right now `TradingClient` can only submit a new order (`submit_order`). That's not
enough to actually manage orders against the Alpaca trading API — there's no way to
list existing orders, look one up, change one, or cancel them. Please round out the
client so it covers the rest of the `/v2/orders` routes.

Add the following methods to `TradingClient`:

- **`get_orders(filter=None)`** — returns a `list` of `Order` objects by issuing a
  `GET` to `/v2/orders`. The optional `filter` is a `GetOrdersRequest` describing the
  standard query parameters: order `status`, `limit`, `after`/`until` timestamps, sort
  `direction`, `nested`, `side`, and a list of `symbols`. Every field is optional and
  only the ones that are set should be sent. When the filter supplies a list of
  symbols, they must be transmitted as a single comma-separated `symbols` query
  parameter (e.g. `symbols=SPY,AAPL`), not as repeated parameters. Calling it with no
  filter must still work and simply send no query parameters.

- **`get_order_by_id(order_id, filter=None)`** — returns the `Order` retrieved from
  `GET /v2/orders/{order_id}`. The optional `filter` is a `GetOrderByIdRequest`
  carrying the `nested` flag.

- **`replace_order(order_id, order_data=None)`** — updates an existing order via
  `PATCH /v2/orders/{order_id}` and returns the resulting `Order`. The optional
  `order_data` is a `ReplaceOrderRequest` describing the fields that may be changed
  (`qty`, `time_in_force`, `limit_price`, `stop_price`, `trail`, `client_order_id`);
  again, only fields that are set should be sent.

- **`cancel_orders()`** — issues a `DELETE` to `/v2/orders` and returns a `list`
  describing the cancellation outcome of each order. The API responds with an array of
  objects each carrying the order `id` and an integer HTTP `status`; surface each as a
  `CancelOrderResponse` exposing `id` (a `UUID`) and `status` (an `int`).

Wherever a method takes an order id, accept either a `UUID` instance or a UUID-formatted
string. If the value is neither (for example an arbitrary non-UUID string), raise a
`ValueError` before any request is made.

The new request objects (`GetOrdersRequest`, `GetOrderByIdRequest`,
`ReplaceOrderRequest`) and the `CancelOrderResponse` model should be importable from the
same place as the existing order request models (e.g. `MarketOrderRequest`), and the
request objects should follow the existing convention of omitting unset fields when
serialized.

One more thing: an `Order`'s `client_order_id` is a user-supplied identifier that is not
necessarily a UUID, so make sure an `Order` whose `client_order_id` is an arbitrary
string parses correctly.
