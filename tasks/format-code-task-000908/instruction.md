# Restart single-host task groups as a unit

Evergreen supports *task groups* — a named, ordered set of tasks declared in a
project's configuration. When a task group is configured with `max_hosts: 1`
(a "single-host task group"), all of its tasks are guaranteed to run, in order,
on the same host. Tasks carry the task group's name and its configured max-hosts
value on themselves.

Restarting a single task that belongs to a single-host task group in isolation
is incorrect: because the whole group runs together on one host, the entire
group has to be re-run, not just one member. Right now the task-reset machinery
treats every task independently — it immediately archives the task's current
execution and gives it a fresh one — which leaves the rest of the group behind.

Fix this so that single-host task groups are always restarted as a unit.

Expected behavior:

- A task should be recognizable as belonging to a single-host task group when it
  has a non-empty task group name **and** its task-group max-hosts value is `1`.

- The existing "reset this task when it finishes" request currently only applies
  to display tasks. Extend it so it is also valid to make this request for a
  member of a single-host task group, and it must persist that request on the
  task. Requesting it for a task that is neither a display task nor part of a
  single-host task group must remain an error.

- When a member of a single-host task group is reset/restarted through the normal
  task-reset entry point, the member must **not** be archived and given a fresh
  execution on its own. Instead, the group is flagged to reset, and the actual
  reset is deferred: it only happens once every task in the group has finished.
  If some task in the group is still running when the reset is requested, nothing
  is reset yet (the request is simply recorded on the group, and the already
  finished members keep their current status and execution).

- Once every task in a single-host task group has finished and a reset has been
  requested for the group, the act of the final member finishing (being marked
  ended) must reset the entire group together: every task in the group is
  archived (its current execution is preserved and its execution counter
  incremented) and returned to an un-run, undispatched state, and the
  reset-when-finished request is cleared.

- If no reset has been requested for the group, a member of a single-host task
  group finishing must behave exactly as before: the task ends with its result
  status and the group is left untouched.

These semantics should hold regardless of which user/caller initiates the
restart.
