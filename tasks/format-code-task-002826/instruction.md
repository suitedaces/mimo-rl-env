## Pubsub generates a lot of unnecessary traffic on long-running nodes

We've been running a few `threadsd` nodes for a while and noticed something off about the pubsub layer.

The way it currently works, every thread that the node knows about ends up with a corresponding pubsub topic. For a long-running node that participates in many threads, this list keeps growing over its lifetime. The problem shows up when a new peer connects: the libp2p pubsub handshake responds with a "hello" packet that enumerates all topics seen so far, and most of those topics are completely irrelevant to whoever just connected. On nodes with high thread counts and a high connection rate, this becomes a non-trivial amount of wasted bandwidth.

For our use case the pubsub channel isn't actually critical — records are also propagated through the normal direct push path, so pubsub is effectively a secondary delivery mechanism. We'd be happy to just turn it off on these nodes.

Right now there doesn't seem to be a way to do that: when the network is constructed via `common.DefaultNetwork` (or directly through `net.NewNetwork`), pubsub is unconditionally initialized inside the server, every existing thread is registered as a topic at startup, and `CreateThread` / `AddThread` / `DeleteThread` / record push all interact with it. There's no knob to skip any of that.

It would be great if pubsub could be made optional at the network level — pass an option in, and the node just doesn't bring up the pubsub subsystem at all (no topics added, no publish on push, no removal on delete). For backwards compatibility with existing setups, the default behavior shouldn't change; it should only be off when explicitly requested. It would also be useful to be able to flip this from the `threadsd` command line, since these are exactly the long-running nodes where the issue hurts the most.

The new knob I'd expect is something like a `common.WithNetPubSub(...)` NetOption that maps to a `PubSub` field on `net.Config`.
