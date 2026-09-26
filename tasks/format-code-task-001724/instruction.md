## CoreDNS upgrade from v1.20 to v1.21 fails — image cannot be pulled

When upgrading a workload cluster managed by KCP from Kubernetes v1.20 to v1.21, the CoreDNS pods end up in `ImagePullBackOff` after KCP rolls the upgrade.

What I see in the rolled-out deployment is that KCP sets the CoreDNS container image to:

```
k8s.gcr.io/coredns:v1.8.0
```

But this image does not exist on the upstream registry anymore for the 1.8.x line — the upstream CoreDNS image was moved/renamed under `k8s.gcr.io/coredns/coredns`, so the image that actually exists is:

```
k8s.gcr.io/coredns/coredns:v1.8.0
```

This is also what a fresh `kubeadm` install on 1.21 ends up using. So the upgrade path through KCP is broken for anyone tracking the default upstream registry: the new CoreDNS deployment that KCP writes points at a path that 404s on `k8s.gcr.io`.

### Repro

1. Create a workload cluster on Kubernetes v1.20 (CoreDNS comes up fine, image `k8s.gcr.io/coredns:1.7.0`).
2. Bump the KCP `version` to v1.21.x, leaving `dns.imageRepository` / `dns.imageTag` at defaults (i.e. relying on the upstream `k8s.gcr.io` registry).
3. KCP performs the CoreDNS update step and patches the coredns Deployment.
4. New CoreDNS pods never come up — they sit in `ImagePullBackOff` because the image KCP wrote does not exist upstream.

### Expected

Upgrading from v1.20 to v1.21 through KCP should result in a CoreDNS deployment pointing at an image that actually exists on the upstream registry, so the upgrade completes without manual intervention.

### Note for users on a custom registry

This only seems to affect users on the default upstream `k8s.gcr.io` registry. If you mirror CoreDNS under your own registry (e.g. `myrepo.io/coredns:<tag>`), the rename does not apply and the existing behaviour is what you want — please make sure the fix does not break that case.
