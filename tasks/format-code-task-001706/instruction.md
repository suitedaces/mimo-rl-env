## Batch resources stop being updated on the node when a pod requests fractional memory like `0.1Gi`

I'm running Koordinator on my cluster for colocation and I noticed that
sometimes the BE batch resources on a node (`kubernetes.io/batch-cpu`,
`kubernetes.io/batch-memory` under `Status.Capacity` /
`Status.Allocatable`) just stop refreshing — they stay stuck at an old
value instead of tracking the live colocation calculation.

### How to reproduce

1. Schedule a pod with a memory request that doesn't land on a clean
   integer number of bytes, e.g. `memory: 0.1Gi`.
2. Wait for the next node-resource sync and check the node's
   `Status.Capacity` / `Status.Allocatable` — `batch-memory` is not
   moving.
3. Look at the `koord-manager` `noderesource-controller` logs: every
   reconcile cycle is logging something along the lines of "memory
   quantity ... is not int64" / "cpu quantity ... is not int64", and
   the update is being aborted.

### What I expected

A weird-looking pod request shouldn't bring batch resource sync on the
whole node to a halt. Even if the calculated batch quantity can't be
represented exactly in the units the controller wants to write, I'd
expect the controller to still publish a reasonable value to the node
(and maybe just log that something had to be adjusted), so colocation
keeps working. Right now one fractional request is enough to silently
freeze the batch resources of a node, which is pretty surprising
behavior.
