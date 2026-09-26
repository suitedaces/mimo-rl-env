# Add optional LDAP authentication settings to the server configuration

We want lakeFS operators to be able to point the server at an LDAP/AD directory for
authenticating users. The first step is configuration plumbing: the loaded server
configuration needs to expose the LDAP settings so the rest of the system can later wire up an
LDAP authenticator.

Settings live under `auth.ldap` in the YAML configuration. Add a public accessor on the
configuration object, `GetLDAPConfiguration()`, that returns the LDAP settings as a pointer to a
struct (call it `LDAP`) with the following exported fields, each mapped from the corresponding
config key:

| config key                    | field               | notes                                         |
|-------------------------------|---------------------|-----------------------------------------------|
| `auth.ldap.server_endpoint`   | `ServerEndpoint`    | LDAP server URL                               |
| `auth.ldap.bind_dn`           | `BindDN`            | DN lakeFS binds as to search for users        |
| `auth.ldap.bind_password`     | `BindPassword`      | password for the bind DN; may be empty        |
| `auth.ldap.user_base_dn`      | `UserBaseDN`        | base DN under which users are searched        |
| `auth.ldap.username_attribute`| `UsernameAttribute` | attribute holding the login name (e.g. `uid`) |
| `auth.ldap.user_filter`       | `UserFilter`        | extra LDAP filter; may be empty               |
| `auth.ldap.default_user_group`| `DefaultUserGroup`  | group new LDAP users join                     |

Behavior:

- When the loaded configuration contains **no** LDAP settings at all, `GetLDAPConfiguration()`
  must return `nil` (LDAP disabled).
- When LDAP settings are present, it must return a populated value with every field above filled
  in from the configuration.
- `DefaultUserGroup` must default to `"Viewers"` when it is not specified in the configuration,
  but an explicitly configured value must be preserved.

Configurations that don't mention LDAP must keep loading and behaving exactly as before.
