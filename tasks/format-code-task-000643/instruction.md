# Add explicit `sequence` and `parallel` flow primitives

Right now the only way to express concurrency in a function tree is by nesting a
plain array inside the tree — an "array inside an array" means "run these in
parallel". This is implicit and surprising: people import chains from other
files and accidentally change execution semantics, and there is no way to label
a group of steps.

I'd like to introduce two first-class primitives for describing execution flow
and make them part of the package's public API (named exports alongside the
existing default factory):

- `sequence(...)` — runs its items one after the other.
- `parallel(...)` — runs its items at the same time.

Both should accept an **optional leading string** used as a human-friendly name
for the group, followed by any number of items. An item may be a function, a
plain array, or another `sequence`/`parallel` value. The name is purely a label
— it must never be executed as a step.

The runnable tree you hand to `execute(...)` should now accept a value produced
by these primitives just like it already accepts a plain array.

Behavior that must hold:

- **Sequence is sequential.** `sequence(a, b)` runs `a` then `b`, threading the
  payload through and merging each step's returned object into the payload, the
  same way a plain top-level array already behaves. A plain array must keep
  working and must keep meaning "a sequence".

- **Parallel is concurrent.** `parallel(a, b)` runs its items concurrently. The
  `parallelStart` event must report the number of items being run as the number
  of branches, and the final payload must be the merge of every branch's
  resulting payload.

- **A group is one branch.** When a parallel's item is a plain array (or a
  `sequence`), that group is treated as a *single* parallel branch and runs as
  one unit: its inner functions execute sequentially (a later step only runs
  after the earlier one has resolved), and the group counts as exactly one
  branch in the parallel — not one branch per inner function.

- **Nesting an array no longer means parallel.** A plain array nested inside
  another array (or sequence) is just a nested sequence and runs sequentially;
  it must not trigger parallel execution.

- **Parallel flag.** The per-function details already emitted on the function
  lifecycle events expose an `isParallel` indicator. It must be `true` only for
  functions that are *direct* branches of a `parallel`. Functions that live
  inside a grouped sequence — even one nested within a `parallel` — are not
  themselves parallel branches and must report `false`.

Keep everything else (paths/outputs, providers, payload merging, existing
events) working as before.
