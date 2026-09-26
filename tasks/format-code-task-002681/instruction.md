## Flood of retry warnings after the context is canceled

I'm using gosnowflake (via the ADBC driver) and cancel the context attached to a query while results are still being fetched. Instead of stopping promptly, the driver emits a flood of warnings like:

```
WARN[0026]retry.go:330 gosnowflake.(*retryHTTP).execute failed http connection. err: Get "https://<host>/results/<...>/main/data_W_X_Y_Z?<query-parameters>": context canceled. retrying...
```

These keep coming until the retry loop eventually gives up, even though the context has clearly been canceled by the caller. The same thing happens when the context's deadline is exceeded.

It doesn't make much sense to keep retrying HTTP requests once the caller has already signaled (via the context) that they no longer want the operation to continue — every subsequent attempt is going to fail the same way, and the function is going to return the context error at the end anyway. The noisy logs also make real failures harder to spot.

I'd expect that once the context driving the request is canceled or its deadline has been exceeded, the retry machinery bails out immediately with that context error rather than treating the failure as a transient connection problem and looping.
