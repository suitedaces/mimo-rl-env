# Problem Statement

Been hitting a few annoying things with client replay in mitmproxy. When I kick off a replay and check how many are pending, the one that's currently running doesn't seem to be counted — feels like it drops to zero too early. Also after a replay finishes the UI just sits there until I poke it, would be nice if it refreshed on its own. And the worst one: if a replay hangs, I can't even quit mitmproxy, have to kill it. Any chance of cleaning these up?

# Expected outcomes

- Client replay progress/counting:
  - `ClientPlayback.count()` should include replay work that is currently in progress, not only items still waiting to be started.
  - Starting client replay with a caller-owned sequence should not consume or mutate that caller-owned container as replay progresses.

- Client replay lifecycle notifications:
  - When a replayed flow finishes, the normal addon/UI update mechanism should be notified without requiring further user interaction.
  - The client replay completion notification should be emitted once when the final replay item has finished, not repeatedly on later idle ticks.

- Shutdown behavior:
  - A client replay operation that hangs or runs indefinitely should not prevent mitmproxy from exiting normally.

- State restoration:
  - Public flow/request state restoration APIs such as `Flow.set_state(state)` and HTTP request `set_state(state)` should not mutate the state dictionary supplied by the caller.

# Implementation notes

- The concrete data structures, lifecycle bookkeeping, and notification placement are implementation details; preserve the externally observable replay, notification, shutdown, and state-restoration behavior described above.
