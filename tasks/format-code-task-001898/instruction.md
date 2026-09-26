# Support restarting a ParaView time-series from a checkpoint

When a transient simulation writes its output through MFEM's ParaView data collection,
each call to `Save()` appends one time-step entry to the collection's `.pvd` index file
(the `<DataSet timestep="..." .../>` lines inside `<Collection>`). The index file lets
ParaView animate the run as an ordered series of time steps.

Today there is no good way to *restart* such a run. If a simulation dies at some time and
is relaunched from the most recent checkpoint, the new run constructs a fresh ParaView data
collection with the same name and starts saving again — which recreates the `.pvd` index
from scratch, throwing away every time step that had already been recorded before the
restart. The animation then only contains the post-restart steps.

Add a way to opt a ParaView data collection into a *restart* behavior so that relaunching a
simulation continues the existing time series instead of clobbering it.

Expected behavior:

- Add a public method `void UseRestartMode(bool restart_mode_)` on the ParaView data collection
  to turn restart behavior on or off. Restart behavior is **off by default**, and with it off the
  collection behaves exactly as before: the first `Save()` of a freshly constructed collection
  (re)creates the `.pvd` index, so it contains only the entries written by that collection.

- With restart behavior **on**, the first `Save()` consults any pre-existing `.pvd` index for
  the collection. Every previously recorded time-step entry whose time value is strictly less
  than the collection's current time (the value set via `SetTime()`) is preserved, and every
  entry whose time value is greater than or equal to the current time is discarded. The entry
  being saved is then appended after the preserved ones. Subsequent `Save()` calls append
  normally.

- The net effect: re-saving at a time `t` replaces any earlier record at `t` and drops any
  records that were written for times at or after `t`, while keeping the history before `t`.
  Enabling restart for a collection whose `.pvd` index does not yet exist simply starts a new
  series.

- The resulting `.pvd` index must remain a valid ParaView collection (well-formed XML with the
  `<DataSet .../>` entries enclosed in `<Collection>...</Collection>`), so it can be opened and
  animated directly.
