## Activating / deactivating individual tasks in a single-host task group leaves the group in an inconsistent state

I'm using a single-host task group (the kind where every task in the group runs sequentially on the same host) and ran into two related issues when I try to manage tasks in the group from the UI.

### Setup

A task group `my_group` containing, in order, `task_a`, `task_b`, `task_c`, configured as single-host (so they all run back-to-back on one host).

### Issue 1: deactivating a task in the middle of the group leaves later tasks "scheduled"

Suppose all three are activated and `task_a` hasn't run yet. I decide I no longer want this run, so from the UI I deactivate `task_b`.

What I expected: since this is a single-host group and `task_c` runs after `task_b` on the same host, deactivating `task_b` should also stop `task_c` from being scheduled — `task_c` literally cannot run if its predecessor in the group has been pulled.

What actually happens: only `task_b` gets deactivated. `task_c` still shows as activated/scheduled in the UI, even though there is no realistic path for it to run anymore. This is confusing — the displayed state does not match what will actually happen.

### Issue 2: re-activating / restarting a task in a group that has already finished doesn't reset the rest of the group

Now suppose the whole group has already run and all of `task_a`, `task_b`, `task_c` are finished. I want to re-run from `task_b` (e.g. I'm restarting an upstream dependency that `task_b` depends on, and that dep is itself in the same task group).

What I expected: because the group is single-host and runs as a unit on one host, re-activating something in the group should bring the already-finished tasks in the same group back to a runnable state, so the group can actually re-execute end-to-end.

What actually happens: the already-finished tasks in the same group are left as-is (still in their finished state), so the activation doesn't translate into the group re-running cleanly. I have to manually go restart the rest of the group to get sane behavior.

### Summary

In both cases the underlying problem is the same: `SetActiveState` on a task that's part of a single-host task group only acts on that one task and ignores the fact that, for a single-host group, the group is effectively atomic — turning one task on/off has implications for the rest of the group on the same host. Could the activation/deactivation path be made aware of single-host task groups so that the group as a whole stays in a consistent state?
