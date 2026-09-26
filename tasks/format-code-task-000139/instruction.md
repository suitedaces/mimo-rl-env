## Problem Statement

Hey, I noticed `kusion apply` still has all those `--backend-*` flags hanging around and it's building its state storage the old way, while the rest of the CLI seems to be moving toward the new backend + workspace setup. Can we bring `apply` in line with that? Just pulling the default backend and running against the `default` workspace would be fine for now — I don't really need to pick a backend per-invocation from flags anymore.

Also while you're in there, the ApplyRequest we send downstream still carries that `Cluster` field pulled from `-D cluster=...`, which feels like a leftover from the old model — I'd rather it carry the workspace instead so operators see something consistent with preview.

## Expected outcomes

- `kusion apply` CLI behavior
  - The `kusion apply` command no longer exposes backend-specific command-line flags.
  - Invoking `kusion apply` with an old backend-specific flag is rejected as an unknown flag instead of being accepted as a per-invocation backend override.

- Default workspace/backend behavior
  - Applying a stack uses the repository’s default backend behavior rather than backend options supplied on the `apply` command line.
  - The apply flow runs against the `default` workspace for now.
  - Preview information produced during apply is associated with that same workspace.

- Downstream apply request behavior
  - The apply request sent to the operation layer carries workspace information consistently with preview.
  - A `cluster` value supplied through `-D cluster=...` is not forwarded as the apply request’s cluster routing value.

## Implementation notes

- Keep the implementation aligned with the repository’s current backend and workspace concepts.
- The exact internal wiring, helper structure, and validation location are up to the implementation, as long as the externally observable CLI behavior and downstream request behavior match the outcomes above.
