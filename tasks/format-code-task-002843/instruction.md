## Problem Statement

Is there a way to pin the Kubernetes version when I create a kind cluster with ctlptl? I tried setting `kubernetesVersion` in my cluster spec (same as I do for minikube) but it complains that kind doesn't support that field. Would be great if I could just say `kubernetesVersion: v1.19.0` and have it spin up a kind cluster on that version.

## Expected outcomes

- KIND cluster specs accept the existing `kubernetesVersion` field as valid input, in addition to the support already available for minikube.
- When creating a KIND cluster with `kubernetesVersion` set, ctlptl honors the requested Kubernetes version so that the created cluster runs a compatible Kubernetes release.
- Requests for different patch versions within the same supported Kubernetes minor version are treated as requests for that minor version, so patch-level differences do not prevent creating a compatible KIND cluster.
- If ctlptl cannot determine how to satisfy the requested Kubernetes version for the local KIND environment, cluster creation fails with a clear error instead of silently creating an unpinned or incompatible cluster.
- If the requested Kubernetes version is outside the versions ctlptl can support for KIND, cluster creation fails with a clear error explaining that the requested Kubernetes version is unsupported.
- If `kubernetesVersion` is not a parseable Kubernetes version, cluster creation fails with a clear parsing error.
- If ctlptl cannot parse required version information from the local KIND tooling, cluster creation fails with a clear parsing error.

## Implementation notes

- The specific data structures, parsing helpers, KIND invocation details, and validation locations are up to the implementer.
- Preserve existing behavior for KIND clusters that do not set `kubernetesVersion`, and preserve existing minikube support for `kubernetesVersion`.
- Prefer externally observable behavior for validation: accepted cluster specs, subprocess invocation behavior, returned errors, and cluster creation outcomes.

## Required local KIND compatibility fixture (mechanical binding)

Downstream tests mechanically simulate local KIND tooling with `kind version` output `kind v0.9.0`. Implementations MUST treat that local KIND version as supportable for Kubernetes minor `1.19`; additional KIND versions and Kubernetes minors may also be supported.
