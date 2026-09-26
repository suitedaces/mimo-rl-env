# Make offline evaluation usable and enforce label consistency

The library exposes a public evaluation helper `evaluate`, importable from
`libreco.evaluation`. It is meant to score an already-fitted model on a chunk of
data and return the requested metrics. Two problems: the entry point is
currently broken (importing/using it blows up), and even once that is sorted it
does nothing to guard against ill-formed evaluation labels. Please get it
working and make it honor the contract below.

## Public surface

```
evaluate(model, data, neg_sampling, eval_batch_size=8192,
         metrics=None, k=10, sample_user_num=None, seed=42)
```

- `model` is a fitted model (it carries a `task` of either `"rating"` or
  `"ranking"`, knows its `data_info`, and can `predict`).
- `data` is the evaluation data, either a `pandas.DataFrame` or an
  already-transformed dataset object produced by the dataset builders.
- `neg_sampling` is a **required** boolean. Callers must pass it explicitly;
  invoking `evaluate` without it is an error.
- The function returns a `dict` mapping each requested metric name to its value.

## Behavior of `neg_sampling`

Negative sampling exists because implicit-feedback ("ranking") data often
contains only positive interactions, which is not directly usable for computing
ranking metrics.

- **`neg_sampling=True`** — negative items are generated for the evaluation data
  before scoring. As a result, data that contains only positive interactions can
  still be evaluated for ranking metrics and produces results.

- **`neg_sampling=False`** — the data is evaluated as-is, with a consistency
  check on its labels:
  - For a **ranking** model the labels are expected to be implicit binary
    feedback: the set of distinct label values must be exactly `{0, 1}`. If the
    labels are anything else — raw non-binary values, or only one of the two
    classes present — raise `ValueError`, with a message explaining that for a
    ranking task without negative sampling the labels must be 0 and 1.
  - For a **rating** model there is no such restriction: arbitrary numeric
    ratings are accepted and evaluation proceeds.

A run that passes the checks computes the requested `metrics` (defaulting to a
single loss metric when none are given) and returns them as a `dict`.
