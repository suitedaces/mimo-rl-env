## Envoy fails to start when Envoy Access Log Service is enabled

I'm trying to ship sidecar / gateway access logs to a gRPC Access Log Service (ALS) backend. I followed the same pattern that's already used for `envoyMetricsService` and set the corresponding values for ALS in the istio helm chart, e.g.

```yaml
global:
  proxy:
    envoyAccessLogService:
      enabled: true
      host: accesslog-service.istio-system
      port: 15000
```

After deploying the chart (and likewise when injecting sidecars), the proxy never comes up cleanly:

- For ingress/egress gateways, the `istio-proxy` container in the gateway deployment crash-loops at startup.
- For injected sidecars, envoy similarly fails to start; the pod's proxy never becomes ready, so the application pod stays in a not-ready state.
- No access logs ever reach my ALS backend, even after the proxy briefly comes up.

Disabling `envoyAccessLogService` makes everything work again, so the problem is clearly tied to enabling ALS. By contrast, enabling `envoyMetricsService` with the same shape of configuration works fine — that's why I assumed ALS would just work analogously.

I'd expect that enabling `envoyAccessLogService` in the helm values (and/or enabling ALS via mesh config) results in a working envoy that actually sends access logs to the configured backend, the same way `envoyMetricsService` does today.
