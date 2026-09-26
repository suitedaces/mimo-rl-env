# Add Kindnet as a networking provider (spec + validation)

kops should understand [kindnet](https://github.com/aojea/kindnet) as a CNI/networking
provider that users can configure on a cluster. For this change we only need the cluster
**API model** and the **validation** wired up; addon manifests, nodeup, IAM, etc. are out of
scope.

## API model

Add a kindnet option to the internal cluster networking model
(`k8s.io/kops/pkg/apis/kops`). A cluster's networking spec must be able to carry a kindnet
configuration, and that configuration must at minimum expose a masquerade section:

- The networking spec gains a `Kindnet *KindnetNetworkingSpec` field.
- `KindnetNetworkingSpec` carries a `Masquerade *KindnetMasqueradeSpec` field. (You may add
  other kindnet tunables too, but they are not required here.)
- `KindnetMasqueradeSpec` carries:
  - `Enabled *bool`
  - `NonMasqueradeCIDRs []string`

## Validation

Hook kindnet into the existing cluster networking validation so the following holds when a
cluster is validated:

- **Masquerade CIDRs.** When masquerade is enabled (`Masquerade.Enabled` is non-nil and
  `true`), every entry in `NonMasqueradeCIDRs` must be a valid CIDR prefix (IPv4 or IPv6). Any
  entry that does not parse as a CIDR prefix produces an *invalid value* error reported on the
  kindnet networking field path. Empty-string entries are skipped (no error). When masquerade
  is not enabled (`Enabled` is nil or `false`), the CIDR list is not validated at all, even if
  it contains malformed values.

- **Mutual exclusivity.** kindnet is a networking provider like any other: selecting it
  together with another networking provider must be rejected. When kindnet is configured
  alongside another networking option, validation produces a *forbidden* error reported on the
  kindnet networking field path.

A cluster that selects only kindnet with a valid (or empty) masquerade configuration must
validate without any networking errors.
