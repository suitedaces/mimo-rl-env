我现在想按租户把任务的 groupKey 分片，比如 `sync:tenantA`，但默认的 sync/action 这些 worker 只会拉到原来的固定 key，分片后的任务就没人处理了。能不能让这些 worker 按前缀把同一类任务都消费掉，同时我自己建 `ProcessorWorker` 的时候也能传这种自定义的 groupKey/pattern？

Expected outcomes:
- Dequeueing tasks by `groupKey` should support pattern strings containing `*`, so a worker can request a group-key prefix and receive eligible tasks in that family.
- Pattern-based dequeueing should still respect the existing dequeue constraints, including task state, start time, and requested limit, and dequeued tasks should transition as normal.
- Built-in processing workers that currently consume fixed task-family group keys should consume tenant- or suffix-partitioned group keys for their own families.
- Callers should be able to use custom group-key values or group-key pattern values through the existing `ProcessorWorker` constructor path.

Implementation notes:
- The exact matching mechanism, validation location, and internal representation of group-key patterns are implementation details.
- Keep existing exact-key behavior compatible for callers that do not use patterns.
- Do not require callers to use a different public entry point in order to use custom group keys or group-key patterns.
