## Lander drops EVM transactions when the node responds with "nonce too low"

We're running the lander against an EVM chain and noticed that messages occasionally vanish even though the underlying transaction actually made it on-chain. Digging into the logs, the pattern is always the same: the provider returns a `nonce too low` error during submission, the inclusion stage treats that as a fatal submission failure, and the transaction gets dropped from the pool right after.

The thing is — `nonce too low` from an EVM node almost always means the nonce we're trying to use has already been consumed, i.e. some earlier submission of this same transaction (or its replacement) is already in the mempool or already mined. Dropping the transaction in that situation is the worst possible reaction:

- If it was the very first submission attempt and the node rejected us with `nonce too low` because of a stale local nonce, we still want a chance to recover.
- If it was a re-submission, we already have prior tx hashes recorded for this transaction; one of them is very likely on-chain. Dropping the lander-side `Transaction` means we throw away those hashes and lose track of a payload that actually went through.

Today the EVM adapter's `submit` path bubbles the raw provider error up, the inclusion stage sees a generic submission error, and the tx gets dropped together with all its payloads. That's how we end up with "successfully delivered on chain, but lander reports it as dropped".

### Expected behavior

The lander should recognize `nonce too low` from the EVM provider as a signal that the transaction may already exist on chain rather than as a hard submission failure. Instead of dropping the transaction, the inclusion stage should keep it around and let the normal status-checking path determine what actually happened (mempool / included / finalized / genuinely missing) before deciding whether to drop.

In other words: a `nonce too low` response on submit must not, by itself, cause the transaction to be removed from the inclusion pool.
