## `Split` with `n_splits=1` should be optimized away

When I use `theano.tensor.split` with `n_splits=1` (this comes up in generic code where the number of splits is computed from a parameter that can be 1), the resulting graph still contains a full `Split` Apply node, even though semantically it's a no-op — it just returns the input tensor unchanged along the requested axis.

Minimal example:

```python
import theano
import theano.tensor as T

x = T.vector('x')
axis = 0
splits = T.as_tensor_variable([x.shape[0]])
y, = T.split(x, splits, n_splits=1, axis=axis)

f = theano.function([x], y)
theano.printing.debugprint(f)
```

The compiled function still has a `Split` node in it, while ideally the optimizer should recognize this case and just forward `x` through (it's the identity along that axis).

This matters for a few reasons:

- It's wasted work at runtime — every call to `f` goes through `Split`'s perform, allocates a list, etc., for what is mathematically a pass-through.
- It blocks downstream optimizations that would otherwise see `x` directly instead of seeing it behind a `Split`.

Could the canonicalize / specialize pass include a rule that strips `Split` when there is only one output split? In that case the only thing that conceptually has to hold for the original graph to be well-formed is that the single split size equals the size of `x` along `axis` (and that the splits vector has length 1) — but those are already promised by the user constructing a 1-split Split, so I don't think the optimization should refuse to fire on that account.
