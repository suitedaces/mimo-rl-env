## Feature request: find nearest index in a cartesian grid without building the product

I'm working with value-function iteration on a multi-dimensional state space built from a few 1-D grids (capital, productivity, etc.). The discretized state space is the cartesian product of these per-dimension grids, and I often need to map a continuous point back to the index of its nearest neighbor in that product.

The natural way with what's currently in `quantecon.gridtools` is:

```python
import numpy as np
import quantecon as qe

nodes = (np.linspace(0, 1, 50), np.linspace(0, 1, 50), np.linspace(0, 1, 50))
prod = qe.cartesian(nodes)             # shape (50**3, 3)

x = np.array([0.13, 0.42, 0.77])
i = np.argmin(np.sum((prod - x)**2, axis=1))   # nearest index in prod
```

This works for toy sizes but is wasteful and quickly becomes unusable as I add dimensions or refine grids — `cartesian` materializes the full `m**n` array even though I only want one integer back. With `n = 5` and `m = 100` per dimension I'm already allocating 10^10 floats just to do a nearest-neighbor lookup, while each per-dimension grid is sorted and the 1-D nearest lookup is trivially `O(log m)`.

It would be very useful if `gridtools` provided a helper that, given the per-dimension `nodes` (not the materialized product) and a query point `x`, returns the index that the nearest product point *would* have, had we built the product with `qe.cartesian(nodes)`. Concretely I'd like to be able to do something like:

```python
nodes = (np.arange(3), np.arange(2))
# qe.cartesian(nodes) would be:
# [[0 0], [0 1], [1 0], [1 1], [2 0], [2 1]]

# closest product point to (0.6, 0.4) is (1, 0), which is row 2
idx = qe.<helper>((0.6, 0.4), nodes)
assert idx == 2
```

A few things I'd want from it:

- It should agree with what you'd get from `np.argmin` over `qe.cartesian(nodes, order=...)`, for both `'C'` and `'F'` enumeration order, since I sometimes use `mlinspace`/`cartesian` with `order='F'`.
- It should accept a batch of query points too (I typically map a whole simulated path at once), and return an array of indices in that case.
- The complexity should scale like `O(n log m)` per query (binary search per dimension), not `O(m**n)` — that's the whole point of not building the product.

Happy to help if there's interest.

A name like `cartesian_nearest_index` would fit alongside the existing `cartesian` / `mlinspace` helpers in `gridtools`.
