## ENH: allow `default_rng` to accept a legacy `RandomState`

I maintain a downstream library that is going through the [SPEC 7](https://scientific-python.org/specs/spec-0007/) transition — moving from legacy `np.random.RandomState` to the newer `Generator` API. As part of that, our public functions still need to accept whatever rng-like object the caller hands us (because callers haven't migrated yet), but internally we'd like to deal with only one type.

The obvious pattern for this normalization is to funnel everything through `default_rng` at the top of the function:

```python
def my_func(..., rng=None):
    rng = np.random.default_rng(rng)
    # from here on, use only the Generator API
    x = rng.random(size=10)
    ...
```

That already works nicely for the input types `default_rng` documents today: `None`, an `int`/array of ints, a `SeedSequence`, a `BitGenerator`, or an existing `Generator` (which is passed through unchanged). So as long as the user gives me any of those, the rest of the function only has to know about `Generator`.

The frustrating gap is the one input type that downstream code is *most* likely to receive during a SPEC 7 migration — a `RandomState`:

```python
>>> import numpy as np
>>> rs = np.random.RandomState(0)
>>> np.random.default_rng(rs)
```

This does not give me back a `Generator`. So in practice I still have to special-case `RandomState` at every call site, which kind of defeats the purpose of having `default_rng` as a normalization entry point.

It would be really helpful if `default_rng` also accepted a `RandomState` and coerced it to a `Generator`, so the pattern above works uniformly for every kind of rng input a downstream caller might still be passing in.
