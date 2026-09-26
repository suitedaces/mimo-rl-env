Dependency on go-control-plane v0.9.4 too old
**Description**
[envoyproxy/go-control-plane](https://github.com/envoyproxy/go-control-plane) [v0.9.5](https://github.com/envoyproxy/go-control-plane/tree/v0.9.5) introduced a [breaking change](https://github.com/envoyproxy/go-control-plane/commit/247a40fffb7959df88f886c0c383b6000e771752) to its xds cache package to support xds v3. Since clutch is still targeting `v0.9.4`, its difficult to integrate go-control-plane v0.9.5+ based workflows into a custom gateway without forking clutch. 

**Expected Behavior**
As a custom gateway owner, I shouldn't need to worry about bundled workflows and modules I don't need/want breaking my builds.

Workflows and modules that are bundled with clutch should either take minimal dependencies or make an effort to stay current on versions.

 In general, I'm curious about what the long term strategy is of adding modules and workflows to the main clutch repo vs moving them out to "official" external repos or an "official" custom gateway.  

**Actual Behavior**
Depending on a newer go-control-plane in a custom-gateway breaks compiles.

```
my-clutch-gateway$ make backend                                                                                               
cd backend && go build -o ../build/clutch main.go
go: finding module for package github.com/envoyproxy/go-control-plane/pkg/cache
go: finding module for package github.com/envoyproxy/go-control-plane/pkg/server
/home/willb/go/pkg/mod/github.com/lyft/clutch/backend@v0.0.0-20200730230015-4804adceb434/module/chaos/experimentation/rtds/rtds.go:16:2: module github.com/envoyproxy/go-control-plane@latest found (v0.9.6), but does not contain package github.com/envoyproxy/go-control-plane/pkg/cache
/home/willb/go/pkg/mod/github.com/lyft/clutch/backend@v0.0.0-20200730230015-4804adceb434/module/chaos/experimentation/rtds/rtds.go:17:2: module github.com/envoyproxy/go-control-plane@latest found (v0.9.6), but does not contain package github.com/envoyproxy/go-control-plane/pkg/server
Makefile:19: recipe for target 'backend' failed
make: *** [backend] Error 1
```

**Version**
`4804adceb4347fb902f03af6d28bb26d7229c598`

**Other Context**
This isn't a huge issue for me as I can work around it by forking clutch and removing the offending chaos code, but I wanted to flag as I think this might come up more the future as the number of bundled workflows and modules grows.
