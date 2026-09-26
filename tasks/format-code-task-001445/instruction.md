## Nomad client crashes during Consul fingerprinting when the agent's self response is incomplete

I'm running a Nomad client alongside a Consul agent. In some of my environments
(older Consul versions, plus a couple where ACLs restrict what the agent's
`/v1/agent/self` endpoint returns), the Nomad client process dies shortly after
startup with a panic that comes out of the Consul fingerprinter — i.e. it
blows up while populating the `consul.*` node attributes from whatever the
Consul agent returned.

In environments where the Consul agent returns the "full" self info, everything
is fine and I can see `consul.server`, `consul.version`, `consul.datacenter`,
etc. show up on the node. But as soon as I point the same Nomad client at one
of the funkier Consul setups, the whole client process goes down — not just the
Consul fingerprint, the entire client. That seems wrong: even if Consul info is
partially missing or shaped slightly differently than expected, I'd expect Nomad
to log something and move on, not crash.

A few things I'd like out of the fingerprinter:

- It should be defensive about whatever the Consul agent hands back. If a
  particular piece of info isn't there (or isn't the shape Nomad expected), the
  fingerprinter should skip just that piece rather than take the client down.
- I'd still like *some* signal in the Nomad logs when this happens, so I can
  tell which Consul environments are returning incomplete data — silent skipping
  would make this very hard to debug.
- Whatever info *is* available should still be recorded on the node, so the
  client is at least partially usable against a Consul agent that doesn't
  expose everything.

Happy to test a fix against the Consul setups where I'm currently seeing the
crash.
