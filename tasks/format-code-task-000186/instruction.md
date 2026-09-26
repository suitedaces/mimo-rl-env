# Problem Statement

When I run `validator accounts import --keys-dir=... --holesky` and there's no wallet yet, it asks me "Enter a wallet directory" twice — and whatever I type the first time gets thrown away, only the second answer counts. I've also got my keystore JSON files sorted into subfolders under my keys dir, and the import doesn't seem to pick those up at all, only the ones sitting at the top level.

# Expected outcomes

- Wallet setup during `validator accounts import` should prompt for the wallet directory exactly once when no wallet exists yet, and the directory entered at that prompt should be the directory used for the wallet.
- Importing through `validator accounts import --keys-dir <DIR>` should discover keystore JSON files in the keys directory and in nested subdirectories up to a maximum scan depth of 2 nested directory levels below the keys directory.
- Keystore files located deeper than that maximum scan depth should not be imported, and the command should emit an informational message indicating that the maximum keystore-folder scan depth of 2 was reached.
- The import operation should emit an informational message when validator keystore importing begins.
- If directory processing fails during import, the command should report the failure as an inability to process the directory and import keys.

# Implementation notes

The exact internal structure, helper boundaries, traversal mechanism, and validation location are up to the implementer. Preserve existing command-line behavior aside from the observable import-flow changes described above, and avoid making tests or behavior depend on private implementation details.
