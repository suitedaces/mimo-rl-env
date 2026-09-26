# Add a configurable Azure cloud abstraction

Right now azd assumes it is always talking to the Azure public cloud — portal links,
storage and container-registry hostnames, and the SDK client configuration are all
hard-wired to the public cloud's values. We want to support the sovereign clouds
(Azure China and Azure US Government) too, so the rest of the codebase can ask for the
correct endpoints instead of hard-coding `portal.azure.com`, `core.windows.net`, etc.

Introduce a small self-contained package, importable as
`github.com/azure/azure-dev/cli/azd/pkg/cloud`, that models a target cloud and lets
callers resolve one from user/project configuration.

## What a "cloud" carries

A cloud is represented by a `Cloud` value exposing, as readable fields:

- `Configuration` — the underlying `azcore` cloud configuration (the
  `cloud.Configuration` type from
  `github.com/Azure/azure-sdk-for-go/sdk/azcore/cloud`), so SDK clients can be pointed at
  the right authority/management endpoints,
- `PortalUrlBase` — the base URL of the cloud's web portal,
- `StorageEndpointSuffix` — the DNS suffix used for the cloud's storage endpoints,
- `ContainerRegistryEndpointSuffix` — the DNS suffix used for the cloud's container
  registry endpoints.

Provide a no-argument constructor for each of the three well-known clouds —
`AzurePublic()`, `AzureChina()`, and `AzureGovernment()` — each returning a `*Cloud`
populated with the correct values:

| constructor          | azcore configuration    | portal base URL            | storage suffix           | container registry suffix |
|----------------------|-------------------------|----------------------------|--------------------------|---------------------------|
| `AzurePublic()`      | `cloud.AzurePublic`     | `https://portal.azure.com` | `core.windows.net`       | `azurecr.io`              |
| `AzureChina()`       | `cloud.AzureChina`      | `https://portal.azure.cn`  | `core.chinacloudapi.cn`  | `azurecr.cn`              |
| `AzureGovernment()`  | `cloud.AzureGovernment` | `https://portal.azure.us`  | `core.usgovcloudapi.net` | `azurecr.us`              |

## Resolving a cloud from configuration

A cloud is selected by a stable, configuration-friendly name. Expose these as exported
string constants:

- `AzurePublicName` = `AzureCloud`
- `AzureChinaCloudName` = `AzureChinaCloud`
- `AzureUSGovernmentName` = `AzureUSGovernment`

Define a `Config` struct that holds a single name field, serializable to/from both JSON
and YAML under the key `name`.

`NewCloud(config *Config) (*Cloud, error)` builds a cloud from such a config:

- a recognized name resolves to the matching cloud,
- an empty name defaults to the Azure public cloud,
- any other value is an error whose message includes the offending name.

`ParseCloudConfig(partialConfig any) (*Config, error)` takes a loosely-typed
configuration value — the kind of thing you get back when reading a node out of azd's
JSON/YAML config (e.g. a `map[string]any{"name": "AzureChinaCloud"}`) — and turns it
into a `*Config`.

Finally, expose the configuration key under which the cloud node lives as an exported
constant `ConfigPath` whose value is `cloud`.
