## gsdkConfig.json contains placeholder values for node IP and VM ID

When a game server pod starts up under thundernetes, the init container writes `gsdkConfig.json` (at `/data/Config/gsdkConfig.json`) for the GSDK to consume. Two fields in that file are currently useless:

- `publicIpV4Address` (both at the top level and inside `gameServerConnectionInfo`) is always the literal string `"N/A"`.
- `vmId` is always the same hard-coded string regardless of which node the pod is actually scheduled on.

Example of what I see in the file right now:

```json
{
  "sessionHostId": "...",
  "vmId": "thundernetes-aks-cluster",
  "publicIpV4Address": "N/A",
  "gameServerConnectionInfo": {
    "publicIpV4Address": "N/A",
    "gamePortsConfiguration": [ ... ]
  },
  ...
}
```

This means a game server using GSDK has no way to know:

1. what IP address it can actually be reached on, and
2. which node / VM it is running on (every server in the cluster reports the same `vmId`).

For our use case we don't necessarily need a routable public IP at this layer — the IP of the node the pod landed on is good enough for the server to advertise itself and for us to distinguish instances. The `vmId` should similarly be tied to the actual node, not a single constant shared by every game server in the cluster.

Could the init container populate these fields with values that reflect the node the pod is actually running on, instead of fixed placeholders? I'd expect the init container to pick up the node's IP from a new `PF_*` env variable (something like `PF_NODE_INTERNAL_IP`) that the operator injects per-pod.
