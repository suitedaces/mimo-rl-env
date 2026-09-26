## etcd panics on startup when recovering v3 backend from a snapshot

I run a small etcd cluster in production. Recently one of the members fell behind far enough that the leader had to send it a full snapshot to catch up. After the snapshot was transferred, when that member restarted to apply it, etcd panicked during startup and the node never came back online.

What I see in the logs:

- Normal bootstrap progress, including a line about recovering the v3 backend from a snapshot.
- Right after that, the process panics with what looks like an `assertion failed: tx closed` from the underlying bolt store, and exits.
- The member never finishes bootstrap, so it can't rejoin the cluster.

The data directory does have the `snap.db` from the snapshot transfer present at the time of the crash — the panic seems to happen while etcd is trying to load that snapshot into its v3 backend during bootstrap, not later during normal operation.

The only "workaround" I've found is to wipe the member's data directory entirely and have it rejoin as if it were a fresh node. That's obviously not something we want to do every time a member happens to need a snapshot to catch up — it defeats the point of the snapshot recovery path.

So as far as I can tell, today any member that has to receive a full snapshot from the leader becomes unrecoverable on the next restart without manual intervention. Could someone take a look at the snapshot-recovery path in bootstrap?
