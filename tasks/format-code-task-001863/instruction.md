## Pairwise distance returns `inf` on series with near-zero variance

I'm using matrixprofile to compute the pairwise distance on a time series I have, and the output contains `inf` values where I'd expect finite numbers.

After digging around, I noticed this only happens on series that contain a stretch where the values are basically constant (so the rolling standard deviation over that window is essentially zero). On series with normal variability, everything works fine.

Minimal-ish repro (a series with a flat segment):

```python
import numpy as np
import matrixprofile as mp

# a series with a flat (constant) region
ts = np.concatenate([
    np.random.randn(50),
    np.ones(50) * 3.14,   # flat segment, std ~ 0 here
    np.random.randn(50),
])

# compute on this — output contains inf values
profile = mp.compute(ts, windows=8)
print(profile['mp'])
# -> array([..., inf, inf, inf, inf, inf, ...])
```

The `inf`s then propagate into anything downstream that consumes these distances (motif/discord discovery, plots, comparisons, etc.), which makes the whole pipeline unusable on data that happens to contain a flat region — and real-world sensor data often has flat stretches (sensor stuck, padding, idle periods, etc.).

I'd expect the library to handle these degenerate windows gracefully and return a finite value rather than `inf`, so that the rest of the computation stays well-defined.
