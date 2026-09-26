## Problem Statement

我在 headscale 里用 subnet router，发现只有一个节点 advertise 某个 prefix 的时候，这条路由完全不生效——别的节点的 AllowedIPs 里根本看不到它，必须再起第二个节点 advertise 同一个 prefix 才会被当成 primary 推下去。是我哪里配错了吗？另外顺带发现，如果一个节点只 advertise 了 exit route (0.0.0.0/0)，它也会被算进 primary route 的选举里，看起来怪怪的。

## Expected outcomes

- Subnet route primary selection: when a node advertises a non-exit subnet prefix, that prefix should be eligible for primary routing immediately, even if it is the only node advertising the prefix.
- Route propagation: the node selected as primary for a subnet prefix should expose that prefix through primary route state and through generated node data sent to peers.
- Non-primary subnet routers: a node advertising a subnet prefix should not automatically receive that subnet prefix in its generated AllowedIPs unless it is currently the primary route owner for that prefix.
- Exit route handling: exit-route prefixes such as IPv4 or IPv6 default routes should not participate in subnet primary-route election.
- Exit route propagation: a node with an enabled exit route should still expose the appropriate exit-route prefixes in its generated AllowedIPs independently of subnet primary-route selection.

## Implementation notes

- Keep the fix behavior-focused: the data structures, helper functions, and validation location are implementation details.
- Preserve existing public routing behavior other than the subnet-primary and exit-route semantics described above.
- Tests should validate externally observable routing state and generated node output, not a particular internal map layout or helper call path.
