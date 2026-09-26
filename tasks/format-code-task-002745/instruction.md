### `txnbuild.PathPaymentStrictReceive` is declared but unusable

I'm updating some transaction-building code to match the Protocol 12 / [CAP-0024](https://github.com/stellar/stellar-protocol/blob/master/core/cap-0024.md) naming, where the old `path_payment` op was renamed to `path_payment_strict_receive`. I noticed `txnbuild` already exposes a `PathPaymentStrictReceive` type, so I tried to use it directly:

```go
op := &txnbuild.PathPaymentStrictReceive{
    SendAsset:   txnbuild.NativeAsset{},
    SendMax:     "10",
    Destination: destAddress,
    DestAsset:   txnbuild.NativeAsset{},
    DestAmount:  "1",
    Path:        []txnbuild.Asset{ /* ... */ },
}

tx := txnbuild.Transaction{
    SourceAccount: &sourceAccount,
    Operations:    []txnbuild.Operation{op},
    Timebounds:    txnbuild.NewInfiniteTimeout(),
    Network:       network.TestNetworkPassphrase,
}
err := tx.Build()
```

This doesn't compile — `*PathPaymentStrictReceive` is not accepted as a `txnbuild.Operation`, and if I try calling `op.BuildXDR()` / `op.Validate()` directly they aren't found either. The only way I can actually send this operation today is to keep using `txnbuild.PathPayment{...}`, which is the pre-Protocol-12 name.

I'd expect `PathPaymentStrictReceive` to be the usable, first-class way to build this operation now that the protocol has renamed it, while existing code using `PathPayment` still keeps working so nobody has to migrate in a panic.

Also, since CAP-0024 is about making path payments symmetrical, I'd expect `txnbuild` to additionally expose the new dual operation (something like `PathPaymentStrictSend`) so both directions of the symmetric pair are usable.
