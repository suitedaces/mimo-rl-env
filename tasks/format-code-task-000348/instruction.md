# Bring the EMR (v2) cluster resource up to date with newer service capabilities

The `alicloud_emrv2_cluster` resource is missing a few configuration options that the
underlying EMR service now supports. Please extend the resource so users can express them
in their Terraform configurations.

## System disk encryption

Today the node-attributes block of a cluster only lets users turn on encryption for *data*
disks (`data_disk_encrypted` / `data_disk_kms_key_id`). Add the equivalent options for the
**system** disk:

- `system_disk_encrypted` — a boolean toggle for whether the node's system disk is encrypted.
  Optional.
- `system_disk_kms_key_id` — the KMS key id used to encrypt the system disk. Optional, and a
  string. An empty value is not a meaningful key id and must be rejected during validation
  (i.e. configuring it as `""` should produce a validation error); any non-empty value is
  accepted.

Both options describe how a node is provisioned at creation time, so — like the existing
node-attribute fields — they are immutable: changing either of them must force the cluster to
be recreated rather than updated in place.

## Newer enumerated values

Two existing fields reject values that the service now accepts. Widen their accepted sets
(without dropping any value already accepted today, and while still rejecting anything outside
the set):

- The node group type now also supports `MASTER-EXTEND`, in addition to the existing
  `MASTER`, `CORE`, `TASK`, and `GATEWAY`.
- A bootstrap script's execution moment now also supports `BEFORE_START`, in addition to the
  existing `BEFORE_INSTALL` and `AFTER_STARTED`.

These should behave like the other validated string fields: a configuration using one of the
accepted values plans cleanly, and a value outside the accepted set is reported as invalid.
