## Watch API on Postgres occasionally reports namespace modifications as deletions, corrupting the schema cache

We're running SpiceDB in production with Postgres as the datastore, and we have the experimental schema cache enabled (the one that's driven by the Watch API). After running for a while, we start seeing requests fail with errors like:

```
unknown namespace "document"
```

…even though the namespace is clearly still defined — `zed schema read` against the same cluster shows it's there. Restarting SpiceDB clears the cache and the errors go away, but they come back after some more schema activity.

While digging into this we started subscribing to the Watch API directly to see what events were actually being emitted when our team edits the schema. What we observed is that **a plain modification to a namespace** (e.g. adding a new relation to an existing `document` namespace and writing the updated schema) sometimes shows up on the Watch stream as a **deletion event for that namespace**, instead of as a "definition changed" event. It's not consistent — the same kind of edit will sometimes correctly come through as "changed" and sometimes incorrectly come through as "deleted". We haven't been able to find a reliable repro on demand; it feels like a race / ordering thing inside SpiceDB.

This obviously breaks the schema cache: it sees the spurious deletion event, drops the namespace from its cache, and then subsequent permission checks against that namespace fail with "unknown namespace" until something else forces a refresh.

A few extra data points:

- We **only** see this on clusters using Postgres as the datastore. We have another cluster on CockroachDB and have never reproduced it there — Watch events for schema edits on CRDB always look correct.
- The user never actually deleted the namespace. There is no `DeleteNamespace` / `WriteSchema`-with-namespace-removed in the audit log around the time of the bad event. The schema modification was a pure edit.
- Because the cache is wrong, end users hit the failure even though the schema in the datastore is fine, which makes this pretty painful to operate around.

Expected behavior: when a namespace (or caveat) is modified in a single transaction, the Watch API should consistently emit it as a definition change, regardless of which datastore backend is in use. It shouldn't sometimes look like a delete just because of how the underlying datastore happens to surface the update.
