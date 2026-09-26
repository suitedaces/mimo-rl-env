## i32 encode/decode helpers in `api` package are incomplete / asymmetric

I'm embedding wazero and writing some host functions. To pass values to/from the `[]uint64` stack, the `api` package exposes encode/decode helpers — but the coverage across value types is inconsistent.

For 64-bit integers and both float types I get a clean pair:

- `api.EncodeI64` / `api.DecodeI64`
- `api.EncodeF32` / `api.DecodeF32`
- `api.EncodeF64` / `api.DecodeF64`
- `api.EncodeExternref` / `api.DecodeExternref`

But for `ValueTypeI32` there is only `api.EncodeI32` (for `int32`). There's no decode counterpart, and nothing at all for `uint32` in either direction. So every time I touch an i32 parameter or result on the stack I end up writing the cast inline, e.g.

```go
func myHostFn(ctx context.Context, stack []uint64) {
    offset := uint32(stack[0])          // decode uint32 by hand
    someInt32Param := int32(stack[1])   // decode int32 by hand

    ret := doWork(offset, someInt32Param)

    stack[0] = uint64(ret)              // encode uint32 result by hand
}
```

This is awkward for a couple of reasons:

1. It's inconsistent with how the docs steer you for the other value types — for `f32/f64/i64/externref` the message is "use the api helpers", but for `i32` you're silently expected to roll your own cast.
2. The `int32 → uint64` direction is easy to get subtly wrong. A naive `uint64(myInt32)` does a sign-extending conversion, which is *not* what you want when stuffing the value into the i32 slot of a `uint64` stack — you have to remember to go through `uint32` first (`uint64(uint32(myInt32))`). That's exactly the kind of thing a helper should hide; otherwise every embedder has to learn this trap independently.

Could the `api` package round out the i32 helpers so they mirror the other value types (encode + decode, for both signed and unsigned 32-bit ints)? Then host function authors can just call the helpers uniformly across all `ValueTypeXxx` without having to reason about which conversions are safe to write inline.
