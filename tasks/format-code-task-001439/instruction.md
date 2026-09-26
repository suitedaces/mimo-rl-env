## Migrate node health controller to use the cache

We've been moving controllers off direct calls to the resource service and onto the controller cache. The node health controller (`internal/catalog/internal/controllers/nodehealth`) is still on the old path and should be migrated.

Two things stand out reading the current `Reconcile`:

1. The node lookup is a direct `rt.Client.Read(...)` against the resource service. Every other migrated controller now reads through `rt.Cache`, so this one is inconsistent and avoidably hits the service on every reconcile.

2. `getNodeHealth` calls `rt.Client.ListByOwner` to get *everything* owned by the node, then loops and filters with `resource.EqualType(res.Id.Type, pbcatalog.NodeHealthStatusType)` to pick out just the health statuses. For a node that owns lots of stuff this is wasteful — we pull resources we're going to throw away and we do the type filtering in user code. The cache layer should be able to give us "the `NodeHealthStatus` resources owned by this node" directly, without the post-filter.

Goal: have the node health controller's reconcile path go through the cache for both the node read and the owned-health-statuses lookup, and drop the manual type filtering in `getNodeHealth`. Existing nodehealth controller tests should still pass (some of the error-path tests that depend on forcing failures from the resource service may not be reproducible through the cache and can be dropped if so).
