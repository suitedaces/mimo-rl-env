### Refactor websocket dial into its own package with extensible options

Right now the websocket client lives in `pkg/conn` alongside the generic `Conn` interface and `RetryableError`, and the dial entrypoint looks like:

```go
conn.DialWebsocket(ctx, url, token)
```

A couple of things make this awkward:

1. The websocket-specific code (dialer, retryable status codes, message-type checks, the `WebsocketConn` wrapper) is mixed into the same package as the transport-agnostic `Conn` interface. They're really two different concerns.

2. `DialWebsocket` takes its configuration as positional arguments. Today it's just `token`, but as soon as we want to expose anything else for the dialer (TLS config, custom headers, timeouts, etc.) we'd have to either keep growing the positional parameter list or break every caller.

I'd like to pull the websocket client out into its own subpackage under `pkg/conn`, and make the dial function take an extensible set of options instead of hard-coded positional args, so the bearer token is just the first such option and additional ones can be added later without churn.

Callers are in `agent/endpoint.go` (client side, currently passes `e.conf.Auth.APIKey`) and `server/server/upstream/server.go` (server side, just wraps an already-upgraded `*websocket.Conn`) — both should be updated to the new package.

Behaviour of the connection itself (binary-only messages, retryable status code handling, wrapping the underlying `*websocket.Conn`) should stay the same; this is purely a packaging + API-shape change.
