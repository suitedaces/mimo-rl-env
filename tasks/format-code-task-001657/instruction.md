## Custom `MarshalText` / `UnmarshalText` on map keys is ignored when the underlying kind is `string` (or another basic kind)

I'm using `json-iterator/go` as a drop-in for `encoding/json`, and noticed that custom text marshalling on map key types is silently skipped.

Minimal repro — a string-backed ID type that defines its own text encoding so it can be used as a map key:

```go
type MyID string

func (id MyID) MarshalText() ([]byte, error) {
    return []byte("id:" + string(id)), nil
}

func (id *MyID) UnmarshalText(text []byte) error {
    *id = MyID(strings.TrimPrefix(string(text), "id:"))
    return nil
}

func main() {
    m := map[MyID]int{"abc": 1}

    b, _ := jsoniter.Marshal(m)
    fmt.Println(string(b))
    // encoding/json:  {"id:abc":1}
    // jsoniter:       {"abc":1}    <- MarshalText never called

    var out map[MyID]int
    _ = jsoniter.Unmarshal([]byte(`{"id:abc":1}`), &out)
    fmt.Println(out)
    // encoding/json:  map[abc:1]
    // jsoniter:       map[id:abc:1]   <- UnmarshalText never called
}
```

Both directions just use the raw `string` representation of `MyID`. The custom `MarshalText` / `UnmarshalText` methods are completely bypassed.

The same thing happens for numeric-backed types (`type MyNum int` with `MarshalText`/`UnmarshalText`) — anything whose underlying kind is one of the basic kinds jsoniter handles directly for map keys.

For comparison, the equivalent code with `encoding/json` calls the user-defined text methods as expected, since the standard library prefers `TextMarshaler` / `TextUnmarshaler` for map keys regardless of the underlying kind. Since jsoniter advertises itself as a drop-in replacement, it would be great if it behaved the same way here.
