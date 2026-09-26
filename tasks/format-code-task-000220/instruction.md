# Track virtualenv usage and clean up stale environments

fades caches the virtualenvs it builds, but right now nothing ever removes the
ones you stopped using. Over time the cache directory just grows. I'd like fades
to keep a lightweight record of *when* each cached virtualenv was last used, and
to be able to purge the ones that haven't been touched in a while.

## What I want

**1. Expose the cached virtualenvs' metadata.**

The virtualenv cache class should grow a `get_venvs_metadata()` method that
iterates over the metadata of every virtualenv currently recorded in the cache
index, yielding one metadata mapping (the same `metadata` dict that was stored
for each venv, which includes its `env_path`) per cached virtualenv.

**2. A usage manager.**

Add a `UsageManager` class that owns a plain-text *usage stats* file and is
constructed from the path to that file and the virtualenv cache
(`UsageManager(stat_file_path, venvscache)`). Each virtualenv is identified by
the last path component of its `env_path` (its uuid).

The usage stats file has one record per line, formatted as the virtualenv's
uuid, a single space, and a UTC timestamp in ISO-8601 form
`YYYY-MM-DDTHH:MM:SS.ffffff` (i.e. `datetime.strftime(dt, "%Y-%m-%dT%H:%M:%S.%f")`),
e.g.:

```
2b6e6b1e-... 2020-03-21T18:42:07.123456
```

The manager must behave as follows:

- *On construction*: if the usage stats file does not exist yet, create it and
  seed it with one record per virtualenv currently known to the cache, each
  stamped with the current UTC time. If the file already exists, leave it
  exactly as it is (do not rewrite or reorder it).

- *Recording usage* (`store_usage_stat(venv_data)`): given a virtualenv's
  metadata (a mapping containing its `env_path`), append a new usage record for
  it stamped with the current UTC time. Appending must not drop or rewrite the
  records that are already there.

- *Cleaning unused venvs* (`clean_unused_venvs(max_days_to_keep)`): given a
  maximum number of days to keep, look at the
  most recent usage timestamp recorded for each virtualenv. Any virtualenv whose
  most recent use was **strictly more than** that many days ago must be removed:
  its directory is destroyed on disk and its entry is dropped from the
  virtualenv cache. A virtualenv last used exactly that many days ago is kept.
  After cleaning, the usage stats file is rewritten in compacted form: exactly
  one record per surviving virtualenv (keeping its most recent timestamp), and
  no records at all for virtualenvs that were removed.

The "days ago" comparison is the whole-day difference between now and the
recorded timestamp (e.g. an environment last used 43 full days ago is older than
a 42-day threshold, while one used 42 days ago is not).
