I'm trying to pull a list of all the chart repositories under one of my Container Registry instances so I can iterate over them in Terraform, but the alicloud provider doesn't seem to expose a data source for that — I can list image repos but not chart ones. Could you add something on the alicloud provider side so I can query chart repos under a given CR instance? Ideally I'd also be able to filter by name or by a set of ids, and dump the result to a file if I want.

Expected outcomes:
- Data source availability: Terraform configurations can use `data "alicloud_cr_chart_repositories"` to read chart repositories for a Container Registry instance.
- Required input: `alicloud_cr_chart_repositories.instance_id` is required, so validation or planning reports a missing required argument when it is omitted.
- Repository results: `alicloud_cr_chart_repositories.repositories` returns the matching chart repositories, with each item exposing `chart_repository_id`, `create_time`, `instance_id`, `id`, `repo_name`, `repo_namespace_name`, `repo_type`, and `summary`.
- Stable identifiers: each repository `id`, and each value in the top-level `ids` output, identifies a chart repository using its instance, namespace, and repository name; the top-level `names` output contains the repository names.
- Filtering: `alicloud_cr_chart_repositories.name_regex` limits results to repository names matching the regular expression, and invalid regular expressions are rejected during configuration validation.
- Filtering by identifiers: `alicloud_cr_chart_repositories.ids` can be supplied to return only repositories whose identifiers are in the supplied set.
- Optional file output: when `alicloud_cr_chart_repositories.output_file` is set, the data source writes the returned repository list to that path.

Implementation notes:
- Follow the provider’s existing conventions for Terraform data sources, schema validation, state shape, pagination, retries, and optional file output.
- The specific helper functions, internal data structures, request construction, and filtering location are implementation details, as long as the public Terraform behavior above is satisfied.
- Do not require users to manage chart repositories with a new resource in order to use this data source; it should work for existing chart repositories in the target instance.
