## Cap HTTP request header size to prevent DoS

Looking at `StartHTTPServer` in `server/service.go`, the `http.Server` is
configured with the various timeout fields explicitly set, but there's
no upper bound on request header size — it just inherits the Go default,
which is generous enough to be uncomfortable for a process that's
sitting on a public-facing port.

mev-boost is exposed to the network and talks to outside clients, so as
it stands a misbehaving or malicious client can keep sending oversized
request headers and put memory pressure on the boost process pretty
cheaply. The actual endpoints all take JSON bodies and the headers
themselves don't need to carry much, so a small cap should be safe in
practice.

Could we set a reasonable upper bound on incoming header bytes at the
HTTP server level as basic DoS hardening? Ideally the bound is
configurable (the rest of the server options already pick up defaults
from env vars in `cmd/mev-boost/main.go`, so the same pattern would fit)
so operators can tune it for their deployment instead of being stuck
with whatever we hardcode.
