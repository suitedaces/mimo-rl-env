Sliding window inconsistency between PyTorch and Flax
### System Info

transformers main (ae49b218c), Python 3.10.8

### Who can help?

@ArthurZucker, @sanchit-gandhi

### Reproduction

The attention `sliding_window` has different interpretation for PyTorch and Flax. Here's are matching examples:

**PyTorch**

```python
from transformers import MistralModel
import torch

model = MistralModel.from_pretrained("hf-internal-testing/tiny-random-MistralModel", sliding_window=2)

inputs = {
  "input_ids": torch.tensor([[10, 20, 30, 40, 50, 60, 70, 80, 0, 0]]),
  "attention_mask": torch.tensor([[1, 1, 1, 1, 1, 1, 1, 1, 0, 0]])
}

outputs = model(**inputs)

print(outputs.last_hidden_state[:, 1:4, 1:4])
```

**Flax**

```python
from transformers import FlaxMistralModel
import jax.numpy as jnp

model = FlaxMistralModel.from_pretrained("hf-internal-testing/tiny-random-MistralModel", sliding_window=2, from_pt=True)

inputs = {
  "input_ids": jnp.array([[10, 20, 30, 40, 50, 60, 70, 80, 0, 0]]),
  "attention_mask": jnp.array([[1, 1, 1, 1, 1, 1, 1, 1, 0, 0]])
}

outputs = model(**inputs)

print(outputs.last_hidden_state[:, 1:4, 1:4])
```

Both snippets return different results, however, if we use `sliding_window=3` in the PyTorch version, the results are the same.

In the Flax implementation, `sliding_window=2` means that a position will attend to self, and two previous position inclusive (which intuitively seems correct to me). It looks like in the PyTorch version it is not inclusive. Which behaviour is expected?

### Expected behavior

The `sliding_window` meaning to be consistent.
