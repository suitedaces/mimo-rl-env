## Read-side processor replays unhandled events on every restart

I'm using Lagom's read-side support (this happens in both Cassandra and JDBC backends, so I think the issue is shared across them, but I noticed it first with `CassandraReadSide`).

My setup is fairly standard:

- A `PersistentEntity` that emits ~6 different event types.
- A read-side processor that only cares about 2 of those event types, so on the `ReadSideHandlerBuilder` I only call `setEventHandler` for those 2 classes. The other 4 event types I deliberately don't register handlers for — I have no projection to update for them.

When I run the service normally, everything looks fine: the 2 event types I care about get projected into my read-side tables.

The problem shows up when I restart the service. After a restart, the read-side processor doesn't resume near the latest offset — it picks up from a much older position and re-streams a large chunk of history. From the logs I can see it's re-processing all the event types I never registered a handler for. Each restart does the same thing.

Concretely, what I observe:

- If a contiguous slice of the event log contains only event types I haven't registered a handler for, the stored offset for my processor doesn't advance past that slice. The next event of a type I *do* handle moves the offset forward, but everything before it in that "unhandled-only" slice stays effectively un-acknowledged.
- After a restart, the processor therefore replays that slice from scratch every time. In one of my tag streams this slice is large (the unhandled events vastly outnumber the handled ones), so startup is slow and the processor spends most of its time re-receiving events it ultimately does nothing with.

My expectation as a user of the API is the opposite: if I don't register a handler for some event type, the processor should treat those events as "seen" and move past them — i.e. they should advance the persisted offset just like handled events do. The whole point of selectively registering handlers is to be able to ignore event types, and ignoring them should not come at the cost of unbounded replay on every restart.

Could read-side processors be changed so that an event with no registered handler still advances the stored offset, instead of leaving it stuck?
