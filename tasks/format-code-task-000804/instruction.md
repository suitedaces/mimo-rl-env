## No metric for per-pool available/free space

I'm running `ceph_exporter` to scrape pool stats and feed them into Prometheus + Grafana. For each pool I'm getting `ceph_pool_used_bytes`, `ceph_pool_objects_total`, and the read/write counters from `PoolUsageCollector`, which is great for tracking growth and IO load.

What I can't figure out is **how much room is left in each pool**. The exporter doesn't seem to expose anything for available / free bytes per pool, only consumption.

This becomes a problem when I try to set up "pool is filling up" alerts. I can't just compute `total - used` from cluster-level metrics either, because pools in our cluster have different replication settings and quotas, so the headroom for each pool isn't simply `(cluster free) / (num pools)` — it really is per-pool. `ceph df` reports this number per pool just fine, so the data is there, but the exporter isn't surfacing it.

Could `PoolUsageCollector` be extended to also export a per-pool gauge for the currently available bytes (i.e. how much can still be written into the pool given its replication settings), alongside the existing `used_bytes` / objects / IO metrics? That would let me write a sensible `available / (used + available)` style alert per pool.
