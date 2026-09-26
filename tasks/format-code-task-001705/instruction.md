# Node allocatable resource amplification

Koordinator already lets operators advertise *amplified* node resources by storing a per-resource
amplification ratio in the node annotation `node.koordinator.sh/resource-amplification-ratio`
(a JSON object such as `{"cpu":1.5,"memory":2}`). What's missing is the piece that actually
reconciles a node's `status.allocatable` against those ratios.

Add a function to the node resource-amplification extension API (the package that already defines
the amplification-ratio and raw-allocatable annotation helpers) with this signature:

```go
func AmplifyNodeAllocatable(node *corev1.Node) error
```

Calling it should bring the node's reported allocatable in line with the configured ratios.

Required behavior:

- **Scope.** Only `cpu` and `memory` are amplifiable. Any other resource named in the ratio map
  (e.g. `nvidia.com/gpu`) is ignored, and other allocatable resources are never changed.

- **Raw baseline.** Amplification must always be computed from the *un-amplified* allocatable, not
  from the current (possibly already-amplified) value. The first time the function amplifies a
  node it must capture the current cpu/memory allocatable as the raw baseline and persist it in the
  `node.koordinator.sh/raw-allocatable` annotation. On later calls, when that annotation is already
  present, its stored values are used as the baseline. This makes the function idempotent: invoking
  it repeatedly yields the same allocatable rather than compounding the ratio.

- **Computation.** For each of cpu and memory, when a ratio greater than 1 is configured and a raw
  baseline value exists for it, the resulting allocatable is the baseline value scaled by the
  ratio. A ratio of 1 or less, or a missing baseline value for that resource, leaves the
  allocatable for that resource untouched.

- **Disabled.** When the amplification-ratio annotation is absent or empty, the feature is off: any
  previously stored `node.koordinator.sh/raw-allocatable` annotation must be removed and the
  allocatable must be left exactly as-is.

- **No allocatable.** If the node reports no allocatable at all, there is nothing to do and no raw
  baseline is recorded.

- **Errors.** A malformed amplification-ratio annotation (or a malformed stored raw-allocatable
  annotation) must surface as a returned error.

The change should not regress any of the existing amplification annotation helpers.
