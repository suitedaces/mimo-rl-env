# Add block-volume snapshot support to the Supervisor (WCP) controller

The Supervisor-cluster CSI controller currently rejects every snapshot request: its
`CreateSnapshot` and `DeleteSnapshot` entry points just return an "unimplemented" gRPC
error. We already support CSI snapshots for block volumes elsewhere in the driver; we now
need the same lifecycle to work when the controller is running in the Supervisor (WCP)
flavor.

Wire up `CreateSnapshot` and `DeleteSnapshot` on the WCP controller so a block volume can
be snapshotted and the snapshot later removed, using the same CNS-backed snapshot
operations the rest of the driver relies on.

## Expected behavior

**CreateSnapshot**

- Given a request that carries the source volume ID of an existing block volume and a
  snapshot name, create a snapshot of that volume and return a populated response whose
  `Snapshot` has:
  - a `SnapshotId` that identifies the snapshot by combining the CNS volume ID and the CNS
    snapshot ID, joined by the driver's snapshot-ID delimiter (`"+"`), i.e.
    `"<sourceVolumeID>+<cnsSnapshotID>"`. This combined ID must be the value that
    `DeleteSnapshot` later accepts.
  - `SourceVolumeId` equal to the request's source volume ID,
  - `SizeBytes` equal to the size of the source volume (in bytes),
  - `ReadyToUse` set to `true`,
  - a non-nil `CreationTime`.
- A request without a source volume ID, or without a snapshot name, is invalid and must be
  rejected with an error rather than producing a snapshot.
- A request whose source volume ID refers to a migrated in-tree vSphere volume (the volume
  ID contains `.vmdk`) is not supported and must fail with the gRPC `Unimplemented` code.
- The number of snapshots per block volume is capped by the configured maximum
  (`GlobalMaxSnapshotsPerBlockVolume`). A `CreateSnapshot` request for a volume that has
  already reached that maximum must be rejected with the gRPC `FailedPrecondition` code
  rather than creating another snapshot.

**DeleteSnapshot**

- Given the combined `SnapshotId` returned by `CreateSnapshot`, delete the underlying CNS
  snapshot and return a non-nil, empty response with no error.

The two operations must round-trip: a snapshot created through `CreateSnapshot` can be
deleted through `DeleteSnapshot` using the returned snapshot ID, and after deletion that
snapshot no longer exists on the source volume.
