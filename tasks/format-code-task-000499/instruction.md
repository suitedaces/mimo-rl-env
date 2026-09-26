## Container health status stops updating once container reaches RUNNING

I'm running an ECS task whose container definition has a Docker `HEALTHCHECK` configured (one that flips between `starting` → `healthy` → `unhealthy` depending on a probe). I'd expect the ECS agent to keep my container's health status in sync with what Docker reports, so that `DescribeTasks` and the console reflect the current health.

What I actually see: the health value the agent reports is essentially "whatever Docker happened to say at the moment the container first transitioned to RUNNING", and after that it never moves again, even when the container clearly becomes unhealthy and `docker inspect` shows the new state.

If I tail the agent logs while this is happening, I see a steady stream of lines like:

```
Managed task [...]: redundant container state change. <name> to RUNNING, but already RUNNING
```

…and nothing else. So Docker is delivering events for my container after it reached RUNNING (which makes sense — health transitions are reported as container events), but the agent treats every one of those events as a no-op because the container's known status is already RUNNING. The health info / other metadata riding along with those events appears to just get dropped.

Other metadata that I'd expect to be refreshed for a running container (e.g. what comes back from Docker about the container after start) seems to be affected by the same thing — once the container has settled into RUNNING, the agent stops folding new information into its in-memory container state.

Expected behavior: while a container is sitting in steady-state RUNNING, the agent should still pick up updated info (especially health status) from subsequent Docker container events for that container, instead of treating "RUNNING → RUNNING" events as completely uninteresting. The "redundant state change" log is fine, but the side data on those events shouldn't be thrown away.

Repro is basically:
1. Run a task with a container that has a `HEALTHCHECK` that will eventually flip its health state.
2. Wait until the container is RUNNING.
3. Force the healthcheck to go unhealthy (e.g. break whatever the probe depends on).
4. Observe via the agent introspection / `DescribeTasks` that the agent never reports the new health value.
