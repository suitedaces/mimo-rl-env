## mempool: remove dead `isTreasuryEnabled` / `isAutoRevocationsEnabled` parameters

A bunch of methods on `mempool.TxPool` currently require callers to pass
`isTreasuryEnabled` and `isAutoRevocationsEnabled` flags, but the methods
themselves don't actually do anything with those flags — they're just
threaded through to the next call, which also doesn't use them.

For example, in `server.go` every time we want to evict something from the
pool we end up with code like this:

```go
tipHash := &s.chain.BestSnapshot().Hash
isTreasuryEnabled, err := s.chain.IsTreasuryAgendaActive(tipHash)
if err != nil {
    srvrLog.Errorf("Could not obtain treasury agenda status: %v", err)
}

isAutoRevocationsEnabled, err :=
    s.chain.IsAutoRevocationsAgendaActive(tipHash)
if err != nil {
    srvrLog.Errorf("Could not obtain automatic ticket revocations agenda "+
        "status: %v", err)
}

numEvicted := s.txMemPool.RemoveOrphansByTag(mempool.Tag(sp.ID()),
    isTreasuryEnabled, isAutoRevocationsEnabled)
```

…just to call into `RemoveOrphansByTag`, which forwards the two booleans to
`removeOrphan`, which… also doesn't read them. The same pattern shows up
around `RemoveTransaction`, `RemoveDoubleSpends`, `RemoveOrphan`, and friends
on the public surface of `TxPool`, and across a number of the internal
helpers that back them.

These parameters are effectively dead weight on the API: callers have to go
fetch agenda state from the chain solely to satisfy a signature, the values
then get tunneled through several layers of mempool internals, and nothing
ever actually consumes them.

It would be nice to clean this up — drop the unused agenda flag parameters
from the affected `TxPool` methods and simplify the call sites accordingly,
so callers no longer have to query agenda status just to feed parameters
that don't do anything.
