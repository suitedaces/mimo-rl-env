## hypershift-operator goes into a hot reconcile loop when running multiple HostedClusters

I'm running several HostedClusters off a single management cluster with the hypershift-operator. With just one HostedCluster things look fine, but as soon as I have two or more provisioned I see the operator never settle:

- CPU usage on the hypershift-operator pod stays high indefinitely
- The reconcile-rate metrics for the HostedCluster controller keep climbing instead of flattening out once the clusters are up
- Tailing the logs, the controller keeps reconciling over and over even though nothing on my end is changing — no spec edits, no new workloads, the HostedClusters are just sitting there

When I diff some of the objects the operator manages between reconciles, the only thing that's actually changing on disk is an annotation the operator itself writes. It looks like each HostedCluster's reconcile is overwriting that annotation with its own value, which then makes the next HostedCluster's reconcile see drift and write it back — so the two (or more) reconcile loops just keep poking each other forever and nothing converges.

With a single HostedCluster there's no second writer so the loop terminates, which is why this only shows up at >1 cluster. I'd expect the operator to reach a steady state regardless of how many HostedClusters are running on the same management cluster — resources that legitimately don't "belong" to any single HostedCluster shouldn't be getting fought over like this.
