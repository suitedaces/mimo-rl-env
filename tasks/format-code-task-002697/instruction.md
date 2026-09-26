# Problem Statement

Right now when I call `stack.apply(func, ...)` the only choice I get is `is_volume` — either it runs my function on 2D (Y,X) tiles or on the whole 3D (Z,Y,X) volume. But I've got cases where I want to process across other axes, like running something per-channel or over some other subset of axes, and there's just no way to express that with a boolean flag. Could `apply` let me actually specify which axes to split on instead of being locked into just tile vs. volume?

# Expected outcomes

- `ImageStack.apply` should expose a public axis-selection keyword, `split_by`, that lets callers specify the set of image axes that each invocation of the supplied function should receive, rather than exposing only a tile-versus-volume boolean choice.
- Calling `ImageStack.apply` with axes corresponding to 2D planes should preserve the existing per-plane behavior, and calling it with axes corresponding to 3D volumes should preserve the existing per-volume behavior.
- Calling `ImageStack.apply` with another valid subset of axes should apply the function over subarrays shaped by that subset, while iterating over the remaining axes.
- Existing image filters that expose an `is_volume` option should continue to support their public `is_volume=True` and `is_volume=False` behavior after the generalized `apply` API is introduced.
- Existing higher-level image operations that relied on the previous plane-wise default behavior should continue to produce the same public behavior unless they explicitly opt into a different axis selection.

# Implementation notes

- The exact internal representation of the axis set, how it is validated, and where compatibility mapping is performed are implementation details.
- Preserve existing public behavior for callers that still use higher-level filters with `is_volume`; the generalized axis selection should not force those filters to expose a new API.
- Prefer behaviorally compatible changes over duplicating any particular internal organization.
