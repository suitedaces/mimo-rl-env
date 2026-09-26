I'm hitting a weird issue with KubeVirt VMs on ovn-kubernetes after a live migration fails. When the migration aborts, the source virt-launcher pod ends up in Completed state but it sticks around with a creation timestamp that's actually newer than the pod where the VM is really running. After that, the routes for the VM get reconstructed pointing at the wrong pod and traffic to the VM breaks. If I manually delete the leftover completed pod things recover, so it really looks like the stale-pod detection is getting confused by that completed leftover and picking it as the live one.

Expected outcomes:
- A terminal Completed live-migratable virt-launcher pod should no longer be considered the active pod for the VM during stale-pod decisions.
- A lingering completed virt-launcher pod from a failed migration should not hide the pod where the VM is actually running when VM-related routes are reconstructed.
- The fix should not broaden stale handling to unrelated or non-live-migratable pods merely because they are completed.

Implementation notes:
- The exact validation order, helper usage, and data structures are up to the implementation, as long as the externally observable stale-pod decision and route reconstruction behavior match the outcomes above.
- Preserve existing behavior for non-completed live-migratable pods and for pods that are not live-migratable.
