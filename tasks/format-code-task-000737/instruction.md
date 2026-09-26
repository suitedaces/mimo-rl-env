**Problem Statement**

I’m trying to use CuPy sparse matrices the same way I use SciPy, where I can create an empty CSR or CSC matrix just by passing a shape, but `cupy.sparse.csr_matrix((m, n))` and `csc_matrix((m, n))` don’t seem to accept that. It would be really helpful if those constructors could handle a shape-only empty matrix, including when I pass a dtype.

**Expected Outcomes**
- `cupy.sparse.csr_matrix((M, N))` accepts a two-dimensional shape tuple and creates an empty CSR matrix with shape `(M, N)`.
- `cupy.sparse.csc_matrix((M, N))` accepts a two-dimensional shape tuple and creates an empty CSC matrix with shape `(M, N)`.
- When no `dtype` is supplied for this shape-only form, the resulting empty CSR or CSC matrix defaults to `float64`.
- When a `dtype` is supplied for this shape-only form, the resulting empty CSR or CSC matrix preserves that dtype.
- The documented constructor forms for these APIs include shape-only empty-matrix construction, including `csr_matrix((M, N), [dtype])` and `csc_matrix((M, N), [dtype])`.

**Implementation Notes**

Any implementation that preserves the current sparse matrix API and makes the public constructor behavior match these outcomes is acceptable. The exact validation flow, helper structure, and internal sparse-storage construction strategy are left to the implementer.
