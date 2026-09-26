Examples: `8.6` (Ampere), or `8.9` (Ada Lovelace), etc.

This is important, for example, when you want to run something using Flash Attention 2 (used by TGI) that requires Ampere or higher.

I'd expect to be able to specify this via a new `compute_capability` field on the GPU spec, accepting forms like `7.5`, `"7.5"`, or `(7, 5)`.
