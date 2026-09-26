Druid configurations can currently resolve one dynamic configuration provider, but deployments often need to combine values from several sources, such as a base map plus an extension-provided secret source. Add a composable DynamicConfigProvider that can be selected in JSON with type `"composite"`.

A composite provider has an ordered `providers` array. Every element is a normal polymorphic `DynamicConfigProvider<String>`, including provider subtypes registered by extensions. Calling `getConfig()` resolves every child in array order and merges its non-null entries. The optional JSON property `mergePolicy` accepts these exact values:

- `"lastWins"` (the default when omitted): a later non-null value replaces an earlier value for the same key.
- `"firstWins"`: the first non-null value is retained.
- `"failOnConflict"`: repeated equal non-null values are allowed, but different non-null values for the same key cause `getConfig()` to throw `IllegalArgumentException`; the message must identify the conflicting key.

Treat a child entry whose value is null as absent: it must not override another value, count as a conflict, or appear in the result.

The optional `requiredKeys` array is checked against the final merged, null-filtered result. Required keys may be supplied by different children. If a required key is absent or resolves only to null, `getConfig()` throws `IllegalArgumentException` and its message identifies that key.

Dynamic providers can rotate values, so do not memoize a composite result. Each `getConfig()` call must invoke all children again. If a child throws, preserve its exception type and message and abandon that resolution. A later call starts a fresh resolution and invokes the children again rather than returning or extending a partial result from the failed call.

Composite providers must deserialize through the existing `DynamicConfigProvider` JSON API and serialize back with type `"composite"` so a serialized instance can be deserialized and resolve equivalently. They must also work wherever Druid already accepts a provider object: both `DynamicConfigProviderUtils.extraConfigAndSetStringMap` and `extraConfigAndSetObjectMap` must resolve the composite, let dynamic values override same-named static entries, omit the provider-control property, and otherwise retain each utility's existing treatment of ordinary static values. Existing `mapString` provider JSON and the current non-composite utility behavior must remain compatible.
