## `einsum` fails when input arrays have different dtypes

I'm running into an issue when calling `geomstats.backend.einsum` with arrays of different dtypes. For example, mixing an integer array with a float array (a common case when one of them is built from indices and the other from coordinates) blows up the call instead of just doing the contraction.

A minimal reproducer:

```python
import geomstats.backend as gs

a = gs.array([1, 2, 3])           # ends up as an int dtype
b = gs.array([1.0, 2.0, 3.0])     # float dtype

gs.einsum('i,i->', a, b)
```

This fails on at least the pytorch and tensorflow backends. The numpy backend behaves a bit differently but is still inconsistent across backends.

I'd expect `einsum` to "just work" for mixed-dtype inputs the way numpy's own `np.einsum` mostly does — i.e. the user shouldn't have to manually cast every operand to a common dtype before calling it. This shows up all over the place in higher-level code that combines tensors coming from different sources, and having to sprinkle `gs.cast(...)` at every call site is pretty painful.

Could `einsum` be made to handle inputs of differing dtypes consistently across all backends?

Related to #769.

It would also be nice if the dtype-widening logic was exposed as a small public helper on the backend (something like `gs.convert_to_wider_dtype(tensor_list)`) so user code can reuse it directly instead of re-implementing it at every call site.
