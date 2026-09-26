### Calling `NpyIter_GetIterNext` from Cython via the bundled numpy pxd doesn't work

I'm trying to use NumPy's NpyIter C API from a Cython extension to iterate over an ndarray efficiently. The standard idiom (straight out of the NumPy C-API docs) is to grab an `iternext` function via `NpyIter_GetIterNext` and call it in a loop.

Minimal repro (`demo.pyx`):

```cython
# cython: language_level=3
cimport numpy as cnp
from numpy cimport (
    NpyIter, NpyIter_AdvancedNew, NpyIter_GetIterNext,
    NpyIter_Deallocate, NPY_KEEPORDER, NPY_NO_CASTING,
)
from libc.stdio cimport printf

def run(cnp.ndarray a):
    cdef NpyIter* it
    cdef char* errmsg = NULL
    cdef cnp.PyArrayObject* ops[1]
    ops[0] = <cnp.PyArrayObject*>a

    it = NpyIter_AdvancedNew(1, ops, 0, NPY_KEEPORDER, NPY_NO_CASTING,
                             NULL, NULL, 0, NULL, NULL, 0)
    iternext = NpyIter_GetIterNext(it, &errmsg)
    while iternext(it):
        pass
    NpyIter_Deallocate(it)
```

Building this with `cythonize -i demo.pyx` (Cython 3.x) fails — Cython doesn't accept calling the result of `NpyIter_GetIterNext` as a function. If I look at what `from numpy cimport NpyIter_GetIterNext` actually pulls in from the numpy pxd, the return type isn't quite what I'd expect for a function-pointer-returning C function, and Cython refuses to let me invoke it.

The same pattern in plain C works fine — `NpyIter_IterNextFunc *iternext = NpyIter_GetIterNext(iter, NULL); while (iternext(iter)) { ... }`. So the C API is fine; it's the Cython declaration that's getting in the way. Same problem with `NpyIter_GetGetMultiIndex`.

Could the declarations in `numpy/__init__.pxd` / `numpy/__init__.cython-30.pxd` be made usable from Cython so that the returned `iternext` / `get_multi_index` can be called directly the way the C API documents them? Right now there's no way (that I can find) to drive NpyIter from Cython using the shipped pxd.
