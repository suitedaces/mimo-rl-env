# Problem Statement

I'm setting up environments in my helmfile and trying to reuse a value I declared under `environments:` elsewhere in the file. For example, I declared a `releaseName` value per environment and want to use it in my release name like `myapp-{{ .Environment.Values.releaseName }}`, and also gate some releases behind a conditional like `{{ if eq .Environment.Values.releaseName "prod" }}`. But it just renders empty — the environment values don't seem to be available outside the `environments:` block itself. Is there a way to actually reference those values in the rest of the helmfile? It'd be great if I could switch environments with `--environment` and have those references resolve to the right per-env values.

# Expected outcomes

- Environment values declared under `environments:` should be available to template expressions in the rest of the same helmfile through `.Environment.Values.<key>`.
  - A release name such as `myapp-{{ .Environment.Values.releaseName }}` should render using the selected environment’s value.
  - Template conditionals in the release list should be able to include or exclude releases based on `.Environment.Values.<key>`.

- Selecting an environment should affect those references consistently.
  - Running the same helmfile with the default environment versus `--environment production` should use the values configured for the selected environment.
  - Release names, values paths, and conditional release blocks that reference `.Environment.Values.<key>` should reflect the selected environment’s values.

- Helmfile rendering should not fail prematurely only because some template content cannot be fully resolved before the selected environment’s values have been loaded, as long as the helmfile can be rendered successfully once those values are available.

- When final helmfile template rendering fails, the returned error should identify the helmfile file being parsed and include the underlying template error.

# Implementation notes

- The exact rendering strategy, data flow, and validation location are up to the implementation.
- Preserve existing helmfile behavior for environment value files, release parsing, and strict reporting of real template errors during final rendering.
- Tests and users should rely on externally observable helmfile behavior rather than on any particular internal helper, struct layout, or intermediate rendering step.
