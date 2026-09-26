## Allow tuning of proxy liveness/readiness probe timeouts and delays

I'm installing Linkerd via the helm chart and ran into an issue on some of our slower nodes: the injected `linkerd-proxy` sidecar occasionally fails its liveness/readiness probes during pod startup and we end up in restart loops until things settle.

Looking at the rendered pod spec, both probes have a fixed `initialDelaySeconds` and no `timeoutSeconds` set at all (so kubelet uses its 1s default). For our environments that's too tight — we'd like to give the proxy a bit more headroom on both fronts (larger initial delay before the first check, and a bigger per-probe timeout so a slow response doesn't immediately count as a failure).

I went looking through `charts/linkerd-control-plane/values.yaml` to override these, but there's nothing exposed for the liveness or readiness probes — the values appear to be baked directly into the partial template. The chart already exposes a `proxy.startupProbe` block where I can tune the equivalent fields for the native-sidecar startup probe, so it feels like an oversight that the same isn't possible for liveness/readiness.

Could we get helm values for these so they can be configured per install? Different clusters legitimately need different settings here and right now the only way to change them is to fork the chart.
