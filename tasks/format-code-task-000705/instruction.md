### Conan crashes when a cached recipe/package is missing its manifest.txt

I keep a local conan cache shared across a few CI machines, and occasionally one of the cached entries ends up without a `manifest.txt` (manual cleanup gone wrong, partial copy between machines, an interrupted download, etc.). The recipe / package folder itself is still there, just the manifest file is gone.

When I then run `conan install` with integrity checking enabled against that cache, conan blows up instead of doing something reasonable. From the user's point of view the situation is recoverable — the recipe/package can simply be re-fetched from the remote — but right now I get a hard crash partway through and have to manually `conan remove` the entry to get unstuck.

I'd expect that if the integrity check finds no manifest at all in the cache for a given recipe or package, conan treats that entry the same way it treats one whose checksums don't match: warn that it's bad, drop it, and refetch from the configured remote. Having a missing manifest take down the whole install is pretty unfriendly, especially because the fix from the user side is exactly the same as for a corrupted manifest.
