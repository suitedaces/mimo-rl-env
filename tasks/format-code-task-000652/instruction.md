ZeroDivisionError in softmax_cross_entropy when I pass masked array
- Chainer version: `origin/master`
  - CuPy version: `2.0.0b1`
  - OS/Platform: `Ubuntu 14.04`
  - CUDA/cuDNN version: `CUDA-8.0.61-1/cudnn5.1.5-1`

## Problem

When I mask two arrays and calculate `softmax_cross_entroy`, `ZeroDivisionError` occurs when masked array's data is `[]`
I thought it should be checked in ndim and shape check at the beginning of the function, but the array's shape was something like `(0, 2, 2)`

## Reproduction

```python
import chainer
import cupy
import numpy as np


data = np.random.random((10, 2, 2))
t = cupy.ones((data.shape[0], data.shape[2]), dtype=cupy.int32)
x = chainer.Variable(data)
x.to_gpu()
mask = t[:, 0] == 0
x_masked = x[mask]
print('=================')
print('x_masked')
print('    data: {}'.format(x_masked.data))
print('    shape: {}'.format(x_masked.shape))
print('=================')
t_masked = t[mask]
print('=================')
print('t_masked')
print('    data: {}'.format(t_masked))
print('    shape: {}'.format(t_masked.shape))
print('=================')
chainer.functions.softmax_cross_entropy(x_masked, t_masked)
```
* Shape
```
=================
x_masked
    data: []
    shape: (0, 2, 2)
=================
=================
t_masked
    data: []
    shape: (0, 2)
=================
```
* Error
```bash
Traceback (most recent call last):
  File "spam.py", line 25, in <module>
    chainer.functions.softmax_cross_entropy(x_masked, t_masked)
  File "/home/shingo/chainer/chainer/functions/loss/softmax_cross_entropy.py", line 275, in softmax_cross_entropy
    normalize, cache_score, class_weight, ignore_label, reduce)(x, t)
  File "/home/shingo/chainer/chainer/function.py", line 212, in __call__
    ret = node.apply(inputs)
  File "/home/shingo/chainer/chainer/function_node.py", line 219, in apply
    outputs = self.forward(in_data)
  File "/home/shingo/chainer/chainer/function.py", line 117, in forward
    return self._function.forward(inputs)
  File "/home/shingo/chainer/chainer/function.py", line 319, in forward
    return self.forward_gpu(inputs)
  File "/home/shingo/chainer/chainer/functions/loss/softmax_cross_entropy.py", line 102, in forward_gpu
    log_y = log_softmax._log_softmax(x)
  File "/home/shingo/chainer/chainer/functions/activation/log_softmax.py", line 36, in _log_softmax
    x.reshape(x.shape[:2] + (-1, 1)))
  File "cupy/core/core.pyx", line 461, in cupy.core.core.ndarray.reshape (cupy/core/core.cpp:11315)
  File "cupy/core/core.pyx", line 434, in cupy.core.core.ndarray._reshape (cupy/core/core.cpp:10994)
  File "cupy/core/internal.pyx", line 139, in cupy.core.internal.infer_unknown_dimension (cupy/core/internal.cpp:3060)
ZeroDivisionError: integer division or modulo by zero
```
