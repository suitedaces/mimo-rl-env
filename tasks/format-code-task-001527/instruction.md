# Add the InceptionNeXt model family

We'd like `timm` to ship the **InceptionNeXt** architecture
(*"InceptionNeXt: When Inception Meets ConvNeXt"*, https://arxiv.org/abs/2303.16900).

InceptionNeXt is a ConvNeXt-style hierarchical convolutional backbone whose token
mixer is an *Inception depthwise convolution*: the channels of each block are split
into groups that are processed by a small square depthwise conv, a 1×k band conv, a
k×1 band conv, and an untouched identity branch, then concatenated. Blocks follow the
MetaFormer recipe (token mixer → norm → channel MLP, residual, with a layer-scale
parameter), arranged into four sequential stages with a patchify stem.

Please implement it and register it as standard `timm` models so it works through the
usual public API (`timm.create_model`, `timm.list_models`, feature extraction, etc.).

## Required variants

Register at least these three named models, with the published per-stage
configurations:

| model name             | stage depths       | stage channel widths        |
|------------------------|--------------------|-----------------------------|
| `inception_next_tiny`  | (3, 3, 9, 3)       | (96, 192, 384, 768)         |
| `inception_next_small` | (3, 3, 27, 3)      | (96, 192, 384, 768)         |
| `inception_next_base`  | (3, 3, 27, 3)      | (128, 256, 512, 1024)       |

## Observable contract

Each registered variant must behave like a normal `timm` classification model:

- **Construction & listing.** It is discoverable via `timm.list_models('inception_next*')`
  and buildable with `timm.create_model(name, pretrained=False)`.
- **Classification forward.** Default `num_classes` is `1000`; a forward pass on an
  `[B, 3, H, W]` input returns a `[B, num_classes]` tensor (free of NaNs). Passing
  `num_classes=N` changes the output width to `N`, and `get_classifier()` returns the
  final classifier layer whose `out_features == N`.
- **Input channels.** `in_chans` is configurable (e.g. `in_chans=1` accepts single-channel input).
- **Stride / downsampling.** The backbone has four stages and a patchify stem giving a
  total spatial reduction of 32× (so a 224×224 input yields a 7×7 final feature map).
  `forward_features(x)` returns the *unpooled* 4-D `NCHW` feature map whose channel
  dimension equals `model.num_features`, which in turn equals the last stage's width
  (768 for tiny/small, 1024 for base).
- **Head / pooling control.**
  - `reset_classifier(0)` removes the classifier; a subsequent forward returns the
    globally-pooled 2-D tensor `[B, num_features]`.
  - `reset_classifier(0, '')` additionally disables global pooling; a forward then
    returns the unpooled 4-D feature map `[B, num_features, h, w]`.
  - Building with `num_classes=0, global_pool=''` produces the same unpooled 4-D output
    directly.
- **Feature extraction.** Building with `features_only=True` yields a model that returns
  the four stage outputs as a list. `feature_info.channels()` equals the stage widths
  from the table above and `feature_info.reduction()` equals `[4, 8, 16, 32]`; each
  returned feature map has the matching channel count and spatial reduction.
- **Default config.** `model.default_cfg` reports `num_classes == 1000` and
  `input_size == (3, 224, 224)`, and its `first_conv` and `classifier` entries name
  parameters that actually exist in the model's `state_dict`.
- **Trainability.** A backward pass through any variant produces gradients for every
  parameter.
