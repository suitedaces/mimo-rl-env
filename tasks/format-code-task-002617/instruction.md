## No way to retrieve which packages a `LockedProject` actually uses

I'm building a tool on top of gps. After a successful `Solve()`, I walk the
returned `LockedProject`s to write out a lockfile that, for each project,
records exactly which sub-packages of that project the import graph actually
touches (so downstream consumers can prune vendor/ aggressively).

The problem is `LockedProject` only exposes `Ident()` and `Version()`. There
seems to be no public way to ask a `LockedProject` "which packages from you
were used?" — even though, looking at the type, it clearly has that info
internally (the solver assembles it during `pa2lp`). From outside the
package I just can't get at it.

```go
soln, err := solver.Solve()
// ...
for _, lp := range soln.Projects() {
    fmt.Println(lp.Ident(), lp.Version())
    // now what? I want the list of in-use packages for this project,
    // but there's no accessor.
}
```

A couple of related things I noticed while poking at this:

- A teammate on Windows tried the same thing (with a local patch to expose
  the slice) and the package strings he got back still had the full project
  import path baked in as a prefix, while on my Linux box the prefix was
  stripped. We'd expect the entries to be project-root-relative on both
  platforms — they're Go import paths, not filesystem paths.
- It's also unclear how the root package of a project itself is supposed to
  appear in that list (i.e. when the project's own root import path is one
  of the imported packages, not just a sub-path under it). Whatever the
  representation, there should be one — right now it seems to come out as
  an empty string or get lost.

Could `LockedProject` expose its package list through a public accessor,
with the entries normalized to be project-root-relative and OS-independent?
