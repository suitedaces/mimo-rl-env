## `@settings` decorator is not typed, breaks `mypy --strict`

I'm trying to type-check my test suite under `mypy --strict`, and the `@settings(...)` decorator from Hypothesis causes errors on every test it's applied to.

A minimal reproducer:

```python
# test_example.py
from hypothesis import given, settings, strategies as st

@settings(max_examples=10)
@given(st.integers())
def test_addition_is_commutative(x: int) -> None:
    assert x + 0 == x
```

Running `mypy --strict test_example.py` complains about the `@settings(...)` line — mypy treats it as an untyped decorator, which under `--strict` poisons the decorated function (it gets reported as untyped too, even though I've annotated it). The same code without `@settings` (i.e. only `@given(...)`) type-checks fine.

I'd expect `@settings(...)` to be a transparent, type-preserving decorator — applying it to a function should not change the function's type as far as the type checker is concerned. As far as I can tell from the public API, `settings(...)` returns a callable that takes a test function and returns the same test function (it just attaches some metadata), so this should be expressible without losing the original signature.

Could the `@settings` decorator get proper type annotations so that it works cleanly under `mypy --strict`?
