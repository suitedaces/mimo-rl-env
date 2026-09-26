## `ship update` loses the namespace from state, breaking ClusterRoleBindings

I originally installed a Helm chart with `ship` into a custom namespace (not `default`). Looking at my `state.json` after init, I can see the namespace I picked is recorded there alongside the rest of my install state.

A while later upstream pushed a new chart version, so I ran `ship update` to pull the changes in. The update went through fine and produced a new set of rendered manifests under `base/` and the kustomize overlay.

When I `kubectl apply` the result though, things break for the cluster-scoped RBAC objects. Specifically the `ClusterRoleBinding` that the chart ships with references a `ServiceAccount` subject, and after `ship update` the subject doesn't end up bound to my namespace — so the SA in my namespace never actually gets the cluster role, and the pod that depends on those permissions starts failing once it tries to do cluster-wide reads.

The `RoleBinding` in the same chart looks fine after update, it's only the `ClusterRoleBinding` flavour (where the binding itself isn't namespaced) where the subject ends up pointing somewhere wrong.

If I just `ship init` from scratch into the same namespace, everything renders correctly and the binding lands on the right SA. So it looks like the namespace I configured at init time isn't being carried through the `ship update` flow when manifests are re-rendered.

I'd expect `ship update` to honor the namespace stored in state and produce the same output `ship init` would have produced for that namespace — including subjects of cluster-scoped bindings being pinned to it.
