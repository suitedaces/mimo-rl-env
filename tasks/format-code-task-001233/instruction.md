# Add a `Bastion` extension resource with validation

Gardener lets operators provision short-lived "bastion" (jump) hosts so users can
reach Shoot worker nodes over SSH. We need to introduce a new extension resource to
represent these hosts, following the same conventions as the other resources in the
`extensions.gardener.cloud/v1alpha1` API group (e.g. `Extension`, `Infrastructure`).

## The resource

Add a namespaced `Bastion` resource (kind `Bastion`, with a matching `BastionList`)
to the `extensions.gardener.cloud/v1alpha1` API group. It must be a first-class
extension resource: registered in that group's scheme just like the existing kinds,
and usable as an extension `Object` (it exposes its spec and status the same way the
other resources do, and can be deep-copied).

Its spec carries:

- a provider `Type` (the same common extension type field the other resources have),
- `UserData` — a byte slice holding the base64-encoded cloud-init/user data used to
  provision the SSH key on the host,
- `Ingress` — a list of ingress policies describing from where the host may be
  reached. Each policy contains an `IPBlock` (the standard Kubernetes
  `networking/v1` `IPBlock`, i.e. a `CIDR` string plus an optional list of `Except`
  CIDR strings).

The status embeds the common extension status plus the bastion's reachable
ingress endpoint (a Kubernetes `LoadBalancerIngress`).

## Validation

Provide validation entry points `ValidateBastion(bastion)` and
`ValidateBastionUpdate(new, old)` that return a `field.ErrorList` of the standard
Kubernetes shape (each error has a type such as `Required`/`Invalid`/`Forbidden` and
a field path).

`ValidateBastion` must enforce:

- standard object metadata for a namespaced resource — in particular a non-empty
  `metadata.name` (a DNS subdomain) and a non-empty `metadata.namespace`;
- `spec.type` is required;
- `spec.userData` is required (a non-empty byte slice);
- `spec.ingress` is required — at least one ingress policy must be present;
- for every ingress policy, its IP block is checked:
  - the block's `cidr` is required, and when present must be a parseable CIDR;
  - every entry in the block's `except` list must be a parseable CIDR **and** must
    fall within the block's `cidr` range.

  Each problem is reported against the offending field, using the index of the
  ingress policy and (for except entries) the index within the except list, e.g.
  `spec.ingress[0].ipBlock.cidr` or `spec.ingress[0].ipBlock.except[1]`.

`ValidateBastionUpdate` must enforce standard metadata update rules and treat
`spec.type` and `spec.userData` as immutable (changing either is an error reported
against the respective field). As a special case, once the object is being deleted
(its deletion timestamp is set) the entire spec is immutable — any change to it is
reported as a single error against `spec`. The ingress list otherwise remains
mutable. An update is additionally subject to all the `ValidateBastion` rules above.

A valid `Bastion` produces an empty error list.
