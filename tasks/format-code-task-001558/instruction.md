Deprecation in pillow causing problems with imageio gif writing
Hi there, thanks for all the great work on imageio! 🙂 

I had a bug report at napari/napari-animation#174 which boils down to a deprecation in pillow causing a problem with the imageio gif writing, reporting here 


```python
import numpy as np
import imageio

writer = imageio.get_writer(
    'test.gif',
    fps=20,
)
for i in range(5):
    writer.append_data(np.random.random((32, 32)).astype(np.uint8))
```

```txt
  File "/Users/alisterburt/micromamba/envs/napari-animation/lib/python3.9/site-packages/imageio/v2.py", line 215, in append_data
    return self.instance.write(im, **self.write_args)
  File "/Users/alisterburt/micromamba/envs/napari-animation/lib/python3.9/site-packages/imageio/plugins/pillow.py", line 354, in write
    raise TypeError(
TypeError: The keyword `fps` is no longer supported. Use `duration`(in ms) instead, e.g. `fps=50` == `duration=20` (1000 * 1/50).
```
