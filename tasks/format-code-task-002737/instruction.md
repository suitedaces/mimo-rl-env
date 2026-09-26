# Let Archimedean copula parameters be supplied per call

The single-parameter Archimedean copulas (`ClaytonCopula`, `FrankCopula`,
`GumbelCopula`) currently bake their dependence parameter into the instance: you
pass `theta` to the constructor and every `cdf`/`pdf`/`logpdf` call uses that
stored value. That makes them awkward to use for anything that needs to evaluate
the same copula family at many different parameter values (e.g. plugging a
copula into an optimizer), because you have to keep building new objects.

Make the dependence parameter overridable on a per-call basis, consistently
across all three of these copulas.

Concretely:

- `cdf`, `pdf` and `logpdf` accept an optional `args` argument holding the
  copula parameter(s) for that single call. For these one-parameter families
  that means `args=(theta,)`.
- When `args` is non-empty, the value in `args` is used for that call and
  overrides whatever parameter the instance was constructed with. Evaluating
  `SomeCopula(theta=a).cdf(u, args=(b,))` must give exactly the same result as
  `SomeCopula(theta=b).cdf(u)`, and likewise for `pdf` and `logpdf`.
- When `args` is empty (`()`, the default) or omitted, the parameter supplied at
  construction is used, exactly as before.
- It must be possible to construct any of these copulas without supplying a
  parameter at all (i.e. leaving `theta` unset / `None`) without raising. Such an
  instance produces correct results when the parameter is provided through
  `args`.

`pdf` and `logpdf` must stay consistent with each other: for the bivariate case,
`pdf` equals `exp(logpdf)` regardless of whether the parameter came from the
constructor or from `args`.

The existing behaviour for instances built with a fixed `theta` and called
without `args` must be unchanged.
