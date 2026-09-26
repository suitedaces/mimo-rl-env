## `keras_core.ops.softmax` default axis is inconsistent with other libraries

I'm porting some code that uses `tf.nn.softmax` / `torch.nn.functional.softmax` / `scipy.special.softmax` over to `keras_core.ops.softmax`, and I'm getting different numbers when I don't pass an explicit `axis`.

In all of TF, PyTorch, JAX, and SciPy, calling `softmax(x)` on a 2D tensor (no axis argument) gives row-wise softmax — i.e. it normalizes along the last axis, and the result has each row summing to 1.

With `keras_core.ops.softmax(x)`, the output does not behave that way — instead the whole tensor sums to 1 (looks like it's normalizing across every element flattened together). Same issue with `keras_core.ops.log_softmax`.

Minimal repro:

```python
import numpy as np
from keras_core import ops

x = np.array([[1., 2., 3.],
              [1., 2., 3.]])

print(ops.softmax(x))
# I expect each row to sum to 1 (last-axis softmax), matching
# tf.nn.softmax / torch / scipy / jax behavior.
```

This is a footgun when migrating code — same call, silently different math. Would it make sense to align the default with the rest of the ecosystem so that `softmax(x)` / `log_softmax(x)` without an axis just does the obvious last-axis thing?
