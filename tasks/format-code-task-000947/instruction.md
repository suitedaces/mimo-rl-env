# Problem Statement

I’m checking whether an FFI memory object has a size limit, and I noticed `FFI::Pointer.new(0).size_limit?` works but `FFI::MemoryPointer.new(:int, 10).size_limit?` blows up with `NoMethodError`, even though both are memory objects I’m handling the same way.

# Expected outcomes

- `size_limit?` is available as a public query on supported FFI memory objects, including `FFI::MemoryPointer` instances.
- Calling `size_limit?` on supported FFI memory objects returns a boolean value and does not fail because the method is missing.
- Bounded memory objects, such as allocated memory pointers, report that they have a size limit.
- Unbounded pointer-style memory objects, such as `FFI::Pointer.new(0)`, report that they do not have a size limit.
- Code using the public FFI Ruby API can rely on the same `size_limit?` query across supported Ruby implementations.

# Implementation notes

- The specific implementation location and internal structure are up to the implementer, as long as the public FFI memory-object behavior above is satisfied.
- Preserve existing `FFI::Pointer` behavior while making the size-limit query consistently available to other relevant FFI memory objects.
