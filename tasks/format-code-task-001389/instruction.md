# Configurable gRPC message size limits

The gRPC client module (`k6/net/grpc`) currently relies on the gRPC library's
built-in defaults for the maximum size of messages it will send and receive on a
connection. Some users load-test services that exchange large messages and need
to raise that ceiling; others want to cap it deliberately. Today there's no way
to control either limit from a script.

Add two optional parameters to the client's `connect(address, params)` call:

- `maxReceiveSize` — the largest message, in bytes, the client will accept in a
  response on this connection.
- `maxSendSize` — the largest message, in bytes, the client will send in a
  request on this connection.

Behavior:

- Both are optional. When a parameter is omitted (or left at its default), the
  connection keeps the current behavior and uses the gRPC library defaults — a
  script that never sets them must work exactly as before.
- Each value must be an integer. A non-integer value (e.g. a string or boolean)
  must make `connect` fail with an error reading
  `invalid maxReceiveSize value: '<value>', it needs to be an integer`
  (and the analogous message for `maxSendSize`).
- A negative integer must make `connect` fail with an error reading
  `invalid maxReceiveSize value: '<value>', it needs to be a positive integer`
  (and the analogous message for `maxSendSize`).
- When `maxReceiveSize` is set to a positive value and the server returns a
  message larger than it, the RPC fails: the response's status is the
  resource-exhausted status code.
- When `maxSendSize` is set to a positive value and the script tries to send a
  request larger than it, the RPC fails the same way.

The existing connect parameters and their validation (`plaintext`, `timeout`,
`reflect`, and the rejection of unknown parameters) must keep working unchanged.
