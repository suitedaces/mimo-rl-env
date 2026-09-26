# Problem Statement

Hey, small thing that keeps tripping me up — when I run something like `tk status stage/service` from my repo root, it just errors out because `stage/service` isn't a real path on disk. But that's actually the name of one of my inline environments. Could tanka be a bit smarter here and, when the path doesn't exist, try treating it as an environment name and look for it in the current dir? Would save me from always having to pass the full path or `--name`.

Also while you're in there, when there are multiple envs matching and I *did* pass a name, the error doesn't even mention the name I gave — would be nice if it told me what I asked for vs. what it found.

# Expected outcomes

- Environment selection from the CLI should accept an argument that is not an existing filesystem path as a possible environment name, and should resolve that name against environments discoverable from the current working directory.
- This fallback should only apply when the supplied path truly does not exist; other filesystem errors while checking the supplied path should still be surfaced as errors.
- Existing path-based environment loading and explicit `--name` selection should continue to work as before.
- When a command or loader selection finds multiple matching environments after a name was provided, the error should make clear both the requested name and the matching environments found, so the user knows how to choose a more specific name.
- When multiple environments are found without a provided name, the existing guidance to use `--name` should remain clear and should still list the available environment names.

# Implementation notes

- The exact place where the fallback is handled, and the internal structure used to carry selection state, are up to the implementation.
- Preserve existing behavior for valid paths and for unambiguous environment matches.
- Keep error reporting user-oriented; do not require callers to know internal loader details in order to understand what went wrong.
