### Add support for CNS QueryVolumeInfo API in cns client and simulator

The `cns.Client` currently exposes `QueryVolume` and `QueryAllVolume`, but both return `CnsVolume` entries that don't include the underlying `VStorageObject` details (backing file path, capacity, policy, etc.).

For a CSI-style workflow I want to feed in a list of volume IDs and get back the `VStorageObject` info for each volume. The CNS service on vCenter already supports this via its `QueryVolumeInfo` operation — it takes a list of `CnsVolumeId` and returns a task whose result carries the per-volume `VStorageObject`. There's just no way to invoke it from govmomi today.

Could the `cns` package be extended so that I can call this from a `cns.Client` given a `[]cnstypes.CnsVolumeId` and wait on the resulting task to get the `VStorageObject` for each id? The `cns/simulator` should be updated accordingly so this is testable against the simulator (synthetic `VStorageObject` per requested volume id is fine).
