Error with control_flow.scan and plated uniform random variables
Hi -- I'm facing this weird issue where I'm unable to run a model with `control_flow.scan` and uniformly distributed random variables in it. The following is a simplified reproducer of what I'm trying to do
```python
import jax
from jax import numpy as jnp

import numpyro
from numpyro import distributions as dist
from numpyro.contrib import control_flow

def layer_unit_model(M,N):
    with numpyro.plate('units', M*N):
        us = numpyro.sample('us', dist.Uniform())
    return us.reshape((M, N))

def model(lower_bounds, upper_bounds):
    # sequentially sample thicknesses using scan
    # define step function
    def transition(current_height, height_bounds):
        height_lb, height_ub = height_bounds
        thickness_lb = height_lb - current_height
        new_units = layer_unit_model(*current_height.shape)
        thickness = thickness_lb + (height_ub-height_lb) * new_units
        new_height = current_height + thickness # === height_lb + (height_ub-height_lb) * new_units
        return new_height, thickness

    # run
    _, thicknesses = control_flow.scan(
        transition, 
        jnp.zeros_like(upper_bounds[0]),
        (lower_bounds, upper_bounds)
    )
    return thicknesses

lower_bounds = jnp.array(
    [[[106.0026 , 214.71115, 208.37521, 241.16296, 149.16177],
        [106.48185, 110.21102, 220.84187, 182.59181, 228.84312]],

       [[352.876  , 567.84467, 477.1498 , 548.78644, 467.59097],
        [528.7906 , 481.11255, 476.48227, 521.28345, 503.7652 ]]]
)
upper_bounds = jnp.array(
    [[[326.3172 , 431.25897, 277.67496, 475.2467 , 286.37335],
        [181.98593, 383.44434, 293.90152, 348.08966, 391.97644]],

       [[594.8691 , 688.70105, 813.79987, 736.4565 , 848.7659 ],
        [625.6504 , 527.63043, 815.475  , 551.9418 , 789.07635]]]
)
```

Attempting to sample from the above model raises an error
```python
>>> seeded_model = numpyro.handlers.seed(model, rng_seed=2)
>>> seeded_model(lower_bounds, upper_bounds)
Traceback (most recent call last):
  File "<python-input-0>", line 43, in <module>
    thicknesses = seeded_model(lower_bounds, upper_bounds)
  File "/home/mbiron/projects/layermodels/.venv/lib/python3.13/site-packages/numpyro/primitives.py", line 105, in __call__
    return self.fn(*args, **kwargs)
           ~~~~~~~^^^^^^^^^^^^^^^^^
  File "<python-input-0>", line 21, in model
    _, thicknesses = control_flow.scan(
                     ~~~~~~~~~~~~~~~~~^
        transition,
        ^^^^^^^^^^^
        jnp.zeros_like(upper_bounds[0]),
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        (lower_bounds, upper_bounds)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/home/mbiron/projects/layermodels/.venv/lib/python3.13/site-packages/numpyro/contrib/control_flow/scan.py", line 476, in scan
    msg = apply_stack(initial_msg)
  File "/home/mbiron/projects/layermodels/.venv/lib/python3.13/site-packages/numpyro/primitives.py", line 53, in apply_stack
    default_process_message(msg)
    ~~~~~~~~~~~~~~~~~~~~~~~^^^^^
  File "/home/mbiron/projects/layermodels/.venv/lib/python3.13/site-packages/numpyro/primitives.py", line 28, in default_process_message
    msg["value"] = msg["fn"](*msg["args"], **msg["kwargs"])
                   ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/mbiron/projects/layermodels/.venv/lib/python3.13/site-packages/numpyro/contrib/control_flow/scan.py", line 341, in scan_wrapper
    site["fn"] = promote_batch_shape(site["fn"])
                 ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^
  File "/home/mbiron/opt/python/lib/python3.13/functools.py", line 931, in wrapper
    return dispatch(args[0].__class__)(*args, **kw)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "/home/mbiron/projects/layermodels/.venv/lib/python3.13/site-packages/numpyro/distributions/batch_util.py", line 527, in _promote_batch_shape_expanded
    promoted_base_dist = promote_batch_shape(new_self.base_dist)
  File "/home/mbiron/opt/python/lib/python3.13/functools.py", line 931, in wrapper
    return dispatch(args[0].__class__)(*args, **kw)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "/home/mbiron/projects/layermodels/.venv/lib/python3.13/site-packages/numpyro/distributions/batch_util.py", line 508, in _default_promote_batch_shape
    attr_event_dim = d.arg_constraints[attr_name].event_dim
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/mbiron/projects/layermodels/.venv/lib/python3.13/site-packages/numpyro/distributions/constraints.py", line 217, in event_dim
    raise NotImplementedError(".event_dim cannot be determined statically")
NotImplementedError: .event_dim cannot be determined statically
```

However, if I sample U[0,1] in a roundabout way by first sampling a Normal(0,1) and then transforming using its cdf, the model runs fine 
```python
def layer_unit_model(M,N):
    with numpyro.plate('z_units', M*N):
        zs = numpyro.sample('zs', dist.Normal())
    return jax.scipy.special.ndtr(zs).reshape((M, N))

[...]

>>> seeded_model(lower_bounds, upper_bounds)
Array([[[312.56985, 305.90314, 276.85083, 467.60272, 160.2734 ],
        [107.59826, 171.91122, 234.5139 , 319.7326 , 290.80072]],

       [[253.15756, 363.28387, 300.6725 , 229.57504, 448.96625],
        [479.48203, 311.6913 , 544.35925, 224.66612, 310.71204]]],      dtype=float32)
```

I don't know much about the numpyro internals, but one obvious difference between a `Uniform` and a `Normal` distribution is how their argument constraints are coded: for the former are marked as `Dependent`, whereas for the latter they are simply `Real` and `Positive`.

**Uniform**
https://github.com/pyro-ppl/numpyro/blob/93e11c2e43a99a450b2d857ff1f0a84ac1057f9e/numpyro/distributions/continuous.py#L2429

**Normal**
https://github.com/pyro-ppl/numpyro/blob/93e11c2e43a99a450b2d857ff1f0a84ac1057f9e/numpyro/distributions/continuous.py#L2179
