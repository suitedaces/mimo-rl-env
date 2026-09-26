## Stale binary symlinks after a package's binaries change

I'm using hermit to manage tooling for my project. When a package gets
upgraded (either via a channel update or because I bump it manually), I
sometimes end up with broken or wrong-version commands afterwards — even
though `hermit` itself reports the new version is installed and ready.

### What I'm seeing

Steps that reproduce it for me:

1. Install some package `foo` whose extracted layout puts a binary at
   e.g. `pkg/foo-1.0.0/bin/foo`. hermit creates a symlink under
   `state/binaries/foo-1.0.0/foo` pointing there. Everything works.
2. Upgrade the package to a new version where the on-disk binary now
   lives at a different path inside the extracted package (different
   directory inside the archive, renamed, etc.). The package gets
   re-extracted under a new `pkg/...` directory.
3. Run `foo` again.

What I get: the command either fails with a "no such file or directory"
sort of error, or runs something stale. If I `ls -l` the entries in the
`state/binaries/...` directory, the symlinks for that package are still
pointing at the old extracted location, not the new one. The link target
is just wrong now.

It also happens in the reverse direction — if a package adds a brand new
binary, or removes/renames one — the symlink folder for that package
doesn't reflect what the package actually ships post-upgrade. Old links
hang around, and links that *do* exist sometimes point at paths that no
longer make sense.

### What I'd expect

After hermit decides a package is installed and its binaries are linked,
the symlinks under `state/binaries/<pkg>/` should be a faithful view of
that package's *current* binaries — every link should point at the path
the package actually expects right now, with nothing left over from a
previous install of the same package.

Right now hermit seems to treat "a symlink with the right filename
exists" as good enough and skips re-linking, which is what's leaving the
stale targets in place.
