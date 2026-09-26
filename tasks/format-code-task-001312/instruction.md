## Feature request: built-in validator for DNS RFC 1035 labels

I'm using this library to validate config / API request structs for a service that ends up producing Kubernetes resource names and DNS subdomain components. A lot of those fields need to be a single valid DNS label as defined in RFC 1035 (the same shape Kubernetes calls a "DNS-1035 label" in its naming docs).

Looking through the baked-in validators, the closest things I can find are:

- `hostname` (RFC 952)
- `hostname_rfc1123`
- `fqdn`

None of these match what I actually want. `hostname` / `hostname_rfc1123` allow uppercase letters and are aimed at full hostnames (multiple dot-separated segments, leading digits OK in 1123, etc.), and `fqdn` requires a TLD. What I need is the stricter "single label" rule from RFC 1035, which is used all over the place for things like k8s resource names, service names, and individual subdomain segments — typically validated with a single regex.

Right now I have to do this with a `RegisterValidation` call and a hand-written regex in every project that needs it, which feels silly given how common this case is and given that you already ship validators for the closely-related hostname / FQDN cases.

Could a built-in validator for "valid DNS RFC 1035 label" be added, in the same spirit / naming style as `hostname_rfc1123`? Something I can just drop into a struct tag:

```go
type MyResource struct {
    Name string `validate:"required,<the new tag>"`
}
```

so I don't have to register a custom validator in every service that deals with k8s-style names.

Reference: https://datatracker.ietf.org/doc/html/rfc1035

(For consistency with the existing naming I'd expect the new tag to be something like `dns_rfc1035_label`.)
