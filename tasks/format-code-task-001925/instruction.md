## Client no longer retries when the server rate-limits the request

We have a pymilvus client that issues a fairly high rate of `insert` / `search`
calls against a cluster that has quota / rate-limit enabled on the server side.

On older versions, when we hit the quota, the client would back off and retry
transparently — our application barely noticed. After upgrading, the same
workload starts surfacing rate-limit errors straight to our application code on
the very first attempt, with no retries and no backoff log messages from the
decorator at all.

A minimal repro looks like:

```python
from pymilvus import connections, Collection

connections.connect(host="...", port="19530")
col = Collection("my_collection")

# Loop hard enough to trip the server-side quota.
for i in range(10000):
    col.insert([...])   # eventually raises immediately, no retry
```

What we observe:

- Other transient gRPC failures (DEADLINE_EXCEEDED, UNAVAILABLE) still get
  retried the way they always did — the retry decorator clearly still works
  for those.
- Only rate-limit responses go straight through. From the client side they
  arrive as a regular `MilvusException` carrying a rate-limit error code,
  rather than as a gRPC-level error.

It looks like the server's rate-limit response shape changed and the retry
path in `retry_on_rpc_failure` no longer recognizes it as "retryable". For a
client that's deliberately pushing close to the quota, the right behavior is
to back off and retry (the existing exponential backoff / `retry_times` /
`timeout` machinery is already exactly what we want here) — not to bubble the
error up on the first hit.

Could rate-limit responses please be treated as a retryable condition again?
And ideally there should still be a way for callers who *don't* want this
(e.g. latency-sensitive paths that would rather fail fast) to opt out, the
same way other retry behaviors on this decorator can be turned off via a
kwarg.

(Note: only the rate-limit code path should be auto-retried — other
`MilvusException` codes like force-deny should still propagate as before. The
opt-out kwarg I'd expect is something like `retry_on_rate_limit=False`.)
