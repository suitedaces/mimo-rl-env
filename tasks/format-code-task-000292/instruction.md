# Check whether granted permissions satisfy requested permissions

Acorn images can declare the RBAC permissions a workload needs, and an operator
separately decides which permissions they are willing to *grant* to that
workload. Before we deploy anything we need to answer one question: **do the
granted permissions fully cover everything the image is requesting?** — and when
they don't, we want to know exactly which requested rules are still missing so we
can report them back to the user.

Permissions are already modeled in the internal `v1` API package
(`pkg/apis/internal.acorn.io/v1`): a `Permissions` value has a `ServiceName` and a
list of `PolicyRule`s (each rule embeds the standard Kubernetes
`rbacv1.PolicyRule` — `Verbs`, `APIGroups`, `Resources`, `ResourceNames`,
`NonResourceURLs` — plus a list of acorn `Scopes`). Helpers already exist on these
types for things like resolving the namespaces a rule applies to based on its
scopes.

Add a function to that package that compares a set of *granted* permissions
against a set of *requested* permissions and reports what, if anything, is
missing:

```go
func Grants(granted Permissions, currentNamespace string, requested Permissions) (missing Permissions, granted bool)
```

It must return a `Permissions` value holding the subset of the requested rules
that are **not** covered by the granted permissions, together with a boolean that
is `true` only when nothing is missing. The returned value must always carry the
requested permissions' `ServiceName`, even when nothing is missing. A request with
no rules is trivially satisfied.

A single requested rule is considered covered only if the granted permissions
share the same `ServiceName` **and** at least one granted rule is broad enough to
cover it. Coverage of one rule by another works like this:

- **Resource rules** (rules that don't list any `NonResourceURLs`): the granted
  rule covers the requested rule only when they apply to at least one common
  resolved namespace (derived from each rule's scopes relative to
  `currentNamespace`) and the granted rule's `Verbs`, `APIGroups`, and `Resources`
  each cover *all* of the corresponding values on the requested rule. The granted
  rule's `ResourceNames` must likewise cover the requested `ResourceNames`, with
  one special case: an **empty** `ResourceNames` on the granted rule means "any
  resource name", so it covers any requested `ResourceNames`.

- **Non-resource URL rules**: a granted rule that lists `NonResourceURLs` (and no
  `Resources`) covers a requested rule only when neither rule declares any scopes
  and the granted `NonResourceURLs` cover the requested `NonResourceURLs`. A
  granted rule that lists `NonResourceURLs` *together with* `Resources` covers
  nothing.

A list of allowed values "covers" a requested value when: the requested value is
the empty string; or the allowed list contains `"*"`; or it contains the value
exactly; or it contains an entry ending in `"*"` whose leading portion is a prefix
of the requested value (e.g. allowed `"secret*"` covers requested `"secrets"`).
An allowed list covers a list of requested values only when it covers every one of
them. (The empty-list-means-all rule above applies only to `ResourceNames`; for
the other fields an empty allowed list covers only empty requested values.)
