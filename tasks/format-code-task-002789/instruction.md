# Surface state-store health through reconcilers

Right now nothing actively checks whether a `GitStateStore` or `BucketStateStore` is
usable. A store can reference a missing Secret, have bad credentials, or point at an
unreachable backend, and operators only find out indirectly when a `Destination`
fails. We want each state store to continuously report its own health.

Add a controller (reconciler) for each of the `BucketStateStore` and `GitStateStore`
resources that determines readiness by attempting to write to the store, and records
the outcome on the resource's status and as Kubernetes events.

## Readiness check

On every reconcile, a store is considered **ready** only if Kratix can write a probe
file to the root of the backing store. The reconciler must:

1. Fetch the credentials Secret referenced by the store.
2. Build a writer for the store from its spec and that Secret.
3. Use the writer to write a single probe file named `kratix-write-probe.txt` to the
   root of the store (i.e. not under any sub-directory). The file must have
   non-empty, human-readable content; include a timestamp so that the content changes
   between writes.

The store is ready if all three steps succeed; otherwise it is not ready, and the
step that failed determines how the failure is reported.

## Status

Extend the status of both resources so it carries:

- `Status` (serialized as `status`): a string that is `"Ready"` when the store is
  ready and `"NotReady"` otherwise.
- `Conditions` (serialized as `conditions`): a list of `metav1.Condition`. The
  reconciler maintains a single condition of type `Ready` whose `Status`, `Reason`
  and `Message` reflect the latest outcome:

  | Outcome                         | condition Status | Reason                    | Message                                   |
  |---------------------------------|------------------|---------------------------|-------------------------------------------|
  | store is ready                  | `True`           | `StateStoreReady`         | `State store is ready`                    |
  | referenced Secret not found     | `False`          | `SecretNotFound`          | `Secret not found: <error>`               |
  | writer could not be initialised | `False`          | `ErrorInitialisingWriter` | `Error initialising writer: <error>`      |
  | probe file could not be written | `False`          | `ErrorWritingTestFile`    | `Error writing test file: <error>`        |

  `<error>` is the underlying error string from the failed step.

When the reconcile cannot establish readiness, the reconciler must still surface the
underlying error to the caller (i.e. return it) after recording the status.

## Events

Whenever the readiness changes, emit a Kubernetes event on the store:

- Becoming ready: a `Normal` event with reason `Ready` and message
  `<Kind> "<name>" is ready`.
- Becoming not ready: a `Warning` event with reason `NotReady` and message
  `<Kind> "<name>" is not ready: <condition message>`.

`<Kind>` is `BucketStateStore` or `GitStateStore` as appropriate, and `<name>` is the
resource name.

## Behaviour details

- Reconciling a store that does not exist is a no-op: return without error and without
  requeueing.
- Reconciliation must be idempotent. Once the status already reflects the current
  readiness, reconciling again must not rewrite the status or emit duplicate events.

## Public API

Expose the two reconcilers as exported types named `BucketStateStoreReconciler` and
`GitStateStoreReconciler` in the controllers package. Each must be constructible with
these exported fields: a controller-runtime `Client`, a runtime `Scheme`, a
`logr.Logger` named `Log`, and a `record.EventRecorder` named `EventRecorder`; and each
must implement the standard `Reconcile(ctx, ctrl.Request)` method.
