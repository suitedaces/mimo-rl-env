Boolean indexing does not compatible with Ellipsis
It seems that the following snippet does not work anymore.

```python
import jax
import jax.numpy as jnp
import numpy as np

jnp.ones((4, 3, 2))[..., np.array([True, False])]  # fail
jnp.ones((4, 3, 2))[:, :, np.array([True, False])]  # work
np.ones((4, 3, 2))[..., np.array([True, False])]  # work
```
