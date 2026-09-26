# Add OAuth2Proxy (header-based) authentication

We deploy Keep behind [oauth2-proxy](https://github.com/oauth2-proxy/oauth2-proxy), which
terminates authentication for us and forwards the authenticated identity to the backend as HTTP
headers. We want Keep to trust those headers as an authentication method, so no Keep-managed
login/JWT is involved.

Add a new authentication mode that is selected by setting the environment variable
`AUTH_TYPE=oauth2proxy` (the value is matched case-insensitively, like the other auth types). When
this mode is active, every API request is authenticated and authorized purely from request headers,
and it must plug into the existing identity-manager / RBAC machinery so that the normal
scope-based authorization runs against the role derived from the request.

## Reading the identity from headers

- The authenticated user's email/username is read from a header whose name defaults to
  `x-forwarded-email` and is overridable with `KEEP_OAUTH2_PROXY_USER_HEADER`.
- The user's groups are read from a header whose name defaults to `x-forwarded-groups` and is
  overridable with `KEEP_OAUTH2_PROXY_ROLE_HEADER`. The value is a comma-separated list of group
  names (a single value with no comma is valid). Surrounding whitespace around each group name is
  ignored.
- If the user header is missing/empty, the request is rejected with **401**.
- If the groups header is missing/empty, the request is rejected with **401**.

## Mapping groups to roles

Keep already has three built-in roles — `admin`, `noc`, and `webhook` — with their existing scopes.
Resolve the request's groups to exactly one of these roles:

- Optionally, external group names can be mapped onto the built-in roles via
  `KEEP_OAUTH2_PROXY_ADMIN_ROLE`, `KEEP_OAUTH2_PROXY_NOC_ROLE`, and
  `KEEP_OAUTH2_PROXY_WEBHOOK_ROLE`. If a group in the header equals one of these configured values,
  it resolves to the corresponding built-in role. Any group that is not a configured value is used
  directly as a role name (so a group literally named `admin`/`noc`/`webhook` resolves to that
  role even when no mapping is configured).
- A user typically belongs to several groups. When more than one group resolves to a known role,
  the role with the highest privilege wins, in the precedence order `admin` > `noc` > `webhook`.
  The order in which the groups appear in the header must not affect the outcome.
- If none of the groups resolve to a known built-in role, the request is rejected with **403**.

The resolved role then drives the usual RBAC authorization: the request succeeds only if that role
holds the scopes required by the endpoint (e.g. an `admin` group grants write access, while a
`noc` group is read-only and is rejected with **403** on write-scoped endpoints).

## User provisioning

- By default the authenticated user is provisioned automatically: if a user with that
  username does not yet exist for the tenant, it is created with the resolved role. This is
  controlled by `KEEP_OAUTH2_PROXY_AUTO_CREATE_USER`, which defaults to enabled; setting it to
  `false` disables auto-creation. When disabled, requests are still authenticated and authorized
  from the headers, but no user record is created.
- Listing users for this tenant must reflect the users that have been provisioned this way.
