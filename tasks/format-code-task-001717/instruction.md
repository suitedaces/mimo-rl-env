# Track pending cluster operations as an ordered queue on the Cluster

When a user asks to add or remove nodes (or triggers any other long-running
cluster operation), we want to stop kicking the work off immediately and
instead **record the request on the cluster object** so a controller can pick
it up and run the operations one at a time, in the order they were submitted.

Extend the core `Cluster` API type (the `v1` cluster scheme type in the
`core.kubeclipper.io` group) so a cluster can carry a queue of *pending
operations*.

## Public surface to add

A serializable value type describing one queued request:

```go
type PendingOperation struct {
    OperationID   string   `json:"operationID,omitempty"`
    OperationType string   `json:"operationType,omitempty"`
    Nodes         []string `json:"nodes,omitempty"`
}
```

`Cluster` gains an exported, JSON-serializable slice field holding the ordered
queue:

```go
PendingOperations []PendingOperation
```

And the following methods on `*Cluster` to manage that queue:

```go
func (c *Cluster) AddPendingOperation(op PendingOperation) error
func (c *Cluster) NextPendingOperation() (PendingOperation, bool)
func (c *Cluster) RemovePendingOperation(operationID string)
```

## Behavior

- `AddPendingOperation` appends to the queue, preserving submission order (new
  entries go to the back). It must reject the request with a non-nil error — and
  leave the queue exactly as it was — in either of these cases:
  - `op.OperationType` is empty;
  - the cluster already has a pending operation of the **same type** (operations
    of the same type may not be queued concurrently). Two operations of
    *different* types may coexist in the queue.

  A successful enqueue returns a nil error.

- `NextPendingOperation` returns the oldest still-pending operation and `true`,
  without mutating the queue. On an empty queue it returns the zero value and
  `false`.

- `RemovePendingOperation` drops the entry whose `OperationID` matches, keeping
  the relative order of the remaining entries. It is idempotent: removing an id
  that is not present, or removing from an empty queue, is a no-op and must not
  panic.

The `Cluster` type already participates in Kubernetes-style deep copying; the
new field must be handled so that a deep-copied cluster does not share the
underlying queue with the original (mutating one queue must not affect the
other).
