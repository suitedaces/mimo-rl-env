## `MRG_RandomStreams` has no `seed()` method

I'm using `theano.sandbox.rng_mrg.MRG_RandomStreams` for the random ops in a model (dropout, init noise, etc.) because it's faster and works on the GPU. For reproducibility I want to be able to reset the random source between runs of the same compiled function — same workflow I use with `theano.tensor.shared_randomstreams.RandomStreams`:

```python
from theano.sandbox.rng_mrg import MRG_RandomStreams

srng = MRG_RandomStreams(seed=234)
# ... build some random variables off srng, compile a function f ...

# I want to reset everything and replay the exact same samples:
srng.seed(123)
# run f again
```

But `MRG_RandomStreams` doesn't have a `seed` method, so the call above just blows up with an AttributeError. The constructor takes a `seed` argument, but once you've built RVs off the stream there's no way to re-seed them after the fact.

The plain `theano.tensor.shared_randomstreams.RandomStreams` class supports this — you can call `.seed(N)` on it and the RVs that were already built off that stream get reset to a deterministic state, so re-running the compiled function produces the same sample sequence. It would be great if `MRG_RandomStreams` behaved the same way, since otherwise switching between the two stream implementations changes what reproducibility tools you have.
