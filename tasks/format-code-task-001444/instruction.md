### Job summary counters drift from the real allocation states

I'm running a few jobs on a small Nomad cluster and using `nomad status <job>` to keep an eye on what's going on. After allocations cycle through their normal lifecycle (pending → running, completes, restarts, gets marked lost when I take a node down, etc.), the **Summary** block in `nomad status` stops matching reality.

For example, after running a job for a while and bouncing a client node, I'll see something like:

- The allocation list shows N allocations actually running on the remaining nodes,
- but the job summary reports a different number for `Running` / `Starting` / `Lost` / `Complete`.

Sometimes the running count is too high (looks like a previous state never got decremented when the alloc transitioned), sometimes a "lost" count never shows up after I stop a node even though the per-alloc client status correctly flips to lost. Restarting the server doesn't fix it — the summary stays wrong until I redeploy the job.

I can reproduce this most reliably by:

1. Submitting a job with a few task groups / a few instances each.
2. Letting allocs come up so they're all in `running`.
3. Either (a) shutting down a node that is hosting some of those allocs so they get marked lost, or (b) just letting the client report status updates back over a few cycles.
4. Comparing `nomad status <job>` summary counts against the actual allocation list.

The per-allocation `ClientStatus` values look correct in the alloc listing — it's just the aggregated summary on the job that drifts. Once the summary is wrong it stays wrong, which makes the `nomad status` output unreliable for monitoring and for any automation we build on top of it.

The summary should always reflect the current states of the allocations that belong to the job.
