The small `lib/lru` package is now being used by callers that need to inspect and manage a cache without reaching into its implementation. Extend its public API while fixing the byte-accounting bug when an existing key is updated.

Add these methods to `*Cache`: `Bytes() int64`, `Peek(key string) (Value, bool)`, `Keys() []string`, `Remove(key string) (Value, bool)`, `Clear()`, `Resize(maxBytes int64)`, `Stats()` returning a struct value with exported `Hits` and `Misses` fields of type `uint64`, and `ResetStats()`.

The observable contract is:

- An entry consumes `len(key) + value.Len()` bytes. `Bytes` reports the sum for entries currently retained. Replacing an existing key must account for both larger and smaller values, make that key most recently used, and must not itself invoke `OnEvicted`.
- A positive byte limit is enforced after every add or replacement by evicting least-recently-used entries until the cache fits. If one entry is larger than the limit, it is added and then evicted through the normal callback path. A limit of zero continues to mean unlimited capacity.
- `Get` keeps its current lookup and recency behavior and increments exactly one counter: `Hits` for a found key or `Misses` for an absent key. `Peek` returns the same value/found pair without changing recency or either counter. `Keys` returns the current keys from most to least recently used and does not change recency or counters. `ResetStats` zeros both counters without changing entries.
- `Remove` returns the removed value and `true`, updates byte usage, and invokes `OnEvicted` once when the key exists. For a missing key it returns the zero `Value` and `false` without a callback.
- `Clear` removes every entry, leaves both `Len()` and `Bytes()` at zero, and invokes `OnEvicted` once per entry in least-to-most-recently-used order.
- `Resize` changes the byte limit immediately. A positive limit evicts least-recently-used entries, using `OnEvicted`, until the cache fits; resizing to zero disables the limit without discarding retained entries.

Keep the existing `New`, `Add`, `Get`, `RemoveOldest`, `Len`, `Value`, and `OnEvicted` surfaces compatible. In particular, `Get` and replacement still promote an entry, `RemoveOldest` removes the least-recently-used entry and invokes the callback, and existing zero-limit callers remain unlimited. The cache may remain documented as unsafe for concurrent access.
