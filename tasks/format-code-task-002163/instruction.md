### What happened?

When the cloud apiserver becomes unreachable and yurthub takes over serving requests locally, any `watch` request that does not carry a `timeoutSeconds` query parameter is closed by yurthub immediately. The client sees the watch end right away, reconnects, gets closed again, and the loop repeats as fast as the client can retry.

The visible symptom is that both the yurthub log and the client (e.g. kubelet, controllers) log start filling up with watch open/close messages within seconds of cloud connectivity being lost. On a busy edge node this quickly produces tens of MB of logs and noticeable CPU from the retry storm, even though nothing is actually wrong other than the cloud being temporarily unreachable.

### What did you expect to happen?

A `watch` request without `timeoutSeconds` should not be terminated instantly. The kube-apiserver itself keeps such watches open for a long, slightly randomized period (so that watches don't all expire at the same instant) and only returns when the timeout elapses. yurthub's local watch handler should behave similarly so that clients don't enter a hot retry loop when yurthub is serving from cache.

It would also be useful to have this default duration configurable on the yurthub side, since different deployments may want different behavior.

### How to reproduce

1. Run yurthub in edge working mode against a cloud apiserver.
2. Take the cloud apiserver offline (or block the network) so yurthub falls back to the local proxy path.
3. Have a client issue a `watch` request without setting `timeoutSeconds` (kubelet does this for some informers).
4. Observe yurthub and client logs — watches return immediately and the client reconnects in a tight loop.

### Environment

- OpenYurt: master
- Component: yurthub (local proxy / watch handling)
