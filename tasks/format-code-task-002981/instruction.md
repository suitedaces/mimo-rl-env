# Track config dependencies in memory so child changes can trigger parent reconciles

Wave watches ConfigMaps and Secrets so that when one of them changes we can
re-reconcile the Deployments / StatefulSets / DaemonSets that consume it. Today
the controllers rely on `EnqueueRequestForOwner`, which only works because we
write owner references onto every child. I want the `Handler` to keep its own
in-memory record of which pod controllers depend on which ConfigMaps/Secrets,
and a controller-runtime event handler that uses that record to fan a child
event out to the interested parents. This is the groundwork for dropping the
owner-reference machinery later.

## What to build

### A per-Handler watch registry

The `Handler` (the type returned by `NewHandler`) must maintain two in-memory
indexes — one for ConfigMaps and one for Secrets. Each index maps a *child*
object to the set of *pod controllers* that currently reference it. Both the
child and the watching instance are identified by their
`k8s.io/apimachinery/pkg/types.NamespacedName`. Expose read access to them:

```go
func (h *Handler) GetWatchedConfigmaps() map[types.NamespacedName]map[types.NamespacedName]bool
func (h *Handler) GetWatchedSecrets()    map[types.NamespacedName]map[types.NamespacedName]bool
```

The outer key is the child's namespaced name; the inner map is the set of
namespaced names of the instances watching that child (membership is indicated
by a `true` value). A freshly constructed `Handler` has both indexes empty.

### Keeping the registry up to date during reconciliation

Reconciling an instance (the existing `HandleDeployment` / `HandleStatefulSet` /
`HandleDaemonSet` entry points) must keep the registry in sync with the
instance's current configuration:

- When an instance that carries the required annotation is reconciled, every
  ConfigMap and Secret it currently references is recorded as watched by that
  instance, in the appropriate index.
- The registry reflects only *current* references. If a subsequent reconcile
  finds that the instance no longer references a child it referenced before,
  that instance must be dropped from that child's watcher set. A child with no
  remaining watchers must disappear from the index entirely (no empty leftover
  entries).
- When an instance does not (or no longer) carries the required annotation, it
  must not appear anywhere in either index.

### Removing an instance explicitly

Provide a way to forget everything about one instance, given its namespaced
name:

```go
func (h *Handler) RemoveWatches(instance types.NamespacedName)
```

After this call the instance must not appear in any watcher set in either
index, and any child left with no watchers must be removed from the index. This
is what a controller calls when its object has been deleted.

### An event handler backed by the registry

Add an exported constructor that turns one of these indexes into a
`sigs.k8s.io/controller-runtime/pkg/handler.EventHandler`:

```go
func EnqueueRequestForWatcher(
    watcherList map[types.NamespacedName]map[types.NamespacedName]bool,
) handler.EventHandler
```

The returned handler reacts to events for child objects (ConfigMaps or Secrets)
by enqueuing a `reconcile.Request` for **every** instance currently watching the
object the event is about, looked up by the object's namespaced name:

- Create, Delete and Generic events enqueue requests for the watchers of the
  event's object.
- Update events consider both the old and the new object, enqueuing the
  watchers of each.
- An event for an object that no watcher is interested in enqueues nothing.

The handler reads through the same map instance it was given, so updates the
`Handler` makes to its registry are visible to a handler created from it.
