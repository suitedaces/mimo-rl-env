## Treat prereleases as equal to their corresponding release version

I'm using `go-version` in a tool that picks a schema/ruleset based on the version of another component (think along the lines of how the Terraform Language Server resolves a schema for a given Terraform CLI version: see [terraform-schema/schema/core_schema.go](https://github.com/hashicorp/terraform-schema/blob/8c206fbd85ae346716b4efbd776c8b8097fc5b42/schema/core_schema.go#L47-L52) for the kind of usage I have in mind).

In practice, the version string I get often looks like `0.15.0-dev` (a local/dev build) or `1.2.3-rc1`, but for the purpose of selecting which schema applies, I want to treat those as equivalent to `0.15.0` and `1.2.3` respectively. The actual prerelease/metadata suffix doesn't matter for that decision — only `MAJOR.MINOR.PATCH` does.

With the current API I can't express this concisely. Something like:

```go
v, _ := version.NewVersion("0.15.0-dev")
target, _ := version.NewVersion("0.15.0")

v.Equal(target) // false, because prerelease differs
```

returns `false`, which is correct per the existing comparison semantics, but it's not what I want here.

To work around this I currently have to grab the segments via `Segments64()`, format them back into a `MAJOR.MINOR.PATCH` string, and call `NewVersion` again to get a "clean" `*Version` to compare against — every consumer that wants this behavior ends up reimplementing the same little helper.

It would be nice if `go-version` exposed a first-class, opt-in way to get a `*Version` derived from another one with the prerelease and metadata portions stripped off, so consumers who explicitly want the "treat prereleases as equal to the corresponding release" semantics can do it in one call without dropping back to manual string formatting. The default comparison behavior should stay as it is — this is just a convenience for the cases where I deliberately want to ignore prerelease/metadata.
