## Easy way to profile model likelihood / gradient evaluation

When sampling is slow, I want to figure out which part of the log-probability (or its gradient) is the bottleneck. Theano has nice profiling support built in via `theano.function(..., profile=True)` plus `ProfileStats.summary()`, but right now there's no convenient way to use it on a pymc3 `Model`.

Take the stochastic volatility example:

```python
import numpy as np
from pymc3 import *
from pymc3.distributions.timeseries import *

n = 400
returns = np.genfromtxt(get_data_file('pymc3.examples', "data/SP500.csv"))[-n:]

with Model() as model:
    sigma, log_sigma = model.TransformedVar(
        'sigma', Exponential.dist(1. / .02, testval=.1), logtransform)
    nu = Exponential('nu', 1. / 10)
    s = GaussianRandomWalk('s', sigma ** -2, shape=n)
    r = T('r', nu, lam=exp(-2 * s), observed=returns)
```

What I'd like to do is something like

```python
model.profile(model.logpt).summary()
model.profile(gradient(model.logpt, model.vars)).summary()
```

and get the standard Theano profile report (time per Op / Apply, total time, etc.) so I can see which nodes dominate the cost of evaluating the likelihood or its gradient.

Right now `model.fn` / `model.fastfn` / `model.makefn` compile a Theano function but don't expose Theano's profiling options, so I'd have to bypass the model and rebuild the function by hand. It would be much nicer if the model itself offered a one-liner for this — compile the function with profiling on, run it some reasonable number of times on the test point, and hand back the resulting profile stats.
