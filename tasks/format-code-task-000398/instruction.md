## Problem Statement

Hey, I'm running Antrea with the Flow Aggregator and I'd really like a stable way to tag the flow records with a unique cluster ID so I can tell flows from different clusters apart downstream. Right now the shipped manifests do not provide a persistent cluster identity that the Flow Aggregator and other Antrea components can discover and use out of the box. Would be great if this worked across all supported install variants without me having to hand-roll a ConfigMap and ClusterRole myself.

## Expected Outcomes

- Cluster identity storage: all shipped Antrea install manifests expose an initially empty cluster identity `ConfigMap` named `antrea-cluster-identity` in namespace `kube-system`, labeled consistently with Antrea resources.
- Shared read access: the manifests provide a reusable `ClusterRole` named `antrea-cluster-identity-reader` whose permissions are limited to reading the cluster identity `ConfigMap`.
- Controller persistence access: shipped RBAC allows the Antrea Controller to read and update the cluster identity `ConfigMap` while preserving its existing access to related Antrea `ConfigMap` resources.
- Flow Aggregator consumption access: shipped Flow Aggregator RBAC allows the Flow Aggregator ServiceAccount to read the persisted cluster identity through the shared reader role.
- Kustomize base propagation: the base manifest resources include the shared cluster identity reader role so downstream generated install manifests can inherit it.

## Implementation Notes

- Keep the solution focused on externally observable Kubernetes resources and RBAC behavior; the exact manifest organization and generation workflow may follow existing repository conventions.
- RBAC should remain scoped to the cluster identity resource needed by consumers rather than granting broad ConfigMap permissions.
- The cluster identity storage should be reusable by components beyond the Flow Aggregator without requiring users to create custom manifests manually.
