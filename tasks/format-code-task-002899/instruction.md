# Add a circuit breaker for the Typesense HTTP transport

When the Typesense server starts failing, the client currently keeps hammering it with
requests, which makes a bad situation worse. I'd like us to add a **circuit breaker** that
monitors request failures and short-circuits calls once failures pile up, so we stop sending
traffic to a server that is clearly unhealthy.

Please add a self-contained package that is importable as
`github.com/v-byte-cpu/typesense-go/typesense/api/circuit`. It should provide a reusable circuit
breaker plus a thin HTTP client wrapper that runs requests through the breaker. Use only the Go
standard library — don't pull in new third-party dependencies.

## The breaker

Expose a breaker created by a constructor `NewGoBreaker(opts ...)` that takes functional options
(the same "`With...`" pattern used elsewhere in this repo). The breaker tracks the outcomes of the
function calls it runs and decides, based on those outcomes, whether to keep letting calls through.

Required public surface and behavior:

- An `Execute(req func() error) error` method that runs `req` and returns its error. While the
  breaker is **closed** (the initial state), every call is passed through to `req` and `req`'s
  return value is what `Execute` returns.

- A `State()` accessor returning the current state as an exported `State` type. There are three
  states — closed, open and half-open — each rendered as a distinct human-readable string by
  `State`'s `String()` method; the closed state renders as `"closed"` and the open state as
  `"open"`.

- A `Counts()` accessor returning an exported `Counts` snapshot of the current tallies with the
  unsigned-integer fields `Requests`, `TotalSuccesses`, `TotalFailures`, `ConsecutiveSuccesses`
  and `ConsecutiveFailures`. A call that returns `nil` is a success; a call that returns a non-nil
  error is a failure. A success increments `Requests`, `TotalSuccesses` and `ConsecutiveSuccesses`
  and resets `ConsecutiveFailures` to zero; a failure increments `Requests`, `TotalFailures` and
  `ConsecutiveFailures` and resets `ConsecutiveSuccesses` to zero.

- A `Name()` accessor returning the configured name.

- Functional options, one per setting, named after the setting they configure:
  `WithGoBreakerName(string)`, `WithGoBreakerMaxRequests(uint32)` (trial requests allowed while
  half-open), `WithGoBreakerInterval(time.Duration)` (cyclic period for clearing the closed-state
  counts), `WithGoBreakerTimeout(time.Duration)` (governs the open state),
  `WithGoBreakerReadyToTrip(func(Counts) bool)` and
  `WithGoBreakerOnStateChange(func(name string, from, to State))`.

- **Tripping:** whenever a call fails while the breaker is closed, the breaker consults the
  "ready to trip" predicate with the current counts. If it returns `true`, the breaker moves to
  the open state. The call that crosses the threshold still runs and still returns its own error;
  it is the *next* call that is rejected.

- **Default trip policy:** if no predicate is supplied, the breaker trips when the number of
  consecutive failures is greater than 5.

- **Open state:** while open, `Execute` rejects calls immediately — it must not invoke `req` —
  and returns the exported sentinel error `ErrOpenState`, which callers can detect with
  `errors.Is`.

- **State-change callback:** every time the state changes, the configured "on state change"
  callback (if any) is invoked with the breaker name and the old and new states. Whenever the
  state changes the counts are reset to zero.

- A sensible default name should be used when none is configured.

## The HTTP client wrapper

Also provide a small HTTP client, created by `NewHTTPClient(opts ...)`, that adapts the breaker to
Go's `net/http`. It should:

- Implement `Do(*http.Request) (*http.Response, error)`.
- Be configured with functional options `WithHTTPRequestDoer(...)` to plug in the underlying
  request executor — anything with a `Do(*http.Request) (*http.Response, error)` method — and
  `WithCircuitBreaker(...)` to plug in the breaker. The breaker parameter should be an interface
  (anything offering the `Execute(func() error) error` method), so a custom breaker can be
  supplied in its place.
- Run the underlying request inside the breaker. A transport error from the underlying executor
  is reported to the breaker as a failure and returned to the caller. A returned HTTP response
  with a `nil` error is reported as a success and handed back to the caller unchanged — including
  responses with 4xx/5xx status codes, which are *not* treated as breaker failures.
- When the breaker rejects the call (open state), `Do` must return the breaker's rejection error
  without ever calling the underlying executor.
