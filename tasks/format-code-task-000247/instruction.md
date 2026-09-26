# Add configurable "toxics" to proxies

Right now a proxy is a dumb pipe: whatever a client sends is forwarded verbatim to the
upstream and back. We want to be able to deliberately degrade a proxied connection so we can
test how applications behave against a flaky network. The first degradation we need is
**latency**.

Introduce the notion of a *toxic* that can be attached to a proxy, independently for each of
the two traffic directions:

- **upstream** — data travelling from the client toward the upstream server.
- **downstream** — data travelling from the upstream server back to the client.

## HTTP API

Add these endpoints to the existing API server (the one that already serves `/proxies`):

- `GET /proxies/{proxy}/upstream/toxics`
- `GET /proxies/{proxy}/downstream/toxics`

  Returns a JSON object that maps each available toxic's name to its current state. A freshly
  created proxy must already list a toxic named `latency` in **both** directions, and that
  toxic must start **disabled**. The latency toxic's state is a JSON object with these fields:
  `enabled` (bool), `latency` (number, milliseconds) and `jitter` (number, milliseconds). On a
  new proxy it reads `{"enabled": false, "latency": 0, "jitter": 0}`.

- `POST /proxies/{proxy}/upstream/toxics/{name}`
- `POST /proxies/{proxy}/downstream/toxics/{name}`

  Sets the complete desired state of the named toxic for that direction from the JSON request
  body and responds with the resulting toxic state as JSON. The body fully specifies the new
  state: any field that is omitted is reset to its zero value (so `enabled` defaults to
  `false`, and `latency`/`jitter` default to `0`). The change must persist — a subsequent
  `GET` reflects it — and must affect **only** the direction it was posted to; the same toxic
  in the other direction is left untouched.

### Errors

- A request for a proxy that does not exist responds with HTTP `404`.
- A `POST` to a toxic name that does not exist responds with HTTP `404`.

## Behavior

The latency toxic must actually slow traffic down, not just record settings. When the
`latency` toxic is enabled with a latency of *L* milliseconds (and `jitter` 0) on a direction,
data flowing in that direction is delayed by approximately *L* milliseconds before it reaches
the other side. A direction whose latency toxic is disabled forwards data with no added delay,
exactly as before.

Configuration applied before a client connects takes effect for that connection.
