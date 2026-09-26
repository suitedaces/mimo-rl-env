Preventing storing environment variables' values in archive
# What?

Add a new flag to a `k6 archive` that will prevent storing environment variables (passed with the `--env`) in the archive's `metadata.json`.

# Why?

Sometimes scripts can use the environment variables in the init context and it's not possible to produce an archive without passing them, however storing the actual values of the environment variables can be harmful from the security perspective.
