## Per-location traffic pricing isn't exposed on `ServerType` / `LoadBalancerType`

Hetzner announced that the traffic pricing model is changing on **2024-08-05**: included traffic and traffic overage prices are no longer global, they're per server type / load balancer type and per location. The pricing API has already been updated to return this — each entry under `server_types[].prices[]` and `load_balancer_types[].prices[]` now includes:

```json
{
  "location": "fsn1",
  "price_hourly": { ... },
  "price_monthly": { ... },
  "included_traffic": 21990232555520,
  "price_per_tb_traffic": { "net": "...", "gross": "..." }
}
```

The problem is that `hcloud-go` silently drops these two fields. If I do something like:

```go
pricing, _, _ := client.Pricing.Get(ctx)
for _, st := range pricing.ServerTypes {
    for _, p := range st.Pricings {
        fmt.Println(p.Location.Name, p.Hourly, p.Monthly)
        // no way to see included traffic or per-TB overage here
    }
}
```

…there's nowhere on `ServerTypeLocationPricing` (or `LoadBalancerTypeLocationPricing`) to read the per-location included traffic or the per-TB traffic price. The same goes for the schema struct used for JSON decoding — it doesn't carry those fields, so even if I unmarshalled the response myself through the schema package I'd lose them.

After 2024-08-05 the existing top-level `Pricing.Traffic.PerTB` and `ServerType.IncludedTraffic` will start reporting 0, so anyone relying on those values today will silently get wrong pricing data unless the SDK exposes the new per-location fields and clearly signals that the old ones are going away.

It would be great if `hcloud-go` could:

1. Surface the new per-location included traffic + per-TB traffic price coming from the API so callers can actually use the new pricing model, and
2. Make it obvious (via the type system / godoc) that the old global traffic fields are on their way out, so users can migrate before they start returning zeros.

The fields I'd expect on the location-pricing structs are something like `IncludedTraffic` and `PerTBTraffic`.
