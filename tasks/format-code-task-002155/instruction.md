## Upgrade jobs flake on duplicate-events test for transient probe / connection refused noise

Upgrade e2e jobs are intermittently failing on the duplicate-events synthetic test because of events that look like normal transient noise while components are rolling to a new revision during the upgrade. Two recurring patterns I keep seeing flagged:

1. Readiness probe timing out talking to a component that's restarting:

   ```
   reason/ProbeError Readiness probe error: Get "https://10.x.x.x:8443/healthz": net/http: request canceled while waiting for connection (Client.Timeout exceeded while awaiting headers)
   ```

2. Connection refused while a component is briefly down:

   ```
   ... dial tcp 10.x.x.x:8443: connect: connection refused
   ```

Both bursts are short — they show up while a pod rolls to its new revision and stop once the new pod is ready. The upgrade itself succeeds and the cluster recovers on its own; only the synthetic test fails the job because those events repeated more than the threshold within the burst.

This kind of churn is expected during an upgrade (a component being unreachable for a few seconds while it restarts is the whole point of a rolling update), so it shouldn't fail upgrade jobs. It should still be caught during a normal (non-upgrade) run though — outside an upgrade these events would be a real signal.

Could we tolerate these two patterns specifically in the upgrade scenario?
