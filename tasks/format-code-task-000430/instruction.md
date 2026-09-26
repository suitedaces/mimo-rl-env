# Replica-aware node selection for the round-robin selector

Our cluster places the shards of a group across the available data nodes using the
round-robin node selector. Today the selector can only tell you which node owns a
given shard. We're adding replication, so a shard now has a primary copy plus zero
or more replicas, and we need the selector to tell us which node owns each copy.

Please extend the round-robin selector so a caller can ask for the node that owns a
specific replica of a shard, identified by a zero-based replica index. Replica `0`
is the primary copy.

Requirements for the observable behavior:

- Asking for the node of a shard **without** specifying a replica must keep working
  exactly as it does now, and must return the same node as asking for replica `0`
  of that shard. Existing callers must not have to change.
- For the same shard, distinct replica indices must map to **distinct** nodes, as
  long as there are at least that many data nodes available. With `N` data nodes,
  the copies for a shard (the primary together with its replicas, replica indices
  `0` through `N-1`) must be spread across `N` different nodes — no two copies of
  the same shard may land on the same node.
- Selection must be deterministic and stable: repeated lookups for the same
  (group, shard, replica) always return the same node, regardless of how many other
  lookups happen in between or in what order.
- The existing error behavior must be preserved for every replica index: if there
  are no data nodes, or the group/shard is unknown, picking any replica of that
  shard must return an error rather than a node.
