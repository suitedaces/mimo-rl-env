Support idempotent clusterctl init usage
**User Story**

As a developer/operator I would like to run `clusterctl init` with specific provider flags/versions in an idempotent way to simplify developer workflows.

**Detailed Description**

In my organization, developers use (a wrapped version of) `clusterctl` to bring up clusters for development and testing purposes. We want to enforce specific provider versions to ensure consistent behavior and avoid version drift.

`clusterctl init` already support specifying provider versions for this purpose, e.g.:

```
clusterctl init --core cluster-api:v0.4.8 --control-plane kubeadm:v0.4.8
```

This works well when a management cluster has not been brought up yet. However, if it has and the command is run again with the flags, an error is returned:

```
Error: installing provider "cluster-api" can lead to a non functioning management cluster: there is already an instance of the "cluster-api" provider installed in the "capi-system" namespace
```

We work around the issue by detecting if a given provider is already installed (by checking if the corresponding Deployment exists) and adjust the `clusterctl init` flags accordingly. This feels a bit tedious / cumbersome though -- ideally, `clusterctl` should only error out if any of the given versions diverge, thereby better serving gitops / idempotence needs.

(There might also be a potential to trigger an upgrade if the versions diverge, though that may be for a different feature request.)

Related Slack convo with @vincepri at https://kubernetes.slack.com/archives/C8TSNPY4T/p1651502359080819.

/kind feature
