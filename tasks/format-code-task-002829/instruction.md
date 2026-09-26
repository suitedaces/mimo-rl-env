Metadata API: Root.consistent_snapshot should be optional
Spec:
> Finally, the root metadata should write the Boolean "consistent_snapshot" attribute at the root level of its keys of attributes. If consistent snapshots are not written by the repository, then the attribute may either be left unspecified or be set to the False value. Otherwise, it must be set to the True value.

Metadata API (tuf/api/metadata.py) seems like it would fail to read json that does not contain "consistent_snapshot"
