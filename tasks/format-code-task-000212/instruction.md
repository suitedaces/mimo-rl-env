## Docker agent fails to deploy a flow run when a container with the same name already exists

I'm running flows via the Prefect Docker Agent. The container name is derived from the flow run name (slugified), which is fine — but if there's *already* a container with that name on the host (e.g. a stopped container left over from a previous run, or two flow runs that happen to slug to the same name), the agent fails to deploy the flow run.

### What I see

1. Start a flow that produces some container name (whatever the slug of the flow run name ends up being).
2. The flow run finishes and the container is left around (stopped, not removed).
3. Trigger another run of the same flow.
4. The agent logs an error from the Docker daemon complaining that the container name is already in use, and the flow run never starts. The agent does not retry with a different name.

The same thing happens if I happen to have an unrelated container on the host that just happens to share the name.

### What I expected

The agent already tries to pick a unique container name — there's logic that's supposed to detect a collision and append `-1`, `-2`, etc. to the slug. But in practice that logic doesn't seem to be doing anything: the conflict still slips through and `create_container` blows up. From a user's point of view, a name collision shouldn't be fatal — the agent should just pick the next free name and carry on deploying the flow run.

It would also help debugging a lot if the "starting container" log line included the actual container name that ended up being used, not just the container ID, so I can correlate agent logs with `docker ps` output when names get suffixed.
