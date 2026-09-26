### Cannot override the default image registry on `SecuredCluster` via the operator

When deploying RHACS Secured Cluster services through the operator, there is no way to make the secured-cluster components pull their images from a mirror / internal registry instead of the default upstream registry.

The Helm chart for secured cluster services already supports a registry override (the same knob that lets you rewrite e.g. `nginx:latest` → `<my-mirror>/library/nginx:latest`), and the `Central` CR exposes equivalent configuration. But the `SecuredCluster` CR (`platform.stackrox.io/v1alpha1`) does not expose anything analogous, so operator users in disconnected / air‑gapped / mirrored-registry environments are stuck.

#### What I tried

I install the operator and apply a `SecuredCluster` resource:

```yaml
apiVersion: platform.stackrox.io/v1alpha1
kind: SecuredCluster
metadata:
  name: stackrox-secured-cluster-services
  namespace: stackrox
spec:
  clusterName: my-cluster
  # ... no way to point image pulls at our internal mirror here
```

There is no field on `SecuredClusterSpec` that gets plumbed through to the Helm `registryOverride` value, so the resulting workloads always try to pull from the default registry. In a disconnected cluster that has no egress to the default registry, the pods just keep failing to pull.

#### What I expected

Parity with what the Helm chart and `Central` already allow: I should be able to specify a default-registry override on the `SecuredCluster` CR, and the operator should pass that through to the underlying chart so that all images used by secured cluster components get rewritten to come from my chosen registry.

This should be a normal optional field (an empty / unset value should keep today's behavior — no rewriting), and it should show up in the operator's CSV/CRD so it's visible to users editing the resource through the OperatorHub UI as an advanced setting, alongside things like `imagePullSecrets`, `customize`, `misc`, etc.
