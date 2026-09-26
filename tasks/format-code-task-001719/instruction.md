## Update machine-controller dependency and switch to its new SDK module

Upstream `machine-controller` has now introduced a standalone SDK module (similar to what we did for KKP itself recently), so consumers no longer need to depend on `machine-controller`'s internal packages directly.

We should update KKP's `machine-controller` dependency to a version that ships this new SDK, and migrate our codebase so that everywhere we currently import from `machine-controller`'s internal packages we instead consume the new SDK module.

After this change KKP should no longer reach into the upstream `machine-controller` internal package tree for the types and helpers it uses; it should go through the SDK module that `machine-controller` now exposes for downstream consumers.
