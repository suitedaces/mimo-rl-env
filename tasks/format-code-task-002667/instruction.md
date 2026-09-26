# Add a TEASER early time series classifier

`sktime`'s early-classification family currently only contains a single
probability-threshold based classifier. I'd like to add the **TEASER** algorithm
("Two-tier Early and Accurate Series classifiER") alongside it, exposed as a new
classifier named `TEASER` that can be imported from the early-classification part
of `sktime.classification`.

## What it should do

Early time series classification is about committing to a label after seeing as
little of each series as possible while staying accurate. TEASER works in two
tiers: it trains a base time series classifier at a set of increasing series
lengths ("classification points"), and at each length it uses a safety/novelty
check on the base classifier's output to decide whether an early prediction is
reliable enough to commit to. A prediction is only committed once it has been
judged safe for enough *consecutive* classification points predicting the same
class — and the number of consecutive safe predictions required should be tuned
during fitting (e.g. to balance how early vs. how accurately the model decides).

The classifier takes a base sktime time series classifier (anything that produces
class probabilities) and an optional explicit list of integer `classification_points`
(the series lengths at which classifiers are built and predictions are allowed),
plus the usual `random_state` / `n_jobs` options. It must behave like a normal
sktime classifier: `fit(X, y)` trains it and returns `self`, and it integrates
with the standard estimator machinery (`classes_`, `n_classes_`, etc.).

## Observable contract

**`predict(X)`** returns a 1D array with one entry per instance in `X`; every
entry is one of the fitted class labels (`classes_`).

**`predict_proba(X, state_info=None)`** drives the early-classification decision and
returns a tuple `(probabilities, decisions, state_info)`:

- `probabilities` is a 2D array of shape `(n_instances, n_classes)`. For every
  instance that has been *committed* (decided), its row is a valid probability
  distribution (non-negative, summing to 1).
- `decisions` is a length-`n_instances` sequence of booleans: `True` for an
  instance that has been committed at this point, `False` otherwise.
- `state_info` is a per-instance state object (one entry per instance) that the
  caller feeds back into the next call to continue the decision process on a
  longer prefix of the same instances. Pass `None` on the first call.

The decision process is a streaming one: you call `predict_proba` repeatedly on
increasingly long prefixes of the same instances, passing the previously returned
`state_info` back in each time. The following must hold:

- Decisions are **monotonic**: once an instance has been committed it stays
  committed on every subsequent call, and the call always reports it as decided.
- When `X` has the full series length (the largest classification point), **every**
  instance is committed (`decisions` is all `True`).
- If `X`'s series length is not one of the classification points produced during
  fitting, a `ValueError` is raised.

**`score(X, y)`** evaluates early-classification quality by internally running the
streaming decision process over the classification points up to the length of `X`,
committing each instance at the earliest length deemed safe. It returns a tuple of
three floats `(harmonic_mean, accuracy, earliness)`, each in `[0, 1]`:

- `accuracy` — the proportion of instances whose committed prediction matches the
  true label.
- `earliness` — the average fraction of the full series length consumed before
  committing (smaller means earlier decisions).
- `harmonic_mean` — the harmonic mean of `accuracy` and `(1 - earliness)`, i.e.
  `2 * accuracy * (1 - earliness) / (accuracy + (1 - earliness))`, and `0` when
  that denominator is `0`.

The existing probability-threshold early classifier and its tests must keep
working unchanged.
