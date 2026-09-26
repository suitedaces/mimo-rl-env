### Bug: ServiceEntries labeled for a different revision are still processed by this istiod

I'm running a canary upgrade with two control planes: `istio.io/rev=stable` and `istio.io/rev=canary`. I expect each istiod to only act on configuration that matches its own revision (which is what `Get`/`List` on the config store already do).

But for event-driven config (ServiceEntry, VirtualService, etc.), this doesn't seem to hold:

1. If I create a `ServiceEntry` with `istio.io/rev: canary`, the **stable** istiod still picks it up — workloads attached to the stable revision end up with endpoints/clusters from that ServiceEntry, even though the resource is clearly tagged for the other revision.

2. If I take a `ServiceEntry` that previously had `istio.io/rev: stable` (or no rev label, defaulting to stable) and edit its label to `istio.io/rev: canary`, the stable istiod still keeps the old config around. From the stable revision's point of view, that resource is no longer ours, so workloads on the stable revision shouldn't see it anymore — but they do.

Listing the configs directly through the store does respect the revision, so this seems specific to the live event path (add / update / delete callbacks coming off the informers, plus whatever runs during the initial sync at startup). Both the steady-state event flow and the bootstrap sync need to honor the revision the same way `List` already does.

Repro is roughly:

```
# two istiods, revisions "stable" and "canary"
kubectl apply -f - <<EOF
apiVersion: networking.istio.io/v1beta1
kind: ServiceEntry
metadata:
  name: example
  namespace: default
  labels:
    istio.io/rev: canary
spec:
  hosts: [example.com]
  ports:
  - number: 80
    name: http
    protocol: HTTP
  resolution: DNS
EOF

# Then inspect a sidecar attached to the *stable* revision:
istioctl proxy-config clusters <pod-on-stable> | grep example.com
# -> shows the cluster, but it shouldn't
```

And for the "moved between revisions" case: start with the label set to stable, let things settle, then patch the label to canary. The stable istiod's view of that workload still contains the entry.

Expected: a control plane should completely ignore resources whose `istio.io/rev` doesn't match it, including resources that *used to* match and have since been re-tagged for a different revision.
