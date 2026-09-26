## `resources.Parse` rejects scope collection IDs

I'm working with UCP resource IDs and need to handle the URL that lists all resources under a resource group (a "collection" at the scope level), e.g.

```
/planes/radius/local/resourceGroups/test-rg/resources
```

This is the natural URL you hit when enumerating resources under a scope — there's a trailing segment (`resources`) that names the collection but has no instance name after it. It's analogous to how a resource collection like `/planes/radius/local/.../providers/Applications.Core/applications` (no app name on the end) is accepted today.

When I run it through `resources.Parse`:

```go
id, err := resources.Parse("/planes/radius/local/resourceGroups/test-rg/resources")
fmt.Println(id, err)
```

I get back an error saying the id is not a valid resource id, and parsing fails. The same shape without the trailing `resources` (`/planes/radius/local/resourceGroups/test-rg`) parses fine, and adding a name after it (`/planes/radius/local/resourceGroups/test-rg/resources/my-resource`) also parses fine — it's specifically the collection-style id, with an odd number of segments where the last one has no name, that gets rejected.

It would be great if `Parse` accepted these scope-level collection IDs, and round-tripping one back to a string (via `String()` / `MakeUCPID`) produced the same valid id rather than something with a stray empty segment.
