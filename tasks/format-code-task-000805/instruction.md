## Problem Statement

I just ran `doctl kubernetes cluster node-pool update <pool-id>` to change the pool's labels and my pool got resized to 0 nodes — I didn't pass `--count` at all. Same thing seems to happen with `doctl kubernetes cluster update`: if I don't pass `--auto-upgrade`, auto-upgrade gets turned off on the cluster even though I never touched that flag. Can you take a look?

## Expected Outcomes

- Kubernetes cluster updates preserve the existing auto-upgrade setting when `doctl kubernetes cluster update` is run without `--auto-upgrade`.
- Kubernetes cluster updates still apply an explicit `--auto-upgrade=true` or `--auto-upgrade=false` value when the user passes that flag.
- Kubernetes node pool updates preserve the existing node count when `doctl kubernetes cluster node-pool update` is run without `--count`.
- Kubernetes node pool updates still apply an explicit `--count` value when the user passes that flag.

## Implementation Notes

Updates should only modify fields that the user actually requested to change. The specific data structures, helper methods, validation location, and request-building approach are up to the implementation, as long as the externally observable CLI behavior above is satisfied.
