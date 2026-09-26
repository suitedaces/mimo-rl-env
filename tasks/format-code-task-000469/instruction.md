# Add a "consecutive irrelevant" stopping rule

The active learning loop decides when to stop screening through a *stopping
mechanism*: a small object with a `stop(results, data)` method that returns
`True` when the review should halt. The project already ships a handful of these
(for example `StoppingDefault`, `StoppingN`, `StoppingQuantile`,
`StoppingIsFittable`), and an `ActiveLearningCycle` delegates to whatever object
is passed as its `stopping` criterion.

A very common heuristic in screening is missing: stop once the reviewer has seen
a run of irrelevant records in a row. Please add a new stopping mechanism for
this, exposed from the same place as the existing stopping rules and named
`StoppingNConsecutiveIrrelevant`.

Behaviour:

- It is constructed with a single threshold `n` — the number of consecutive
  irrelevant records that should trigger stopping.
- `stop(results, data)` follows the same calling convention as the other
  stopping rules. `results` is a `pandas.DataFrame` holding the records labeled
  so far in labeling order, with a `label` column where `1` means relevant and
  `0` means irrelevant. `data` is the full collection of records being screened;
  only its length (the total number of records) is relevant.
- It returns `True` when the most recently labeled `n` records are *all*
  irrelevant. The run must be contiguous and at the end of `results`: scattered
  irrelevant records that do not form a trailing run of length `n` must not
  trigger stopping.
- It also returns `True` when there is nothing left to screen — i.e. every
  record has been labeled (`len(results) >= len(data)`) or `data` is empty.
- Otherwise it returns `False`. In particular, when fewer than `n` records have
  been labeled and the pool is not yet exhausted, it must return `False`.

The new mechanism must work both on its own and when handed to an
`ActiveLearningCycle` as its stopping criterion (so that `cycle.stop(results,
data)` reflects the rule above).
