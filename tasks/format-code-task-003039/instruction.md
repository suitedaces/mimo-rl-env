## Unify the SDK RPC server and the Admin RPC server into a single endpoint

Right now Yorkie exposes two separate gRPC servers from the same process:

- the SDK-facing RPC server (default `:11101`)
- the Admin RPC server (default `:11103`)

Operationally this is awkward and I'd like to propose collapsing them into a single RPC server.

### Why this is painful today

- **Two ports / two addresses to manage.** Every consumer that talks to both APIs (e.g. our dashboard, internal tooling, the `yorkie` CLI) has to be configured with two endpoints. The CLI for example takes `--admin-addr` separately from wherever the SDK connects, and that pair has to be kept consistent across environments.
- **Public URL surface gets duplicated.** When deploying behind an ingress / istio gateway we end up provisioning a second host (something like `admin.<host>` next to `api.<host>`), with its own Ingress, its own VirtualService route, its own DestinationRule entry, etc. — purely because the admin traffic has to land on a different backend port. Two trees of YAML to keep in sync for what is functionally the same service.
- **Affects downstream repos.** Anything that consumes both the SDK and the admin API today (dashboard etc.) has to know about both base URLs. If the server exposed a single unified URL, those consumers could be configured with one address.

There isn't a real reason for these to be separate processes/ports — both are gRPC services living in the same binary, sharing the same backend, the same auth/secret key, the same metrics. The split is just historical.

### What I'd like

One RPC server inside the yorkie process that serves **both** the SDK service and the Admin service. After the change:

- a single port (the existing SDK port `11101` is the natural choice) serves all `yorkie.v1.*` gRPC services
- the CLI and admin client connect to that one address — no separate "admin address" concept
- ingress / gateway / k8s service definitions only need to expose that one port and route `/yorkie.v1*` to it
- existing auth behavior is preserved: admin endpoints still require a token, SDK endpoints still go through the API-key / project context path the same way they do today

This is a user-facing breaking change for anyone currently pointing tooling at the admin port, so it should be called out in the release notes, but the simplification is worth it.
