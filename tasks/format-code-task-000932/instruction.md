Enforce schema when using json_writer() or json_reader()
Hi,

I have reproduced the example in https://fastavro.readthedocs.io/en/latest/json_writer.html but I've changed some items of the `records` array in order to introduce some type mismatches.

```
from fastavro import json_writer, parse_schema
from io import StringIO

schema = {
    'doc': 'A weather reading.',
    'name': 'Weather',
    'namespace': 'test',
    'type': 'record',
    'fields': [
        {'name': 'station', 'type': 'string'},
        {'name': 'time', 'type': 'long'},
        {'name': 'temp', 'type': 'int'},
    ],
}
parsed_schema = parse_schema(schema)

records = [
    {u'station': u'011990-99999', u'temp': 0, u'time': 1433269388},
    {u'station': u'011990-99999', u'temp': 22, u'time': "last day"},
    {u'station': u'011990-99999', u'temp': -11, u'time': 1433273379},
    {u'station': u'012650-99999', u'temp': 111.9, u'time': 1433275478},
]

text_stream = StringIO()
json_writer(text_stream, parsed_schema, records)
print(text_stream.getvalue())
```

The 2nd row now has a string `time` instead of a long.
The 4th row now has a float `temp` instead of a int.

So clearly, some of the records doesn't respect the avro schema.

When I run this code, I get this output:

```
{"station": "011990-99999", "time": 1433269388, "temp": 0}
{"station": "011990-99999", "time": "last day", "temp": 22}
{"station": "011990-99999", "time": 1433273379, "temp": -11}
{"station": "012650-99999", "time": 1433275478, "temp": 111.9}
```

No warning, no error, the items are written as-is.

Same thing happens to the `json_reader`.
This code runs flawlessly:

```
from fastavro import json_reader
from io import StringIO

schema = {
    'doc': 'A weather reading.',
    'name': 'Weather',
    'namespace': 'test',
    'type': 'record',
    'fields': [
        {'name': 'station', 'type': 'string'},
        {'name': 'time', 'type': 'long'},
        {'name': 'temp', 'type': 'int'},
    ]
}

records = """{"station": "011990-99999", "time": 1433269388, "temp": 0}
{"station": "011990-99999", "time": "last day", "temp": 22}
{"station": "011990-99999", "time": 1433273379, "temp": -11}
{"station": "012650-99999", "time": 1433275478, "temp": 111.9}
"""

avro_reader = json_reader(StringIO(records), schema)
for record in avro_reader:
    print(record)
```

I would have expected these two snippets to raise an Exception because of incompatible types. Since I use a schema, I expect the encoder/decoder to respect it.

Is it possible to fix that in the library? Or maybe add a parameter to enforce schema validation?

Thanks.
