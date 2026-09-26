# Persist sublattice metadata atomically and track the root dispatch

When the dispatcher runs a workflow that contains sublattices, each sublattice is
itself dispatched and gets its own lattice record in the results database. Two
things are currently awkward about how those records are created.

First, the database column that links a sublattice's lattice record back to the
parent electron that spawned it (`electron_id`) is only filled in *after* the
sublattice has already been written to the database. There is a window during
which a sublattice record exists with no link to its parent, so an interruption
can leave it orphaned. We want the parent electron id to be written in the *same*
insertion that creates the lattice record, not in a later update.

Second, we are about to need a way to identify, for any (sub)lattice in a
hierarchy, the dispatch id of the top-level ("root") workflow that ultimately
kicked everything off. A nested sublattice three levels deep should still be able
to report the dispatch id of the original top-level dispatch.

Please make the following behavior available.

## `root_dispatch_id` on the result object

The result object should expose a read-only `root_dispatch_id`. For a result
object that represents a top-level dispatch, this equals its own dispatch id. A
result object constructed for a given dispatch id reports that same id as its
root dispatch id until it is told otherwise (see the factory below).

## Persisting a parent electron id atomically

Persisting a result object should optionally accept the database id of the parent
electron that spawned this workflow. When provided, that id must be stored on the
lattice record in the very same transaction that first creates the lattice
record — not written by a subsequent update. When it is not provided, the
lattice record's `electron_id` stays null. Persisting a top-level workflow must
continue to behave exactly as before (its `electron_id` is null).

## A factory for building a result object from a serialized lattice

Add a convenience factory, importable as
`covalent._results_manager.result.initialize_result_object`, that constructs and
persists a result object from a JSON-serialized lattice. It takes the JSON
lattice and, optionally, a parent result object and a parent electron id:

```
initialize_result_object(json_lattice, parent_result_object=None, parent_electron_id=None)
```

It must:

- deserialize the lattice and assign the new result object a freshly generated,
  unique dispatch id (two calls never collide);
- initialize the result object's nodes and persist it before returning, passing
  along the parent electron id so it lands atomically on the lattice record as
  described above;
- when a parent result object is supplied (i.e. this lattice is a sublattice),
  make the new result object inherit the parent's `root_dispatch_id` rather than
  using its own dispatch id;
- return the fully constructed result object.

The returned result object's own dispatch id must still be distinct from its
parent's.
