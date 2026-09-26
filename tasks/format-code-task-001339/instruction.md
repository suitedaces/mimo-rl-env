# Fix packed-struct lowering for opaque-pointer kernels

The `rewrite-packed-structs` transformation is responsible for reducing the
alignment of packed structures that are used as kernel buffer arguments, so
that the buffer can later be emitted with a layout Vulkan accepts. It does this
by treating the packed structure as a flat byte buffer.

This works for kernels written with typed pointers, but it is effectively
broken once the IR uses opaque pointers (`ptr`): for those kernels the
transformation currently bails out and leaves the packed-struct accesses
untouched. Consider a kernel that indexes a packed-struct buffer by the global
id:

```llvm
%struct = type <{ i32, i16 }>

define spir_kernel void @test(ptr addrspace(1) nocapture %in) {
  %1 = call spir_func i32 @_Z13get_global_idj(i32 0)
  %2 = getelementptr inbounds %struct, ptr addrspace(1) %in, i32 %1
  store %struct <{ i32 2100483600, i16 127 }>, ptr addrspace(1) %2
  ret void
}
```

Nothing is lowered here, which leads to wrong layouts and broken downstream
indexing.

Make the transformation handle opaque-pointer kernels. When it runs on a kernel
that addresses a packed structure through a `getelementptr`, it must rewrite
that access so that it operates on a byte-array equivalent of the packed
structure instead of on the structure type itself. Specifically:

- The equivalent type the access is performed on must be an `i8` array whose
  length equals the structure's allocation size (e.g. a `<{ i32, i16 }>`, which
  is 6 bytes, becomes a 6-element `i8` array; a `<{ i32, i8 }>`, which is 5
  bytes, becomes a 5-element `i8` array). The array may be wrapped in a struct.
- The original element index must be preserved exactly as the outermost index
  of the rewritten access, whether it is a dynamic value (such as the global
  id) or a constant. The byte-array element size means the per-element stride
  stays equal to the structure's allocation size.
- The buffer argument itself must continue to be addressed directly; the
  transformation must not redirect accesses through a private copy of the data.

Kernels that do not address a packed structure must be left unchanged.
