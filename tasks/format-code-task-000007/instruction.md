## Filling an order against a non-contract takerAsset silently "succeeds"

I was stress-testing edge cases against `fillOrderArgs` and noticed that the protocol does not behave like SafeERC20 when the taker asset address has no contract code at it.

### Repro

1. Build a regular order, but set `takerAsset` to an address that has no code deployed at it on the current network. Realistic ways this happens:
   - typo in the token address,
   - signing an order on mainnet for a token that only exists on another chain,
   - a token that has been self-destructed.
2. Maker signs and the order goes on the book.
3. A taker calls `fillOrderArgs` for that order.

### What I see

The fill goes through. `OrderFilled` is emitted, the maker's `makerAsset` is transferred out to the taker, and on the maker side I see no `takerAsset` arrived (which makes sense — there's no token contract there to actually move balances). From the maker's point of view they just gave funds away for nothing.

### What I expected

The taker→maker transfer leg should be treated as failed and the whole `fillOrderArgs` call should revert (with the existing `TransferFromTakerToMakerFailed`), so the maker's asset is never moved. That's what OpenZeppelin's `SafeERC20.safeTransferFrom` does — if the call to `transferFrom` returns no data, it still requires the callee to actually be a contract; otherwise the "success" is meaningless.

### Why I think this is in scope here

The protocol uses an internal helper (`_callTransferFromWithSuffix`) for the taker→maker transfer instead of the standard SafeERC20 path, presumably so it can append the taker asset suffix. That helper's success check is more permissive than SafeERC20's — calling into an EOA returns no return data and is being accepted as a successful ERC20 transfer. The helper should have the same "no code, no deal" guarantee that SafeERC20 has, otherwise orders against bogus / non-existent token addresses will keep draining makers.
