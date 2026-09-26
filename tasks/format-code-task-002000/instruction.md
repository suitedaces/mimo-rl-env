## Refactor: move `TxPreProcessorCreator` into `RunTypeComponents`

Right now `TxPreProcessorCreator` is wired into the node as a standalone field on both `ProcessComponentsFactoryArgs` and `ArgsGenesisBlockCreator`. Every entry point (`nodeRunner`, `sovereignNodeRunner`, the chain simulator, integration tests, the realcomponents test runner, `testscommon/components`, etc.) has to remember to construct it (shard variant for the regular node, sovereign variant for the sovereign node) and plumb it through separately.

This is inconsistent with how all the other "run-type-dependent" creators are handled. Things like `SCResultsPreProcessorCreator`, `SCProcessorCreator`, `AccountsCreator`, `ShardCoordinatorCreator`, `RequestersContainerFactoryCreator`, `InterceptorsContainerFactoryCreator`, `ShardResolversContainerFactoryCreator`, etc. all live on `RunTypeComponents` and are picked from there by whoever needs them — the regular `runTypeComponentsFactory` returns the shard variant, the `sovereignRunTypeComponentsFactory` returns the sovereign variant, and the call sites just ask `runTypeComponents` for the creator.

`TxPreProcessorCreator` is the odd one out — it's the same kind of thing (a per-run-type factory used when building the preprocessor container in shard/meta block processors and in the genesis block creators), but it's passed around manually as a top-level argument.

Please move it into `RunTypeComponents` so it follows the same pattern as the others:

- `runTypeComponents` should hold a tx-pre-processor creator field, populated with the shard variant in the regular factory and the sovereign variant in the sovereign factory.
- The managed run-type components handler should expose it, and the `RunTypeComponentsHolder` interface in `factory/interface.go` should include it.
- `processComponentsFactory` (shard + meta block processor creation) and the genesis block creators (shard + meta) should pull it from `runTypeComponents` instead of receiving it via their own args.
- The standalone field on `ProcessComponentsFactoryArgs` and `ArgsGenesisBlockCreator` should go away, along with all the call sites that construct and pass it explicitly.
- The nil-check that currently lives in `checkProcessComponentsArgs` for the standalone field should move next to the other run-type-component nil checks (and the genesis block creator should also nil-check it through the run-type-components handler, like it does for the other creators it pulls from there).

Existing tests that build a `RunTypeComponentsStub` will need a stub entry for the new accessor so the stub still satisfies the interface.
