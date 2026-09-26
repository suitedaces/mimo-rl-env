## Problem Statement

Is there any way to have Volcano automatically clean up jobs after they finish? Right now completed and failed jobs just pile up and I have to go delete them by hand, which is annoying when I'm running a lot of short jobs. Ideally I'd like to set some kind of TTL per job so it gets garbage collected on its own once it's been done for a while.

## Expected outcomes

- Volcano Jobs support an optional per-job `spec.ttlSecondsAfterFinished` setting. When the field is omitted, the Job keeps the existing behavior and is not automatically removed because of TTL.
- A finished Job that has `spec.ttlSecondsAfterFinished` set is eligible for automatic deletion after it has remained finished for the configured number of seconds.
- A Job with `spec.ttlSecondsAfterFinished: 0` becomes eligible for deletion immediately after it reaches a finished state.
- Both successfully completed and failed Jobs are treated as finished for this cleanup behavior.
- The standard Volcano controller-manager run path enables the cleanup behavior without requiring users to manually run a separate one-off cleanup command.
- Job status exposes `status.state.lastTransitionTime` so clients can observe when the Job last entered its current state, including finished states used for TTL timing.

## Implementation notes

- The specific controller structure, queueing strategy, retry behavior, and cleanup scheduling mechanism are implementation details, as long as the externally observable Job API and automatic cleanup behavior match the outcomes above.
- The implementation should follow existing Volcano and Kubernetes controller conventions for API type changes, status updates, and deletion through the API server.
- Tests and callers should rely on public Job API fields and observable object lifecycle behavior rather than private helper names or internal control flow.
