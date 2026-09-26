Inconsistency in numba mode when passing scalar to function
In numba mode:
```python
import aesara
aesara.config.mode = "NUMBA"
import aesara.tensor as at

x = at.scalar(name="x")
f = aesara.function([x], 2*x)
print(repr(f(10)))  # prints 20.0
```

In c mode:

```python
import aesara
import aesara.tensor as at

x = at.scalar(name="x")
f = aesara.function([x], 2*x)
print(repr(f(10))) # prints array(20.)
```

This came up in https://github.com/pymc-devs/pymc/issues/5937. Found by [bherwerth](https://github.com/bherwerth).
