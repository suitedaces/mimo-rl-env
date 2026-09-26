## `RecListAnalysis(include_missing=True)` loses the algorithm label for users with no recs when comparing multiple algorithms

I'm running an offline experiment that evaluates several recommenders on the same test set and uses `RecListAnalysis` to compute per-user metrics. My recs frame has an `Algorithm` column on top of `user`, so I get one row per (Algorithm, user). My truth frame is keyed only on `user`.

Because some algorithms don't produce recommendations for every test user, I want to include those users (with `nrecs = 0`) in the output so the metrics aren't biased by silently-dropped users. So I pass `include_missing=True`:

```python
rla = topn.RecListAnalysis()
rla.add_metric(topn.ndcg)
results = rla.compute(all_recs, test_data, include_missing=True)
print(results.reset_index().head(20))
```

The row count looks roughly right (recs users + missing-from-recs users, per algorithm), but the output is unusable: every row that corresponds to a user who was missing from a given algorithm's recs has `Algorithm = NaN`. So I can't tell which algorithm those "missing" rows are supposed to belong to, and any subsequent `groupby('Algorithm')` either drops them or lumps them all into one bogus group.

A concrete minimal-ish reproducer:

```python
import pandas as pd
from lenskit import topn

truth = pd.DataFrame({
    'user': [1, 1, 2, 2, 3, 3],
    'item': [10, 11, 20, 21, 30, 31],
})

recs = pd.DataFrame({
    'Algorithm': ['A', 'A', 'A', 'A', 'B', 'B'],
    'user':      [  1,   1,   2,   2,   1,   1],   # B has no recs for users 2 and 3
    'item':      [ 10,  99,  20,  88,  10,  77],
    'rank':      [  1,   2,   1,   2,   1,   2],
})

rla = topn.RecListAnalysis()
out = rla.compute(recs, truth, include_missing=True).reset_index()
print(out)
```

What I expected: every test user shows up once per algorithm (so 3 users × 2 algorithms = 6 rows), with `Algorithm` correctly set to `'A'` or `'B'` on every row, `nrecs = 0` where that algorithm gave the user nothing, and `ntruth` filled in.

What I actually get: the rows for "users that this algorithm didn't recommend to" come back with `Algorithm` blank, so I can't group results by algorithm afterwards. Setting `include_missing=False` works fine but drops the users I specifically want to keep.

It looks like the missing-user fill only works correctly when the rec key equals the truth key (single ungrouped evaluation). As soon as there's an extra grouping column like `Algorithm`, the fill-in for missing users doesn't carry that column over.
