## EnvoyFilter using deprecated filter names overwrites other EnvoyFilters

We have two `EnvoyFilter` resources targeting the sidecar listeners. One of them uses a legacy/deprecated filter name (e.g. `envoy.http_connection_manager`) in its `match` block to find the HCM and `MERGE` some config into it. The other uses the canonical name (`envoy.filters.network.http_connection_manager`) to patch a different field.

What we observe: after both EnvoyFilters are applied, the patch from the second one disappears — it looks like the two are clobbering each other and only the last one wins. If we rewrite the first EnvoyFilter to use the canonical name instead of the deprecated one, both patches apply correctly and everything works as expected.

So it seems that mixing deprecated and canonical filter names across EnvoyFilters causes them to step on each other, even though Istio is supposed to accept the deprecated names. From a user perspective, two EnvoyFilters that target the same logical filter (one by old name, one by new name) should compose the same way as if both had used the canonical name — neither should be erased.

Repro is essentially:

1. Apply EnvoyFilter A with `match.listener.filterChain.filter.name: envoy.http_connection_manager` (the deprecated name), `MERGE` some config.
2. Apply EnvoyFilter B with `match.listener.filterChain.filter.name: envoy.filters.network.http_connection_manager` (the canonical name), `MERGE` some different config.
3. Inspect the resulting listener config on the sidecar — only one of the two merges is present.

Expected: both merges are applied, regardless of which name spelling each EnvoyFilter uses to refer to the same filter.
