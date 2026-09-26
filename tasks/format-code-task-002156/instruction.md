I'm running `openshift ex sync-groups prune` after deleting a group from LDAP, but the matching OpenShift group is still left behind. The LDAP lookup for that group comes back with no group entries, and with our config that has multiple group lookup methods it looks like one of them is enough to keep the stale group around. I thought maybe my sync config was wrong, but the command exits cleanly and the old group never gets pruned.

Expected outcomes:
- LDAP group existence: when `openshift ex sync-groups prune` checks an LDAP group and the lookup completes without error but returns no group entries, that LDAP group is treated as missing so the corresponding OpenShift group is eligible for pruning.
- Multiple lookup methods: when a sync configuration uses multiple LDAP group lookup methods for the same group, the OpenShift group is retained only when every applicable lookup method confirms that the LDAP group still exists.
- Prune behavior: if any configured LDAP group lookup method cannot find the LDAP group, `openshift ex sync-groups prune` should be able to remove the stale OpenShift group instead of silently preserving it.
- Existing error handling: LDAP lookup failures that already meant "not found" continue to make the group eligible for pruning, while unexpected lookup errors still fail the operation rather than being treated as a missing group.

Implementation notes:
- The specific data structures, helper boundaries, and validation location are up to the implementation.
- The fix should preserve the existing command-line interface and sync configuration format.
- Prefer behavior that is consistent across supported LDAP group lookup styles rather than special-casing a single configuration example.
