jnp.mean(x, dtype=bfloat16) is not respected
### Description

Regarding accumulation dtype for np.mean, the numpy docs say:
```
Note that for floating-point input, the mean is computed using the same precision the input has. Depending on the input data, this can cause the results to be inaccurate, especially for float32 (see example below). Specifying a higher-precision accumulator using the dtype keyword can alleviate this issue.

By default, float16 results are computed using float32 intermediates for extra precision.
```

This suggests that for a bfloat16/float16 input, the default value for `dtype` is float32, but the user can request a different precision.

In #[17792](https://github.com/jax-ml/jax/pull/17792), we fixed the default upcasting, but in my testing on TPU, `jnp.mean(x, dtype=jnp.bfloat16)` still casts to fp32 so the `dtype` parameter does not seem to allow the user to override it.

I reprod this under pjit with simply:
```
x = jnp.zeros((2, 3, 5), dtype=jnp.bfloat16)
y = jnp.mean(x, axis=-1, keepdims=True, dtype=x.dtype)
```

and I observe the following:
<img width="427" alt="Image" src="https://github.com/user-attachments/assets/9deabae5-273b-482a-afa2-a536178a9060" />





### System info (python version, jaxlib version, accelerator, etc.)

(internal to google, running around cl/723930299 on borg)
