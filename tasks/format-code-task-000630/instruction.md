## Bitso integration: all REST calls fail

I'm trying to use ccxt to pull market data from Bitso (Python). Pretty
standard setup — instantiate the exchange, call `fetch_markets()` or
`fetch_ticker('BTC/MXN')`. Every call fails immediately: I'm getting
connection errors / non-2xx responses back from ccxt and nothing comes
through.

When I dug into the request that ccxt is actually firing, the host it's
hitting doesn't appear to be reachable anymore. Trying the same base
host straight from a browser / curl doesn't load either, so it looks like
Bitso has moved their REST API to a different URL and the one shipped
inside ccxt is stale.

Could the Bitso URLs in ccxt be updated to whatever the currently-live
endpoint is? Same goes for the sandbox/test endpoint if that also moved
— I haven't been able to reach the test environment either.

Minimal repro:

```python
import ccxt
ex = ccxt.bitso()
print(ex.fetch_markets())   # fails
```

Happy to test once it's updated.
