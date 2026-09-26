`lightning_getattr` should raise `AttributeError`
## 🚀 ~Feature~ Enhancement
Currently, `lightning_getattr(model, attribute)` raises one of `(ValueError, KeyError, AttributeError` when `attribute` is not found in `model`, but I think it should raise `AttributeError` in all cases since Python built-in `getattr()` only raises `AttributeError`.

https://github.com/PyTorchLightning/pytorch-lightning/blob/4bdf2fe55f45c4cc8b397d4b45041265c402519f/pytorch_lightning/utilities/parsing.py#L241
