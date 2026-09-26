I'm using the Queue plugin and I can push and pop items fine, but once I've popped something and finished processing it, there's no way to actually tell the queue "this one's done, don't hand it out again." On SQS that means messages just come back after the visibility timeout, and on PubSub they never get acked. Can we get a Complete (or ack) method on the QueuePlugin so I can finalize an item by its lease ID, ideally exposed over the gRPC API too so I can call it from my worker?

Expected outcomes:
- Queue plugins provide a public completion/acknowledgement operation for a previously popped item in a specific queue using that item's lease identifier, following the existing queue API style for success and error reporting.
- Supported queue backends implement the same completion behavior: successful completion prevents the backend from re-delivering the leased item, while backend failures or unresolved queues are reported to the caller instead of being silently ignored.
- The local development queue also accepts completion calls so code written against the queue completion contract works consistently in local development.
- The Queue gRPC service exposes a completion endpoint for workers; it forwards the requested queue and lease identifier to the registered queue plugin, reports success when the plugin succeeds, and propagates plugin/registration failures when completion cannot be performed.

Implementation notes:
- Keep the public shape and naming consistent with the existing queue push/pop APIs and generated gRPC conventions in this repository.
- Do not rely on a particular private helper, data structure, validation location, or mock-only mechanism; any implementation that satisfies the public queue plugin and gRPC behavior above is acceptable.
