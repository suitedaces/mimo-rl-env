## `OTEL_RESOURCE_ATTRIBUTES` values are not URL-decoded

The OpenTelemetry environment-variable spec for `OTEL_RESOURCE_ATTRIBUTES` says that attribute values are percent-encoded, so that values containing characters such as spaces, `,` or `=` (which would otherwise collide with the list/pair separators) can be passed safely. See the spec:

> Attribute values MUST be considered as percent-encoded as defined by RFC 3986.

The Go SDK's env resource detector doesn't appear to be honoring that. For example, setting:

```
OTEL_RESOURCE_ATTRIBUTES=service.namespace=my%20team,service.version=1.0.0+build%3D42
```

and then detecting resources via `resource.New(ctx, resource.WithFromEnv())` gives me attributes whose values are still the raw, encoded strings (`"my%20team"`, `"1.0.0+build%3D42"`) rather than the decoded ones I'd expect (`"my team"`, `"1.0.0+build=42"`).

This makes it effectively impossible to put a space, `,` or `=` in any resource attribute value via this env var — the workaround of "just don't encode" doesn't work because the unencoded characters break the `key=value,key=value` parsing.

Would it be possible to have the env detector decode the values per the spec?
