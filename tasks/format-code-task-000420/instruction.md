## Add support for the `decimal` logical type in Python AVRO

The Avro spec defines a `decimal` logical type that annotates either a `bytes` or `fixed` schema with `precision` and `scale` properties — typically used for representing exact-precision values like monetary amounts. The Java implementation handles this, but the Python library currently has no real support for it.

For example, I have a schema like:

```json
{
  "type": "record",
  "name": "Transaction",
  "fields": [
    {
      "name": "amount",
      "type": {
        "type": "bytes",
        "logicalType": "decimal",
        "precision": 4,
        "scale": 2
      }
    }
  ]
}
```

Parsing this with `avro.schema.parse(...)` succeeds, but the `logicalType` / `precision` / `scale` keys just end up sitting in the "other properties" bucket of the parsed schema — there's no decimal-aware behaviour anywhere downstream. Concretely:

- if I try to write `{"amount": Decimal("12.34")}` the writer fails validation, because a `bytes` field is expected to be a `str`;
- the same problem happens for a `fixed`-typed decimal;
- and on the read side I just get raw bytes back instead of a `Decimal`.

I'd like the Python implementation to actually support the `decimal` logical type on both `bytes`- and `fixed`-backed schemas, so a Python `decimal.Decimal` value can be round-tripped through serialization and deserialization, with the bytes encoded per the Avro spec (two's-complement big-endian of the unscaled integer).

It would also be very useful if schema parsing validated `precision` / `scale` at parse time — misconfigured schemas (e.g. non-positive precision, negative scale, scale greater than precision, or a precision that wouldn't even fit in the declared fixed size) should fail loudly rather than silently producing garbage at write time.

Tracked upstream as AVRO-1816.
