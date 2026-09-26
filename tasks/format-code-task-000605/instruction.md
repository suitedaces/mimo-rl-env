# Add a filesystem-backed metadata key/value store

Our data-join components persist their metadata through a small key/value
interface (the existing etcd and MySQL clients in `fedlearner.common` are
examples). We now need to be able to keep that metadata on a distributed
filesystem (HDFS or an NFS mount) instead of a database, so deployments that
already have shared storage don't have to stand up a separate KV service.

Add a new client, importable as

```python
from fedlearner.common.dfs_client import DFSClient
```

`DFSClient(base_dir)` is constructed with a base directory under which all
metadata lives, and it must expose the same key/value surface the other
clients already provide:

- `set_data(key, data)` — store `data` (`bytes` or `str`) under `key`,
  creating any intermediate directories as needed. Returns a truthy value on
  success. Storing an existing key overwrites its value.
- `get_data(key)` — return the stored value **as `bytes`**, or `None` if the
  key was never set (values stored as `str` come back as `bytes`).
- `delete(key)` — remove the value stored at `key`. Afterwards `get_data(key)`
  is `None`.
- `delete_prefix(key)` — recursively remove everything stored at or below
  `key`. Returns a truthy value when something was removed and a falsy value
  when there was nothing to delete.
- `cas(key, old_data, new_data)` — atomic compare-and-swap. Compare the
  currently stored value against `old_data` **by textual content** (so a
  value previously stored as `b'x'` matches an expected `'x'` and vice
  versa); if they match, write `new_data` and return a truthy value, otherwise
  leave the value untouched and return a falsy value. Comparing against a key
  that has never been set succeeds only when `old_data` is `None`, in which
  case the key is created.
- `get_prefix_kvs(prefix, ignore_prefix=False)` — return a list of
  `(key, value)` pairs, both `bytes`, for every key stored at or below
  `prefix`, sorted in ascending key order. The returned keys are relative to
  the client's base directory. When `ignore_prefix` is `True`, the pair for
  the exact `prefix` key itself is excluded. An unknown prefix yields an empty
  list.

Keys use `/` as a separator and form a hierarchy: the **same** key may both
hold a value and serve as the prefix of other, nested keys (e.g. `foo` can
hold a value while `foo/a` and `foo/b` hold their own values), and
`get_prefix_kvs('foo')` then returns the value at `foo` followed by the values
at `foo/a` and `foo/b`.

Because the data lives on a shared filesystem under the base directory, the
store is not in-process state: a freshly constructed `DFSClient` pointed at the
same base directory must observe everything a previous client wrote there.
