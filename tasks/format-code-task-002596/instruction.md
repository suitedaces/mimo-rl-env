## Empty hashes (`array<K, V>`) are not serialized correctly

I have a Symfony entity with a property that holds a key/value map, annotated like this:

```php
/**
 * @Type("array<string, string>")
 */
private $metadata;
```

When `$metadata` actually has entries, everything works fine across all three formats — JSON gives me an object, XML wraps the entries in the property element, YAML emits a proper mapping.

The trouble is when `$metadata` is just an empty array.

- **JSON**: I get `"metadata":[]` instead of `"metadata":{}`. My consumers (a JS frontend and another service that has a typed schema) treat the property as an object, so receiving an array breaks them — they either crash or silently misbehave depending on the client.
- **XML**: The `<metadata>` element doesn't show up at all in the output. The property is simply gone, which is indistinguishable from "the property wasn't there" vs. "the property was empty".
- **YAML**: Same kind of disappearance — the key gets emitted (or doesn't) without any value to indicate an empty mapping.

As far as I can tell, plain list-typed arrays (`@Type("array<string>")`) serialize fine when empty — JSON gives `[]`, etc. The problem is specific to the hash form where both a key type and a value type are declared.

Since I explicitly told the serializer this is a `K => V` map, an empty value should still be serialized as an empty map in each format, not as a list and not by dropping the property entirely. The shape of the output shouldn't flip depending on whether the map happens to have entries.
