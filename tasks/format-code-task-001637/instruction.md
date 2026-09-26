## Problem Statement

I’m parsing some `.proto` files with `desc/protoparse` and it chokes on numeric option values that `protoc` accepts, like `08`/`09` and a huge float literal such as `1e10000`. I first thought I had a bad option value somewhere, but the same files compile with `protoc`, so it looks like protoparse is rejecting these number literals differently.

## Expected outcomes

- Numeric option values such as `08` and `09` are accepted when parsing `.proto` input through `desc/protoparse`, and their parsed values match the corresponding decimal values.
- Existing accepted numeric literal behavior is preserved for unrelated numeric forms.
- Positive numeric option values that `protoc` accepts even though they overflow the finite floating-point range, such as `1e10000`, are accepted and represented as positive infinity.

## Implementation notes

The fix should preserve existing parsing behavior for unrelated numeric syntax and error cases. The exact parsing structure, helper functions, and validation location are implementation details; ensure the externally observable behavior of `.proto` parsing matches the outcomes above.
