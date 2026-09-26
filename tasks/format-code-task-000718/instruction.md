# Problem Statement

我现在在 Cortex 里上传 Alertmanager 配置时，receiver 的 HTTP 通知鉴权基本只能用 basic auth 或 bearer token，但我们这边的 webhook 接口要求走 OAuth2 client credentials。能不能让 `http_config` 这类通知配置直接支持 `oauth2`，比如用 client id、inline secret 和 token URL 去拿 token？另外这个配置是租户自己传的，最好不要允许它通过 `client_secret_file` 去读服务器上的本地文件。

# Expected outcomes

- **OAuth2 notification authentication**
  - Alertmanager receiver HTTP notification configuration accepts an `oauth2` block under `http_config` where HTTP client configuration is supported.
  - A valid OAuth2 client-credentials configuration using `client_id`, inline `client_secret`, and `token_url` is accepted and used to obtain an access token for outgoing notification requests.
  - Optional OAuth2 settings such as `scopes` and `endpoint_params` are preserved and applied when obtaining the token.

- **Tenant-uploaded config safety**
  - Tenant-uploaded Alertmanager configurations must reject any OAuth2 configuration that sets `client_secret_file`.
  - Rejection must happen during configuration validation, before the server can read the referenced local file.
  - The validation failure should clearly state that setting OAuth2 `client_secret_file` is not allowed.

- **OAuth2 validation**
  - When an `oauth2` block is present, `client_id` and `token_url` are required.
  - Exactly one OAuth2 client secret source is allowed: inline `client_secret` or `client_secret_file`.
  - Missing required OAuth2 fields, missing a secret source, or setting both secret sources should produce configuration validation errors.

- **Authentication mutual exclusion**
  - OAuth2 authentication must participate in the existing HTTP authentication mutual-exclusion rules.
  - `oauth2` must not be accepted together with any other existing HTTP authentication mechanism in the same HTTP client configuration.

# Implementation notes

- The exact internal data structures, validation placement, and HTTP client wiring are up to the implementation.
- Preserve existing Alertmanager configuration behavior unrelated to OAuth2.
- Do not introduce a path that lets tenant-uploaded Alertmanager configuration read OAuth2 client secrets from server-local files.
