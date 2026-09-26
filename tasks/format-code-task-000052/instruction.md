# Run custom database-initialization SQL after a cluster comes up

Users want a way to have the operator run their own SQL against a freshly
initialized PostgresCluster — e.g. to `CREATE EXTENSION`, seed reference tables,
or create application objects — without manually `exec`-ing into a pod. We want
to support pointing the cluster at a ConfigMap that holds a SQL file and have
the operator execute it once the cluster is running.

## API

Add an optional field to the `PostgresCluster` **spec** called `databaseInitSQL`.
It is an object that references a ConfigMap living in the same namespace as the
cluster, with two required string sub-fields:

- `name` — the name of the ConfigMap.
- `key`  — the data key inside that ConfigMap whose value is the SQL to run.

Add an optional **status** field, also called `databaseInitSQL` (a string). Its
presence records that the initialization SQL has been applied successfully.

Both new types must support the project's deep-copy conventions (copying a
cluster must produce an independent copy of these values).

## Behavior

Hook this into the reconcile loop as an additional step. Expose that step as a
method on the reconciler with the signature

```go
func (r *Reconciler) reconcileDatabaseInitSQL(ctx context.Context,
    cluster *v1beta1.PostgresCluster, instances *observedInstances) error
```

so it can be driven directly. The `instances` argument is the set of observed
instances for the cluster. The step must behave as follows:

- **Spec absent.** If `spec.databaseInitSQL` is not set, the status field must be
  cleared (set back to nil) and the step returns without doing anything else. In
  particular it must never try to execute SQL.

- **Already applied.** If `spec.databaseInitSQL` is set but the status field is
  already set, the step is a no-op: it must not execute SQL and must leave the
  status unchanged.

- **Needs applying.** If `spec.databaseInitSQL` is set and the status is not yet
  set, the step attempts to apply the SQL:
  - Fetch the named ConfigMap from the cluster's namespace. If it cannot be
    fetched, return that error (e.g. a not-found error from the API surfaces
    unchanged) without executing SQL.
  - If the ConfigMap exists but does not contain the requested `key`, return an
    error whose message identifies the missing key, without executing SQL.
  - Find the instance that is running, non-terminating, and writable (the
    primary), and execute the SQL string against its database container, passing
    the SQL on standard input. If no such instance is currently available, the
    step returns without error and without setting the status (so it is retried
    on a later reconcile).
  - If execution succeeds, set the status field so the SQL will not run again.
    If execution fails, return the error and leave the status unset so it is
    retried.

Because the status can be lost or the field re-added, the SQL may run more than
once; that is acceptable and is the user's responsibility to make idempotent.
