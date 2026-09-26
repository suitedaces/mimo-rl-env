I need a `deepdow.experiments.History` object for experiment logging.

`History()` should start empty, and `add_entry(...)` should append one row per call with the fields `model`, `metric`, `value`, `batch`, `epoch`, `dataloader`, `lookback`, `timestamp`, and `current_time`. If I omit `value`, it should default to `NaN`.

`metrics_per_epoch(epoch)` should return a pandas DataFrame for that epoch, and asking for an unknown epoch should raise `KeyError`. `metrics` should return a pandas DataFrame that concatenates every stored row across all epochs.

`pretty_print(epoch=None)` should print mean `value` grouped by `model`, `metric`, `epoch`, and `dataloader`; when `epoch` is `None`, it should use all stored epochs, and when an epoch is provided, it should only use that one.

Repeated `add_entry` calls should accumulate history instead of replacing earlier rows.
