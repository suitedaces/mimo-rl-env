## Problem Statement

I’m using MONAI and I’d like to track one of my loss functions the same way I track other metrics across validation iterations, but right now I have to write my own metric wrapper just to accumulate and aggregate it. It would be really helpful if MONAI had a generic metric for “use this loss function as a metric,” so I can plug in losses that take either predictions alone or predictions plus labels and then aggregate the results like the built-in metrics.

## Expected outcomes

- `monai.metrics.LossMetric` is available as a public metric wrapper that accepts a `loss_fn` callable and can be instantiated from `monai.metrics`.
- Calling `LossMetric(loss_fn=...)` during validation computes the loss for the current iteration, returns that iteration’s loss value, and records it so multiple iterations can later be aggregated.
- The wrapped loss callable works both when only `y_pred` is supplied and when both `y_pred` and `y` are supplied.
- Loss outputs that are scalar or one-dimensional tensors can still be used through `LossMetric` and aggregated consistently with MONAI’s batch-first metric behavior.
- `LossMetric.aggregate()` aggregates all recorded iteration losses using MONAI’s existing metric reduction modes.
- The reduction configured on `LossMetric` can be overridden for a single `aggregate(reduction=...)` call.
- When `LossMetric(get_not_nans=True)` is used, aggregation returns both the reduced metric value and the corresponding not-NaN count; otherwise aggregation returns only the metric value.
- Calling `aggregate()` before any iteration has been recorded returns a zero tensor value, and with `get_not_nans=True` returns zero tensor values for both outputs.
- The metrics documentation includes an API entry for `LossMetric`.

## Implementation notes

- Follow MONAI’s existing metric conventions for cumulative iteration metrics, reductions, reset behavior, tensors, and documentation style.
- The internal class organization, helper functions, validation location, and storage details are up to the implementer as long as the public behavior above is satisfied.
