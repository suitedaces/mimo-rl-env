# Make the Redis engine's PUB/SUB subscriptions concurrency-safe

The Redis engine drives all of its channel fan-out through a single Redis PUB/SUB
connection. Under load this falls apart: many client connections call into the
engine's `subscribe` / `unsubscribe` paths from different goroutines at the same
time, and they all poke that one shared PUB/SUB connection directly. The result is
a corrupted protocol stream — most of the calls come back with errors (you'll see
things like `redigo: connection closed`) and the channels never actually end up
subscribed, so messages published to them are silently dropped.

Fix the engine so that subscribing and unsubscribing are safe to call
concurrently from any number of goroutines, while keeping the existing
single-threaded behavior intact.

Required observable behavior:

- `subscribe(chID)` and `unsubscribe(chID)` may be called concurrently from many
  goroutines, including for different channels at the same time and for the same
  channel from several goroutines. Each call must return only after its
  subscription change has been applied to Redis, returning a `nil` error on
  success.
- After a set of `subscribe` calls return successfully, every one of those
  channels must really be subscribed on the engine's PUB/SUB connection: a
  `publish` to such a channel must report that it has active subscribers.
- After a successful `unsubscribe`, the channel must no longer be subscribed: a
  `publish` to it must report no active subscribers.
- Subscribing the same channel is idempotent — a single `unsubscribe` for a
  channel returns it to the unsubscribed state regardless of how many times it was
  subscribed.
- The engine must continue to receive and dispatch messages published to
  subscribed channels exactly as before, and all of the engine's other operations
  (publish, presence, history, the API listener) keep working unchanged.

The engine is started via its `run` method before any subscribe/unsubscribe calls
are made.
