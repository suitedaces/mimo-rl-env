# Reference-counted, event-driven sequence-rate reporter

Our store reports per-extent replica stats (begin/last sequence numbers and the
*rate* at which the sequence number is advancing) up to the metadata service.
Today those stats are produced by a periodic poll that snapshots every active
extent once a minute. The problem: extents that are opened only for a very
short-lived operation (a purge, a seal, a one-shot replication) are frequently
opened and closed *between* two polls, so their final stats are never captured.

We want to move to an **event-driven** model. Add a small, concurrency-safe
helper to the `common` package that components can drive from extent lifecycle
events (open / update / close) and periodically drain to obtain the set of
stats that need to be flushed upstream. The helper must guarantee that the last
state of a short-lived item is reported even if it lived entirely between two
drains, and it must avoid re-reporting items whose state has not changed.

## What to build

Expose the following public surface from the `common` package:

```go
type RateReport struct {
    Value int64   // the latest recorded value for the key
    Time  int64   // the timestamp (unix-nanos) of that value
    Rate  float64 // rate of change since this key's previous report
    Final bool    // true iff this is the key's last report
}

func NewRateReporter() *RateReporter

func (r *RateReporter) Open(key string)
func (r *RateReporter) Update(key string, value int64, nanoTime int64)
func (r *RateReporter) Close(key string)
func (r *RateReporter) Collect() map[string]RateReport
```

### Behavior

`Open`, `Update`, `Close` track the lifecycle of a *key* (e.g. an extent id).
`Collect` returns, keyed by key id, the reports that should be flushed upstream
since the previous `Collect`.

- **Reference counting.** A key is "active" while it has outstanding
  references. `Open` adds a reference; `Close` removes one. A key becomes
  *final* exactly when a `Close` drops its reference count from one to zero.
  Nested opens are supported: a key opened N times stays active until it has
  been closed N times. A `Close` on a key with no outstanding references is a
  no-op.

- **Recording samples.** `Update` records the latest observed value and its
  timestamp for a key (last-write-wins between drains) and marks the key as
  having pending data to report.

- **What `Collect` returns.** A key appears in the returned map iff, since the
  previous `Collect`, it either received at least one `Update` (pending data)
  or became final. Active keys that received no `Update` since the last
  `Collect` are omitted (no redundant reports). A key that became final without
  ever having recorded a sample produces no report at all.

  Each returned report carries the key's latest recorded `Value` and `Time`,
  the `Rate` of change, and `Final` set true iff the key became final.

- **Rate.** The rate is the change in value per second since the *previous
  report emitted for that same key*:
  `(value - prevValue) / ((nanoTime - prevNanoTime) / 1e9)`.
  The rate is `0` when there is no previous report for the key, when either
  timestamp is zero, or when the elapsed time is not positive (so equal or
  out-of-order timestamps never yield infinities or NaNs). The value itself may
  decrease, which yields a negative rate.

- **After a drain.** Reporting clears the pending flag and makes the just-drained
  sample the "previous report" used for the next rate calculation. A key
  reported as final is removed entirely; a subsequent `Open`/`Update` of the
  same key id starts fresh (its first report again has rate `0`).

The reporter must be safe for concurrent use from many goroutines.
