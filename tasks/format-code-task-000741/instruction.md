# Problem Statement

I’m using Cython with C++20/23 code and keep having to write little wrappers because `libcpp` doesn’t expose things like `std::gcd`/`std::lcm`, container `.contains()`, or `std::string` helpers like `starts_with`, `ends_with`, and `contains`. It would be really nice if I could just cimport/use these standard library APIs directly from Cython.

# Expected outcomes

- Cython C++ code can cimport and call modern numeric helpers from `libcpp.numeric`, including `gcd`, `lcm`, and `midpoint`, with the corresponding standard-library behavior.
- The standard ordered and unordered associative containers exposed by `libcpp` support their C++ membership query through `.contains(...)`, returning whether the requested key or value is present.
- `libcpp.string.string` supports the standard prefix, suffix, and substring-style helpers `starts_with(...)`, `ends_with(...)`, and `contains(...)` for normal Cython byte/character string inputs, returning the corresponding boolean result.

# Notes

These APIs should be available through normal Cython `cimport` usage in C++ mode and should work under the appropriate C++ standard level for the underlying standard-library feature.
