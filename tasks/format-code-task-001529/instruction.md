## TF OpenAI GPT model fails under mixed precision (AMP) and XLA

I'd like to train/run `TFOpenAIGPTModel` (and `TFOpenAIGPTForSequenceClassification`) with mixed precision and/or XLA, both of which work fine on most other TF models in this repo. With OpenAI GPT specifically, neither works.

### AMP (mixed precision)

Minimal repro:

```python
import tensorflow as tf
from transformers import TFOpenAIGPTModel, OpenAIGPTConfig

tf.keras.mixed_precision.set_global_policy("mixed_float16")

config = OpenAIGPTConfig()
model = TFOpenAIGPTModel(config)

input_ids = tf.constant([[1, 2, 3, 4, 5]])
out = model(input_ids)  # blows up with a dtype mismatch
```

Other TF models in `transformers` run end-to-end under the `mixed_float16` policy, so I'd expect this one to as well.

### XLA

Same story when I try to compile the sequence classification head with XLA:

```python
import tensorflow as tf
from transformers import TFOpenAIGPTForSequenceClassification, OpenAIGPTConfig

config = OpenAIGPTConfig(pad_token_id=0, num_labels=2)
model = TFOpenAIGPTForSequenceClassification(config)

@tf.function(jit_compile=True)
def run(x):
    return model(x).logits

run(tf.constant([[1, 2, 3, 0, 0], [4, 5, 6, 7, 0]]))
```

This fails to compile under XLA, while eager / non-jit calls work fine.

### Expected

Both AMP and XLA should work for the TF OpenAI GPT models, the same way they do for the other TF model families in this repo. Could the OpenAI GPT TF implementation be made AMP- and XLA-compliant? Happy to help test.
