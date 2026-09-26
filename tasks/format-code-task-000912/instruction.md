### Refactor: move `DeductTxCostsFromUserBalance` onto the EVM keeper

While reading `app/ante/eth.go` I noticed that `EthGasConsumeDecorator` carries three fields:

```go
type EthGasConsumeDecorator struct {
    ak         evmtypes.AccountKeeper
    bankKeeper evmtypes.BankKeeper
    evmKeeper  EVMKeeper
}
```

But if you look at how `ak` and `bankKeeper` are actually used inside `AnteHandle`, they are only there so the decorator can call the free function in `x/evm/keeper`:

```go
fees, err := evmkeeper.DeductTxCostsFromUserBalance(
    ctx,
    egcd.bankKeeper,
    egcd.ak,
    *msgEthTx,
    txData,
    evmDenom,
    homestead,
    istanbul,
)
```

The decorator itself doesn't otherwise need the account keeper or bank keeper — it just forwards them. And the EVM `Keeper` already holds an account keeper and a bank keeper internally, so at the call site we are effectively threading the same dependencies through the ante layer twice (once when constructing the EVM keeper, again when constructing the ante decorator via `NewEthGasConsumeDecorator(ak, bankKeeper, evmKeeper)`).

This feels like a layering smell: fee deduction is conceptually an EVM-keeper concern (it knows about the sender account, balances, and tx cost computation), and the ante decorator is just orchestrating when it runs.

It would be cleaner if the ante decorator only depended on the EVM keeper, and the fee/cost deduction lived as a behavior of the EVM keeper itself rather than as a free function that has to be handed its collaborators from outside. Then `EthGasConsumeDecorator` could shrink to just the evm keeper, and `NewAnteHandler` wouldn't need to pass the account/bank keepers separately into this particular decorator anymore.

Would it make sense to move `DeductTxCostsFromUserBalance` onto the EVM keeper so it can use its own account/bank keeper internally, and trim `EthGasConsumeDecorator` accordingly?
