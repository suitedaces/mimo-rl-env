## Problem Statement

I'm hitting an issue with `chainercv.transforms.resize` on CHW grayscale images: when I pass a NumPy array shaped like `(1, H, W)`, the result seems to get squeezed into 2D or sometimes errors out. In my no-`cv2` setup I also noticed non-RGB inputs behave oddly, like a 1-channel image failing and extra channels disappearing.

## Expected outcomes

- Grayscale CHW inputs passed to `chainercv.transforms.resize` should resize successfully and preserve their single channel dimension, returning an array shaped `(1, new_H, new_W)`.
- When `chainercv.transforms.resize` runs without `cv2` available, non-RGB CHW inputs should resize according to their actual number of channels rather than assuming exactly three channels.
- The resized output should preserve the input channel count for both fewer-than-three-channel and more-than-three-channel inputs in the no-`cv2` fallback path.
- Resizing should operate on the image data in the preserved channels rather than replacing valid non-constant input with a constant placeholder.
- Existing RGB CHW resize behavior should continue to return the expected channel-first shape.

## Implementation notes

- The implementation may choose any appropriate internal handling for channel order, backend-specific image resizing behavior, and per-channel processing, as long as the public resize behavior above is satisfied.
- Keep the public API behavior centered on `chainercv.transforms.resize`; no particular private helper structure or internal code organization is required.
