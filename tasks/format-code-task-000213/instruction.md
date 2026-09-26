I’m starting a flow run from Prefect Cloud with a custom context value like `my_var`, but inside the flow and tasks `prefect.context.get("my_var")` is coming back as `None`. I also noticed `Client.get_flow_run_info(...)` gives me the run info but doesn’t show that context value, even though I can see it set on the Cloud run, so I’m not sure if I’m passing it wrong or if it’s getting lost somewhere.

**Expected outcomes**
- Cloud flow runs should make the stored per-run context available during execution, so flow code and task code can read custom values through `prefect.context`.
- If Cloud context includes keys that are also part of the runner-populated runtime context, including scheduled start time and flow run version metadata, the runtime-generated values should still win for those keys.
- `Client.get_flow_run_info(flow_run_id: str)` should expose the flow run’s stored context through the returned `FlowRunInfoResult`.
- `FlowRunInfoResult` should carry the flow run’s context together with the other run metadata already returned by the client.

**Implementation notes**
- The exact place where the Cloud context is fetched, merged, and serialized is up to the implementation.
- Keep existing behavior for unrelated flow-run metadata and failure handling unless it is required to satisfy the outcomes above.
- Any internal data structures, helper functions, and merge mechanics may vary as long as the externally observable behavior matches the outcomes.
