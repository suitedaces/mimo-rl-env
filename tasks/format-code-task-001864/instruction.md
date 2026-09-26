## Cannot inject an external `MOCluster` into `lockservice.NewClient`

I'm working on a service that talks to multiple MatrixOne clusters from the same process. In my code I keep a separate `clusterservice.MOCluster` instance per physical cluster, and I route operations to the right one based on which cluster a request belongs to.

When I want to acquire locks against a specific cluster, I do:

```go
c, err := lockservice.NewClient(cfg)
```

The problem is that the client doesn't actually use the `MOCluster` I'm holding — it always resolves the topology against the global one returned by `clusterservice.GetMOCluster()`. So even though my process has, say, two distinct `MOCluster` instances for two clusters, every lockservice client created via `NewClient` ends up looking up `LockServiceAddress` from whichever `MOCluster` happens to be registered as the global singleton. In a multi-cluster process this is ambiguous at best and just routes to the wrong cluster at worst — there's no way for me to say "this client belongs to *that* cluster."

It would be great if `NewClient` let me pass in the `MOCluster` instance I already have, so the client uses the topology I care about. If I don't pass anything, the existing behavior (falling back to the global `MOCluster`) should stay the same so existing callers aren't affected.

I'd expect the entry point to grow something like a functional option, e.g. `NewClient(cfg, WithMOCluster(cluster))`.
