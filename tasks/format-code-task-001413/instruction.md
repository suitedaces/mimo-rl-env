## Feature request: hook to observe retries in `grpc_retry`

I'm using the retry interceptor from this package on a gRPC client and would
like to react to retries from my own application code, for things like:

- Bumping a Prometheus counter whenever a retry is fired, labelled by
  method name and attempt number.
- Sending the retry into our existing structured logger (zap) with the
  attempt number and the error that triggered the retry — the tracing the
  interceptor does internally goes through `golang.org/x/net/trace`, which
  we don't expose in production, so it's effectively invisible to us.
- Surfacing a breadcrumb to our error tracker when a particular call keeps
  hitting the retry path.

Right now I don't see any clean way to do any of this. The knobs the
interceptor already exposes (`WithMax`, `WithBackoff`, `WithCodes`, …)
control *how* retries happen, but there's nothing that lets me plug in
behavior *for when* a retry happens. As far as I can tell my only options
are forking the package or wrapping every single RPC at the call site,
neither of which is great.

Could `grpc_retry` expose an option that lets callers register a function
to be invoked each time a retry is attempted? The information I'd need at
that callsite is at least the attempt number and the error that caused the
retry; access to the request context would also be nice so I can pull
things like the method name, deadline, or trace IDs out of it.

This should work the same way for both the unary and the server-streaming
interceptors — anywhere the interceptor decides to retry a call, my hook
should run. And of course users who don't configure such a hook shouldn't
see any behavioral change.

The new call option I'd expect would be something like `WithOnRetryCallback(...)`.
