## `predict_batch` returns wrong results when given a batch of images

I'm trying to speed up inference by running prediction on a stack of images
at once instead of looping over them in Python. I have a bunch of pre-processed
image tensors stacked into shape `(B, C, H, W)` and I'm calling:

```python
from deepforest import main
import torch

model = main.deepforest()
model.load_model("weecology/deepforest-tree")

# images: a torch.Tensor of shape (B, C, H, W), already preprocessed
results = model.predict_batch(images)
```

I expected `results` to be a list of length `B`, where `results[i]` is the
predictions for `images[i]` — basically the per-image equivalent of what I get
when I call the single-image prediction APIs.

What I actually get back doesn't line up with the input batch. With a batch
of e.g. 4 images I'm not getting 4 sensible per-image dataframes — the count
is off and the contents look duplicated / not matching the corresponding input.
On top of that the call isn't really any faster than just calling prediction
in a Python `for` loop over the images, which kind of defeats the point of
having a batch entry point.

It would be great if `predict_batch` actually ran the batch through the model
in one shot and returned one prediction dataframe per input image, with the
same format/columns as the other `predict_*` methods so I can downstream them
the same way.
