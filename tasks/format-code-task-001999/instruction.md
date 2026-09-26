### Accumulated fees not fully reverted for failed relayed user transactions

While inspecting block-level fee bookkeeping I noticed that when a relayed transaction's inner user transaction has to be reverted, the `accumulatedFees` / `developerFees` reported by the fee handler don't go back to what they should be — some of the fee that was charged for the user tx is still counted.

Reproduction is roughly:

1. Process a relayed transaction that wraps a user tx (any of MoveBalance / SCDeployment / SCInvoking / BuiltInFunctionCall as the inner type). During processing, the move-balance cost of the inner user tx gets fed into `txFeeHandler.ProcessTransactionFee(...)` — so the accumulator now tracks fee entries for both the relayed/original tx and the inner user tx.
2. Later, something causes the post-processor to call `RevertFees([...])` with the **original** (relayed) tx hash — e.g. the inner execution ends up failing and the block-level revert path kicks in.
3. Read `GetAccumulatedFees()` / `GetDeveloperFees()` afterwards.

Expected: the fee that was added on behalf of that relayed transaction is fully removed — including the part that was added while processing its inner user tx.

Actual: only the entry stored under the original tx hash is removed. The fee entry that was registered for the inner user tx survives, so `accumulatedFees` ends up higher than it should be. Over a block this shows up as the block's accumulated fees not matching the sum of the fees that actually stuck.

The root of the asymmetry seems to be that on the "process" side the fees for a relayed tx end up split across two different hash keys (original tx + user tx), but on the "revert" side the caller only knows about the original tx hash — there is no way for it to find the user-tx entry that belongs to the same relayed transaction. It would be good if the fee handler took care of this internally so callers can keep reverting by original tx hash and get the whole thing rolled back.

I'd expect a new entry point on the fee handler along the lines of `ProcessTransactionFeeRelayedUserTx(...)` that the relayed-tx code path can use when registering the inner user-tx fee, so the handler can link it back to the original tx hash.
