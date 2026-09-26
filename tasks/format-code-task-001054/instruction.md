## Complete the v2 KeysAPI mutation surface

The current `client.KeysAPI` only exposes create, get, and watch operations, which means callers have to leave the typed client API for ordinary v2 key mutations. Extend this public API, and the implementation returned by `NewKeysAPI`, with these methods:

```go
Set(ctx context.Context, key, value string, ttl time.Duration) (*Response, error)
Update(ctx context.Context, key, value string, ttl time.Duration) (*Response, error)
Delete(ctx context.Context, key string, recursive bool) (*Response, error)
CompareAndSwap(ctx context.Context, key, value string, ttl time.Duration, prevValue string, prevIndex uint64) (*Response, error)
CompareAndDelete(ctx context.Context, key, prevValue string, prevIndex uint64) (*Response, error)
```

All five methods must use the same endpoint path composition as the existing v2 key operations, preserving an endpoint's base path and routing under the API's configured keys prefix. Encode mutation values as `application/x-www-form-urlencoded`. Request controls (`prevExist`, `recursive`, `prevValue`, and `prevIndex`) are URL query parameters. TTL follows the existing `Create` convention: a negative duration omits `ttl`; zero and positive durations include it as the whole number of seconds, truncating any fractional second.

`Set` is an unconditional `PUT` whose form contains `value`. `Update` is a `PUT` with `prevExist=true` and the same value/TTL form. `Delete` is a bodyless `DELETE` and must send the requested `recursive` value for both true and false.

The compare methods are conditional mutations. `CompareAndSwap` uses `PUT` with the new value/TTL form, while `CompareAndDelete` uses a bodyless `DELETE`. A non-empty `prevValue` supplies the `prevValue` condition, a nonzero `prevIndex` supplies the decimal `prevIndex` condition, and when both are supplied both must be sent so the server enforces both. If neither condition is supplied, return an error before issuing any HTTP request. Values and conditions must be encoded normally so spaces and reserved form characters round-trip correctly.

On success, every new operation must decode and return the v2 response body and `X-Etcd-Index` header exactly like the existing `Create` and `Get` methods. Transport errors must pass through unchanged, and non-success HTTP statuses must use the client's existing status-to-error mapping for every new operation.
