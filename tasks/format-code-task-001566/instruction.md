Send metrics from oldest to newest, always
## Feature Request

### Proposal:

Telegraf should always send metrics point from the older to the newer. During "normal" behavior and while catch-up backlog if an output become slow.

### Current behavior:

Since #5287, when buffer is not empty and contains more than one gather cycle, metrics are sent from newest to older.

### Desired behavior:

Batch() should send oldest metrics and metrics in the batch should be in increasing order of age.

We should still drop the oldest metrics if the buffer become full, so #5194 is still fixed

### Use case:

Currently metric points are not in consistent order. When buffer is empty, the order is from older to newer, but if buffer start to fill, batch with be in the opposite order (newer to older).

In practice, the buffer while often contains few metrics from previous gather cycle, so it may happen even if output is not down.

At the end, that means that the output could not rely on having metrics ordered, which was (mosly) true before #5287.
Having metrics ordered allow to easily do some transformation on the fly (e.g. difference between two point to compute the rate) and generally make working with time series easier.

If this change seems good, I could come with a PR.
