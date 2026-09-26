## Index name support should be folded into the main `client` package, drop the experimental `v2` package

Right now the SDK ships two parallel client packages and it's confusing:

- The main `client.Client` (v1) covers everything but its index APIs — `CreateIndex` / `DescribeIndex` / `DropIndex` / `GetIndexState` / `GetIndexBuildProgress` — take only a `(collName, fieldName)` pair and have no way to refer to a specific index by name. The comments on these methods literally say "currently index naming is not supported, so only one index on vector field is supported", so today there is no path to manage a named index from the supported client.

- A separate `client/v2` package exists solely to add index-name support. It re-declares the whole `Client` interface, re-implements index methods with a totally different style (no `collName` / `fieldName` positional args at all, everything is passed via a long list of `SetCollectionNameForCreateIndex` / `SetFieldNameForCreateIndex` / `SetIndexNameForCreateIndex` functional options), and there's a separate `examples/index/index_v2` demonstrating it. Using the v2 client means giving up on the more ergonomic v1 signatures just to be able to name an index.

This split has been causing friction:

1. Users of the main client cannot specify an index name at all, even though the Milvus server supports it.
2. Users who do need named indexes have to import `client/v2`, switch to a different `Client` interface, and rewrite call sites in the much more verbose option-only style — even for the parts that have nothing to do with index naming.
3. Maintenance-wise, every index change has to be made twice and the two surfaces drift.

I'd like the index-name capability to live on the main `client.Client` itself, in a way that doesn't break existing `CreateIndex(ctx, coll, field, idx, async)` / `DescribeIndex(ctx, coll, field)` / `DropIndex(ctx, coll, field)` / `GetIndexState(ctx, coll, field)` call sites — callers who don't care about index names should not have to change anything, callers who do should be able to opt in. Once that's in place, the `client/v2` package (and its example) is redundant and should go away so there's only one Client to learn.

The opt-in knob I'd expect to use at the call site is something like `WithIndexName("...")`.
