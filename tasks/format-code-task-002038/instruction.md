# Problem Statement

Right now the only way I can run my custom scripts is by clicking through the web UI or hitting the REST API, but I really want to be able to kick them off straight from the command line on the server. Ideally I'd just point `manage.py` at a script and have it run, and be able to pass in input data and have any DB changes actually saved when I want them to be. Can we get a way to do this from the CLI?

# Expected outcomes

- CLI script execution
  - NetBox provides a `manage.py runscript <module>.<script>` command that can execute a named custom script from the server command line.
  - The required `<module>.<script>` argument identifies which custom script to run.
  - Running the command invokes the selected script and reports its script output/logging to the console in a way suitable for command-line use.

- Script input and execution options
  - The CLI command supports passing JSON-encoded input data to the selected script via `--data`.
  - The CLI command supports selecting the console log level for script output via `--loglevel`.
  - The CLI command supports an explicit `--commit` option to commit database changes made by the script.

- Persistence behavior
  - Without the explicit commit option, database changes made by a script run from the CLI must not be persisted.
  - With the explicit commit option, database changes made by a script run from the CLI must be persisted when the script succeeds.

# Implementation notes

- The concrete command implementation, validation structure, transaction boundaries, and script-loading mechanics are left to the implementer, provided the public command-line behavior above is satisfied.
- Keep existing web UI and REST API script execution behavior compatible while adding the command-line entry point.
