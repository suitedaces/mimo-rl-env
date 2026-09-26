Hey, I'm trying to add websocket subscription support to juno's JSON-RPC server (think `eth_subscribe`-style stuff where the server keeps pushing events to the client after the initial call returns). Two things are blocking me right now: registered RPC handlers need a supported way to push messages back to the websocket client after the initial request starts, while ordinary non-websocket requests should continue behaving like regular request/response calls. I also need shared lifecycle plumbing for active subscriptions so callers can register a subscription, get a handle for it, and tear it down later.

Expected outcomes:
- Websocket-backed JSON-RPC handlers can access a writable client connection through the request context helper and use it during handler execution to send an additional message to the same client, without preventing the normal JSON-RPC response from being returned.
- Ordinary non-websocket JSON-RPC requests report that no writable client connection is available through that helper and continue returning normal responses.
- A subscription registry API is available for creating a registry, adding an `event.Subscription`, receiving an opaque `uint64` subscription id, and deleting the subscription later by that id.
- Deleting a registered subscription unsubscribes it exactly once for that successful deletion and removes it from the registry.
- Deleting an unknown or already-deleted subscription id fails with the registry's stable public not-found error and does not panic.
- The subscription registry is safe to use from concurrent callers.

Required public API:
- `jsonrpc.ConnFromContext(ctx context.Context) (io.Writer, bool)`
- `pubsub.New(log utils.SimpleLogger) *Registry`
- `pubsub.Registry.Add(ctx context.Context, sub event.Subscription) uint64`
- `pubsub.Registry.Delete(id uint64) error`
- `pubsub.ErrNotFound`
- Keep the new plumbing at the public behavior level described above; internal storage, synchronization strategy, id generation details, websocket loop organization, and where the websocket request context is populated are up to the implementation.
