## Missing `lower` compute kernel for string arrays

I'm doing some text normalization on Arrow data with arrow2. A common preprocessing step is lowercasing every string in a column before doing comparison / dedup / grouping. Looking through `src/compute/` I see kernels like `length`, `substring`, `like`, `regex_match` etc. for string arrays, but there's no kernel that does case conversion.

I'd like to do something like:

```rust
use arrow2::array::Utf8Array;
// imagine some compute import here

let arr = Utf8Array::<i32>::from_slice(["Hello", "WORLD", "Rust"]);
let out = /* lowercase kernel */(&arr)?;
// out should contain "hello", "world", "rust"
```

Right now I have to drop out of the compute layer, iterate the array myself, build a new `Utf8Array`, and re-attach validity, which is annoying boilerplate that every user of this lib has to repeat.

Could we get a lowercase kernel added under `compute`, in the same style as the other string kernels? Specifically:

- works on `Utf8Array<i32>` and `Utf8Array<i64>` (i.e. both `Utf8` and `LargeUtf8`),
- takes `&dyn Array` so it fits the dynamically-typed compute API,
- preserves the input's null mask,
- returns an error for non-string input types instead of panicking,
- gated behind its own cargo feature, consistent with the per-kernel feature flags already in `Cargo.toml` (and pulled in by the umbrella `compute` feature).

Part of the broader effort to fill in the missing compute kernels.
