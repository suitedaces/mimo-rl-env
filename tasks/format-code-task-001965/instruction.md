## Problem Statement

When I create a project with `mongodbatlas_project`, only the API key I'm using to run Terraform ends up attached to the new project. I've got a few other programmatic keys in the org that need to operate on this project for automation, and right now I have to go click around in the UI (or run a separate script) to attach them with the right roles afterwards. Could the project resource let me declare extra API keys + their project roles inline so they get attached on create? And ideally the project data sources would surface the keys currently on a project too, so I can reference them.

## Expected Outcomes

- Project resource configuration: `mongodbatlas_project` supports optional `api_keys` entries, where each entry declares an `api_key_id` and `role_names`; when a project is created with these entries, the declared programmatic API keys are associated with the project using the declared project roles.
- Create-time errors: if attaching any declared API key to the project fails during project creation, Terraform reports a diagnostic whose message starts with `error assigning api keys to the project:`.
- Single project data source: `data.mongodbatlas_project` exposes the project’s API-key associations through `api_keys` entries containing `api_key_id` and `role_names`.
- Projects collection data source: each element in `data.mongodbatlas_projects.results` exposes the project’s API-key associations through `api_keys` entries with the same item shape.
- Role output filtering: data source `api_keys[*].role_names` includes project-level roles and excludes organization-level roles whose names begin with `ORG_`.
- Documentation: the acceptance-test environment variable documentation for Project(s) resource configuration includes `MONGODB_ATLAS_API_KEYS_IDS=<API_KEYS_IDS>`.

## Implementation Notes

- The exact internal data structures, helper functions, and validation locations are up to the implementation.
- Keep the behavior compatible with Terraform provider conventions for optional resource configuration and computed data source attributes.
- Data source reads should remain focused on externally visible project API-key associations rather than exposing provider-internal representations.
