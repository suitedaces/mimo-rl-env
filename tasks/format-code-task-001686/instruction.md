Keras 3 error with keras.ops.tile
I was working in Keras 3 on the Jax backend, and switched to the Torch backend. I received this error
`TypeError: tile(): argument 'dims' must be tuple of ints, not int`

The call site of tile() looks like:
`keras.ops.tile(tensor, n)`
where is a scalar integer, which according to the documentation is a valid input. This works on the jax backend, but fails on the torch backend specifically.

I believe this is an error with the torch backend of Keras 3, and converting the scalar to a tuple solves the issue.
