wgsl: AbstractFloat execution tests for `fma` builtin
Add AbstractFloat execution tests for the `fma` builtin.
```
@const @must_use fn fma(e1: T,
                        e2: T,
                        e3: T) -> T
S is AbstractFloat
T is S or vecN<S>
```
Returns e1 * e2 + e3. [Component-wise](https://www.w3.org/TR/WGSL/#component-wise) when T is a vector.

Accuracy is `Inherited from x * y + z`

See https://www.w3.org/TR/WGSL/#fma-builtin
