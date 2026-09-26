## FVM meter has no way to query remaining computation capacity for a given kind

Today the meter interface in `fvm/environment` (and the underlying `ComputationMeter` / `ExecutionState` / `transactionState`) only exposes:

- `MeterComputation(kind, intensity)` — charge `intensity` units of `kind`
- `ComputationAvailable(kind, intensity) bool` — predicate: "is there room for this many?"
- `TotalComputationUsed()` / `TotalComputationLimit()` — aggregates across all kinds

What's missing is a way to ask "for this `ComputationKind`, given its weight and the remaining budget, how much more `intensity` can I still meter?"

### Why I need this

I'm working on an FVM-side component that wants to do as much work as the remaining transaction budget allows and then stop cleanly (think gas-style accounting for something like EVM execution / RLP). With only `ComputationAvailable`, the best I can do is keep guessing intensities or binary-search until the predicate flips, which is awkward and noisy. A direct "how many units of `kind` do I still have room for" query would let me size the next chunk of work in one shot.

### Cadence runtime integration

Separately, the latest `runtime.MeterInterface` in cadence now expects implementations to expose a "remaining computation for kind" method alongside the usual `MeterComputation` / `ComputationUsed` / `MeterMemory` / `MemoryUsed` / `InteractionUsed` ones. Right now `fvm/environment.Meter` re-declares those methods by hand and doesn't satisfy the new cadence interface, so the FVM meter can't be plugged into cadence as-is. It would be nice if the environment-level `Meter` interface simply lined up with what cadence's runtime requires, instead of drifting from it.

### Expected behavior of the query

Whatever the exact shape ends up being, the answer should be consistent with how `MeterComputation` already behaves:

- For a `ComputationKind` that has a weight configured: report how much more `intensity` of that kind can still be metered before the transaction's computation limit is hit (i.e. take the weight into account, not just raw used vs. limit).
- For a `ComputationKind` with no weight configured: `MeterComputation` already silently accepts any intensity for these kinds, so the answer should reflect "effectively unbounded" rather than zero.
- If the budget is already exhausted, the answer should be zero (not negative / not wrap around).
- The same query should propagate through the stack (`ComputationMeter` → `ExecutionState` → `transactionState` → `environment.Meter`) and behave correctly when limits enforcement is disabled or the state is finalized, mirroring how the existing `ComputationAvailable` / `MeterComputation` calls treat those cases.
