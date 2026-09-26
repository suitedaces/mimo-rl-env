## Validator registrations never reach my external block builder

I'm running a Prysm beacon node together with an external block builder service (MEV-Boost style setup). My validator client is configured to send validator registrations through the beacon node, and the calls all come back successful — but on the builder side, nothing ever shows up. The builder keeps reporting that it has zero registered validators, and as a result it never produces any blocks for me, so I'm always falling back to local block production.

From the validator's point of view this looks like a complete success: the registration RPC against the beacon node returns OK every time. But the builder behind it is clearly never being told about any of these validators, so the whole external-builder pipeline is effectively a no-op for me even though I've wired everything up.

What I'd expect: when a block builder is configured on the beacon node, validator registrations that come in over `SubmitValidatorRegistration` should actually be delivered to that builder so it can start producing blocks for those validators. If something goes wrong on the builder side while accepting the registration, I'd want that surfaced back to the caller as an error rather than silently swallowed.

One thing to keep in mind: not every node operator runs a builder. For nodes that don't have one configured, this RPC should still respond normally so that validator clients which always send registrations don't start erroring out against builder-less setups.
