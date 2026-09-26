## S3 bucket client keeps retrying after the request context is canceled

When running Cortex against S3-backed object storage, I noticed that if an in-flight operation's context gets canceled (either explicitly, or because an upstream deadline expires), the bucket client doesn't actually stop right away. It keeps going around the retry loop and re-issuing the operation, even though the context is already done so every attempt is guaranteed to fail immediately.

The two visible symptoms:

1. **Extra latency unwinding canceled requests.** After cancellation/timeout I'd expect the bucket call to return essentially immediately, but instead it sits there going through retry iterations before finally giving up.
2. **Misleading error logs.** Each canceled operation ends up producing a `bucket operation fail after retries` error in the logs, which makes it look like S3 is unhealthy and the retries got exhausted, when in reality the caller had already canceled the request and nothing was going to succeed regardless.

The retry wrapper already knows how to short-circuit and return immediately for some error classes (object-not-found and access-denied) — those don't get retried because retrying them is pointless. The same logic should apply when the operation failed because the caller's context was canceled or its deadline was exceeded: there's no point spinning through more attempts, we should just propagate the context error back to the caller right away and not log it as a "fail after retries" outcome.
