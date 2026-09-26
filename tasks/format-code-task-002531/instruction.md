## ceph-crash collector pods get restarted on every Rook operator upgrade

I'm running a Rook-Ceph cluster in production and recently bumped the Rook operator to a newer minor version. The Ceph image itself stayed exactly the same — only the operator changed.

Right after the upgrade I noticed that every `rook-ceph-crash-collector-*` pod on every node was rolled (new pod age across the board). The OSDs, mons and mgrs that I expected to potentially be touched were fine, but the crash collectors all restarted, which I wasn't expecting at all — the crash collector is just a passive sidecar that scrapes `/var/lib/ceph/crash`, it has nothing to do with what version of the Rook operator is running.

This isn't a one-off either; it happens on every operator upgrade we do, even patch-level ones where the Ceph version, the crash collector image, env vars, volume mounts, tolerations etc. are all unchanged. From the outside the pod spec looks functionally identical before and after, yet the Deployment decides it needs to roll the pods.

This is annoying for a few reasons:

- During the rollout the cluster temporarily loses crash-collection coverage on whichever nodes are mid-restart.
- On larger clusters (we have a few dozen nodes) it generates a noisy wave of pod churn for no operational benefit.
- It makes operator upgrades look more disruptive than they actually are, which makes them harder to justify in a change window.

I'd expect crash collector pods to only be restarted when something that actually affects how the pod runs changes (image, args, env, mounts, resources, tolerations, …). A pure Rook operator version bump, with no change to the crash collector's actual runtime configuration, shouldn't be causing a rolling restart of these pods.
