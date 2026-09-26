## RandomToneCurve: float32 images aren't supported, and there's no per-channel mode

I'm building an augmentation pipeline for a model that consumes float32 images (values in `[0, 1]`). Most albumentations transforms (`RandomBrightnessContrast`, `HueSaturationValue`, etc.) handle float32 fine, but `RandomToneCurve` doesn't:

```python
import numpy as np
import albumentations as A

img = np.random.rand(256, 256, 3).astype(np.float32)
A.RandomToneCurve(scale=0.1, p=1.0)(image=img)
```

This raises an error complaining about the image dtype. I'd have to convert to uint8 just for this one transform and convert back, which is awkward in a `Compose` pipeline. Could `RandomToneCurve` (and the underlying `move_tone_curve`) support float32 the same way the other photometric transforms do?

While we're at it — currently `RandomToneCurve` samples one curve and applies the same remapping to every channel, so it only changes brightness/contrast, never color. For color-augmentation experiments (à la WB augmenter / "color constancy" style augmentation) it'd be really useful to have an option that samples an independent tone curve per channel, so the transform can also shift the color balance. The single-curve behavior should stay the default to keep existing pipelines reproducible.

It would also be nice if `move_tone_curve` didn't assume RGB/grayscale specifically — I sometimes work with 4-channel (RGBA) or multi-spectral images, and it'd be good if the same code path just worked for any number of channels.

I'd expect the new option to be exposed as something like a `per_channel` flag on `RandomToneCurve`.
