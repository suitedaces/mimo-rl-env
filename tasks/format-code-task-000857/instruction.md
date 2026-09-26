## Feature request: support spot allocation strategy in `instancesDistribution`

I'm setting up spot nodegroups in eksctl using the `instancesDistribution` block on a NodeGroup. Today I can specify `instanceTypes`, `maxPrice`, `onDemandBaseCapacity`, `onDemandPercentageAboveBaseCapacity`, and `spotInstancePools`, but I don't see a way to control which spot allocation strategy the underlying Auto Scaling Group / MixedInstancesPolicy will use.

The ASG MixedInstancesPolicy supports two allocation strategies for spot:

- `lowest-price` (what you effectively get today, since AWS defaults to it)
- `capacity-optimized` — ASG picks instances from the deepest Spot capacity pools across the configured instance types

The capacity-optimized strategy is what I actually want for production workloads: I give it a broad list of instance types and let ASG pick from the pools least likely to be interrupted. Right now I can't express this through an eksctl config file — I have to drop down to raw CloudFormation or post-hoc edit the ASG, which defeats the point of declaring the nodegroup in eksctl.

Could `instancesDistribution` grow a knob for this? My yaml would look roughly like:

```yaml
nodeGroups:
  - name: ng-capacity-optimized
    minSize: 2
    maxSize: 5
    instancesDistribution:
      instanceTypes: ["t3.small", "t3.medium"]
      maxPrice: 0.017
      onDemandBaseCapacity: 0
      onDemandPercentageAboveBaseCapacity: 50
      # something here to pick capacity-optimized vs lowest-price
```

Behavior I'd expect:

- If I don't set it, nothing changes — eksctl produces the same template as today, and AWS' default kicks in.
- If I do set it, the value flows through to the generated `MixedInstancesPolicy.InstancesDistribution` on the ASG.
- Only the strategies that AWS actually supports should be accepted; anything else should fail validation up front rather than after CloudFormation rejects the stack.
- The strategy and `spotInstancePools` interact in a not-entirely-obvious way at the AWS layer — eksctl should make that interaction sane (e.g. not silently produce a config the AWS API will refuse).

Docs under `usage/spot-instances` and the config schema should mention the new field so people can discover it.
