# Problem Statement

When I run `jobber log` and there happen to be no run log entries yet, it just prints out the bare column header row (TIME JOB SUCCEEDED RESULT ...) and nothing else, so for a second I can't tell if the command actually worked or if something went wrong. It's a bit confusing to stare at an empty table with no rows under it.

# Expected outcomes

- Empty run-log output:
  - When `jobber log` has no run-log entries to display for the current user, it should print a clear empty-state message: `No run logs.`
  - When `jobber log` has no run-log entries to display in the all-users view, it should print the same clear empty-state message: `No run logs.`
  - In the empty-state case, the command should not print a table header such as `TIME JOB SUCCEEDED RESULT`.

- Existing log output:
  - When run-log entries do exist, `jobber log` should continue to show the normal tabular log output, including the appropriate header and one or more entry rows.
  - Existing behavior for ordering and formatting non-empty log output should remain unchanged from the user’s perspective.

# Implementation notes

The exact code structure, helper functions, and retrieval path used to determine whether there are run-log entries are up to the implementer. Prefer behavior-preserving changes that keep the non-empty log display working while making the empty log display unambiguous.
