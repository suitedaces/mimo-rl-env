## Add subnet-level metrics for canister snapshot usage

We're operating an IC subnet and starting to see real use of the canister snapshot feature. From the operator side, snapshots are a resource users can create that consumes subnet memory, with per-canister limits — basically the same shape as wasm memory, stable memory, queue memory, cycles balance, etc.

The problem is that snapshots are basically invisible from the subnet's `/metrics` output. We can scrape things like:

- `scheduler_canister_balance_cycles_total`
- `replicated_state_registered_canisters{status=...}`
- canister wasm / stable memory histograms
- queue memory / response bytes

…but there is no aggregate signal for snapshots. We can't answer two pretty basic capacity questions from Prometheus:

1. How many canister snapshots currently exist on this subnet?
2. How much memory are they using in total?

Both questions matter for capacity planning and for alerting (e.g. notice when snapshot memory grows unexpectedly, or when adoption ramps up after a release). Right now the only way to get either number is to walk the replicated state out-of-band, which doesn't help us when we're staring at a Grafana dashboard.

Could the scheduler expose these as subnet-wide gauges, refreshed each round, alongside the other per-round scheduler metrics? That way they show up in the existing scrape and we can graph / alert on them like everything else. To fit our existing dashboards, please expose them under the names `scheduler_canister_snapshots_memory_usage_bytes` (total snapshot memory in bytes) and `scheduler_num_canister_snapshots` (snapshot count).
