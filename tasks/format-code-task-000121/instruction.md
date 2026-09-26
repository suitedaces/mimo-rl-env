# Problem Statement

I'm seeing a weird imbalance with Sarama's round-robin consumer group balancing: if I have several topics with only one or a few partitions each, and the same consumers subscribe to all of them, the first partitions keep landing on the same consumer while others sit idle. Is the round-robin strategy supposed to spread partitions across topics too? It would be great if those topic partitions were distributed more evenly across the group instead of restarting the rotation for each topic.

# Expected outcomes

- Round-robin planning through `BalanceStrategyRoundRobin.Plan(...)` should distribute partitions across topics as part of one continuous round-robin assignment, rather than starting the member rotation over independently for each topic.
- When multiple members subscribe to the same small-partition topics, partitions from different topics should be spread across the eligible members as evenly as the round-robin sequence allows.
- When members have different topic subscriptions, `BalanceStrategyRoundRobin.Plan(...)` should still keep the round-robin progression across topic partitions and assign each partition to an eligible subscribed member, skipping members that are not subscribed to that partition’s topic.

# Implementation notes

- Preserve the existing public strategy surface and observable behavior outside the round-robin assignment semantics described above.
- The concrete data structures, helper functions, and exact location of the assignment logic are implementation choices, as long as the public round-robin plan results match the expected behavior.
