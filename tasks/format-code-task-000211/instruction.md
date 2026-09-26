# Add a declarative config abstraction for data-import sources

Our data-import sources hand-roll a lot of boilerplate to turn loosely-typed
dictionaries (coming from API requests and from rows stored in our database)
into typed configuration objects. We want a small, reusable abstraction built on
top of the standard library's dataclasses so that defining a config and
initializing it from a dictionary becomes declarative.

Add a new module `posthog/temporal/data_imports/pipelines/source/config.py`
that is importable on its own (it should only depend on the standard library)
and exposes the following public surface: a class decorator `config`, a field
helper `value`, and a converter helper `str_to_bool`.

## `config` decorator

`config` turns a plain class into a dataclass and additionally gives it a
`from_dict` classmethod. All the usual dataclass behavior must keep working
(generated `__init__`, equality, `repr`, field access, defaults, etc.).

It must be usable both bare and with keyword arguments:

```python
@config
class A: ...

@config(prefix="db")
class B: ...
```

`from_dict(d)` is a classmethod that builds and returns an instance of the class
from a dictionary `d`.

For a class with only scalar fields, each field is looked up in `d` by its field
name. Keys present in `d` that don't correspond to a field are ignored. If a
field is absent from `d`, its declared default (if any) is used; if such a field
has no default, calling `from_dict` raises `TypeError` (the dataclass
constructor's error for a missing required argument).

If the decorator is given a `prefix`, every field of that class is instead
looked up under that prefix joined with the field name by an underscore, e.g.
with `@config(prefix="db")` a field `host` is read from the key `db_host`.

## `value` field helper

`value` is the analogue of `dataclasses.field` for configs. It supports the
usual `default` and `default_factory`, plus three config-specific keyword-only
options:

- `alias`: look the field up under this key instead of the field name.
- `prefix`: look the field up under `<prefix>_<name>` (this replaces any prefix
  the field would otherwise inherit).
- `converter`: a one-argument callable applied to the value read from the
  dictionary before it is stored on the instance. Defaults must not be passed
  through the converter.

## Nested configs

A field whose declared type is itself a `config`-decorated class is built
recursively. There are two supported layouts in the source dictionary:

1. **Nested dict.** If `d` contains a key equal to the field's name (or its
   `alias`) and the corresponding value is a dictionary, the nested config is
   built from that sub-dictionary, looking up its fields by their own names.

2. **Flat dict.** Otherwise the nested config is built from the *same*
   dictionary `d`, with its fields looked up under an additional prefix. The
   prefix is resolved in this precedence order:
   - the field's `value(prefix=...)`, if set; otherwise
   - the nested class's own `@config(prefix=...)`, if set; otherwise
   - a prefix derived automatically from the nested class's name.

   The automatically derived prefix is the class name split into words and
   joined by underscores in lower case. Words break on a lower-to-upper
   transition, and a run of consecutive capitals is treated as one word except
   that its final capital starts the next word. A trailing `Config` word is
   dropped unless it is the only word. For example: `SSHTunnel` and
   `SSHTunnelConfig` both derive `ssh_tunnel`, `DatabaseConnection` derives
   `database_connection`, `MyClass` derives `my_class`, `Test` derives `test`,
   and `Config` derives `config`.

   These prefixes accumulate across nesting levels (a doubly-nested config's
   fields are looked up under the concatenation of the prefixes).

## `str_to_bool` converter

`str_to_bool(s)` is a convenience converter (suitable for use as a
`value(converter=...)`). If `s` is already a `bool` it is returned unchanged.
Otherwise `s` is treated as a string and the function returns `True` when its
lower-cased value is one of `"true"`, `"yes"`, or `"1"`, and `False` otherwise.
