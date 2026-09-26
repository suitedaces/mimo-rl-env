## Problem Statement

I'm using `mat64.Dense` and getting weird values when I do element-wise ops in place, like `d.Sub(d, b)` or `d.MulElem(a, d)`; it feels like the result is getting clobbered when the output is also one of the inputs. I also hit a similar-looking issue with `Scale` and `Apply` when I pass a transposed Dense view from `a.T()` — the output looks like it's reading the original layout, and `Apply` seems to get the wrong row/col/value. Can you make these work correctly for in-place element-wise calls and transposed Dense inputs?

## Expected outcomes

- In-place element-wise arithmetic: `(*Dense).Sub`, `(*Dense).MulElem`, and `(*Dense).DivElem` should produce the same element-wise results when the receiver aliases either input as they do when writing into a separate output matrix.
- Subtraction aliasing: `(*Dense).Sub(a, b)` should leave the receiver containing the element-wise values of `a - b`, including when the receiver is also `a` or also `b`.
- Element-wise multiplication aliasing: `(*Dense).MulElem(a, b)` should leave the receiver containing the element-wise values of `a * b`, including when the receiver is also `a` or also `b`.
- Element-wise division aliasing: `(*Dense).DivElem(a, b)` should leave the receiver containing the element-wise values of `a / b`, including when the receiver is also `a` or also `b`.
- Transposed Dense inputs: `(*Dense).Scale(f, a.T())` should size and populate the receiver as the logical transpose of `a` scaled by `f`, not as the original untransposed layout.
- Transposed Dense callbacks: `(*Dense).Apply(fn, a.T())` should traverse the logical transposed matrix, and each callback invocation should receive row, column, and value arguments matching that logical transposed view.

## Implementation notes

Keep the existing public API shape and existing behavior for non-aliasing, non-transposed inputs. The specific internal traversal strategy, temporary storage choices, and validation locations are implementation details, as long as the observable matrix dimensions, element values, and callback arguments match the behaviors above.
