## Bump linkerd2-proxy-init to v2.2.1

The [linkerd/linkerd2-proxy-init](https://github.com/linkerd/linkerd2-proxy-init) repo has cut a new release. We should pick up the new versions of all three artifacts it ships:

- `proxy-init` → **v2.2.1** (currently pinned at v2.2.0 in the control-plane chart)
- `cni-plugin` → **v1.1.0** (currently v1.0.0 in the linkerd2-cni chart)
- `linkerd-network-validator` → **v0.1.2** (currently v0.1.1, fetched in `Dockerfile-proxy`)

The chart defaults (`charts/linkerd-control-plane/values.yaml`, `charts/linkerd2-cni/values.yaml`), the proxy image build, and the corresponding chart READMEs all need to reference the new versions. CI golden fixtures will also need to be regenerated against the new defaults.

Heads up on the validator: the new release on GitHub is published differently from the previous one, so the `Dockerfile-proxy` step that downloads it may need adjusting — give it a try and see what the release page actually serves.
