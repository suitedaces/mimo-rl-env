## Gas fees suggested by wallets are way too high — need a reliable way to estimate

We've been seeing very inflated gas fee suggestions on the test network and traced it back to how third-party wallets currently estimate fees.

### What's happening

Today a wallet has no on-chain way to ask "what is the current gas price?". The common workaround is to look at past transactions and compute `GasFee / GasUsed`, then multiply by a simulated gas amount to suggest a fee for the next tx.

The problem: users tend to set `-gas-fee` and `-gas-wanted` very generously to make sure the tx lands (any of: insufficient gas, wrong func name, bad arg type, failing assertion will burn the fee). When a tx fails the chain still keeps the fee, and the actually-used gas is typically much smaller than what the user paid for. So `GasFee / GasUsed` from historical txs ends up being many times the real on-chain gas price, and once a wallet multiplies that by the simulated gas, the suggested fee is wildly too high.

Concretely, even a trivial call ends up being suggested at huge fees, and users either overpay or get scared off.

### What I'd like

Two things, both aimed at giving wallets and CLI users an honest number to work from:

1. **An on-chain query for the current gas price**, so wallets can read it directly instead of inferring it from `GasFee/GasUsed` of historical txs. Something I can hit via `gnokey query ...` and get back the gas price the chain is actually charging right now.

2. **Have `gnokey maketx ... -simulate only` report an estimated gas fee**, not just `GAS USED`. Right now I can run a simulation and see how much gas a call consumes, but I still have to guess the fee separately. It would be much more useful if the simulation output told me both the gas it would use *and* a fee figure derived from the current on-chain gas price, so I can plug those numbers straight into a real broadcast:

   ```
   # simulate
   gnokey maketx call -pkgpath gno.land/r/hello -func Hello \
       -gas-wanted 2000000 -gas-fee 1000000ugnot \
       -broadcast -chainid tendermint_test -simulate only test1

   # then use the suggested gas + fee for the real submission
   gnokey maketx call -pkgpath gno.land/r/hello -func Hello \
       -gas-wanted <from simulation> -gas-fee <from simulation> \
       -broadcast -chainid tendermint_test test1
   ```

   The simulation itself shouldn't charge anything (sequence and balance untouched).

It would also be nice if real-time gas price were exposed as a metric for monitoring, since we already collect telemetry for other parts of the node.

The goal is just: make it possible for a wallet (or a careful CLI user) to suggest a fee that's in the same ballpark as what the chain will actually charge, instead of 100x over.
