## Cannot extend the new role-based model with custom manage roles

We're rolling out the new aggregation-based role model from `user-authz` to our org and we'd like to compose our own scopes / capabilities on top of it. Two concrete cases:

**Case 1 — a custom scope.** The built-in scopes (`deckhouse`, `kubernetes`, `networking`, ...) don't match how we slice responsibilities internally. I'd like a single "scope" that bundles the admin level of the `deckhouse` scope, the admin level of the `kubernetes` scope, and everything from the `user-authn` module.

So I created a `ClusterRole`, marked it as a manage role, and used a plain Kubernetes `aggregationRule` whose selectors point at the labels of the existing built-in roles, e.g.:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: custom:manage:mycustomscope:admin
  labels:
    rbac.deckhouse.io/kind: manage
    rbac.deckhouse.io/level: scope
    rbac.deckhouse.io/scope: custom
aggregationRule:
  clusterRoleSelectors:
    - matchLabels:
        rbac.deckhouse.io/kind: manage
        rbac.deckhouse.io/aggregate-to-deckhouse-as: admin
    - matchLabels:
        rbac.deckhouse.io/kind: manage
        rbac.deckhouse.io/aggregate-to-kubernetes-as: admin
    - matchLabels:
        rbac.deckhouse.io/kind: manage
        module: user-authn
rules: []
```

Aggregation itself works (the role ends up with the union of rules as expected). But when I create a `ClusterRoleBinding` against it for a user, **no namespaced `RoleBinding`s show up** — whereas if I bind the same user directly to `d8:manage:deckhouse:admin`, the use-role bindings appear in the deckhouse-managed namespaces as expected. So my custom scope role is effectively ignored by the machinery that materialises the namespaced bindings.

**Case 2 — extending an existing scope with a new capability.** A separate operator team installed a new cluster-scoped CRD (`MySuperResource`). I want users who hold `d8:manage:deckhouse:admin` to also get get/list/watch on this resource. The natural thing is to add a small `ClusterRole` carrying the rules and a label that says "aggregate me into the deckhouse manage scope":

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: custom:manage:capability:mycustommodule:superresource:view
  labels:
    rbac.deckhouse.io/kind: manage
    rbac.deckhouse.io/aggregate-to-deckhouse-as: admin
rules:
  - apiGroups: [mygroup.io]
    resources: [mysuperresources]
    verbs: [get, list, watch]
```

The rules do get aggregated into `d8:manage:deckhouse:admin`, but if this capability lives in its own namespace and I want a corresponding namespaced use-role binding produced there, I have no way to express that — and nothing happens automatically.

**What I'd expect:**
- Custom `ClusterRole`s that mark themselves as `rbac.deckhouse.io/kind: manage` and use a standard `aggregationRule` should be first-class citizens of the new role model — they shouldn't need to look like internal Deckhouse roles to be recognised.
- Binding a subject to such a custom manage role via `ClusterRoleBinding` should automatically produce the same kind of namespaced `RoleBinding`s that binding to a built-in `d8:manage:*` role produces, covering the namespaces of all the roles it (transitively) aggregates.
- There should be documentation in the user-authz FAQ explaining the contract: which labels a custom role must carry, how to bolt a new capability onto an existing scope, how to introduce a brand-new scope, and how to make the hook create use-role bindings in a namespace that a new capability lives in. Right now operators have to read the hook source to guess at the rules.
