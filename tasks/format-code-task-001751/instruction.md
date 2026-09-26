## Image `registry` and `tag` context fields are empty when not explicitly set in the spec

I'm writing a couple of Kyverno policies around container images:

1. One that requires all images to come from our internal mirror (i.e. denies anything from `docker.io`).
2. One that denies the `latest` tag.

Both policies look at the image context that Kyverno builds from the resource (matching against `registry` and `tag` on each container).

The problem I'm hitting is that when a user submits a Pod with an image like:

```yaml
containers:
  - name: app
    image: nginx
```

…or:

```yaml
containers:
  - name: app
    image: nginx:1.19
```

the `registry` and/or `tag` fields in the extracted image context come out as empty strings. So my "deny docker.io" rule never fires on `image: nginx`, and my "deny latest" rule never fires on `image: nginx` either — even though at runtime the kubelet is absolutely going to pull `docker.io/library/nginx:latest`.

I’d expect the context Kyverno builds to reflect the same defaults the container runtime applies, i.e.:

- if no registry is specified in the image string → treat it as `docker.io`
- if no tag is specified in the image string → treat it as `latest`

Otherwise it’s pretty hard to write reliable registry/tag policies, because users can bypass them just by relying on the implicit defaults in their image references.

Could the image info extraction fill these defaults in so policies see what the runtime is actually going to use?
