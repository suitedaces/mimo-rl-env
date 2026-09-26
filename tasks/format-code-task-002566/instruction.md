## Problem Statement

When I make changes to my Docker containers (creating, starting, stopping them), Salt automatically pushes the full `docker.ps` output into the mine. The problem is my containers have sensitive environment info in them, and now that's sitting in the mine where other minions can pull it via `mine.get_docker`. Is there a way to turn off this automatic mine update for Docker without breaking it for everyone else? Ideally I'd like to keep the current behavior by default but be able to disable it just for my setup.

## Expected outcomes

- Docker mine updates remain backward-compatible by default: if no opt-out setting is provided, Docker container lifecycle changes should continue to refresh the Docker data used by `mine.get_docker`.
- A minion-level configuration option, `docker.update_mine`, can disable the automatic Docker mine refresh for that minion.
- When `docker.update_mine` is set to `False`, Docker container lifecycle changes should not publish refreshed Docker container data into the mine for that minion, so `mine.get_docker` should not receive newly populated Docker data from those automatic updates.
- Disabling Docker mine updates for one setup should not change the default behavior for setups that do not opt out.

## Implementation notes

- The exact location and mechanism used to check the configuration is up to the implementer, as long as Docker lifecycle operations honor the opt-out behavior and preserve the existing default behavior.
- Keep the change scoped to automatic Docker mine refresh behavior; do not require users who rely on the existing default behavior to change their configuration.
- Avoid exposing container details through automatic mine updates when the opt-out is configured.
