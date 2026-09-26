## Message has no way to indicate which network it belongs to

I'm using `iota.MessageBuilder` to construct messages and ship them to nodes. The current `Message` only carries: version, the two parents, payload and nonce.

The problem: there's nothing in the message itself that says *which IOTA network* it was produced for. If I have a node running on a testnet and someone replays a binary message that was actually meant for mainnet (or any other separately‑deployed network), the node has no way of telling — the bytes deserialize fine and look like a valid message. Same on the JSON side: a serialized message round‑tripped through `MarshalJSON` / `UnmarshalJSON` carries no network information.

I'd expect a `Message` to carry an identifier of the network it's intended for, set by the producer at build time and preserved across:

- binary `Serialize` / `Deserialize`
- `MarshalJSON` / `UnmarshalJSON`
- `MessageBuilder` (so I can set it fluently before `Build()`)

That way a node receiving a message can reject it up front if it's meant for a different network, instead of accepting arbitrary bytes from foreign networks.

I'd expect the new field on `Message` to be something like `NetworkID` (a `uint64`), with a JSON representation under the key `"networkId"` (encoded as a string, consistent with how `nonce` is handled).
