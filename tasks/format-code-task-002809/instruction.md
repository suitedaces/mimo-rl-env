## Telepresence fails to connect after a daemon is killed ungracefully, requires manual socket cleanup

If a telepresence daemon process is terminated ungracefully (e.g. `kill -9`, an OOM kill, or a hard reboot), it leaves its unix socket behind in the filesystem. The next time I try to use telepresence, it sees that socket, assumes the daemon is still running, tries to talk to it, and bails out with an error along the lines of "...this usually means that the process has terminated ungracefully".

At that point the only way forward is to go find the stale socket file by hand and `rm` it before telepresence will work again. This is annoying and not at all obvious to users who don't know where these sockets live or that this is what happened — they just see telepresence as "broken" until someone tells them the trick.

### Repro

1. Start telepresence normally so the daemon/connector is up and the socket file exists.
2. `kill -9` the daemon process (or just hard-reboot the machine while it's running).
3. Run telepresence again.

Expected: telepresence connects fine. The previous run is over, there's no live process owning that socket, so a stale socket file from a dead process shouldn't permanently break the next invocation.

Actual: telepresence prints the "process has terminated ungracefully" error and exits. I have to manually delete the socket file before it works again.

It would be much nicer if telepresence detected this situation on its own and recovered, rather than dumping it on the user.
