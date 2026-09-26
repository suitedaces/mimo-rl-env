## Callable objects (instances with `__call__`) rejected as a `typing.Callable` argument

I'm using `runtime_validation` to type-check a function whose parameter is annotated as `typing.Callable[[int], str]`. Plain functions work fine, but if I try to pass an instance of a class that implements `__call__`, validation rejects it.

Minimal repro:

```python
import typing
from enforce import runtime_validation

class Multiplier:
    def __call__(self, a: int) -> str:
        return str(2 * a)

@runtime_validation
def run(f: typing.Callable[[int], str], b: int) -> str:
    return f(b)

# works:
def bar(a: int) -> str:
    return str(2 * a)
run(bar, 5)

# rejected:
run(Multiplier(), 5)
```

In normal Python an object that defines `__call__` *is* callable — `Multiplier()(5)` works exactly like calling a function — so it feels surprising that `runtime_validation` only accepts plain functions here. Ideally, an object implementing `__call__` should be usable anywhere a regular function is expected, including when the parameter is typed as `typing.Callable[...]`, and its signature should still be validated against the declared `Callable[...]` argument/return types.
