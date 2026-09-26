### Feature request: expose Cilium's `enable-host-reachable-services` in the cluster spec

We recently upgraded Cilium to 1.8 on a kops-managed cluster and ran into a total outage. Cilium agents started spamming errors like:

```
level=error msg="endpoint regeneration failed" containerID= datapathPolicyRevision=0 desiredPolicyRevision=1 endpointID=592 error="Failed to load tc filter: exit status 1" identity=40147 ipv4= ipv6= k8sPodName=/ subsys=endpoint
```

After digging around we found a Cilium slack thread (https://cilium.slack.com/archives/C1MATJ5U5/p1616400216167600) recommending that the `enable-host-reachable-services` option be turned on. We confirmed that flipping that value to `true` in Cilium's ConfigMap fixes our problem.

The issue is that there's currently no way to set this through the kops cluster spec — the `networking.cilium` section doesn't have a field for it, so we have to manually edit the rendered Cilium ConfigMap after each `kops update`, which doesn't survive upgrades.

It would be great if kops let us configure this from the Cilium networking spec directly (defaulting to off so existing clusters aren't affected), and rendered it through to the Cilium ConfigMap when set. Reference for what the option does: https://docs.cilium.io/en/v1.9/gettingstarted/host-services/

We'd also appreciate this being backported once it lands.
