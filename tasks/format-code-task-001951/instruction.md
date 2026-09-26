### Parsed `RunCommand` doesn't expose which flags were used on the RUN instruction

I'm building some tooling on top of `frontend/dockerfile/instructions` that needs to react to which flags appear on a `RUN` line in a Dockerfile. For example, given:

```dockerfile
RUN --mount=type=cache,target=/root/.cache/go-build go build ./...
RUN echo hello
```

I'd like to be able to tell the two `RUN` instructions apart after parsing — the first one uses `--mount`, the second doesn't.

After calling `instructions.Parse(...)` (or going through `ParseInstruction` and getting back a `*RunCommand`), I can see the command line and whether the shell is prepended, but the `RunCommand` struct doesn't carry any information about which flags were actually specified on that RUN. The `BFlags` instance used during parsing is internal to `parseRun` and gets discarded once parsing finishes, so there's no way for me (or for a `parseRunPostHooks` callback) to find out which flag names were present on the source line.

This is awkward because the flags are a real part of the `RUN` syntax in modern Dockerfiles (`--mount`, `--network`, `--security`, plus whatever a custom frontend may add), and downstream consumers often need to know which of them the user wrote in order to enable/disable behavior or to validate combinations.

Could `RunCommand` (or the parsing path that produces it) expose the set of flag names that were used on that particular RUN? I don't need the values necessarily — just knowing which flags were set on this specific instruction would be enough.

I'd expect something like a `FlagsUsed` accessor on the parsed `RunCommand`, plus a corresponding `Used()` helper on `BFlags` to surface the set of flag names that were actually set during parsing.
