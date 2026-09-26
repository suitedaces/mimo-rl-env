### CheckStateConsistency doesn't use trieNodeCache during state migration

We run klaytn nodes with trieNodeCache (fastcache) enabled to speed up state access. When triggering a state migration on such a node, the main copy phase finishes fine, but the final `CheckStateConsistency` step at the end of `migrateState` is noticeably problematic compared to ordinary state reads on the same node — the iteration over the source trie is much slower than I'd expect for a node whose trie data is largely hot in cache.

Looking at how the rest of the codebase reads state, normal access goes through `bc.StateCache()` so that the trieNodeCache (fastcache) sits in front of the disk DB. The consistency check at the tail of state migration, however, doesn't seem to participate in that caching path the same way the rest of the system does — so on a cache-heavy setup the check can't take advantage of nodes that the node already has cached.

It would be great if `CheckStateConsistency` (as invoked from `migrateState`) read the source (and target) state through the same cached state database the rest of the chain uses, instead of going through the raw underlying DB. That way reading the old trie during the post-migration check benefits from the same fastcache layer that ordinary block processing benefits from.

No correctness issue observed (the check eventually reports consistent), this is about it not using the cache that's right there.
