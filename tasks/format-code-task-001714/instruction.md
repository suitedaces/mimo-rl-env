# Support OCI "modelcar" sidecars for model loading

Today, when an `InferenceService` pod is admitted, model data is provisioned by an
init container that copies the model from the configured `storageUri` into a shared
volume before the serving container starts. For large models this copy dominates the
cold-start time, and the data is re-fetched on every pod start.

We want to support loading the model straight from an OCI image instead. The idea is
to ship the model inside a container image and run that image as a passive "modelcar"
sidecar alongside the serving container, sharing the process namespace so the serving
container can read the model from the sidecar's filesystem (via `/proc`). No copying,
and the image is pulled once per node.

## What to implement

Add an opt-in feature, controlled by the storage-initializer configuration, that
mutates admitted kserve pods as follows.

### Configuration

The storage-initializer config (the `storageInitializer` section of the
inferenceservice config map, parsed as JSON) gains these fields:

- `enableModelcar` (bool): master switch for the feature. Defaults to `false`.
- `cpuModelcar` (string): CPU request/limit for the modelcar sidecar. Defaults to `10m`.
- `memoryModelcar` (string): memory request/limit for the modelcar sidecar. Defaults to `15Mi`.
- `uidModelcar` (integer, optional): if set, the UID the serving container should run as.

The `oci://` scheme must also be accepted as a valid `storageUri` (it is currently
rejected as an unsupported scheme).

### Behavior

When `enableModelcar` is `true` and a pod's resolved storage source URI uses the
`oci://` prefix, the admission mutation must:

- Inject an additional sidecar container named `modelcar` whose image is the OCI
  reference taken from the source URI (everything after the `oci://` prefix, e.g.
  `oci://myrepo/mymodel:1.0` → image `myrepo/mymodel:1.0`). The sidecar requests
  minimal resources: `cpuModelcar` and `memoryModelcar` are applied as **both** the
  request and the limit for CPU and memory respectively, falling back to the defaults
  above when not configured.
- Enable process-namespace sharing on the pod (`shareProcessNamespace: true`).
- Add a shared `emptyDir` volume and mount it into the serving (`kserve-container`)
  container at the parent directory of the model mount path (i.e. at `/mnt`, the
  parent of `/mnt/models`).
- Set the environment variable `MODEL_INIT_MODE=async` on the serving container, so the
  runtime knows the model directory may appear slightly after startup and should wait
  for it.
- If `uidModelcar` is configured, set the serving container's security context to run
  as that UID. If it is not configured, leave the serving container's security context
  untouched.
- Skip the normal storage-initializer init container entirely for this pod — when a
  modelcar is used, no `storage-initializer` init container should be injected.

When the feature is disabled, or when the source URI does not use the `oci://` prefix,
nothing modelcar-related should happen: no `modelcar` container and no process-namespace
sharing.
