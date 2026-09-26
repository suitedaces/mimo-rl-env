# Problem Statement

我们用 fxhttpclient 发了不少外部请求，现在 `/metrics` 上能看到 server 端的指标，但 client 这边啥都没有，没法做请求量、耗时、错误率的监控和告警。能不能也给 client 加一套 Prometheus 指标，至少有请求数和耗时分布，带上 method/status/url 这些 label？最好能在 config 里开关，status 也能按 2xx/3xx 这种聚合一下，不然 url 一多基数就爆了。

# Expected outcomes

- Configuration:
  - The HTTP client module accepts a `modules.http.client.metrics` configuration block.
  - Metrics collection can be enabled or disabled through `modules.http.client.metrics.collect.enabled`.
  - The metrics namespace and subsystem can be configured through `modules.http.client.metrics.collect.namespace` and `modules.http.client.metrics.collect.subsystem`, with sensible defaults based on the application name and the HTTP client subsystem.
  - Request-duration histogram buckets can be overridden through `modules.http.client.metrics.buckets`.
  - Status label normalization can be enabled through `modules.http.client.metrics.normalize`.

- Emitted metrics:
  - When client metrics collection is enabled, each outgoing HTTP client request increments a Prometheus counter named with the configured namespace/subsystem prefix and the `client_requests_total` suffix.
  - The request counter exposes `method`, `status`, and `url` labels.
  - When status normalization is enabled, the counter’s `status` label uses HTTP status classes such as `2xx`; when it is disabled, the label remains specific to the response status.
  - When client metrics collection is enabled, outgoing HTTP client requests are observed in a Prometheus histogram named with the configured namespace/subsystem prefix and the `client_request_duration_seconds` suffix.
  - The request-duration histogram exposes `method` and `url` labels and includes bucket, sum, and count series.

- Documentation and integration:
  - The fxhttpclient documentation describes the client metrics configuration and shows the expected metrics behavior.
  - The fxhttpclient module documentation and examples mention the metrics module integration needed to expose these metrics.

# Implementation notes

The concrete instrumentation mechanism, data structures, registration location, and helper functions are implementation details. Preserve the existing HTTP client behavior for logging, tracing, transport configuration, decoration, and request execution while adding the client-side metrics behavior described above.
