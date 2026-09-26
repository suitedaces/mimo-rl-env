## External `$ref` resolution breaks when the base spec is loaded over HTTP

I'm using `kin-openapi` to load an OpenAPI 3 spec that's hosted on an HTTP server. The spec is split across multiple files — the root document references other schema files via `$ref`, e.g.:

```yaml
# served at http://example.com/schemas/openapi.yaml
components:
  schemas:
    Pet:
      $ref: './pet.yaml'
```

with `pet.yaml` sitting next to it on the same server.

I load it like this:

```go
loader := openapi3.NewSwaggerLoader()
loader.IsExternalRefsAllowed = true

u, _ := url.Parse("http://example.com/schemas/openapi.yaml")
swagger, err := loader.LoadSwaggerFromURI(u)
```

The external `$ref` to `pet.yaml` doesn't get resolved correctly — the loader ends up trying to fetch from a URL that doesn't actually exist on the server, so I either get a fetch error or an unresolved-ref error coming back from `LoadSwaggerFromURI`.

The same exact spec layout works fine when I load it from local disk (using a filesystem path as the base) — refs to sibling files resolve and the spec loads cleanly. It only goes wrong when the base location is an `http://` URL.

I'd expect external `$ref`s to work the same way regardless of whether the base spec was loaded from a local file or from an HTTP URL — sibling refs in the same directory should resolve in both cases.
