## Problem Statement

I’m trying to see all projects in my current org from the CLI, but `coder projects` doesn’t seem to have a way to list them. Could you add a `coder projects list`/`ls` command that shows the basics like name, source, last updated, and how many developers are using each project? It’d also be helpful if the projects API exposed that usage count so the CLI can show it.

## Expected Outcomes

- Project listing from the CLI: `coder projects list` lists projects in the current organization and displays a tabular summary with `Project`, `Source`, `Last Updated`, and `Used By` columns.
- Short alias: `coder projects ls` performs the same listing behavior as `coder projects list`.
- Empty organization output: when there are no projects in the current organization, the list command prints a friendly empty-state message and points users to `coder projects create <directory>` instead of showing an empty table.
- API usage count: project listing API responses include a numeric `workspace_owner_count` field for each project.
- CLI usage count display: the `Used By` column reflects each project’s usage count, using singular wording for exactly one developer and plural wording otherwise.

## Implementation Notes

- The command should use the existing CLI authentication, organization selection, and project retrieval conventions.
- The API and CLI should remain consistent: the CLI should display the usage count exposed by the project listing API.
- Specific data structures, helper functions, query organization, and formatting implementation details are up to the implementer as long as the observable behavior above is satisfied.
