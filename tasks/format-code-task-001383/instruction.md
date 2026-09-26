### Can't override the defaults of the built-in `-v` / `-wd` parameters

I'm using `goyek.Flow` for my build pipeline and I'd like to make verbose mode the default (so that I get streamed logs without having to pass `-v` every time). I'd also like to tweak the default working directory for the OOTB `-wd` parameter in some of my projects.

The natural thing I tried was to just register the parameter again with my own default:

```go
flow := &goyek.Flow{}

flow.RegisterBoolParam(goyek.BoolParam{
    Name:    "v",
    Usage:   "Verbose: log all tasks as they are run.",
    Default: true, // I want verbose ON by default
})

// ... register tasks ...

flow.Main()
```

This panics with `v parameter was already registered`, because `Flow` registers the OOTB `v` (and `wd`) parameter itself.

As far as I can tell from the public API there's no way to change the default value (or the name / usage) of these built-in parameters — `VerboseParam()` / `WorkDirParam()` only return what's already there, and re-registering panics.

It would be great if there were a supported way to override the defaults for the OOTB verbose and working-directory parameters, so that consumers can decide e.g. that verbose should be on by default, or change the default working directory, without forking the library. Maybe something along the lines of `RegisterVerboseParam` / `RegisterWorkDirParam` to mirror the existing `Register*Param` family.
