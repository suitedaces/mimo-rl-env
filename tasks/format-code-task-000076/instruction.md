## `color_deconvolution` fails when passing a stain matrix with only two stains

The docstring of `color_deconvolution` says:

> For two stain images the third column is zero and will be complemented using cross-product. At least two of the three columns must be non-zero.

So I expected that I could just give it the two stain vectors I care about (e.g. hematoxylin and eosin) and let the function fill in the residual third stain itself.

What I actually tried:

```python
import numpy as np
from histomicstk.preprocessing.color_deconvolution import color_deconvolution

# only the two stains I'm interested in (H and E), as columns
w = np.array([
    [0.650, 0.072],
    [0.704, 0.990],
    [0.286, 0.105],
])

Stains, StainsFloat, Wc = color_deconvolution(im_rgb, w)
```

This blows up inside `color_deconvolution` — it clearly assumes `w` already has three columns and tries to look at the third one directly, so a 3x2 input never gets a chance to be complemented.

The only way I've found to make it work is to manually pad `w` with a zero column before calling the function:

```python
w3 = np.zeros((3, 3))
w3[:, :2] = w
color_deconvolution(im_rgb, w3)   # works, third stain gets filled in
```

But based on the docstring (and the fact that `complement_stain_matrix` already handles building the residual stain) I'd expect passing a 3x2 matrix directly to just work — i.e. the function should accept a stain matrix that contains only the two real stain columns and complement the missing one on its own.
