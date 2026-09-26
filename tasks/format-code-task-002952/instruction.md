## Restore picks up backups that aren't actually in the cluster

I'm running Ark with a couple of `BackupStorageLocation`s configured (one default + one extra). I ran into some behavior around restores that I think is a bug, or at least surprising.

### What I'm seeing

If I create a `Restore` whose `spec.backupName` refers to a backup that does **not** have a corresponding `Backup` resource in my cluster, the restore still proceeds. From the logs it looks like the controller is going out to each backup storage location directly and using whichever one happens to have an object under that name.

Concretely I hit this in two situations:

1. **Backup hasn't been synced into the cluster yet.** I add a storage location that already contains backups from another cluster. Before the sync controller has had a chance to create `Backup` CRs for them, I kick off a `Restore` referencing one of those names. The restore just... runs. There is no `Backup` object I can `kubectl get` for it.

2. **`Backup` was removed from the cluster but still exists in object storage.** Same story — a restore against that name still works, even though `kubectl get backup <name>` returns NotFound.

### Why this is a problem

- The `Restore` ends up pointing at a backup that nothing else in the cluster can see, which makes the state really hard to reason about (no `kubectl describe backup`, no listing, etc.).
- With more than one storage location configured, it's not even obvious *which* location served the restore — there's nothing in the `Restore` spec pinning it down, and if two locations happen to contain objects with the same name the picked one feels arbitrary.
- It feels like it's working around the backup-sync controller instead of relying on it. I'd expect sync to be the single thing that decides "this backup exists in this cluster," and restore to just use what sync produced.

### What I'd expect

Restore should only operate on backups that already exist as `Backup` resources in the cluster (i.e. what the sync controller has brought in). If the named backup isn't there, the restore should fail validation with a clear "backup not found" message, the same way a totally bogus name would fail. If I really want to restore something that's only in object storage, I should wait for / trigger a sync first.
