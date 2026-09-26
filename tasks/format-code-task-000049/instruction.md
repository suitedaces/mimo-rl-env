# Problem Statement

I'm trying to spin up containers on my Flocker cluster via the HTTP API but I can't find a way to do it — the configuration endpoints let me create datasets but there's nothing for containers as far as I can tell. Can we get a POST under `/v1/configuration/containers` so I can declare a container (host + name + image) the same way I declare datasets? Also it'd be nice if it actually rejected duplicate names instead of silently letting two containers share one.

One small thing while you're in there: the duplicate-dataset_id 409 returns its error under a `message` key, but every other error I've hit uses `description` — kinda annoying to special-case in my client, would be great to make that consistent.

# Expected outcomes

- Container configuration creation:
  - A `POST` to `/v1/configuration/containers` with a JSON body containing `host`, `name`, and `image` creates a container entry in the cluster configuration.
  - A successful container creation returns HTTP `201 Created`.
  - The successful response body includes the same `host`, `name`, and `image` values supplied by the client.
  - The created container is persisted in the configuration for the specified host.

- Duplicate container names:
  - Creating a container with a `name` that is already used by any configured container is rejected.
  - Duplicate container-name requests return HTTP `409 Conflict`.
  - Duplicate container-name error responses use a `description` field that explains the duplicate-name conflict.

- Dataset conflict error format:
  - Duplicate `dataset_id` configuration requests continue to return HTTP `409 Conflict`.
  - The duplicate-`dataset_id` conflict response uses a `description` field rather than a `message` field.

# Implementation notes

- Match the existing HTTP API conventions in this repository for routing, JSON request/response validation, persistence, and error formatting.
- The internal data structures, helper functions, and exact placement of validation or collision checks are implementation details; preserve the externally observable API behavior described above.
