## `math.exp` returns `inf` instead of raising `OverflowError`

I'm porting some code from CPython to RustPython and noticed that
`math.exp` doesn't behave the same way for large arguments.

In CPython:

```python
>>> import math
>>> math.exp(1e6)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
OverflowError: math range error
```

In RustPython:

```python
>>> import math
>>> math.exp(1e6)
inf
```

This breaks code that wraps `math.exp` in `try/except OverflowError` —
the exception never fires on RustPython, and `inf` silently propagates
through downstream calculations instead.

I'd expect `math.exp` (and the other `math` functions in the same boat)
to match CPython here: when the input is a finite number but the result
would overflow to infinity, raise `OverflowError` rather than returning
`inf`.

In particular, `math.ldexp` has the same issue (e.g. `math.ldexp(1.0, 10000)`
returns `inf` instead of raising) — and while you're at it, please make sure
that special inputs to `ldexp` (NaN, ±inf, 0) are still returned unchanged
rather than getting converted into an `OverflowError`.
