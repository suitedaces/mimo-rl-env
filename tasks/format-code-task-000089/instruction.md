## Auto-generated ExtensionObject dataclasses have awkward default values

When I let opcua-asyncio import custom structs from a server via
`load_data_type_definitions`, the generated `@dataclass` classes work, but
the defaults assigned to their fields are off in two ways.

### 1. Optional fields don't default to `None`

I have a structure defined on the server with optional fields (so the
StructureDefinition is `StructureWithOptionalFields` and individual
`StructureField`s have `IsOptional=True`). For example a field like an
optional `Int32`.

After `load_data_type_definitions`, the generated dataclass looks roughly
like:

```python
@dataclass
class MyStruct:
    ...
    SomeOptionalInt: Optional[ua.Int32] = 0
```

i.e. the optional field defaults to `0` rather than `None`. That makes it
impossible to tell "user did not set this optional field" from "user
explicitly set it to 0", and it doesn't match what `Optional[...]` is
supposed to mean here. I'd expect any field flagged as optional in the
StructureDefinition to default to `None` in the generated dataclass.

### 2. Numeric / string defaults aren't typing-friendly

For non-optional scalar fields the generated code mixes the declared type
with a plain Python literal as the default, e.g.:

```python
SomeInt: ua.Int32 = 0
SomeName: String = None
```

Running mypy against modules that touch these generated classes complains
about the mismatch (the annotation says `ua.Int32` / `String`, the default
is a plain `int` / `None`). It would be nice if the generated defaults
were values of the declared type, so the dataclasses are clean under
static type checking.

Could the default-value generation for ExtensionObject dataclasses be
tweaked so that (a) optional fields default to `None`, and (b) the
defaults for basic numeric/string fields are consistent with the declared
field type?
