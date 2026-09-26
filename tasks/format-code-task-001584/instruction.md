I'm hitting a netlab validation gap around management addressing: with clab/libvirt topologies, nodes with missing management IPs, management IPs outside `addressing.mgmt`, or an IPv6/IPv4 mgmt address when the matching mgmt prefix isn't defined can get through `netlab create` and then fail later in containerlab/libvirt or end up unreachable. I also noticed `addressing.mgmt.ipv6_pfx` rejects a `/64` with `IPv6 pool prefix cannot be longer than /56`, even though this is the mgmt pool.

Expected outcomes:
- Management IPv6 pool validation should allow management IPv6 prefixes that are appropriate for node management networks, including `/64`, without weakening the existing IPv6 prefix-length validation for non-management address pools.
- For clab and libvirt topologies, invalid management-addressing configurations should be rejected during topology validation/conversion, before provider output or runtime execution. The validation should follow the provider’s management-connectivity requirements and cover missing usable management addressing, missing matching management-pool prefixes for configured management address families, and management addresses that do not belong to the configured management subnet.
- Report these failures as clear user-facing provider-specific errors that let the user identify the node, the relevant address family when applicable, and why the management addressing is invalid.

Implementation notes:
- The exact validation location, helper structure, data-flow organization, and address-containment mechanism are up to the implementer.
- Preserve existing behavior for providers and address pools outside the management-addressing cases described above.
- Error reporting should be actionable, but exact wording, internal helper names, log categories, and call sites are not prescribed.
