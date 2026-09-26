# Add configuration validation

Right now the only checks we do on a loaded configuration are that the file
exists and that it is syntactically valid YAML. Anything semantically wrong —
a project with no upstreams, a cache connector with a bogus driver, a
`rateLimitBudget` that points at a budget that was never defined — slips
through and only blows up much later (or silently misbehaves) at runtime, with
errors that give the operator no clue about what is wrong in their config.

I'd like the configuration tree to be able to validate itself. Add a
`Validate() error` method to the top-level configuration type. It should walk
the whole configuration and return a non-nil error for the first problem it
finds, and `nil` when everything checks out. The error message must name the
offending configuration field so an operator can immediately see what to fix.
A configuration that is well-formed must keep validating successfully — this is
a separate, explicitly-invoked check, not something wired into the existing
loading path.

The rules to enforce:

- **Projects.** Every project must have a non-empty `id`, and must declare at
  least one upstream. A project with no upstreams is invalid.

- **Cache connector.** When a database EVM-JSON-RPC cache connector is
  configured, its `driver` is required and must be one of `memory`, `redis`,
  `postgresql`, or `dynamodb`. Any other value (including an empty one) is
  invalid. In addition, the driver-specific settings block matching the chosen
  driver must be present — e.g. choosing the `redis` driver without a `redis`
  block is invalid.

- **Rate limiters.** Every rate-limit budget must contain at least one rule, and
  every rule must specify a non-empty `method`.

- **Rate-limit budget references.** Wherever a `rateLimitBudget` is set — on a
  project, a network, or an upstream — it must reference the `id` of a budget
  that actually exists under the top-level rate limiters. A reference to an
  undefined budget is invalid.

- **Networks.** Every network must specify an `architecture`, and an `evm`
  network must include its `evm` settings block.

- **Durations.** Where a failsafe timeout policy is configured, its `duration`
  must be a valid Go duration string (for example `500ms`, `5s`, `2m`). A value
  that cannot be parsed as a duration is invalid.

Validation only needs to flag the first problem encountered; it does not have to
accumulate every error in one pass.
