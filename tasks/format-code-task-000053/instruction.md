## Operator-managed Pods rejected under the Restricted Pod Security Standard

We're rolling postgres-operator out into a cluster where namespaces enforce the
Kubernetes [Restricted Pod Security Standard][pss]. When the operator brings up
its Postgres pods in such a namespace, the API server rejects them (or, with
`warn`/`audit` configured, surfaces a warning for every container) because the
containers' SecurityContext does not satisfy the Restricted profile.

Looking at `RestrictedSecurityContext()` in `internal/initialize/security.go`,
most of what Restricted requires is already there — `runAsNonRoot`, dropped
capabilities, no privilege escalation, read-only root filesystem, etc. — but
the resulting pods still trip the Restricted check, so the defaults aren't
quite "Restricted-compliant" out of the box.

For an operator that's clearly trying to ship a hardened SecurityContext
(`RestrictedSecurityContext` is even the function name), it would be great
if pods produced by it could be deployed into a Restricted-enforcing namespace
without the user having to layer extra mutating webhooks or post-process the
generated specs.

[pss]: https://kubernetes.io/docs/concepts/security/pod-security-standards/#restricted
