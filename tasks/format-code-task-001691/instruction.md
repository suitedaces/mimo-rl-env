## `RootMeanSquaredError` metric is missing from `keras_core.metrics`

I'm porting a regression model from `tf.keras` to `keras_core` and one of
the metrics I use during training is RMSE. With `tf.keras` this is just:

```python
model.compile(
    optimizer="sgd",
    loss="mse",
    metrics=[tf.keras.metrics.RootMeanSquaredError()],
)
```

The equivalent in `keras_core` doesn't work:

```python
import keras_core

model.compile(
    optimizer="sgd",
    loss="mse",
    metrics=[keras_core.metrics.RootMeanSquaredError()],
)
```

it fails because `keras_core.metrics` doesn't expose `RootMeanSquaredError`.

Looking at `keras_core.metrics`, the other standard regression metrics are
already there — `MeanSquaredError`, `MeanAbsoluteError`,
`MeanAbsolutePercentageError`, `MeanSquaredLogarithmicError`,
`CosineSimilarity`, `LogCoshError` — but RMSE is the one that's missing.
For a lot of regression problems RMSE is the metric you actually report,
so having to roll my own stateful metric just to track it during
`model.fit` feels off when every sibling metric is provided out of the box.

Could `RootMeanSquaredError` be added under `keras_core.metrics` so it
behaves like the `tf.keras` one (accumulates across batches, supports
`sample_weight`, works inside `model.compile(metrics=[...])`)?
