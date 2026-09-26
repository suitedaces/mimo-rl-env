# Problem Statement

Hey, I'm using dd-trace in a long-running Node service and I'm seeing memory creep up over time. When I take a heap snapshot, a lot of it is span tag/metric objects sticking around — they seem to stay alive as long as I hold any reference to a span, even well after the trace has already been flushed and sent. I've also noticed something weird with child spans started after the parent's trace was finished: they end up on what feels like a stale/detached trace instead of continuing on the parent's, so the relationship gets a bit funky. Ideally once a trace is shipped off, all that tag/metric data should be free to GC even if some span ref is still lying around, and a child should just keep using the same trace as its parent without any surprises. Can you take a look?

# Expected outcomes

- Post-flush memory release:
  - After a completed trace has been flushed/sent, retaining references to spans from that trace should not retain their old tag or metric payloads.
  - The flushed trace should no longer keep references to the spans that were part of that completed trace.
  - This cleanup should apply consistently across completed traces that are flushed.

- Parent/child trace continuity:
  - A child span created from a parent span should continue on the same underlying trace as the parent rather than being attached to a detached or reset trace.
  - This should remain true even when the child is created after the parent’s earlier trace work has already completed and been flushed.

# Implementation notes

- The exact cleanup location, data structures, and lifecycle hooks are implementation details; prefer the smallest change that preserves normal trace formatting/sending while allowing already-flushed span metadata to be collected.
- Do not change the user-facing tracing semantics beyond the lifecycle behavior described above.
