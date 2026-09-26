Following the addition of https://github.com/parquet-go/parquet-go/pull/166 into `v0.24.0`, list types are now correctly decoded into their underlying Go type instead of a list of maps in the form:

```
{ "<column_name>": { "list": {"element": <val_1>, "element": <val_2>, ... } } }
```

However, in Bento, we expect the following schema to decode input data as follows:

```yaml
schema:
  - name: mylist
    type: LIST
    fields:
      - { name: element, type: INT64 } 

# In:
# Row | mylist.list[].element
# ----|--------------------
# 0   | [1, 2, 3]

# Out: { "mylist": {"list":[{"element":1},{"element":2},{"element":3}] }
```

However, from `+v0.24.0`, this is instead decoded as a Go type:

```yaml
# Out: { "mylist": [1, 2, 3] }
```

While this newer output is _technically_ more correct, since the type has actually been decoded into its correct corresponding Go value, this will introduce a breaking change when updating versions.

So we should consider the following options:
1. Introduce a new flag (i.e `decode_list_into_logical_type`) when updating.
2. Always return in the original format to preserve backwards compatability.

A flag (option 1) is probably best for now.

The new config field on `parquet_decode` should be called `use_parquet_list_format` (a bool), where `true` keeps the legacy logical-type wrapping `{"list": [{"element": ...}, ...]}` and `false` returns the new Go slice form; default it to `true` to preserve backward compatibility.
