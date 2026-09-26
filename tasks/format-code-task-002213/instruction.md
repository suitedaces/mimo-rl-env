`read_csv` silently renames duplicate column names — no way to opt out

When I read a CSV file whose header has duplicate column names, pandas quietly suffixes the duplicates with `.1`, `.2`, etc. For example, given a file like:

```
A,A,A,B
1,2,3,4
5,6,7,8
```

I get a DataFrame with columns `['A', 'A.1', 'A.2', 'B']` rather than `['A', 'A', 'A', 'B']`.

In my case the duplicate names are intentional — they come from an upstream tool that emits paired columns under the same label — and I need to keep the names exactly as they are in the file so downstream code can match them back to the source. There doesn't seem to be any keyword on `read_csv` / `read_table` to disable the renaming.

Could we get a way to ask the CSV parsers to leave duplicate column names alone? Keeping the current rename as the default is fine (so existing code doesn't break), but I'd like an opt-out so I can get the literal headers back.

A keyword along the lines of `mangle_dupe_cols=False` would be ideal.
