No validation for kernel name
Although `ElementwiseKernel`'s `name` argument is directly used as a function name in generated CUDA code, there are no validation process to raise an exception when invalid characters are used in `name`.
That causes CUDA compile error, which is a bit difficult to debug.
