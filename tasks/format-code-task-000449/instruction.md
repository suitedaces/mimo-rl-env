**Feature request: allow extra command line arguments on the repo-server via the ArgoCD CR**

We're running Argo CD through the operator and recently wanted to tune a flag on the argocd-repo-server (for example, something like `--reposerver.max.combined.directory.manifests.size 10M`) that doesn't have a dedicated knob in the ArgoCD spec yet. The repo-server Deployment is fully managed by the operator, so when we just `kubectl edit` the Deployment to add the flag to the container command, the next reconcile reverts it.

I noticed that `spec.server.extraCommandArgs` already gives us an escape hatch for the argocd-server component — we can use it to pass extra flags that the operator doesn't surface as first-class fields, and they show up on the server Pod's command. There doesn't seem to be an equivalent for the repo-server side of `spec`, though.

The practical problem this creates: every time Argo CD upstream adds a new repo-server flag we want to use, we either have to wait for an operator release that exposes it as a typed field, or we have to fork/patch the operator. For flags we only need temporarily, or that are niche enough that they may never get a dedicated field, this is a lot of friction.

Would it be possible to expose the same kind of escape hatch on the repo section of the ArgoCD CR, so users can declare a list of extra command line arguments that get added on top of whatever the operator already generates for the repo-server (without replacing any of those defaults)? That way the operator stays in charge of the baseline command, but we don't get blocked on operator releases whenever upstream introduces a new repo-server flag.

The new field on `spec.repo` could be named something like `extraRepoCommandArgs`.
