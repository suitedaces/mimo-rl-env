## `max_fetched_series_per_query` is not enforced for the `/series` API

We rely on `max_fetched_series_per_query` to protect our cluster from queries that fan out into too many series. With the limit configured, running a range query with a very loose matcher (e.g. `{__name__=~".+"}`) is correctly rejected once the limit is exceeded — which is exactly what we want.

However, the `/api/v1/series` endpoint doesn't seem to apply the same limit. Hitting `/series` with the same kind of broad matcher happily returns well above `max_fetched_series_per_query` series, and we can see noticeable memory pressure on the distributors when this happens. The series response itself can also be huge.

It feels inconsistent that one read path enforces the limit while another silently ignores it. From an operator's point of view we'd like a single configured value to protect *all* query APIs uniformly, so it would be great if `/series` honored `max_fetched_series_per_query` too and rejected the request (rather than continuing to accumulate) once the limit is reached.
