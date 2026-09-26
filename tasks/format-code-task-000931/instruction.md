## Schema resolution fails when the reader schema contains a union with a record (or other complex type)

I'm trying to read an avro file with a `reader_schema` that's slightly different from the writer schema (schema evolution). It works fine for simple cases, but as soon as the reader schema contains a **union with a complex type** (a record / array / map), reading blows up with a schema mismatch even though the two schemas should be compatible.

Minimal repro:

```python
import io
import fastavro

writer_schema = {
    "type": "record",
    "name": "MyRecord",
    "fields": [
        {"name": "field1", "type": "string"},
        {"name": "field2", "type": "int"},
    ],
}

# Reader wraps the record in a union with null (e.g. to make it optional going forward)
reader_schema = {
    "type": "record",
    "name": "MyRecord",
    "fields": [
        {"name": "field1", "type": "string"},
        {
            "name": "field2",
            "type": [
                "null",
                {
                    "type": "record",
                    "name": "Sub",
                    "fields": [{"name": "x", "type": "int"}],
                },
            ],
            "default": None,
        },
    ],
}

records = [{"field1": "hello", "field2": 1}]

buf = io.BytesIO()
fastavro.writer(buf, writer_schema, records)
buf.seek(0)

# This raises SchemaResolutionError
for r in fastavro.reader(buf, reader_schema=reader_schema):
    print(r)
```

What I'd expect: either the read succeeds (since the writer's `field2: int` is compatible with one branch of the reader union, and the rest of the union's branches are simply not selected), or at the very least the union containing a record schema is considered a valid candidate during resolution.

What actually happens: it errors out. From the user side it looks like the resolver doesn't recognize a complex (record-shaped) member inside a union as something it can match against the writer's type, so the whole branch is rejected.

The simple "both sides are primitives" case works. It's specifically the "union member is a dict-form schema (record / array / map / enum / fixed)" case that breaks.
