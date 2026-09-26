# Add `exec` commands for running arbitrary executables with local bins on PATH

`pyarn` can already `run` package scripts, but there's no way to invoke an arbitrary
executable (for example a binary installed by a dependency) with the project's locally
installed tools available on `PATH`. Add a family of `exec` commands that do this.

There should be four variants, mirroring how the existing `run` commands are organised:

- a top-level `exec` that runs in the package closest to the current directory,
- a `project` `exec` that runs in the project root package,
- a `workspace` `exec` that runs inside a single named workspace,
- a `workspaces` `exec` that runs in every workspace (respecting the usual workspace
  filters).

Expose each one the same way the existing commands are exposed: a runner function plus a
matching `to…Options` builder, re-exported from the commands module, following the same
naming pattern already used by `run`/`toRunOptions`, `projectRun`/`toProjectRunOptions`,
`workspaceRun`/`toWorkspaceRunOptions` and `workspacesRun`/`toWorkspacesRunOptions`.

## Behaviour

**Parsing the command.** The executable to run and its arguments come from the `--`
passthrough array on the parsed flags (`flags['--']`): the first element is the executable
name and the remaining elements are its arguments. As with the other commands, `cwd` comes
from `flags.cwd` and defaults to the current working directory. For the single-workspace
variant the workspace name is the first positional argument.

**Execution.** Unlike `run`, this does not go through a package script — it launches the
named executable directly as a child process. The child must be spawned with:

- its working directory set to the directory of the target package, and
- an environment inherited from the current process **except** that `PATH` is prepended
  with the relevant local `node_modules/.bin` directories.

**PATH precedence.** The augmented `PATH` is built from, in order:

1. the target package's own `node_modules/.bin` directory — but only when the target
   package is not the project root itself (so the project root's bin directory is never
   added twice),
2. the project root package's `node_modules/.bin` directory,
3. the pre-existing `PATH` from the environment (when set).

These entries are joined with `:`. So when running inside a workspace, that workspace's
local bin directory comes first, followed by the project root's bin directory, followed by
the inherited `PATH`. When running at the project root, the project root bin directory
comes first.

**Unknown workspace.** The single-workspace variant must throw an error when no workspace
with the given name exists in the project.
