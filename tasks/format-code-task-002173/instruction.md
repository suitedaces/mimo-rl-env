## Confusing error when swapping against an empty concentrated-liquidity pool

I'm playing with the concentrated-liquidity module on a local node. I created a CL pool but haven't added any positions to it yet (no LP has provided liquidity). When I try to swap against it via `SwapExactAmountIn` / `SwapExactAmountOut`, the call fails — but the error I get back is something internal from deep inside the swap algorithm and doesn't really tell me what went wrong.

From a user's perspective, the failure is obvious in hindsight: there's literally no liquidity in the pool, so of course the swap can't be priced. But the error message I see doesn't say that. It looks more like a generic computation/iteration error, which sent me chasing my own parameters and pool config for a while before I realized the actual issue was just that nobody had opened a position yet.

It would be much friendlier if swapping against a concentrated-liquidity pool that has no positions returned a descriptive, specific error indicating that the pool has no liquidity / no positions to swap against. That way clients (UIs, scripts, other modules) can react to this case cleanly instead of having to pattern-match on an opaque internal message.

This applies to both directions of swap (exact-amount-in and exact-amount-out) since both hit the same underlying problem on an empty pool.

The new error type for this case I'd expect is something like `NoSpotPriceWhenNoLiquidityError` (carrying the pool id).
