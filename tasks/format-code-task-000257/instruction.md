## `extra_ops.repeat` gives wrong shape when `repeats` is a vector and `axis=None`

I'm using `theano.tensor.extra_ops.repeat` to do the same thing as `numpy.repeat` — repeat each element of an array a (possibly different) number of times. When `repeats` is a 1D tensor and I don't pass `axis`, the inferred shape of the result comes out wrong.

Roughly what I'm doing:

```python
import numpy as np
import theano
import theano.tensor as T
from theano.tensor.extra_ops import repeat

x = T.dvector()
r = T.lvector()
y = repeat(x, r)         # no axis -> should behave like numpy.repeat(x, r)

f = theano.function([x, r], y.shape)
print f(np.array([1.0, 2.0, 3.0]), np.array([2, 3, 1]))
```

`numpy.repeat([1,2,3], [2,3,1])` returns a 1D array of length 6 (`2+3+1`), so I expect `y.shape` to be `(6,)` here. Instead the shape Theano infers doesn't match what `perform` actually produces, and downstream ops that rely on shape inference end up broken / mismatched against the real output.

The scalar-`repeats` case (e.g. `repeat(x, 3)` with no axis) and the case where `axis` is given both look fine — it's specifically the combination "`axis=None` + `repeats` is a vector" that's off. Could the shape inference for `repeat` be made consistent with `numpy.repeat` in that case too?
