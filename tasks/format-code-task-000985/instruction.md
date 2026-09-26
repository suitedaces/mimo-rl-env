The reusable `lib/lru` cache currently has too little lifecycle control for long-running callers, and replacing an existing value can leave its byte accounting wrong. Extend this package into a complete, concurrency-safe byte-bounded LRU while keeping its existing callers source-compatible.

Keep `Value`, `New(maxBytes int64, onEvicted func(string, Value))`, the public `OnEvicted` callback, and the existing `Add`, `Get`, `RemoveOldest`, and `Len` method signatures. Add these methods to `*Cache`:

- `Bytes() int64`, returning the current accounted size.
- `Peek(key string) (Value, bool)`, looking up without changing recency. A miss returns `nil, false`.
- `Remove(key string) bool`, returning whether an entry was removed.
- `Purge()`, removing every entry.
- `Resize(maxBytes int64) int`, changing the limit and returning the number of entries removed immediately by that call.

An entry's accounted size is `len(key) + value.Len()`. Adding a new key makes it most recently used. Adding an existing key replaces its value, adjusts the byte total by the old/new size difference, and promotes the key; replacement alone is not an eviction and must not call `OnEvicted`. After an add, a nonzero byte limit evicts least-recently-used entries until the total is at or below the limit. Equality with the limit is allowed, a zero limit means unlimited capacity, and an entry larger than a nonzero limit is consequently evicted, including when it is the only entry.

`Get` continues to promote a hit, whereas `Peek` never does. `RemoveOldest` removes the currently least-recently-used entry and remains a no-op on an empty cache. `Remove`, `RemoveOldest`, `Purge`, capacity eviction, and shrinking `Resize` must update length and byte accounting and synchronously invoke `OnEvicted` exactly once per entry actually removed, with that entry's key and value. Missing-key removal, empty removal/purge, and replacement do not invoke it. Purge callback order is not part of the contract.

Resizing upward does not evict. Resizing downward uses normal LRU order until within the new limit; resizing to zero switches to unlimited mode without evicting. All cache methods must be safe to call concurrently, assuming callers do not mutate the public `OnEvicted` field while the cache is in use. Preserve the established hit/miss behavior and eviction ordering of the existing API.
