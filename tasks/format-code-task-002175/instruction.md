## Add a mutative `QuoRoundUp` for `osmomath.BigDec`

While profiling the concentrated-liquidity swap math (in particular the
`GetNextSqrtPriceFromAmount0InRoundingUp` / `GetNextSqrtPriceFromAmount0OutRoundingUp`
path) I noticed that the round-up quotient step is forced to go through the
non-mutative `BigDec.QuoRoundUp`, which allocates a fresh `big.Int` for the
result every call.

For most of the other arithmetic primitives on `BigDec` we already have
mutative counterparts (`MulMut`, `AddMut`, `QuoMut`, etc.) that the hot paths
use to keep allocations down — chains like `liquidity.Mul(sqrtPriceCurrent).QuoMut(...)`
or `someVal.AddMut(other)` are common in the CL math file precisely to avoid
spinning up extra `big.Int`s inside swap loops. The round-up quotient is the
odd one out: there is no mutative version of `QuoRoundUp`, so any call site
that needs a round-up division has to fall back to the allocating form even
when the receiver is a freshly produced intermediate that we would be perfectly
happy to clobber.

Concretely, in CL math we end up writing things like:

```go
return liquidity.Mul(sqrtPriceCurrent).QuoRoundUp(denominator)
```

The `liquidity.Mul(sqrtPriceCurrent)` already produces a fresh `BigDec` whose
internal `big.Int` we own, but `QuoRoundUp` still allocates a brand new one
for the final result instead of reusing it. The same pattern shows up in
`stableswap.calcInAmtGivenOut`, where we divide the cfmm input by
`(1 - spreadFactor)` using `QuoRoundUp` on an intermediate value.

It would be nice to have a mutative round-up quotient on `BigDec` with the
same numerical behavior as `QuoRoundUp`, and then route the obvious CL /
stableswap call sites that operate on freshly produced intermediates to the
mutative version so we stop paying for those allocations on every swap.

No behavioral change is expected — output values should match the existing
`QuoRoundUp` exactly; this is purely about avoiding the extra `big.Int`
allocation along that code path.
