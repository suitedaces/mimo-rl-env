# Stuck transactions caused by excessive gas limits

We're hitting a nasty bug: a transaction submitted with an absurdly large gas
limit (well above the block gas limit) gets permanently stuck, and worse, it
blocks every later transaction from the same account.

Here's what happens. When the block builder pops a transaction and writes it
into the block being assembled, the write fails because the requested gas can
never fit in a block. But the builder treats *every* write failure identically:
it puts the transaction back and tries again on the next block. So this
transaction is retried forever, and since the pool already advanced the
account's expected nonce when it accepted the transaction, no later transaction
from that account can ever be processed.

The underlying problem is two-fold and I'd like both addressed:

1. **The state executor's transaction-write path doesn't distinguish "retry"
   from "discard" failures.** When writing a transaction to a block fails, the
   caller needs to know whether the failure is *recoverable* — the transaction
   might succeed in a later block, so it should be retried — or *non-recoverable*
   — the transaction can never be included and must be dropped.

   A write failure is **non-recoverable** precisely when the transaction's gas
   requirement exceeds the block's gas limit (no block could ever hold it).
   Every other failure encountered while writing is **recoverable**, including:
   an incorrect nonce, the sender not being able to afford the gas cost, and a
   transaction that would fit a full block but not the gas remaining in the
   current (already partly filled) one.

   Expose this through the value returned by the write call: it must still
   behave as an `error` (and be `nil` on success), but when non-nil it must
   carry an exported `IsRecoverable` boolean field reporting the above.

2. **The pool can't roll back an account's expected nonce.** The pool tracks the
   next expected nonce per account. When a transaction it tracked is discarded,
   that counter has to be rolled back, otherwise the account stays blocked. Add
   a method `DecreaseAccountNonce(tx *types.Transaction)` to the transaction pool
   that decrements by one the next expected nonce it tracks for the sender of
   `tx`. If the pool isn't tracking that account, it must be a safe no-op.

With these in place, the block builder can drop a permanently-invalid
transaction (and roll back the account nonce) while still retrying transactions
that merely didn't fit the current block.
