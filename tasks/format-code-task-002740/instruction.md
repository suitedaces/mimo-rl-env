# Resolve sync committee seats to validator indices

When we process Altair (and Merge) blocks and validator duties, we constantly
need to know *which validator* occupies each seat of the current and next sync
committees. The beacon state only stores the committees as lists of public keys
(`current_sync_committee.pubkeys` / `next_sync_committee.pubkeys`), so every
consumer that wants a `ValidatorIndex` ends up rebuilding a pubkey → index
mapping by scanning the entire validator registry. That scan is wasteful when it
happens on a hot path such as block replay.

Give us a single helper that turns a sync-committee-bearing state into the
validator indices behind both committees.

## What to add

- A public `SyncCommitteeCache` type with two fields, `current_sync_committee`
  and `next_sync_committee`, each an `array[SYNC_COMMITTEE_SIZE, ValidatorIndex]`.

- A public `get_sync_committee_cache(state, cache)` that accepts an Altair or
  Merge `BeaconState` together with a mutable `StateCache` and returns a
  `SyncCommitteeCache`.

## Behavior

For the returned value, at every position `i`:

- `current_sync_committee[i]` is the index of the validator in
  `state.validators` whose public key equals
  `state.current_sync_committee.pubkeys[i]`.
- `next_sync_committee[i]` is the index of the validator in `state.validators`
  whose public key equals `state.next_sync_committee.pubkeys[i]`.

The mapping must be exact for both committees across all `SYNC_COMMITTEE_SIZE`
seats (the committees contain duplicates — the same validator may appear in
many seats — which is fine).

Because recomputing the mapping is expensive, the result should be memoized in
the supplied `StateCache`, keyed by the state's sync committee period, and
reused on subsequent calls. The result must be deterministic and stable: calling
the helper repeatedly — whether reusing the same cache or starting from a fresh
one — yields the same indices.
