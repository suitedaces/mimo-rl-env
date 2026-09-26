### The problem

If the myUplink cloud API is briefly unreachable (or my home network is flaky) when Home Assistant is starting up, the myUplink integration fails to set up and doesn't recover on its own. I have to manually reload the integration once connectivity is back.

### What I expected

When a transient network/connectivity problem happens during startup, I'd expect the myUplink integration to behave like most other cloud integrations in HA: mark itself as "not ready yet" so HA retries setup automatically once things come back, instead of leaving the integration broken until I notice and reload it manually.

A real auth problem (e.g. revoked token) is of course different and should still trigger the reauth flow — but a plain "couldn't reach the server right now" shouldn't put the integration into a broken state.

### Reproduction

1. Set up the myUplink integration normally so it's working.
2. Restart Home Assistant while the myUplink API endpoint is unreachable (kill DNS, block the host, restart while your internet is down, etc.).
3. Watch the integration fail to start. The error from the underlying HTTP client bubbles up out of `async_setup_entry` instead of being handled, and HA does not retry on its own.

### Environment

- Home Assistant Core (current dev)
- `homeassistant/components/myuplink`
