convert_to_tensor does not support torch tensors on "meta" device
I faced the same error then #19376 using the torch backend. While investigating, I found that the "root" issue comes from `convert_to_tensor` not supporting torch tensors defined on "meta" device.

## Way to reproduce

```python
import os

os.environ["KERAS_BACKEND"] = "torch"

import torch
from keras import ops

with torch.device('meta'):
    x = torch.randn(5)

ops.convert_to_tensor(x)
```

Outputs
```python
NotImplementedError: Cannot copy out of meta tensor; no data!
```

## System version

```
3.12.9 | packaged by Anaconda, Inc. | (main, Feb  6 2025, 18:56:27) [GCC 11.2.0]
Linux-5.4.0-208-generic-x86_64-with-glibc2.31
Keras 3.9.0
torch 2.5.1
```
