## Workspace `last_used_at` keeps advancing even when nobody is connected, breaking autostop / dormancy

We rely on inactivity-based automation (autostop, and a dormancy policy that
eventually marks unused workspaces for deletion). After turning those on we
noticed they essentially never fire — workspaces look perpetually "just used"
even when we know for a fact nobody is connected to them.

### What we see

Pick any workspace where the agent is running, then make sure there's nothing
actually interacting with it:

- close VS Code (remote / coder extension)
- close JetBrains Gateway
- exit every `coder ssh` session
- close any web terminal / reconnecting PTY tab in the dashboard

Leave it like that for a while and watch the workspace in the dashboard (or
query `last_used_at` directly). The "last used" timestamp keeps ticking
forward on its own, roughly in sync with the agent's stats reporting cadence,
even though there are zero active sessions of any kind against the agent.

Because `last_used_at` never stops moving, the inactivity clock that
autostop / dormancy depend on never accumulates, and those policies just sit
there doing nothing. Effectively any workspace whose agent is healthy is
considered "in use" forever.

### What we expect

`last_used_at` should track real user activity against the workspace, not
just the fact that the agent process is alive and phoning home. If the user
isn't actually connected through any of the supported session types, the
timestamp should hold steady so the inactivity-based policies can do their
job.
