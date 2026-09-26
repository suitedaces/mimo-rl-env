## Problem Statement

I'm on an M1 Mac and a lot of the actions I'm running only have amd64 images, so they either fail or behave weirdly when act tries to run them natively as arm64. Is there a way to tell act to run the action containers as amd64 instead? Ideally I'd just pass something like a platform/architecture flag on the command line so I can force linux/amd64 when I need to.

## Expected outcomes

- CLI users can pass `--container-architecture <string>` with a value such as `linux/amd64`, and the command accepts it as a global option for workflow runs.
- `act --help` documents `--container-architecture` and explains that omitting it keeps the existing behavior of using the current machine architecture.
- When `--container-architecture` is provided, action containers are created or run using the requested platform instead of implicitly using the host architecture.
- Programmatic runner configuration exposes the requested container architecture through `runner.Config.ContainerArchitecture` so callers can apply the same behavior without going through the CLI.
- User-facing flag documentation, including the README flag list, includes the new `--container-architecture` option.

## Implementation notes

The specific data flow, validation location, and container-runtime integration points are up to the implementation. Preserve existing behavior when the option is not provided, and avoid changing unrelated CLI flags or workflow execution semantics.
