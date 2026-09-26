## `GET /v3/service_plans` ignores `fields[service_offering.service_broker]`

According to the CF API docs, listing service plans supports a `fields` query parameter that lets you sideload related broker info alongside the plans, e.g.

```
GET /v3/service_plans?fields[service_offering.service_broker]=guid,name
```

The expected response has the plans in `resources` and the related brokers under `included.service_brokers` (with only the requested fields).

Against korifi I get the plans back fine, but the `included` section never contains any broker entries no matter what I pass under `fields[service_offering.service_broker]`. It looks like the parameter is just being dropped — the response is identical to a request without it.

For comparison, `include=service_offering` on the same endpoint does work and populates `included.service_offerings`, so plan-side sideloading is partly there, just not the broker fields variant.

Could korifi honour `fields[service_offering.service_broker]` on the service plans list endpoint and return the matching broker resources under `included`?
