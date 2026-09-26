## Feature request: support Apache SkyWalking as a tracing provider

Our observability backend is built around [Apache SkyWalking](https://skywalking.apache.org/) — we already use it to collect traces from our application-side agents (Java, Go, etc.), and we'd like Istio's sidecars to send their distributed traces to the same SkyWalking backend so we have a single place to view end-to-end traces.

Looking at `MeshConfig.extensionProviders`, the available tracing providers right now are Zipkin, Lightstep, Datadog and OpenCensus (and Stackdriver for GCP users). There's no way to point Istio at a SkyWalking backend.

What we'd like:

1. Be able to register a SkyWalking backend as a tracing provider under `extensionProviders`, in the same shape as the other tracing providers — i.e. give it a name and tell Istio where the backend lives (a service address + port). Once registered, picking that provider via Telemetry API / mesh defaults should make the sidecar Envoys actually emit traces to that SkyWalking backend.

2. The usual config validation should apply: if someone leaves the service empty, or uses an invalid port, mesh config validation should reject it just like it does today for Zipkin / Datadog / Lightstep / OpenCensus. Behavior here should feel consistent with the existing tracing providers — no surprises.

3. While we're using SkyWalking, it would be very convenient if `istioctl dashboard` had a `skywalking` subcommand that port-forwards to the SkyWalking UI running in the cluster and opens it in the browser, similar to how `istioctl dashboard jaeger` and `istioctl dashboard zipkin` work today. Right now there's no built-in shortcut for SkyWalking and we end up doing the port-forward by hand every time.

Happy to test against a SkyWalking deployment if someone picks this up.
