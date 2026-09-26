# Properly handle distance metrics in `TSNE`

Right now the behaviour around distance metrics is poorly defined. The `TSNE`
class accepts a `metric` argument, but what actually happens for anything other
than the default depends entirely on whichever nearest-neighbor backend ends up
being used, and there's no way to pass extra arguments that some metrics need
(e.g. the covariance matrix for Mahalanobis distance). The exact-search backend
also silently supports only a small handful of metrics.

I'd like the metric handling to be predictable and consistent regardless of
which neighbor-search method (`'exact'` or `'approx'`) the user picks.

Please make the following hold:

- `TSNE` accepts a new `metric_params` keyword argument (default `None`) for
  passing additional keyword arguments required by a metric (for example
  `metric_params={'V': cov}` for `'mahalanobis'`). These extra arguments must be
  honored when the affinities are computed.

- A metric is only considered valid if it is supported by **both** the exact and
  the approximate nearest-neighbor backends. Selecting a metric that only one of
  the two backends supports must be rejected, regardless of which neighbor
  method was chosen. When an unrecognized/unsupported metric is requested,
  building the embedding must raise a `ValueError`. This applies to both
  `neighbors='exact'` and `neighbors='approx'`.

- Exact nearest-neighbor search must support the full set of valid metrics
  above — not just the limited set that a KD-tree allows. Metrics such as
  `braycurtis` or `canberra` must work end-to-end with `neighbors='exact'`.

Common metrics that both backends support (e.g. `euclidean`, `manhattan`,
`chebyshev`, `braycurtis`, `canberra`, `mahalanobis`) should produce an
embedding of the expected shape when used with exact search.
