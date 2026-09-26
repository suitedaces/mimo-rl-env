## Add support for computing DIC

When comparing Bayesian models fit with pymc3, one of the standard summary statistics people reach for is the **Deviance Information Criterion (DIC)**. As far as I can tell there's no built-in way to compute it from a fitted model + trace right now — I end up writing my own helper every project, which is silly because it's a pretty standard quantity.

It would be great if `pymc3.stats` exposed a function that, given a `Model` and a `MultiTrace`, returned the DIC value so it can be used directly for model comparison alongside the other things in that module (`hpd`, `summary`, etc.).

One thing worth flagging: I often work with bounded parameters (e.g. `HalfNormal`, `Uniform`, things sampled on a transformed scale internally). DIC computed naively on transformed variables doesn't give you what you'd expect on the original parameter scale, so it'd be good if users got some kind of heads-up when the model contains transformed RVs rather than silently getting a number that looks fine but is misleading.
