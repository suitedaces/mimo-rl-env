## Add panic recovery to `checkUsersetSlowPath` and `checkMembership`

Follow-up to #2361, where we added panic recovery for goroutines spawned during check resolution.

While auditing `internal/graph/check.go` I noticed that two functions still spawn goroutines without converting recovered panics into errors:

- `checkUsersetSlowPath`
- `checkMembership`

In both cases, the work that runs inside the spawned goroutine (the producer side of the dispatch / userset channel) is not protected, and the error returned by waiting on the goroutine pool is currently discarded. So if anything deeper in those producers panics — a nil dereference, an out-of-bounds, whatever — the panic is silently swallowed, the consumer side eventually gets garbage / nothing on its channel, and the caller of `ResolveCheck` either hangs on a degraded path or returns a successful-looking response that isn't actually correct. In the worst case, depending on how the runtime is configured, an unrecovered panic in a goroutine can take the whole server down.

These two functions should behave the same way as the other check paths that were updated in #2361: a panic inside the goroutine should be turned into a normal error that propagates back to the caller of `ResolveCheck`, so the request fails cleanly with a meaningful error instead of corrupting the result or crashing the process.

Should be a fairly mechanical change mirroring what was already done elsewhere in this file, but please make sure both functions actually surface the failure to their caller (today the wait-error from the goroutine pool is being dropped on the floor in both of them, which would mask the recovered panic even if you only added the recovery).
