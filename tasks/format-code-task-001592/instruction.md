## Problem Statement

When I run `istioctl analyze` against my cluster, it doesn't say anything about Service ports that are missing names or named in weird ways — but then Istio silently treats them as TCP and things break in ways that are really hard to debug. Could the analyzer flag Service ports whose names don't follow the `<protocol>[-<suffix>]` convention (or have no name at all)? Even just an info-level warning per offending port would save me a ton of time.

## Expected outcomes

- Running `istioctl analyze` or the equivalent Galley configuration analysis over Kubernetes `Service` resources should emit an Info-level diagnostic for every Service port whose name is absent or does not follow Istio's `<protocol>[-<suffix>]` port naming convention.
- Each offending Service port should produce its own diagnostic, so a Service with multiple offending ports should report multiple findings rather than collapsing them into one.
- The diagnostic should use the public code `IST0118` and should make it clear which offending port was involved, including the port name when present, the numeric service port, and the target port.
- Service ports whose names follow the convention, such as names with a supported protocol prefix and an optional suffix, should not produce this diagnostic.

## Implementation notes

- The exact analyzer structure, helper functions, and validation location are up to the implementer, as long as the behavior is visible through the normal configuration analysis path.
- Reuse existing Istio conventions for determining whether a Service port name represents a supported protocol; do not introduce behavior that conflicts with existing supported port naming semantics.
- The change should integrate cleanly with the existing diagnostic/message infrastructure so that downstream tools can consume the warning like other analysis results.
