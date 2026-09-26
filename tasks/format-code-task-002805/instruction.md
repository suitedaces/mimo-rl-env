## `tkn version` requires Deployment read access — could it use the TEP-0041 version ConfigMap instead?

On our shared cluster, my team's regular users only have RBAC permissions to list/get a small handful of resources in `tekton-pipelines`. The cluster admin has intentionally kept Deployments out of that set, but the developers still need to see which version of Pipelines / Triggers / Dashboard is installed so they know which features they can use in their `.tekton/` YAML.

Right now `tkn version` doesn't really work for them. The client version line comes out fine, but for the installed components they hit an RBAC error like:

```
deployments.apps is forbidden: User "alice@example.com" cannot list resource "deployments" in API group "apps" in the namespace "tekton-pipelines"
```

…and the component version line ends up empty / "unknown". Asking the admin to grant Deployment read access to every developer just so they can run `tkn version` is a hard sell on a multi-tenant cluster.

I noticed that [TEP-0041](https://github.com/tektoncd/community/blob/main/teps/0041-tekton-component-versioning.md) has already addressed exactly this problem on the component side: recent releases of the Tekton components publish their version through a dedicated ConfigMap that is specifically intended to be readable by any authenticated user (precisely so that tooling like `tkn` doesn't need broad RBAC just to report a version string). It would be great if `tkn version` picked the version up from there.

A couple of things that matter for us:

- This should cover all three components that `tkn version` already reports — Pipelines, Triggers, and Dashboard.
- It needs to stay backward compatible with older Tekton installs that don't ship the ConfigMap yet — we have a couple of long-lived clusters on older releases and `tkn version` shouldn't regress for them.

Thanks!
