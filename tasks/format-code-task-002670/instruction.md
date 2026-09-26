## `Gateway.GetAddrUxOuts` is awkward to use for multiple addresses, and leaks a JSON type into the gateway layer

I'm writing some tooling on top of `daemon.Gateway` and ran into two issues with `GetAddrUxOuts`:

**1. Can only query one address at a time.**

I have a list of addresses (e.g. all addresses in a wallet) and want their uxouts. Right now I have to loop on the caller side and call `gw.GetAddrUxOuts(addr)` once per address, then concatenate the results myself. Every caller that wants this ends up duplicating the same loop. It would be much nicer to pass the whole batch in one call and get the combined result back.

**2. Gateway returns `*historydb.UxOutJSON` instead of `*historydb.UxOut`.**

Compare it with `Gateway.GetUxOutByID`:

```go
GetUxOutByID(id cipher.SHA256) (*historydb.UxOut, error)
GetAddrUxOuts(addr cipher.Address) ([]*historydb.UxOutJSON, error)
```

`GetUxOutByID` returns the domain object (`UxOut`), but `GetAddrUxOuts` returns the JSON-presentation wrapper (`UxOutJSON`). The gateway is supposed to be a read-only API over daemon state — JSON serialization is the HTTP handler's concern, not the gateway's. As a non-HTTP caller I don't want JSON-shaped data; I want the actual `UxOut` so I can use its typed fields. If I do want JSON output I can convert it myself with `historydb.NewUxOutJSON`, which is what the HTTP handlers should be doing anyway.

Could `GetAddrUxOuts` be reworked to accept a batch of addresses and return the raw `UxOut` values? The existing webrpc (`getAddrUxOutsHandler`) and gui (`getAddrUxOuts`) endpoints that currently surface this data over HTTP should keep returning the same JSON shape they do today — they'd just do the conversion themselves at the handler boundary.
