## Client doesn't retry other machines when a request to one machine fails at the network layer

I'm using go-etcd against a multi-node etcd cluster and relying on the
client's built-in retry/fail-over to keep things working when one node
becomes unavailable (machine down, connection refused, transient network
hiccup, etc.).

What I expected: if the client can't even get a response back from one
of the machines in the cluster, it should move on and try another one,
up to the usual retry limit.

What actually happens: the very first network-level failure bubbles
straight back out of `SendRequest` to my code. The other machines in
the cluster are never tried, even though they're healthy and listed in
`cluster.Machines`. Effectively a single bad node takes the whole call
down instead of being failed over.

Minimal repro: point a `Client` at a cluster where the first machine in
the list is unreachable (e.g. nothing listening on that port, or pull
its network), and do any normal `Get`/`Set`. The call returns the
underlying dial/connection error immediately instead of retrying the
other members.

The HTTP-status retry path (e.g. 500 from the server) seems to behave
correctly — only the "no response at all" path is broken. Since this is
exactly the case where retrying matters most, I'd expect the default
retry policy to keep going here rather than surface the error on the
first attempt.
