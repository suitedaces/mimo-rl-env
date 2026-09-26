## Pod add/delete triggers a full rewrite of the namespace address_set in OVN

While reading through `pkg/ovn` I noticed that whenever a single pod is added to or removed from a namespace, we end up rewriting the entire OVN `address_set` for that namespace, not just touching the one IP that actually changed.

In `addPodToNamespace` / `deletePodFromNamespace` (and the analogous `handlePeerPodSelectorAddUpdate` / `handlePeerPodSelectorDelete` paths for NetworkPolicy peer selectors), after we mutate the local map we always do something like:

```go
oc.namespaceAddressSet[ns][address] = logicalPort
addresses := make([]string, 0)
for address := range oc.namespaceAddressSet[ns] {
    addresses = append(addresses, address)
}
setAddressSet(hashedAddressSet(ns), addresses)
```

…and `setAddressSet` then shoves the whole concatenated list of IPs into `ovn-nbctl set address_set <name> addresses="..."` (or clears it if the list went empty). The peer-selector handlers in `policy_common.go` do the exact same dance with `addressMap`.

This feels wrong for a couple of reasons:

- It's O(N) work per pod event, where N is the number of pods already in the namespace / matched by the policy. In a namespace with hundreds of pods churning, every single pod event re-serializes every other pod's IP into one big nbctl arg.
- The OVN nbctl tooling already supports modifying an `address_set` one element at a time, so there's no reason the controller has to recompute and resubmit the whole set just to add or drop a single IP.

For a single-pod add or delete, the controller already knows exactly which IP changed — it would be much nicer to just push that one IP as a delta to OVN instead of resending the full set. Could the namespace and peer-pod-selector paths be switched over to incremental updates?
