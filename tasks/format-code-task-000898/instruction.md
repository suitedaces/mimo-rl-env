# Add permutation and factorial helpers to the base utilities

The inference code is about to grow support for exploring label assignments over
small groups of variables, and for that it needs a couple of reusable
combinatorics helpers. Please add them to the project's **base** utility library
as free functions, exposed from a new header **`permutationsutil.h`**. Including
that header should be all a caller needs in order to use the functions — in
particular the `std::unordered_set<std::vector<int>>` type they operate on must
be usable as-is straight after the include.

Implement exactly these three functions:

### `void ComputeAllPermutations(std::vector<int> v, std::unordered_set<std::vector<int>>* permutations, size_t beam_size)`

- Enumerates permutations of `v` and adds them into `*permutations`. Because the
  destination is a set of vectors, only **distinct** arrangements are stored — if
  `v` contains repeated values, the arrangements that coincide collapse into one
  entry.
- When `beam_size` is large enough to hold them all, the set ends up containing
  **every** distinct permutation of `v` — that is `n!` arrangements when all
  values are distinct, and correspondingly fewer when some values repeat — and
  this includes `v`'s original arrangement.
- `beam_size` caps the work: generation halts as soon as the number of stored
  permutations exceeds `beam_size`, so the result never holds more than
  `beam_size + 1` entries. When `v` has at least `beam_size` distinct
  permutations, the set is filled up to the beam. Whatever entries were already
  present in `*permutations` on entry are preserved.

### `void ComputeRandomPermutations(std::vector<int> v, std::unordered_set<std::vector<int>>* permutations, size_t beam_size, size_t max_num_duplicates)`

- Repeatedly draws random permutations of `v` and inserts the distinct ones into
  `*permutations`, stopping when either `beam_size` distinct permutations have
  been collected, or `max_num_duplicates` already-seen permutations have been
  drawn. The duplicate limit is a termination guard: it ensures the call returns
  even when `v` has fewer than `beam_size` distinct permutations.
- The result holds at most `beam_size` entries, every one a permutation of `v`.
  When `beam_size` is at least the number of distinct permutations of `v`, the
  set ends up containing all of them.

### `uint64 CalculateFactorial(int n)`

- Returns `n!`. If the true value would not fit in a `uint64`, it returns
  `(uint64)-1` as an overflow sentinel instead of a wrapped-around result.
  (`uint64` is the project's unsigned 64-bit integer type.)
