# Problem Statement

I’d like to use zstd-compressed cache archives with drone-cache, but right now setting `archive_format: zstd` doesn’t seem to give me a real zstd archive. Could you add proper zstd support so rebuild/restore works with it, and ideally let the existing compression level option apply there too?

# Expected outcomes

- Zstd archive format support:
  - When `archive_format: zstd` is configured, including through `PLUGIN_ARCHIVE_FORMAT=zstd`, rebuild should create a real zstd-compressed cache archive rather than falling back to an uncompressed tar archive.
  - Restore should be able to read cache archives created with `archive_format: zstd` and recover the archived files with the same observable behavior as the existing supported archive formats.

- Compression level behavior:
  - The existing `--compression-level` / `PLUGIN_COMPRESSION_LEVEL` setting should also affect zstd archive creation when `archive_format: zstd` is used.
  - Existing gzip and tar behavior should remain compatible with the current behavior.

- User-facing documentation:
  - The user-facing CLI/configuration documentation should list `zstd` as a supported `archive_format`.
  - The compression-level documentation should make clear that the setting applies to both gzip and zstd, and should give users enough information to find valid zstd compression-level values.

# Implementation notes

The internal package structure, concrete compression library, helper functions, and validation location are up to the implementer. Keep the behavior compatible with the existing rebuild/restore flow and configuration mechanisms, and avoid changing unrelated archive formats except where needed to preserve existing behavior.
