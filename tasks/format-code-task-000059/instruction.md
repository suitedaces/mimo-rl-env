I'm running DatadogAgent v2alpha1 and need to control how the operator rolls out the node agent DaemonSet and cluster-agent-related Deployments; right now if I tweak the workload update strategy directly, the operator just reverts it. Can we make that configurable from the DatadogAgent overrides so I can choose the rollout style and tune how aggressive it is?

Expected outcomes:
- DatadogAgent v2alpha1 component overrides should accept an `updateStrategy` setting in the CR, including a strategy type and rolling-update limits.
- When an override sets that strategy, the managed node-agent DaemonSet or cluster-agent-related Deployment should reflect the requested rollout behavior instead of being forced back to the operator default.
- Rolling-update limits for unavailable pods and surge pods should preserve Kubernetes `IntOrString` semantics, so both numeric counts and percentage-style values are accepted and round-trip cleanly.
- Supported strategy values should remain usable in the normal Kubernetes sense for the target workload, including rolling-style and non-rolling-style choices where applicable.
- Unrelated override fields should continue to behave as they do today.

Implementation notes:
- The exact reconciliation structure, helper layout, generated-code organization, and internal data flow are implementation choices.
- Validation, defaulting, and object copying may be organized however is most natural for the codebase, as long as the observable CR/API behavior and resulting workload spec match the expectations above.
