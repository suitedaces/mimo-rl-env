# Add IPv6 support to the ip-masq-agent

The eBPF ip-masq-agent watches a configuration file and provisions the set of
"non-masquerade" CIDRs (destinations that pod traffic should reach without
being source-NAT'd). Today this only works for IPv4: the `nonMasqueradeCIDRs`
list rejects any IPv6 prefix, and the only link-local handling is for IPv4.

Extend the agent so it can manage IPv6 destinations as well.

## What it should do

- The `nonMasqueradeCIDRs` list must accept IPv6 prefixes in addition to IPv4.
  Both families are provisioned together from a single configuration, and each
  CIDR is stored in its canonical network form (host bits cleared), exactly as
  IPv4 entries already are — e.g. `2001:db8::1/32` is provisioned as
  `2001:db8::/32`.

- Add a new optional boolean configuration key `masqLinkLocalIPv6` that mirrors
  the existing `masqLinkLocal` key but for the IPv6 link-local prefix
  `fe80::/10`. When `masqLinkLocalIPv6` is explicitly set to `false`, then
  `fe80::/10` is appended to the non-masquerade set. When the key is absent or
  set to `true`, `fe80::/10` is not added. (Defaulting the absent case to "not
  added" keeps the behavior of existing IPv4-only deployments unchanged.)

- The existing IPv4 link-local behavior is unchanged and independent of the new
  option: when `masqLinkLocal` is absent or `false`, `169.254.0.0/16` is part of
  the non-masquerade set; when it is `true`, it is not.

The configuration may be written as YAML or JSON, as it is today. When the
configuration file is missing or empty, the agent keeps provisioning the
existing default IPv4 non-masquerade CIDRs (plus the IPv4 link-local prefix),
and does not add the IPv6 link-local prefix.
