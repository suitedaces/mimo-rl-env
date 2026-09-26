# Support next-epoch crosslink committees with a registry-change option

Our beacon-chain core exposes a function that returns the crosslink committees
(each a set of validator indices together with the shard it is assigned to) for
a given slot. Today it only knows how to answer for slots that belong to the
**previous** or **current** epoch — asking for a slot in the **next** epoch is
rejected as out of bounds. We need it to answer for next-epoch slots too, since
proposers and attesters have to look one epoch ahead.

Please extend the existing "crosslink committees at slot" lookup so that:

- Slots whose epoch equals the next epoch are now valid and return the
  committees for that epoch instead of an error. The accepted range becomes
  `previousEpoch <= epoch(slot) <= nextEpoch`; a slot whose epoch is earlier
  than the previous epoch or later than the next epoch must still return an
  error.

- Callers can optionally request a *registry change*. There are two valid
  shufflings for the next epoch — one that assumes the validator registry was
  rotated and one that assumes it was not — and the caller chooses between them.
  This option only affects next-epoch slots; for previous- and current-epoch
  slots the result must be exactly the same regardless of what is requested.

- For a next-epoch slot, the default (no registry change) keeps the committees
  starting at the current epoch's start shard. When a registry change is
  requested, the committees are rotated forward: their start shard is advanced
  by the number of committees in the current epoch (taken modulo the configured
  shard count).

Existing callers that only ask for previous/current-epoch committees and do not
care about a registry change must keep working without changes, and their
results must be unchanged.
