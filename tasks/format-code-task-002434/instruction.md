error: Cannot infer type of lambda
Repro:

``` python
from typing import TypeVar, Callable
T = TypeVar('T')
def foo(arg: Callable[..., T]) -> None: pass
foo(lambda: 1)  # E: Cannot infer type of lambda
x = lambda: 1
foo(x)  # OK
```

That error message was introduced in 6edd1b96f39189877b7650082dc0e2eec7b4b34c ("Fix lambda type inference special cases").
