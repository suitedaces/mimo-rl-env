# Deterministic cluster-state translation for the partition mapper

The `mapper` package turns Kafka cluster state into the objects our rebalancing/reassignment
logic consumes. Two pieces of that translation are currently underspecified and need to be made
reliable.

## 1. Stable ordering when building a partition map from topic states

`mapper.PartitionMapFromTopicStates` translates a `kafkaadmin.TopicStates` into a
`*mapper.PartitionMap`. Today the partitions in the returned map come out in whatever order the
underlying maps happen to iterate, so two calls with the same input can produce maps whose
partition lists differ in order. That makes downstream diffs and output noisy and forces every
caller to re-sort.

Make the returned partition map deterministic:

- The `Partitions` list must be sorted ascending by topic name, and within a topic ascending by
  partition ID, regardless of the iteration order of the input.
- Each partition's replica list must preserve the order given in the source partition state
  (the replicas are reported preferred-leader-first; don't reorder them).
- An empty or `nil` `TopicStates` yields an empty but non-`nil` `*PartitionMap` with no
  partitions and a `nil` error.

## 2. Merging stored metrics into broker metadata

Broker metadata assembled from the cluster needs storage metrics (collected out-of-band) merged
in before the planner can use it. Add a way to populate a `mapper.BrokerMetaMap` from a
`mapper.BrokerMetricsMap`:

- For every broker present in the broker-metadata map, look up its entry in the metrics map and
  set the broker's `StorageFree` from it.
- If a broker in the metadata map has no corresponding metrics entry, mark that broker's metadata
  as having incomplete metrics and record an error identifying the broker by its numeric ID. The
  broker's `StorageFree` is left untouched in that case.
- Brokers that appear in the metrics map but not in the metadata map are ignored — they neither
  change anything nor produce an error.
- The returned errors must be ordered ascending by broker ID, with exactly one error per broker
  that is missing metrics. When every broker has metrics, no errors are returned.
- The broker-metadata map is updated in place.

Expose this as a method on `BrokerMetaMap` with the signature
`LoadMetrics(metrics BrokerMetricsMap) []error`.
