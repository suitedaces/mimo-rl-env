## sendConn doesn't support sending to alternate remote addresses (needed for connection migration)

Working on connection migration support (#234). The path validation flow needs two capabilities from the underlying send path that `sendConn` currently doesn't offer:

1. **Probing a candidate path before committing to it.** Before we commit to migrating to a new remote address, we need to send a PATH_CHALLENGE on the new path to validate it. The connection's "real" traffic at that point should still be going to the original remote address — the probe is a one-off send to a different destination. Right now `sendConn.Write` always targets the address that was passed in at construction time, so there's no clean way to fire off a single packet to some other address without disturbing the regular send path.

2. **Switching the remote address after validation succeeds.** Once path validation completes and we decide to migrate, all subsequent traffic on this connection should go to the new remote (with the new `packetInfo` for the local side as well). `sconn` stores `remoteAddr` and `packetInfoOOB` as plain fields set at construction, so today the only way to "switch" would be to tear down and rebuild the sendConn, which isn't what we want — the connection state above it shouldn't care that the path changed.

The `sendConn` interface needs to grow support for both of these. Note that the switch-over has to be safe to call while sends are happening from another goroutine (the connection's send loop), so the address/oob pair needs to be updated atomically as a unit — we don't want a Write to pick up the new address but the stale oob, or vice versa.

I'd expect the new methods on the interface to be named something like `WriteTo(b []byte, addr net.Addr) error` for the one-off send and `ChangeRemoteAddr(addr net.Addr, info packetInfo)` for the switch.
