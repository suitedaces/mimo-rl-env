# Persist an old → new commit-hash mapping during migration

When a repository is migrated to the new storage format, every commit is
rewritten and gets a brand-new commit hash. Today there is no way to find out
which migrated commit a given pre-migration hash turned into, which makes it
hard for tooling and users to correlate references, scripts, or external
records against the migrated history.

Extend the migration so that, once it finishes, the migrated database records
the full correspondence between the old and new commit hashes.

The mapping must be discoverable through normal SQL:

- The migrated database has a branch named `dolt_migrated_commits`.
- On that branch there is a table named `dolt_commit_mapping` with two
  `varchar` columns:
  - `old_commit_hash` — the commit's hash before migration; this is the
    primary key and is never null.
  - `new_commit_hash` — the corresponding commit's hash after migration.
- The table contains exactly one row per migrated commit: every commit in the
  migrated history is represented, and `old_commit_hash` values are unique.
- Every `new_commit_hash` is a real commit in the migrated history (i.e. it
  appears in `dolt_log`), and every migrated commit is the target of some row.
- `old_commit_hash` holds the *pre-migration* hash, which is distinct from any
  post-migration commit hash.

A typical way to read the mapping back is a revision-qualified query such as:

```sql
SELECT old_commit_hash, new_commit_hash
FROM `dolt/dolt_migrated_commits`.dolt_commit_mapping;
```

All existing migration behavior — commit-graph traversal, working-set
migration, tag migration, and branch head mapping — must continue to work
unchanged alongside this new persisted artifact.
