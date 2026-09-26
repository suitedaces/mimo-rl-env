### Feature request: support `clean` as a top-level option in `buf.gen.yaml` (v2)

Right now the only way to wipe plugin output directories before code generation is the `--clean` flag on `buf generate`. There's no equivalent in the config file.

In a v2 `buf.gen.yaml` like this:

```yaml
version: v2
plugins:
  - local: custom-gen-go
    out: gen/go
    opt: paths=source_relative
    strategy: directory
  - protoc_builtin: java
    out: gen/java
```

I always want `gen/go` and `gen/java` to be cleared before regeneration so stale files from renamed/removed protos don't linger. Today I either have to remember to pass `--clean` on every invocation, or wrap `buf generate` in a script that does `rm -rf` first. Both are easy to forget, especially in CI / Makefile setups shared across a team.

It would be much nicer to declare this once in the config, e.g.:

```yaml
version: v2
clean: true
plugins:
  - local: custom-gen-go
    out: gen/go
    ...
```

and have `buf generate` honor it the same way `--clean` does today (delete the directories / jar / zip that each plugin's `out` points at, before generation runs).

### Interaction with the existing `--clean` flag

The CLI flag should still win when the user explicitly passes it, in either direction:

- `clean: true` in config + `buf generate --clean=false` → don't clean
- `clean: false` (or unset) in config + `buf generate --clean` → clean

That way the config sets the project default, and someone running locally can still override it for a single invocation without editing the file.
