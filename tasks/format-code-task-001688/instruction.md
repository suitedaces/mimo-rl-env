# Problem Statement

I'm building transformer-style models and keep having to copy a custom RMSNorm because Keras doesn't seem to expose it as a normal op or layer. `LayerNormalization(rms_scaling=True)` also made me wonder if that's supposed to be the same thing, but it doesn't look like standard RMSNorm. Could Keras add native RMS normalization directly, ideally usable both from `keras.ops` and as a `keras.layers` layer?

# Expected outcomes

- RMS normalization is exposed as public functional APIs at `keras.ops.rms_normalization` and `keras.ops.nn.rms_normalization`.
- The functional APIs implement standard RMS normalization behavior: outputs keep the input shape, values are normalized by their root mean square over caller-selected `axis` values, callers can provide optional `scale` behavior, callers can control numerical stability with `epsilon`, and symbolic Keras tensors preserve their symbolic output shape.
- `keras.layers.RMSNormalization` is exposed as a public layer.
- The layer provides configurable `axis` and `epsilon` behavior, has trainable scaling observable through the public layer weights and outputs, applies RMS normalization consistently with the functional API, and returns outputs with the same shape as its inputs.
- `RMSNormalization.compute_output_shape(input_shape)` preserves the input shape for valid axes and raises `ValueError` for axes outside the input rank.
- The `LayerNormalization` documentation for `rms_scaling=True` clarifies that this mode is not equivalent to the standard `keras.layers.RMSNormalization` computation.

# Implementation notes

The exact internal organization, helper functions, backend dispatch path, validation location, and generated export-file mechanics are left to the implementer. The public behavior should be observable through the Keras ops namespace, the Keras layers namespace, tensor outputs, layer weights, output shapes, exceptions for invalid axes, and documented API behavior.
