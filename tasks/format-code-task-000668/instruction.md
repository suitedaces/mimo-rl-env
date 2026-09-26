## Problem Statement

I'm hitting CRD validation errors when Cilium tries to create identity resources in my cluster — the API server rejects them complaining about label names being longer than 63 characters. Looking at the rejected payload, the offending names all seem to come from namespace labels that Cilium is propagating onto the identity (stuff under `io.cilium.k8s.namespace.labels.<some long namespace label key>`), and some of our namespace labels have pretty long keys. New identities aren't getting created because of this. Can you take a look?

## Expected outcomes

- Identity resource creation should not fail merely because a namespace has label keys that would produce overlong Kubernetes label names when propagated onto the identity object.
- Namespace-derived label information should be omitted from the identity object's Kubernetes metadata labels rather than submitted to the API server.
- Normal Kubernetes-sourced labels that are valid for identity metadata should continue to be included on the identity resource.
- Non-Kubernetes label sources should continue to be excluded from the identity resource's Kubernetes metadata labels.
- Existing identity label semantics outside the Kubernetes metadata-label projection should remain unchanged.

## Implementation notes

- Prefer preserving existing behavior for labels unrelated to namespace metadata propagation.
- The fix should be based on externally observable identity creation and label projection behavior, not on a specific refactor shape.
