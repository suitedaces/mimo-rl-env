## cUSDT balance not detected, CHAI also looks off

I track my DeFi portfolio with rotki and recently added the ethereum address that holds my Compound USDT (cUSDT) position. The token is listed in rotki's supported asset list, so I expected the balance to show up automatically the way cDAI, cUSDC, cBAT etc. all do.

What actually happens:

- cUSDT: the balance never appears at all. Other cTokens on the same address (cDAI, cUSDC) are detected fine, so the address itself and the ethereum connection are working — only cUSDT is silently missing from the totals.
- CHAI: I also hold some CHAI on the same address and the entry behaves strangely compared to other ERC20s I track. Hard for me to say more from the UI alone, but combined with the cUSDT issue it made me look at how these two are configured.

Both of these are declared as supported ethereum tokens in rotki's asset list, so as a user I'd expect "add address → balance shows up" to just work the same as it does for every other supported ERC20.

Could you check the asset entries for `cUSDT` and `CHAI`? Something about how they're registered seems to prevent rotki from querying their on-chain balances correctly.
