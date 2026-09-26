I'm seeing `docker-machine scp` fail or prompt for a password when copying to a machine that I normally access through my loaded `ssh-agent` key. Plain `ssh` to the same host works, and I don't have an explicit SSH private key path configured for that machine, so it looks like `scp` isn't using the agent identity.

Expected outcomes:
- SSH agent compatibility: `docker-machine scp` should allow the underlying SSH/SCP authentication flow to use identities loaded in `ssh-agent` when a docker-machine endpoint involved in the copy does not have an explicit SSH private key path configured.
- Explicit-key preservation: when every docker-machine endpoint involved in a `docker-machine scp` transfer has an explicit SSH private key path configured, the command should continue to restrict authentication to the configured explicit identity.
- Transfer direction coverage: the behavior should apply whether the docker-machine endpoint without an explicit key is the copy source or the copy destination.

Implementation notes:
- The exact validation location and command-construction structure are up to the implementation.
- Preserve existing `docker-machine scp` behavior unrelated to SSH identity selection, including recursive copies and local-path handling.
