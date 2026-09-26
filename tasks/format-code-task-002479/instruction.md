# Detect unreachable nodes for self-healing node pools

We're building a self-healing capability for node pools: when a managed node becomes
unreachable for too long, the controller should delete it (so it can be recreated). Before
wiring that into the controller, we need the detection logic to live as reusable, well-tested
helpers in the repository's shared node utility package (the one that already holds pure helpers
operating on a Rancher node object, e.g. matching a Kubernetes node to its Rancher node — under
`pkg/node`).

Add two exported helper functions that operate on a Rancher node (`*v3.Node` from
`github.com/rancher/types/apis/management.cattle.io/v3`).

## `IsNodeUnreachable(machine *v3.Node) bool`

Reports whether the node is currently considered unreachable. A node is unreachable when **both**
of the following hold:

- It carries the standard Kubernetes unreachable taint — key `node.kubernetes.io/unreachable`
  with effect `NoExecute`. Taint matching follows Kubernetes semantics: a taint counts only when
  both its key and effect match (the taint value is irrelevant). A taint that shares the key but
  has a different effect (e.g. `NoSchedule`) does **not** count.
- Its Kubernetes `Ready` condition currently has status `Unknown`.

If either is missing — no matching taint, or the `Ready` condition is `True`/`False`/absent — the
function returns `false`.

## `ShouldDeleteUnreachableNode(machine *v3.Node, timeout time.Duration) bool`

Reports whether an unreachable node has stayed unreachable long enough that it should be deleted.
It returns `true` only when **all** of the following hold:

- `timeout` is greater than zero. A `timeout` of zero or negative means self-healing is disabled,
  so the function always returns `false`.
- The node is unreachable (same meaning as `IsNodeUnreachable`).
- The unreachable taint records the time it was added, and the elapsed time since then is greater
  than `timeout`.

Otherwise it returns `false`. In particular, if the unreachable taint has no recorded add-time,
the elapsed time cannot be determined and the function returns `false`, regardless of `timeout`.

Both helpers must be safe to call on nodes with missing/empty taint lists and condition lists.
