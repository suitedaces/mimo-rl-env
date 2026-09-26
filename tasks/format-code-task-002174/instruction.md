## Can't `go get` osmosis at v3 — module path doesn't follow Go's major-version convention

I'm writing a Go tool that needs to import some osmosis packages directly as a library dependency (specifically a few things under `x/gamm/types` and `x/lockup/types`). I'd like to pin it to one of the recent `v3.x.x` releases on GitHub.

When I run

```
go get github.com/osmosis-labs/osmosis@latest
```

the Go toolchain refuses to resolve to any of the v3 tags. It complains that the module declares its path without a `/v3` suffix even though the published tag is `v3.x.x` — which AFAIK is just how Go modules require things to be set up once a project crosses to a v2+ major version.

Same thing if I try to pin it explicitly, e.g. `go get github.com/osmosis-labs/osmosis@v3.0.0` — won't resolve.

The only version `go get` will actually pull is something like `v1.0.4`, which is way out of date and obviously doesn't have any of the modules / changes that landed in v3.

End result: at the moment osmosis is effectively unusable as a Go dependency at any recent version. Would be great to get the module path lined up with the published major version so downstream projects can actually consume it.
