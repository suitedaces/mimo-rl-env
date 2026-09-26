## `CoarseDropout` ignores the new `*_range` parameters

I've been migrating my pipeline to the new range-style API of `CoarseDropout` since the docs say `min_holes`/`max_holes`/`min_height`/`max_height`/`min_width`/`max_width` are deprecated and we should use `num_holes_range`, `hole_height_range`, `hole_width_range` instead.

Here's roughly what I'm doing:

```python
import albumentations as A
import numpy as np

img = np.zeros((256, 256, 3), dtype=np.uint8) + 255

aug = A.CoarseDropout(
    num_holes_range=(4, 8),
    hole_height_range=(20, 40),
    hole_width_range=(20, 40),
    p=1.0,
)

out = aug(image=img)["image"]
```

I expected to get somewhere between 4 and 8 dropout regions, each roughly 20-40 px in width and height. What I actually see is just a single small hole around 8x8 pixels, the same as if I hadn't passed any range at all. Increasing the values in the `*_range` tuples makes no difference — the output looks identical.

Inspecting the transform after construction confirms it:

```python
print(aug.num_holes_range, aug.hole_height_range, aug.hole_width_range)
# (1, 8) (8, 8) (8, 8)   <- not what I passed in
```

So the new-style parameters seem to be silently overridden by something during init. This basically means there is no way to actually use the non-deprecated API right now — everyone gets the default 8×8 single-hole behavior regardless of what they pass.

Passing the deprecated `max_holes` / `max_height` / `max_width` still works as before, but the whole point of the new `*_range` parameters is to be the path forward, so they should actually take effect when the user provides them.
