## `os-archs` is required for `os-arch-bin` dist type — inconsistent with `build.os-archs`

I'm setting up a product that uses the `os-arch-bin` distribution type, and I ran into what seems like an unnecessary configuration requirement.

Minimal config to reproduce:

```yaml
products:
  my-product:
    build:
      main-pkg: ./cmd/my-product
    dist:
      dist-type:
        type: os-arch-bin
```

Running the dist task on this fails with a configuration error saying `os-arch must be specified in configuration`.

The reason I expected this to just work: `build.os-archs` right next to it is optional. The docs on `build.os-archs` explicitly say "If blank, defaults to the GOOS and GOARCH of the host system at runtime." So in a project where I haven't bothered to set `build.os-archs`, godel happily builds for whatever machine I'm on — but the moment I want an `os-arch-bin` dist of that same product, I'm suddenly forced to repeat the OS/arch information explicitly.

I'd expect the `os-archs` field on an `os-arch-bin` dist to behave the same way as `build.os-archs`: if I leave it blank, just produce the distribution for the current host. That way the common "I just want a tgz for the platform I'm building on" case works without ceremony, and people who do want to target multiple platforms can still list them out.
