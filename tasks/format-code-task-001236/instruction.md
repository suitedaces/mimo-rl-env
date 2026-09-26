## Shoot deletion blocks on `List`-ing resources whose API endpoint is already gone

We're hitting an issue during shoot deletion where the generic resource cleanup in `pkg/utils/kubernetes/client` refuses to make progress.

Scenario: by the time the cleanup pass runs, some of the aggregated/extension API endpoints on the cluster are already torn down. When the cleanup tries to `List` resources of those kinds, the apiserver returns a 404 for the whole collection — i.e. there's literally no such API serving anymore, so semantically there is nothing left to clean up.

The cleanup helpers, however, propagate that 404 as a fatal error. So `Clean` / `EnsureGone` for those object lists never succeed, and shoot deletion stalls on resources that are already, by any reasonable definition, gone.

The closely related case where the kind isn't registered at the apiserver at all (no matching REST mapping) is already handled — those errors are swallowed and the cleanup correctly treats the collection as empty. It seems inconsistent that "kind not known to discovery" is treated as "nothing to do" while "kind's API endpoint no longer there" is treated as a hard failure: from the operator's point of view both mean the same thing (the resources can't possibly still exist).

Expectation: when the cleanup / ensure-gone helpers encounter that situation while listing or fetching the target object(s), they should consider the work done and let deletion proceed, the same way they already do for unknown kinds. The same reasoning applies to the single-object `Get` paths used by the per-object cleanup action.
