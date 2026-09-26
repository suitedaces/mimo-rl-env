## Can't run syncer integration tests without a full vSphere testbed

I'd like to add integration tests for the metadata syncer / full sync flows under `pkg/syncer`, similar to what already exists for the CSI controller. The problem is the test setup story for syncer — there's no easy way to get a usable `*config.Config` unless you have a real vCenter testbed to point at.

Right now the only way to construct a config is `config.FromEnv`, which requires the full set of `VSPHERE_VCENTER` / `VSPHERE_USER` / `VSPHERE_PASSWORD` / `VSPHERE_DATACENTER` / ... environment variables to be set, and on top of that you actually need a live vCenter reachable on the other end. The `integration-unit-test` Makefile target enforces all of those vars and bails out otherwise.

This is fine when you do have a deployed testbed, but it makes it really painful to:

- write and iterate on syncer integration tests on a dev machine that has no testbed,
- run the syncer integration tests as part of `make integration-unit-test` alongside the existing CSI controller ones.

govmomi already ships in-process simulators (vcsim, plus the CNS and PBM SDK simulators), and other tests in this repo already wire those up locally to exercise code paths against a fake vCenter. It would be great if `pkg/common/config` provided a single entry point for tests to obtain a `Config`: prefer the real environment variables when they're set (so a real testbed is still used when available), and otherwise transparently fall back to a config that points at a freshly stood-up simulator.

With that in place I can write proper integration tests for the syncer workflows and have them included in `integration-unit-test`, without forcing every contributor running the target to have a vCenter on hand. The new helper I'd expect would be something like `FromEnvOrSim` in `pkg/common/config`.
