## `directory` check stops scanning the rest of the tree after one inaccessible subdirectory

We're using the `directory` integration with `recursive: true` to track file counts and total size on some large filesystem trees. Most of the tree is readable by the agent user, but the trees do contain a handful of subdirectories with restricted permissions (different ACLs, a few mount points the agent user isn't on the allow list for, that kind of thing).

The metrics we're getting back are way off:

- `system.disk.directory.files`
- `system.disk.directory.folders`
- `system.disk.directory.bytes`

…all report numbers much smaller than what's actually in the configured root. After bumping the agent log level we see a single error line about a permission problem while traversing the root path, and then nothing more — it looks like the check stops walking the rest of the tree as soon as it bumps into one entry it can't read, even though the vast majority of subdirectories under that same root are perfectly fine to access.

For a monitoring check this is pretty surprising. If one subtree can't be read we'd expect just that subtree to be skipped (with the error logged so we know it happened) and the rest of the tree to still be counted toward the metrics. As things stand, a single restricted folder somewhere under the configured root silently makes our totals wrong, and there's no easy way to tell from the reported numbers that anything is off.

Other filesystem-traversal tools (`find`, `du`, etc.) report errors on a per-entry basis and keep going. Could the recursive walk in this check be made resilient to per-entry errors the same way — skip the unreadable parts, log them, and continue traversing the rest so the metrics reflect everything the agent *could* see?
