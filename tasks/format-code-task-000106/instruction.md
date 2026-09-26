I have a custom artifact where the files Skaffold should watch come from our own build tooling, so keeping `dependencies.paths` updated by hand doesn’t really work. Could Skaffold run a script/command for that artifact and use the file list it returns as the dependencies for watching and rebuilds? Ideally it would give a clear error if the command fails or prints something Skaffold can’t understand.

Expected outcomes:
- Custom artifact configuration supports `dependencies.command`, exposed through `CustomDependencies.Command`, as an alternative dependency source for determining the files used by watching and rebuild decisions.
- When `dependencies.command` is configured, Skaffold runs that command during custom artifact dependency resolution and uses its output as the dependency list.
- The command output must be a valid JSON array of strings; invalid JSON or JSON with a different shape should fail dependency resolution with a clear error.
- If the dependency command exits unsuccessfully, dependency resolution should fail with an error that makes the failing command context clear.
- `dependencies.ignore` remains valid with `dependencies.paths`, but is invalid when combined with `dependencies.command`.
- The public schema and custom builder documentation describe the new `dependencies.command` option and its JSON-array output contract.

Implementation notes:
- The exact execution helper, parsing location, validation organization, and internal data flow are up to the implementer.
- Preserve existing dependency behavior for path-based and Dockerfile-based custom artifacts.
- Error text does not need to match any particular sentence exactly, but it should be actionable enough to distinguish command execution failures from malformed command output.
