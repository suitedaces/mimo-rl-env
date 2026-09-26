The shared `lib/lru` cache is used as a byte-bounded cache, but it cannot currently report or change its budget and replacing an existing key leaves the accounting inconsistent. Extend its public management API and make byte accounting reliable without breaking the existing constructor or cache operations.

Add these methods on `*Cache`:

- `Bytes() int64` returns the cache's current accounted size.
- `Remove(key string) bool` removes one key and reports whether it was present.
- `Purge()` removes every entry.
- `Resize(maxBytes int64) int` changes the byte limit and returns the number of entries evicted by that call. Callers will pass non-negative limits.

An entry consumes `int64(len(key) + value.Len())` bytes. Adding a new key and replacing an existing key both make that key most recently used. Replacement must account for the full size delta in either direction; it must not invoke `OnEvicted` merely because the old value was replaced. With a positive limit, `Add` must evict least-recently-used entries until the cache fits. A value larger than the whole limit is therefore inserted and then evicted after any older entries, with callbacks in that eviction order. Successful `Get` calls continue to refresh recency.

`Remove` must return true only when it actually removes an entry. A successful removal updates length and bytes and invokes `OnEvicted` exactly once with the removed key and value; removing an absent key changes nothing and invokes no callback. `Purge` removes entries from least to most recently used, invoking the callback once per entry in that order. Purging an empty cache is a no-op.

`Resize` takes effect immediately and remains the limit for later additions. Reducing to a positive limit evicts least-recent entries until the cache fits; increasing the limit does not evict. A zero limit means unlimited capacity, matching `New(0, ...)`, and changing to zero does not evict. Every removal callback must run after the removed entry is no longer retrievable and the cache's length and byte total have been updated.

Keep the existing `New`, `Add`, `Get`, `RemoveOldest`, and `Len` APIs compatible, including the existing optional-callback behavior.
