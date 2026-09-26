## Resuming training is broken, and the default `dtype` won't even let me construct a config

I'm trying to spin up an SAE training run with SAELens for the first time and ran into two issues that look like bugs.

### 1. Default `LanguageModelSAERunnerConfig()` doesn't construct

Minimal repro:

```python
from sae_lens.training.config import LanguageModelSAERunnerConfig

cfg = LanguageModelSAERunnerConfig()
```

This blows up inside `__post_init__` — the string default the dataclass ships with for `dtype` doesn't match anything in the `DTYPE_MAP` lookup, so the validator immediately rejects it. The same thing happens for `CacheActivationsRunnerConfig()`.

So you can't actually instantiate either config without passing `dtype=` explicitly. That seems wrong — the default value of a field should at minimum pass the config's own validation.

### 2. Resuming from a checkpoint with `resume=True` is broken

I had a longer training run that died partway, so I wanted to pick it back up from the latest checkpoint. The obvious way to do that, based on the field name, is:

```python
cfg = LanguageModelSAERunnerConfig(
    ...,
    checkpoint_path="checkpoints/<run-id>",
    resume=True,
)
language_model_sae_runner(cfg)
```

This does not work — the resume codepath fails somewhere down inside the runner, and from a user's perspective there's no clear signal about what's wrong or what I'm supposed to do instead. I poked around and noticed there's a separate `from_pretrained_path` field that seems related, but it isn't really documented as the way to continue a training run, and it isn't obvious whether `resume=True` is supposed to work, supposed to be deprecated, or just buggy.

If `resume=True` is no longer the supported way to continue training, I'd expect the runner (or the config) to fail fast with a clear message that points me at whatever the supported alternative is, instead of crashing partway through setup. If it *is* supposed to work, then it should actually pick up from the last checkpoint.

Either way, the current behavior is pretty confusing for someone trying to use this for the first time. Could the `resume` story be cleaned up so users get a sensible result (or a clear error telling them what to do) when they set `resume=True`?
