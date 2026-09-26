# Encode and decode Ethereum event topics

The ABI package can already encode and decode the data portion of a contract call,
but it has no support for the 32-byte *topic words* that Ethereum uses for indexed
event parameters. I'd like to be able to take a parsed ABI `Type` together with a Go
value and turn it into the single 32-byte word that would appear in a log topic, and
to go the other way and recover the Go value from such a word.

Please add two exported functions to the `abi` package:

```go
func EncodeTopic(t *Type, val interface{}) ([32]byte, error)
func ParseTopic(t *Type, topic [32]byte) (interface{}, error)
```

`EncodeTopic` packs `val` into the 32-byte word the way an indexed event parameter of
type `t` is laid out, and `ParseTopic` is its inverse, decoding the word back into a Go
value.

Only the value types that fit in a single word need to be supported:

- **bool** — the word is all zero except for its final byte, which is `1` for `true`
  and `0` for `false`.
- **integers** (`int`/`uint` of every width) — the value is stored big-endian, right
  aligned in the word (i.e. left-padded with zero bytes), using two's complement for
  negative signed values.
- **address** — the 20 address bytes occupy the rightmost 20 bytes of the word and the
  leading 12 bytes are zero.

For any other type (strings, bytes, fixed bytes, arrays, slices, tuples, …) both
functions must return a non-nil error rather than guessing.

`ParseTopic` must return the same Go types the package's ABI value decoder already
produces for a given type, so that decoding round-trips cleanly: for every supported
type, parsing the word produced by `EncodeTopic` yields a value equal to the original
input. When parsing a `bool`, a word that is neither the canonical encoding of `true`
nor of `false` is invalid and must produce an error.
