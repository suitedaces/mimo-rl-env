## Problem Statement

I’m trying to wrap a JS API with an `@unboxed` untagged variant, and one of the cases needs to carry a `bool`, but `| Bool(bool)` doesn’t seem to work like `string` or `float` cases do. Could untagged variants treat boolean payloads as a real distinguishable JS `boolean` case too?

## Expected outcomes

- `@unboxed` untagged variants can include a constructor with a `bool` payload, such as `| Bool(bool)`, in the same way they can include other primitive payload cases.
- Pattern matching over such an untagged variant distinguishes JavaScript boolean values from other supported JavaScript value shapes at runtime.
- Boolean payload cases participate consistently in the untagged-variant validity rules: a single untagged variant definition must not contain more than one boolean-shaped case.
- If an untagged variant definition combines a `bool` payload case with boolean literal cases such as `@as(true)` or `@as(false)`, compilation should fail with a diagnostic explaining that only one boolean type case is allowed.

## Implementation notes

- The concrete compiler representation, validation location, and generated-code structure are left to the implementation.
- Preserve existing behavior for other untagged variant payload kinds and literal cases while adding boolean payload support.
