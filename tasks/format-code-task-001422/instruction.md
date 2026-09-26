Support `nbytes` attribute from NumPy
Enhancement request: support the `nbytes` attribute from NumPy arrays.

Currently, in order to get the approximate size of a h5py dataset, you have to do something like:
```
dset.size * np.dtype(dset.dtype).itemsize
```
Where as with NumPy arrays, you can directly access this value by:
```
arr.nbytes
```
It'd be much more convenient if this could be wrapped into `h5py`'s datasets as well.
Thanks!
