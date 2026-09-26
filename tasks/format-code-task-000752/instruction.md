When I call `dask.array.from_array()` on a large `numpy.memmap`, Dask seems to touch the whole mapped file while just building the graph, and on big files it can blow up memory before any computation starts. Could this avoid reading the memmap contents during tokenization and just treat it like a disk-backed array?

Expected outcomes:
- `dask.base.tokenize(...)` handles `numpy.memmap` inputs without materializing or hashing the full mapped array contents.
- `dask.array.from_array(...)` can build a graph from a large `numpy.memmap` without paging the whole backing file into memory during graph construction.
- Tokens for file-backed memmaps reflect the backing file and array/view metadata rather than only the array values, so distinct backing files, changed backing-file metadata, or distinct file-backed views are not accidentally treated as the same object just because their contents match.
- Tokenization remains deterministic for the same file-backed memmap metadata across independent openings.
- Existing tokenization behavior for ordinary in-memory NumPy arrays remains unchanged.

Implementation notes:
- The concrete token representation, metadata collection strategy, and validation location are up to the implementer.
- The solution should preserve Dask’s public tokenization semantics while avoiding content reads specifically for disk-backed memmap arrays.
