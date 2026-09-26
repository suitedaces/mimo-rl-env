## waagent crashes / mis-behaves when publishing hostname on a VM whose network interface isn't ready yet

I'm running WALinuxAgent on an Azure Linux VM. On some of my VMs, when the agent tries to publish the hostname (e.g. after a hostname change, or early in the boot cycle), it blows up or silently fails to actually restart the right interface.

What I observe:

- On a "good" VM, publishing the hostname works — the DHCP hostname is sent and the interface comes back up with the new name.
- On a "bad" VM (same image, just different luck with timing on boot), the same code path errors out of `publish_hostname` instead of finishing. After that, the new hostname never makes it out to DHCP for that boot.
- I can also reproduce something similar on a host where the primary interface recorded by waagent doesn't match anything in the current `ifconf` listing — the agent logs a warning about the primary interface not being found and then bails out of the whole flow with an exception instead of falling back to whatever non-loopback interface is actually present.

The `get_mac_addr()` side of the world seems to cope with the "interface isn't ready yet" situation fine — I never see it fail this way. It's the hostname publishing path (which ends up calling into the same lower-level "give me an interface name" helper) that doesn't tolerate the interface being momentarily unavailable.

Expected: querying the interface name during `publish_hostname` should be just as tolerant as the MAC-address query is. If no usable interface is available right now, the agent should wait it out / skip gracefully, not raise an exception that aborts the whole publish step. And the underlying helper shouldn't be throwing in a way that takes down callers that just want a best-effort answer.

Repro is annoyingly timing-dependent on a real VM, but you can see the shape of it by forcing the situation where the recorded primary interface isn't in the current ifconf list — the agent ends the call with an exception instead of returning whatever non-loopback interface it found (or nothing at all).
