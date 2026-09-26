## Components can only be constructed from Python; want a config-driven path

Right now the only way to get a `PythonScript` component (and Components in general) is to instantiate them directly in Python, e.g.

```python
PythonScript(
    path="scripts/my_script.py",
    specs=[
        AssetSpec(key="foo", deps=["bar"], group_name="scripts"),
        AssetSpec(key="baz"),
    ],
)
```

This is fine for one-offs, but for the components workflow we want to be able to declare component instances from configuration (a dict that could be loaded from YAML or similar) instead of writing Python for every instance. Something like:

```yaml
- key: foo
  deps: [bar]
  group_name: scripts
- key: baz
```

passed alongside the script path and turned into a `PythonScript` automatically.

Today there's no entry point on `Component` (or `PythonScript`) for this — `PythonScript.__init__` takes already-constructed `AssetSpec` objects, so anything wanting to drive component creation from data has to build the `AssetSpec`s itself and call the constructor manually. That defeats the purpose of having a declarative components layer.

It would be great if a Component subclass could:

1. Declare what configuration shape it accepts (so callers / tooling can validate against it).
2. Be constructed from a plain configuration value matching that shape, with the framework doing the conversion into the real domain objects (e.g. turning `{"key": "foo", "deps": ["bar"], ...}` entries into `AssetSpec`s with proper `AssetKey`s).

`PythonScript` would be the first component to support this path: given the script's path plus a list of spec descriptions like the YAML above, produce an equivalent `PythonScript` to what you'd get by hand-writing the `AssetSpec(...)` calls. String fields like `key` and entries in `deps` should be parsed into `AssetKey`s, and the usual spec fields (description, metadata, group_name, skippable, code_version, owners, tags) should all be supported. If no specs are supplied in the config, behavior should match `PythonScript(path=...)` with no specs (i.e. the existing default).

The new entry point on the component side I'd expect is something like `PythonScript.from_component_params(path, component_params=...)`.
