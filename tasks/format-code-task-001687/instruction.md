## Feature request: `keras.ops.unravel_index`

I'm writing backend-agnostic code on top of `keras.ops` so the same script runs on JAX, TensorFlow and PyTorch backends. A pretty common pattern I have is: flatten a tensor, find the index of the max (or top-k) with something like `keras.ops.argmax(x.reshape(-1))`, and then convert that flat index back to multi-dimensional coordinates inside the original tensor (e.g. to locate the peak in a 2D heatmap / attention map).

In plain NumPy I'd just do:

```python
import numpy as np
flat_idx = np.argmax(scores.ravel())
coords = np.unravel_index(flat_idx, scores.shape)   # tuple of per-axis coordinates
```

`keras.ops` already mirrors a lot of NumPy — `argmax`, `ravel`, `reshape`, etc. — but there doesn't seem to be an equivalent of `np.unravel_index`. Right now I have to drop down to the backend-specific API (or pull the tensor back to NumPy) just for this one step, which defeats the point of using `keras.ops` to stay backend-agnostic.

Could `keras.ops.unravel_index(indices, shape)` be added, with semantics matching `numpy.unravel_index` and support across all the backends keras.ops covers? Both scalar flat indices and arrays of flat indices should work, the same way NumPy handles them.
