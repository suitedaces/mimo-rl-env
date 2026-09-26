`lax.scan` doesn't catch aliased mutable array refs the way `jit` does

`jax.jit` already validates that you don't pass the same mutable array reference in twice, and that a ref isn't both closed over and passed as an argument — you get a nice `ValueError` explaining what's wrong. But `lax.scan` doesn't do any of this checking, so the same mistakes either silently produce wrong results or blow up much later with a confusing error.

Quick repro of the two cases I hit:

```python
import jax
import jax.numpy as jnp
from jax import lax
from jax._src.core import mutable_array

# case 1: same ref passed twice as part of the scan carry
ref = mutable_array(jnp.zeros(3))

def body(carry, x):
    a, b = carry           # a and b are the *same* ref
    a[...] = a[...] + x
    return (a, b), None

lax.scan(body, (ref, ref), jnp.arange(5.))   # should error, currently doesn't

# case 2: ref closed over *and* passed in
ref2 = mutable_array(jnp.zeros(3))

def body2(carry, x):
    carry[...] = carry[...] + ref2[...] + x   # closes over ref2
    return carry, None

lax.scan(body2, ref2, jnp.arange(5.))         # ref2 is both closed-over and the carry
```

Under `jit` both of these raise a clear `ValueError` telling me which arg(s) are the problem. Under `scan` they don't, even though the constraint is the same — you can't have multiple references to the same mutable array reaching the traced function.

It would be great if `scan` performed the same checks and produced the same kind of error message, so the failure mode is consistent across the two APIs.
