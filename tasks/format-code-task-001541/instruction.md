## Rename "transient store" to "protocol state store"

The framework currently exposes a storage provider called `TransientStorageProvider` (e.g. on the framework `Provider`/`Aries` context, with a matching `WithTransientStoreProvider(...)` option). The name is misleading: the data that lives in this store isn't actually transient — it holds protocol state (connection records, per-state snapshots, namespace/threadID mappings, event data used to resume `AcceptExchangeRequest`, etc.) that protocols rely on across messages and across restarts. Several places in the code even already note this, e.g. the `SaveEvent` comment:

```go
// SaveEvent saves event related data for given connection ID
// TODO connection event data shouldn't be transient [Issues #1029]
```

and there's already a tracking TODO on the field itself:

```go
type Aries struct {
    storeProvider storage.Provider
    // TODO Rename transient store to protocol state store
    transientStoreProvider storage.Provider
    ...
}
```

Calling this thing "transient" gives users (and us) the wrong mental model — people reasonably assume they can back it with an in-memory/ephemeral provider and lose nothing important, but in practice protocols like did-exchange, mediator, message pickup, and out-of-band depend on the records stored here to keep working.

We should rename this concept across the codebase to something that reflects what it actually is — a **protocol state** store. That includes the provider interface methods all the protocol services and controller commands depend on, the framework option used to inject it, the field/getter on the framework context, and the corresponding mocks/test helpers. Internal helpers and error messages that currently talk about a "transient store" should be updated to match so the terminology is consistent end-to-end.

No behavioral change is intended — this is purely a naming/terminology fix to stop calling persistent protocol state "transient".
