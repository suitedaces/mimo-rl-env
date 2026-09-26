## `snapcraft assemble` shows no error info when the build fails

When I run `snapcraft assemble` on a snap that has a problem, I get the "Snapping ..." progress line and then the command exits with a non-zero status — but **nothing** is printed about what actually went wrong. I'm left with just an exit code and no way to diagnose the failure.

Steps:
1. Set up a `snapcraft.yaml` that will cause `snappy build` to reject the result (for example, something that violates snappy's checks on the snap dir).
2. Run `snapcraft assemble`.
3. Watch the "Snapping ..." line spin, then the command quits with a non-zero status and no further output.

If I run `snappy build <snapdir>` directly on the same directory, I get a clear error message explaining what's wrong. Going through `snapcraft assemble` seems to throw that information away, which makes failures very hard to debug.

I'd expect a failing assemble to surface whatever the underlying build tool said about the failure so I can fix it.
