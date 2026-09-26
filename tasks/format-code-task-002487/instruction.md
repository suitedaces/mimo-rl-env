## `use_lstm: True` doesn't work with a custom model on a Dict observation space

I'm training on a custom env whose observation space is a `gym.spaces.Dict` (a few named sub-fields). I have a `custom_model` registered via `ModelCatalog.register_custom_model(...)` that knows how to consume that dict observation and produce a feature vector. I'd like to stack an LSTM on top of it, so my model config looks roughly like:

```python
config = {
    # ...
    "model": {
        "custom_model": "my_model",
        "use_lstm": True,
        "max_seq_len": 20,
        "lstm_cell_size": 256,
    },
}
```

Running this immediately blows up at agent setup / first train iteration — the run never gets past initialization.

What does work in isolation:

- Same `custom_model` with `use_lstm: False` and the same Dict observation space — trains fine.
- `use_lstm: True` (no custom model, just the built-in network) on an env with a plain `Box` observation space — trains fine.

It's specifically the combination of **custom model + `use_lstm: True` + Dict (non-flat) observation space** that breaks.

Expected behavior: this combo should work, i.e. the LSTM should wrap the custom model's output the same way it does on top of the built-in networks for flat observations, regardless of whether the underlying env's observation space is a Dict (or Tuple).
