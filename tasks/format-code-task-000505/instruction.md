## LoginNodes should fall back to HeadNode's SSH key when no Ssh section is provided

I'm setting up a Slurm cluster with both a HeadNode and a LoginNodes pool. I want to access everything (head node and login nodes) with the same SSH key, so my config looks roughly like:

```yaml
HeadNode:
  InstanceType: t2.micro
  Networking:
    SubnetId: subnet-xxxxxxxx
  Ssh:
    KeyName: my-key
LoginNodes:
  Pools:
    - Name: pool1
      InstanceType: t2.micro
      Count: 1
      Networking:
        SubnetIds:
          - subnet-xxxxxxxx
Scheduling:
  Scheduler: slurm
  ...
```

When I run `pcluster create-cluster` with this, validation rejects the config because the `Ssh` block under each LoginNodes pool is treated as required — I have to repeat `Ssh: KeyName: my-key` on every pool even though I already declared the same key for the HeadNode.

This feels redundant. In the common case where the operator just wants one key for the whole cluster, the HeadNode's `KeyName` is already enough information. Could the LoginNodes `Ssh` (or at least its `KeyName`) be made optional, so that omitting it just reuses what's configured for the HeadNode? Explicitly setting a different `KeyName` on a LoginNodes pool should of course still work and override that fallback.
