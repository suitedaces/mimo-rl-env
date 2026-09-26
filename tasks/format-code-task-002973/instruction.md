# Problem Statement

用 govultr 管 VKE 集群的时候发现 SDK 里没法做版本升级这块——既查不到某个集群当前能升到哪些版本，也没法直接触发一次升级。能不能给 KubernetesService 补上这两个能力？比如传个 vkeID 就能拿到可升级版本列表，再选一个版本发起升级。这样我就不用绕到 API 那边手撸 HTTP 请求了。

# Expected outcomes

- Kubernetes upgrade discovery:
  - Add a public `KubernetesService.GetUpgrades(ctx context.Context, vkeID string) ([]string, error)` capability for retrieving the Kubernetes versions that a specific VKE cluster can upgrade to.
  - It should use the VKE cluster available-upgrades API route (`GET /v2/kubernetes/clusters/{vkeID}/available-upgrades` under the repository’s existing VKE path conventions), return the available upgrade versions as a `[]string`, and propagate request or response errors normally.
- Kubernetes upgrade initiation:
  - Add a public `KubernetesService.Upgrade(ctx context.Context, vkeID string, body *ClusterUpgradeReq) error` capability for starting an upgrade of a specific VKE cluster to the version described by the request body.
  - It should use the VKE cluster upgrades API route (`POST /v2/kubernetes/clusters/{vkeID}/upgrades` under the repository’s existing VKE path conventions). A successful request should return `nil`; request construction or API errors should be returned to the caller.
- Upgrade request body:
  - The SDK should provide a public request type for cluster upgrades, `ClusterUpgradeReq`, with a caller-settable upgrade version field.
  - When serialized as JSON, a non-empty upgrade version should be sent as `upgrade_version`; an empty upgrade version should be omitted.

# Implementation notes

- Follow the existing govultr service and handler conventions for adding Kubernetes SDK capabilities.
- The public method names and request type above are part of the SDK surface for this task. The exact internal helper types, request-building organization, and response-decoding structure are up to the implementation, as long as the public SDK behavior above is satisfied.
- Keep the new behavior consistent with existing context handling and error propagation patterns in the repository.
