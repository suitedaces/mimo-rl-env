### Cluster validation should check more master static pods, and stops flapping on not-yet-ready nodes

When running `kops validate cluster` (especially during rolling-update), I keep seeing the validation result flap, and I think the static-pod checks on masters are too narrow.

Two concrete things I've hit:

**1. Only kube-controller-manager is being checked on masters.**

If `kube-controller-manager` is missing on a master, validation reports `master "X" is missing kube-controller-manager pod`. Good. But I had a case where a master was up and `kube-controller-manager` was running, and validation passed — meanwhile other critical master static pods were not actually present / healthy and nobody noticed until things further downstream broke. From a "is this master actually a working control-plane node" point of view, controller-manager alone isn't sufficient. The other key control-plane static pods on a master should be covered by the same check.

**2. Validation flaps with redundant errors while a node is still coming up.**

During a rolling-update, while a master/node is being replaced and isn't ready yet, `kops validate cluster` produces a wall of failures for that node — including missing-pod errors against the master that's clearly still in the middle of restarting. Each run prints slightly different combinations as pods come and go, so the validation result keeps flipping between "failing for these reasons" and "failing for those reasons" until the node finally settles. It's noisy and makes it hard to tell whether the cluster is actually progressing.

It would be much nicer if the static-pod presence checks didn't fire on nodes that aren't ready yet — those nodes are already being reported as not-ready, no need to also accuse them of missing every static pod.

Together these two cause `kops validate cluster` (and rolling-update's use of it) to both miss real problems and over-report transient ones.
