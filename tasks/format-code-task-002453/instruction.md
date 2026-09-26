# Problem Statement

When I composite scenes with `combine_metadata`, the merged `start_time` and `end_time` come out as the average of the inputs rather than the actual span. So for a stitched product I'd expect the start to be the earliest granule's start and the end the latest granule's end, but instead I get some mid-point timestamp that doesn't correspond to any real data boundary.

Also, some of my inputs have `start_time`/`end_time` set to `None` (sensors that don't always provide them), and those `None` values seem to break or pollute the merge instead of just being ignored.

Separately, when I run `StaticImageCompositor` on a static background image whose filename has no time info, the output ends up with `start_time`/`end_time` attributes set to the current wall-clock time. I never gave it a time, so I don't get where these timestamps are coming from.

# Expected outcomes

- Merged start and end time metadata should describe the full time span covered by the combined inputs: the start should come from the earliest valid input boundary, and the end should come from the latest valid input boundary.
- Missing or invalid time metadata values, including `None`, should not break the merge or be carried into the result as if they were valid times. If a time field has no valid time values to merge, it should be left out of the merged metadata.
- Existing behavior for non-boundary time metadata should be preserved: ordinary time-like metadata that is merged today by averaging should continue to produce an averaged valid time.
- Time-related metadata stored in nested time-parameter mappings should be merged consistently with the same boundary-vs-non-boundary semantics.
- The legacy `average_times` option should no longer allow callers to opt back into averaging start/end boundaries; callers that pass it should be notified that it is no longer the control for this behavior.
- `StaticImageCompositor` should not invent `start_time` or `end_time` values for static images that do not provide time information. Missing time metadata should remain missing or unset.

# Implementation notes

- Preserve the existing public API behavior of metadata merging outside the time-specific cases above.
- The exact internal structure, helper functions, and validation location are up to the implementation.
- Tests and callers should rely on externally observable metadata results and warnings, not on a particular internal helper or code path.
