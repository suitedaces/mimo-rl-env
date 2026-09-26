# Open a memiavl database at a historical version

The embedded `memiavl` database (the `memiavl` Go module in this repository) can
currently only be opened at its latest committed version: loading the database
replays the entire write-ahead log, so you always end up at the tip.

We need to be able to open the database **at a specific earlier committed
version**, so that callers can reconstruct the exact state of a past version
(for serving versioned queries, state-sync, etc.) without having to mutate or
roll back the database.

Add a load option that selects the version to open. The observable contract:

- The load options gain a way to request a target version, expressed as an
  unsigned integer.
- When the target version is left at its zero value (the default), loading
  behaves exactly as it does today and opens the latest committed version.
- When a positive target version `v` that exists in the database's committed
  history is requested, the loaded database must reflect exactly the committed
  state as of version `v`: the version it reports is `v`, and its commit hash
  (and therefore its per-store contents) is identical to what it was right after
  version `v` was committed — as if the commits made after `v` had never been
  applied.
- Opening at a target version must be non-destructive: it must not delete or
  rewrite the existing on-disk history, so the same database can afterwards be
  reopened at any other version, including the latest.

The existing latest-version load path and all other database behavior must be
unaffected.
