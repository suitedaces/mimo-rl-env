## Feature request: header-only RPC client queries

I'm working on the Evmos JSON-RPC layer, where we translate Ethereum-style JSON-RPC calls onto Tendermint. A couple of those endpoints (`eth_header` / `eth_header_by_hash`, and various light-client paths) only need the block **header** — they don't care about txs, commit signatures, evidence, or the rest of the block body.

Today the only way I can serve those from the Tendermint RPC client is to call `Block(ctx, &height)` or `BlockByHash(ctx, hash)` and then throw everything but `result.Block.Header` away. That's wasteful on two counts:

1. The node serializes and ships the full block payload over the wire (txs, last commit, evidence, ...), all of which I immediately drop.
2. On the client side I pay the deserialization cost for a `*types.Block` I'm not going to use.

For a JSON-RPC gateway that fans out a lot of header lookups (per-block polling, log filters resolving block hashes, light-client header sync, etc.) this adds up quickly.

It would be great if the RPC client exposed header-only equivalents of the existing block queries — one that takes a height and one that takes a block hash — so callers that only need the header can ask for just that. Semantics should line up with what `Block` / `BlockByHash` already do (e.g. an omitted height means "latest", a hash that isn't known returns an empty result rather than an error).

Happy to use these from both the regular HTTP client and the local in-process client, so ideally they live on the shared client interface alongside `Block` and `BlockByHash`. Naming-wise something like `Header(...)` / `HeaderByHash(...)` would line up with the existing `Block` / `BlockByHash` pair.
