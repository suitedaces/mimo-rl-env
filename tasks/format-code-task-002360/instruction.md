# Add an immutable `property.Value` type for the Go SDK

We want a clean, self-contained representation of a Pulumi property value that we can grow into a
replacement for the sprawling `resource.PropertyValue`. Please add a new package, importable as
`github.com/pulumi/pulumi/sdk/v3/go/property`, that exposes an immutable `Value` type.

## What a `Value` is

A `Value` carries one piece of underlying content plus two orthogonal "modifiers": whether the
value is *secret*, and the set of resource *dependencies* (URNs) attached to it. The supported
content kinds are:

- the three primitives `bool`, `float64` (number), and `string`;
- an array of values and a map of values;
- a Pulumi asset (`*asset.Asset`) and archive (`*archive.Archive`);
- a resource reference;
- the marker *computed* (an unknown value);
- *null* (the absence of a value).

For arrays and maps, expose the collection types so callers can build them: `Array` (a slice of
`Value`) and `Map` (a map from a dedicated string-based key type `MapKey` to `Value`).
Construction goes through a single constructor `New` that
accepts any one of the supported Go values (including the two markers described below) and returns
the corresponding `Value`.

Provide two exported marker values, `Computed` and `Null`, of distinct singleton types.
`New(Computed)` builds a computed value; `New(Null)` builds a null value.

### Null normalization and the zero value

The zero `Value` (i.e. `Value{}`) must already be a valid null value — equal to `New(Null)` and
reporting itself as null. Because Go distinguishes a typed nil from an untyped one, constructing a
`Value` from a *nil* array, a *nil* map, a *nil* asset, or a *nil* archive must normalize to null:
the resulting value reports null, and does **not** report itself as an array/map/asset/archive. An
empty-but-non-nil collection (e.g. an empty array) is *not* null.

### Inspecting and reading the content

Provide a predicate per content kind — `IsBool`, `IsNumber`, `IsString`, `IsArray`, `IsMap`,
`IsAsset`, `IsArchive`, `IsResourceReference`, `IsNull`, `IsComputed` — where exactly the predicate
matching the stored content returns true. Provide a matching accessor per non-marker kind —
`AsBool`, `AsNumber`, `AsString`, `AsArray`, `AsMap`, `AsAsset`, `AsArchive`,
`AsResourceReference` — that returns the underlying Go value.

### Modifiers

`Value` is immutable: every operation that "changes" a value returns a new `Value` and leaves the
receiver untouched.

- `Secret()` reports whether *this* value is marked secret (it does not look inside nested values).
  `WithSecret(bool)` returns a copy with the secret flag set accordingly. `HasSecrets()` reports
  whether this value *or any value nested within it* is secret.
- `Dependencies()` returns this value's dependency URNs and `WithDependencies([]urn.URN)` returns a
  copy carrying the given dependencies.
- `HasComputed()` reports whether this value *or any value nested within it* is computed.

`Value` must not be comparable with Go's `==` operator; equality is only meaningful through the
`Equals` method below.

## Equality

Add `Equals(other Value, opts ...EqualOption) bool`. Two values are equal only when **all** of the
following hold:

1. They have the same secret flag.
2. They have the same dependencies, compared in order (same length, equal element by element).
3. Their content is equal, defined as:
   - null equals null;
   - bools, numbers, and strings equal by `==`;
   - arrays are equal when they have the same length and corresponding elements are equal
     (recursively, with the same options);
   - maps are equal when they have the same set of keys and the values under each key are equal;
   - assets equal assets, and archives equal archives, by their own equality;
   - resource references equal by the rule below;
   - by default a computed value is equal *only* to another computed value (it behaves like null);
   - values of differing kinds are not equal.

Equality is recursive: the secret-flag and dependency checks apply at every level, and the options
propagate into nested elements.

Provide one equality option, `EqualRelaxComputed`. When it is supplied, the default computed rule
is relaxed so that a computed value on either side is considered equal to the other value (the
secret-flag and dependency checks in points 1 and 2 still apply).

## Resource references

A resource reference captures a referenced resource's URN, its ID (itself a `Value` that is either
a string or computed, or null for component resources), and the version of its containing package.
Expose it as a struct named `ResourceReference` with exported `URN`, `ID`, and `PackageVersion`
fields (the ID is a `Value`); a `ResourceReference` is itself one of the Go values accepted by `New`.

Two resource references are equal when their URNs match, their package versions match, and their
IDs are equal **treating computed IDs as equal to anything** (i.e. compared with the relaxed
computed rule).
