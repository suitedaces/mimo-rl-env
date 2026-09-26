Change `dims` keyword of sum functions to `dim`
I have come across a case where linopy does not adhere to the naming of xarray and this problem can only be solved with an unnecessary type check. Here is a short linear equation that should work with both pure xarray instances and a xarray/linopy mix.

For this let $$func(A,x,\tilde x) = A^T(x-\tilde x) = A^Tx - A^T\tilde x = u$$

where
- $A \in \mathbb{R}^n \times \mathbb{R}^m$ is some (xarray) data matrix
- $\tilde x \in \mathbb{R}^n$ is a (xarray) data array
- $x \in \mathbb{R}^n$ is **EITHER** a (linopy) variable **OR** a (xarray) data array
- $u \in \mathbb{R}^m$ is the result.

The following minimal example shows that a type check must be made in the implementation of $func$. The reason for this is only the different naming of `dim` and `dims`:

```python
import linopy
import xarray as xr


def func(A, x, x_tilde):
    tmp = A * x - A * x_tilde
    if type(tmp) == xr.DataArray:
        return tmp.sum(dim="X")
    return tmp.sum(dims="X")


dimX = xr.DataArray(["x1", "x2", "x3"], dims=["X"])
dimU = xr.DataArray(["u1", "u2", "u3", "u4"], dims=["U"])
A = xr.DataArray(
    [[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3]],
    coords={"X": dimX, "U": dimU},
)
x_tilde = xr.DataArray([10, 20, 30], dims=["X"])

x_as_variable = linopy.Model().add_variables(coords=[dimX])
x_as_value = xr.DataArray([1, 2, 3], coords=[dimX])

print(func(A, x_as_variable, x_tilde))
print("===")
print(func(A, x_as_value, x_tilde))
```

with the expected output

```
LinearExpression (U: 4):
------------------------
[u1]: +1 var0[x1] + 2 var0[x2] + 3 var0[x3] - 140
[u2]: +1 var0[x1] + 2 var0[x2] + 3 var0[x3] - 140
[u3]: +1 var0[x1] + 2 var0[x2] + 3 var0[x3] - 140
[u4]: +1 var0[x1] + 2 var0[x2] + 3 var0[x3] - 140
===
<xarray.DataArray (U: 4)>
array([-126, -126, -126, -126])
Coordinates:
  * U        (U) <U2 'u1' 'u2' 'u3' 'u4'
```

In my opinion the `dims`keyword should be renamed to `dim`. Of course this is a breaking change, but with a `DeprecationWarning` in the long and an alias in the short run this should be no problem.

I'm happy to submit a PR if this is something worth doing.
