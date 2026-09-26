# Problem Statement

Hey, I'm hitting a weird thing with `mockQuery` — if my query params include an array (like `{tags: ['a','b']}`), the mock never matches the request, even though I'm passing what looks like the exact same array on the other side. Plain string/number params work fine, it's specifically the array-valued ones that break. Would be great if `mockQuery` just matched when the arrays have the same items in the same order.

# Expected outcomes

- `mockQuery` should match requests whose query parameters include array values when the expected and actual arrays contain equivalent items in the same order.
- Array-valued query parameters should remain order-sensitive: the same items in a different order, or arrays of different lengths, should not be treated as equivalent.
- Equivalent array handling should work when array values appear inside ordinary query parameter objects, including nested values that are compared as part of deciding whether the query parameters match.
- Existing query parameter comparison behavior for plain string, number, boolean, and object values should be preserved, including not matching values that differ in kind or differ in any supplied object property.
- Any existing public equivalence helper used by this matching path should reflect the same observable matching semantics.

# Implementation notes

- The specific data structures, helper decomposition, type-checking approach, and validation locations are up to the implementer.
- Preserve the existing public API shape while adding correct handling for array-valued parameters.
