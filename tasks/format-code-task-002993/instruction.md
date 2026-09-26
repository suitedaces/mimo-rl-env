### `make check` doesn't pass, and CI isn't running it

I was trying to clean up a patch before opening a PR and ran `make check` inside the test container to make sure I wasn't introducing any new lint warnings. To my surprise the target failed immediately — there are already a bunch of pylint warnings in the tree on a fresh checkout, before I've touched anything.

After digging around the CI config / `Dockerfile.test` it became obvious why: CI only runs `make test`, never `make check`. So nothing has been stopping lint regressions from sneaking in, and warnings have just been accumulating.

I think two things need to happen here:

1. Fix the existing lint warnings so `make check` exits clean on master.
2. Wire `make check` into the test container / CI alongside `make test`, so this doesn't silently rot again. While doing that, the test image probably also needs whatever extra packages are required for the lint tooling to actually run — right now even after fixing the warnings, a fresh container may not have everything `make check` expects.

Once both are in place, contributors can rely on `make check` locally and PRs will get lint-checked automatically.
