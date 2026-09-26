## `linspace` is missing from `cubed.array_api`

I'm trying to generate an evenly-spaced sequence with a fixed number of points (typical use cases: axis coordinates, sampling grids), and reached for `linspace` since it's part of the standard Array API:

```python
import cubed.array_api as xp

xs = xp.linspace(0.0, 1.0, 50)
```

But `linspace` doesn't exist on `cubed.array_api`. Looking at the API coverage table in `api_status.md`, it's listed under Creation Functions but the "Implemented" column is empty (it's flagged as difficulty 2, "Like `arange`").

`arange` works fine for stepping by a known increment, but it's awkward when what I actually want is "give me exactly N points between a and b" — that's what `linspace` is for, and it's also what the spec requires.

Could `linspace` be implemented so cubed's array API surface matches the standard? It would be nice to have it behave consistently with the numpy/dask version when running large lazy arrays.
