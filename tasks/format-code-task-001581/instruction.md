## Deleting a state inside a transaction and then reading it back returns the old value

I'm writing some action handler code on top of `stateTX` that, within the same uncommitted transaction, deletes an account state and then reads it back to make sure it's gone. Roughly:

```go
// inside one stateTX, before Commit()
if err := ws.DelState(addr); err != nil { ... }

var acc state.Account
err := ws.State(addr, &acc)
// I expect err to indicate the state no longer exists (state.ErrStateNotExist)
```

What I actually get is `err == nil` and `acc` is filled in with whatever the account looked like before I deleted it. So as far as the caller can tell, the `DelState` had no effect — until the transaction is committed and I re-open the world state, at which point the key really is gone.

This is pretty surprising, and it's a problem for any protocol logic that wants to do a delete and then verify / branch on the post-delete view of state mid-transaction (e.g. "delete this entry, then assert it isn't there before re-creating it"). Reads inside a `stateTX` should reflect the writes (including deletes) that have already happened on that same `stateTX`, not silently fall through to the underlying DB's pre-transaction value.

Same thing happens at the lower level with `KVStoreForTrie`: after `Delete(key)` on a `KVStoreForTrie`, calling `Get(key)` on the same instance (before `Flush`) still returns the value that's sitting in the underlying `KVStore`, instead of telling me the key isn't there.

Could the read path be fixed so that a key deleted earlier in the same uncommitted transaction is reported as not-found, the same way it would be after commit?
