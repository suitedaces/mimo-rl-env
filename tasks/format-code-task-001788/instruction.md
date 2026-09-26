# Make pre-confirmation anchor sweeping deadline-aware

When a channel is force-closed, the channel arbitrator submits the commitment
transaction's anchor outputs to the sweeper *before* the commitment confirms, so
the commitment can be CPFP-bumped into a block. Today every one of those anchor
sweeps requests confirmation within a fixed, hard-coded target that is completely
detached from how urgently the commitment actually needs to confirm. That makes
us systematically overpay miner fees: if the soonest HTLC on the channel doesn't
expire for hundreds of blocks, there is no reason to pay for a near-term
confirmation.

Make the anchor sweep **deadline-aware**: when the arbitrator offers the
commitment anchors to the sweeper, the confirmation target it requests must be
derived from the channel's currently active HTLCs instead of a constant.

## Required behavior

Compute a single confirmation deadline (in blocks, relative to the current block
height) from the channel's active incoming and outgoing HTLCs, and use it as the
confirmation target for every anchor swept in that pass.

An HTLC contributes its CLTV expiry height (its refund/timeout height) to the
deadline calculation only when **both** of the following hold:

- It is not a dust HTLC (i.e. it has an actual on-chain output); dust HTLCs are
  ignored regardless of their expiry.
- It is an **outgoing** HTLC, **or** it is an **incoming** HTLC for which we
  currently have the payment preimage available.

Incoming HTLCs whose preimage we do not have are ignored even if their expiry is
the smallest, because we cannot claim them on-chain yet.

From the qualifying HTLCs, determine the deadline as follows:

- Let `minHeight` be the smallest qualifying expiry height. The confirmation
  target is `minHeight - currentHeight`.
- If no HTLC qualifies (no active HTLCs, or none meet the conditions above),
  fall back to a default confirmation target of **144** blocks.
- If `minHeight` is already at or below the current height (the deadline has
  been reached or passed), use a confirmation target of **1** block, since we
  need the sweep to confirm as soon as possible.

The same computed target is applied to all anchor outputs that are swept in the
same pass. Everything else about how anchors are offered to the sweeper (forcing
the sweep, the exclusive grouping, etc.) is unchanged.
