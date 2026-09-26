## `Block` JSON encoding drops the transaction list

When I marshal an `ethgo` `Block` to JSON I get back the usual block fields
(`number`, `hash`, `parentHash`, `gasLimit`, `uncles`, ...) but the transactions
are missing entirely from the output. The `Block` value I'm marshalling does
have its transaction hashes populated — I'm picking them up from a previous
`eth_getBlockByNumber` call — but they don't show up anywhere in the resulting
JSON.

Roughly what I'm doing:

```go
b, err := client.Eth().GetBlockByNumber(..., false)
// b.TransactionsHashes is non-empty here
out, _ := json.Marshal(b)
fmt.Println(string(out))
// -> {"number":"0x...","hash":"0x...",..., "uncles":[...]}
//    no "transactions" key at all
```

I'd expect the marshalled block to include the transaction hashes the same way
a node returns them over JSON-RPC, so I can forward / persist the block as-is
without having to wrap it in my own struct just to re-attach the txns.
