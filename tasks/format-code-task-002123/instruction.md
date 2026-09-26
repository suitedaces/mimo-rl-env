## Duplicate instrument detection is case-sensitive, but instrument names should be case-insensitive

I'm using `go.opentelemetry.io/otel/sdk/metric` to instrument a service. We have two modules independently registering metrics on the same Meter, and one of them accidentally created a counter with a different capitalization than the other — something like:

```go
meter := provider.Meter("my-app")

// somewhere in module A
reqs, _ := meter.Int64Counter("http.server.requests",
    metric.WithDescription("incoming requests"),
    metric.WithUnit("{request}"),
)

// somewhere in module B (different team, didn't realize)
reqs2, _ := meter.Int64Counter("HTTP.Server.Requests",
    metric.WithDescription("requests handled"),
    metric.WithUnit("1"),
)
```

I expected this to trigger the same "duplicate metric stream definitions" warning that I get if I literally re-register the exact same name twice with different units/descriptions. Per the OpenTelemetry specification, instrument names are supposed to be case-insensitive, so `http.server.requests` and `HTTP.Server.Requests` refer to the same instrument.

But the SDK silently accepts both. No warning is logged. Both instruments end up live, which then causes problems downstream — different exporters do different things when they see two streams that the backend considers the same series, and either way it's a misconfiguration the SDK should be telling me about.

Could the duplicate-instrument detection treat names as case-insensitive so that conflicting registrations like the above get flagged the same way exact-match duplicates already are?
