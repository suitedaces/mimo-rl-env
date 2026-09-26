## Problem Statement

Hey, I'm noticing something weird with starboard. When I run `starboard scan vulnerabilityreports deploy/my-app` from the CLI, the VulnerabilityReport that gets created has the Deployment itself as its owner. But when the starboard operator running in my cluster scans the same Deployment, the report it produces is owned by the current ReplicaSet instead. So I end up with two reports for the same workload that never line up, and anything that looks them up by owner ref gets confused. Same kind of thing happens for Pods controlled by Jobs/CronJobs — the CLI just attributes the report to whatever I passed in, while the operator walks up the chain. Can you take a look?

## Expected outcomes

- CLI-created reports should use the same externally visible report owner that the operator would use for the same built-in Kubernetes workload, instead of always using the object named on the command line.
- Deployment scans should be reported against the Deployment’s active child workload object, so the generated report labels and owner references line up with operator-created reports for that Deployment.
- Workloads reached through normal Kubernetes controller ownership chains, including Pods managed through Job/CronJob-style controllers, should be attributed consistently with the operator’s owner-selection behavior; unmanaged workloads or workloads controlled by unrelated/custom controllers should not be incorrectly reassigned.
- The same owner-resolution behavior should be applied to both vulnerability reports and config-audit reports created by the CLI.
- When a Deployment’s expected active child workload cannot be found, callers should receive a distinguishable not-found condition rather than silently falling back to the Deployment itself.
- Unsupported workload objects should fail with a clear error that identifies the unsupported kind/type.

## Implementation notes

- Keep the fix focused on externally visible report ownership: report labels, owner references, and any public owner-resolution behavior should agree with the operator’s semantics.
- The internal structure, helper names, lookup strategy, and call sites used to perform owner resolution are up to the implementation.
- Use Kubernetes object metadata and controller relationships consistently with existing repository conventions.
