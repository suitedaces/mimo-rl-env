# Problem Statement

I built Python from source on my server but forgot to install the xz/lzma dev headers first, and now `import pandas` blows up immediately with a `ModuleNotFoundError` about `lzma`. The thing is, my whole pipeline reads plain CSV and parquet files — I never touch xz-compressed data at all, so I don't get why a missing lzma module takes down the entire pandas import for me.

# Expected outcomes

- Import behavior without lzma:
  - If the standard-library `lzma` module is unavailable, `import pandas` should still complete successfully instead of failing with an import error.
  - During that import path, pandas should warn the user that lzma support is unavailable and that attempting to use lzma compression will fail later.

- Behavior when lzma/xz compression is actually requested:
  - If lzma support is unavailable and code attempts to use xz/lzma compression through pandas I/O, pandas should raise a `RuntimeError` indicating that the lzma module is not available.
  - The failure should be delayed until the xz/lzma functionality is used; users who only use non-xz formats should not be blocked from importing pandas.

- Behavior when lzma is available:
  - Existing xz/lzma compressed I/O should continue to work normally when the standard-library `lzma` module is present.
  - Non-xz I/O behavior should remain unaffected.

# Implementation notes

- Treat lzma as an optional runtime capability: importing pandas should not require it, but xz/lzma operations should still fail clearly when the capability is absent.
- The specific module organization, helper functions, and validation locations are up to the implementation, as long as the externally observable import, warning, error, and I/O behaviors above are satisfied.
