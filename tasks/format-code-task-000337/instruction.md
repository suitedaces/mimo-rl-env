[BUG] Resize with 2D masks crashes
Additional target in Resize fails.

```python
import numpy as np
import albumentations as A

image = np.zeros((256, 256, 3), dtype=np.uint8)
mask = np.ones((256, 256), dtype=np.uint8)  # 2D mask

transform = A.Compose(
    [
        A.Resize(height=512, width=512),  # Resize image + mask
    ],
    additional_targets={"semantic_mask": "mask"},
)

augmented = transform(image=image, semantic_mask=mask)
print(augmented["semantic_mask"].shape)
```

generates error:
```
  File "C:\Users\aselimc\micromamba\envs\dinov3\Lib\site-packages\albumentations\augmentations\geometric\resize.py", line 833, in apply_to_mask
    return fgeometric.resize(mask, (self.height, self.width), interpolation=interpolation)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\aselimc\micromamba\envs\dinov3\Lib\site-packages\albucore\decorators.py", line 42, in wrapped_function
    result = func(img, *args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\aselimc\micromamba\envs\dinov3\Lib\site-packages\albumentations\augmentations\geometric\functional.py", line 261, in resize
    return resize_cv2(img, target_shape, interpolation)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\aselimc\micromamba\envs\dinov3\Lib\site-packages\albumentations\augmentations\geometric\functional.py", line 352, in resize_cv2
    return resize_fn(img)
           ^^^^^^^^^^^^^^
  File "C:\Users\aselimc\micromamba\envs\dinov3\Lib\site-packages\albucore\utils.py", line 92, in __process_fn
    chunk = img[:, :, index : index + 4]
            ~~~^^^^^^^^^^^^^^^^^^^^^^^^^
IndexError: too many indices for array: array is 2-dimensional, but 3 were indexed
```

but error does not occur if I just pass it as 
```python
augmented = transform(image=image, mask=mask)
```

albumentationsx 2.0.10
albucore 0.0.33
