### websocket `eth_subscribe("logs", ...)` doesn't accept standard topic filter combinations

I'm building a dapp that listens to ERC20 `Transfer` events on a specific contract via websocket. On other Ethereum-compatible nodes (geth, infura, etc.) I subscribe like this and it works fine:

```js
ws.send(JSON.stringify({
  id: 1, method: "eth_subscribe",
  params: [
    "logs",
    {
      address: "0xcontract...",
      topics: [
        "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef", // Transfer(address,address,uint256)
        null,                          // any `from`
        [                              // `to` is one of these two
          "0x000000000000000000000000aaaa....",
          "0x000000000000000000000000bbbb...."
        ]
      ]
    }
  ]
}))
```

i.e. the standard ethereum topic filter shape: each position in the `topics` array can be `null` (wildcard), a single hash string (exact match), or an array of hash strings (OR). Against okexchain's websocket, this request comes back with `invalid topics` and the subscription never establishes.

If I dumb it down to only single-hash entries (no nulls, no inner arrays), the subscription succeeds — but then the message I get back over the socket carries an **array** of logs in `params.result` for a single tx, which my client (and standard tooling) doesn't expect; tools assume `result` is a single log object per notification, the same way geth pushes them.

A couple more things I noticed while testing:

- If I pass a malformed/garbage string in `address`, the subscription is still accepted instead of rejected. I'd expect non-hex / wrong-length values to fail the request up front like other clients do.
- Same for `topics` — non-hex strings should be rejected, not silently accepted and turned into junk hashes.

Could the websocket logs subscription be made compatible with the standard ethereum filter behavior? Concretely I'd expect:

1. `topics` accepts the full combination shape (null / single hex hash / array of hex hashes per position).
2. Each matching log is delivered as its own notification (not batched as an array).
3. Bad hex in `address` or `topics` returns an error instead of being accepted.

Right now point 1 makes existing client code unusable against this endpoint, and point 2 means even the simplified case doesn't round-trip through standard libraries. Thanks!
