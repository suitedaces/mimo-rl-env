## Problem Statement

I'm running DiceDB with `EvictionPolicy` set to `allkeys-lfu`, but it doesn't actually seem to evict based on access frequency — feels like the LFU policy just isn't doing anything. I'd really like keys I hit a lot to stick around and the rarely-touched ones to get kicked out first when memory fills up. Could you make `allkeys-lfu` actually work as a real frequency-based eviction strategy? It'd also be nice if I could tune how fast the frequency counter ramps up via some config, and honestly LFU feels like a saner default than LRU for my workload.

## Expected outcomes

- LFU eviction behavior
  - When `EvictionPolicy` is configured as `allkeys-lfu`, memory-pressure eviction should prefer removing keys with lower observed access frequency.
  - If candidate keys have equivalent access frequency, eviction should fall back to recency so that the longer-idle key is preferred for eviction.
  - Frequently accessed keys should remain more likely to survive eviction than rarely accessed keys across representative workloads, not only for one hard-coded key pattern.

- Default and configuration behavior
  - When no eviction policy is explicitly configured, DiceDB should default to LFU-style all-keys eviction.
  - DiceDB should accept an `allkeys-lfu` eviction policy value alongside the existing eviction policy values.
  - A server configuration option for the LFU counter growth factor should be available, with a default value of `10`.
  - Increasing the LFU counter growth factor should make frequency counter growth slower; decreasing it should make growth faster.

- Counter and recency behavior
  - LFU frequency tracking should remain bounded under repeated access and must not wrap around in a way that makes very frequently accessed keys look rarely used.
  - LFU frequency bookkeeping must not corrupt recency-based idle-time behavior used for LRU ordering or LFU tie-breaking.

## Implementation notes

- The exact data structures, sampling strategy, counter representation, and update locations are implementation choices.
- The LFU implementation may use an approximate frequency counter, but externally observable eviction behavior should match the outcomes above.
- Preserve existing eviction modes other than the requested LFU/default behavior changes.
