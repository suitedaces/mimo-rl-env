# Problem Statement

When I run Ray with an explicit `temp_dir`, the logs and socket files from different runs all end up dumped directly in that same directory, so they get mixed together and I sometimes hit socket file conflicts when I restart. It'd be great if Ray just kept each run's stuff in its own separate folder under there automatically, instead of me having to clean things up between runs. Also, on a multi-node setup the workers don't seem to agree on where this directory is, which makes collecting logs a pain — ideally they'd all use the same session folder.

# Expected outcomes

- Per-run temporary layout:
  - A Ray run should create and use a distinct session directory underneath the configured root temporary directory, including when `temp_dir` is provided explicitly.
  - Runtime logs and socket files should be placed inside that session directory rather than directly in the root temporary directory.
  - Multiple starts using the same root temporary directory should not reuse the same session directory.

- Session naming:
  - Session directory names should follow the existing `session_{timestamp}_{pid}` style.
  - The timestamp portion should be precise enough to distinguish rapid successive starts in the same second.

- Cluster consistency:
  - In a multi-node Ray setup, nodes that join the same cluster should use the same root temporary directory and the same session directory for that cluster session.

- Defaults:
  - If no root temporary directory is specified, Ray should continue to use `/tmp/ray` as the root location and create the session directory underneath it.

# Implementation notes

The concrete internal organization, where session metadata is stored, and how joining nodes discover the active session are implementation choices. Preserve the existing Python and cluster-start command-line ways to configure the root temporary directory while ensuring the observable file layout and cluster-wide consistency described above.
