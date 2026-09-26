# Add a `alicloud_cs_application` resource

We support managing container (Swarm) clusters through the provider, but there's no way to
declare the *applications* that run on top of a cluster. Please add a new resource type,
`alicloud_cs_application`, that deploys a Compose-style application onto an existing container
cluster from a YAML template.

The resource must be registered with the provider and be a well-formed, importable Terraform
resource (it supports create/read/update/delete and plain `terraform import`).

### Configurable attributes

- `cluster_name` — (required, force-new) the name of the target cluster the application is
  deployed to.
- `name` — (required, force-new) the application name. Validate it at plan time: it must be
  1–64 characters, may contain only ASCII letters, digits and hyphens, and must start with a
  letter or digit (a leading hyphen is not allowed). Anything else — an empty value, a value
  longer than 64 characters, a leading hyphen, spaces, underscores, dots, or non-ASCII
  characters such as Chinese characters — must produce a validation error.
- `template` — (required) the application definition as a Compose-style YAML document. Reject a
  value that is not well-formed YAML with a validation error at plan time. Because YAML that is
  only cosmetically different (indentation, key ordering, trailing whitespace) describes the same
  application, the value must be stored in a normalized/canonical form so that equivalent
  documents do not show up as spurious diffs.
- `description` — (optional) free-form description.
- `version` — (optional) application version, defaulting to `"1.0"`.
- `environment` — (optional) a map of string environment variables.
- `latest_image` — (optional) boolean, defaults to `false`.
- `blue_green` — (optional) boolean, defaults to `false`.
- `blue_green_confirm` — (optional) boolean, defaults to `false`.

### Read-only attributes

- `services` — the list of service names that make up the application.
- `default_domain` — the application's default domain.
