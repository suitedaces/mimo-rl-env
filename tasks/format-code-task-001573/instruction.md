## Confusing error when calling `fit()` without `search()` first in Nano AutoML

I'm trying out BigDL Nano's AutoML/HPO. I defined a model and put a couple of hpo search spaces in it (e.g. a learning-rate range), then just called `model.fit(...)` to train it, the same way I'd train any normal Keras model.

Instead of training, I get a `ValueError` that says something along the lines of:

> study is None. Please call search before calling end_search.

This is pretty confusing as a user:

- I never called `end_search` myself — it's not in my code at all. The error is pointing at some internal function I don't know about, instead of telling me what I actually did wrong (forgot to run `model.search(...)` before `model.fit(...)`).
- The message doesn't mention `fit` at all, so it took me a while to realize my mistake was calling `fit` directly when I'd put hpo spaces in the model.

It'd be much nicer if the error told me, in terms of the public API I actually use, that I need to run `search` before `fit` whenever the model has search spaces in it.

Also, a related thing I ran into: if I take the search spaces back out of the model (i.e. it's just a plain model with no hpo at all) and call `fit` directly, I'd expect that to just work — there's nothing to search over. Right now the AutoML path still complains about not having done a search even though there's nothing to search.

So basically two things:

1. When the user *did* define search spaces but forgot to call `search` before `fit`, raise an error that's actually phrased in terms of `search`/`fit` so it's obvious what to do.
2. When the user defined no search spaces, calling `fit` directly should just train the model without forcing a `search` step.
