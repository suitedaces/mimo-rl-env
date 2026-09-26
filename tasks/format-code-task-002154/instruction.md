## BuildOverrides should support tolerations

We've set up a dedicated pool of nodes for running builds, tainted with something like `dedicated=builds:NoSchedule` so general workloads stay off them. We're already using `BuildOverrides` to pin every build pod to that pool via nodeSelector — but there's no equivalent knob for tolerations, so the build pods never actually schedule. They just sit in Pending because nothing on the pod tolerates the taint on those nodes.

What we'd like is the same pattern nodeSelector and annotations already follow: configure a list of tolerations once in `BuildOverrides`, and have every build pod the cluster creates pick those tolerations up. That way the cluster admin can guarantee builds land on the right nodes regardless of what individual BuildConfig authors do (or don't) put in their own configs.

Right now the only workaround is asking every BuildConfig author to add the tolerations themselves on each build, which kind of defeats the point of having a cluster-level `BuildOverrides` mechanism in the first place.
