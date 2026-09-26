# Add an SEI message package for AVC and HEVC

The library can already pull SEI (Supplementary Enhancement Information) NAL units out
of a stream, but there is no shared, codec-aware way to parse their contents. I'd like a
new package, importable as `github.com/edgeware/mp4ff/sei`, that turns the raw bytes of an
SEI NAL unit into typed, inspectable messages and can re-encode them.

## Splitting a NAL unit into messages

Expose `func ExtractSEIData(rs io.ReadSeeker) ([]SEIData, error)`. The input is the rbsp
byte stream of one SEI NAL unit **with the NAL unit header already removed**. An SEI NAL
unit packs one or more messages back to back, each laid out as:

- a payload **type**: read bytes one at a time and sum them; keep going while a byte equals
  `0xff`, stop after the first byte that is not `0xff`.
- a payload **size** (in bytes): encoded the same way (sum of bytes, continuing while `0xff`).
- exactly *size* bytes of payload.

The stream is emulation-prevention encoded (the `0x000003` escaping used by Annex B byte
streams), so a `0x03` that follows two `0x00` bytes is not part of the payload and must not
be counted or returned. Keep reading messages until there is no more rbsp data (the
remaining bits are just the rbsp stop bit and zero padding). Return the messages in stream
order. The payload stored for each message is the de-emulated rbsp payload, so its length
equals the declared size.

`SEIData` is the raw, undecoded form of a message. Provide a constructor
`func NewSEIData(payloadType uint, payload []byte) *SEIData` and make it satisfy the
`SEIMessage` interface below, with `Type()` returning the payload type, `Size()` the payload
length in bytes, and `Payload()` the raw payload bytes.

## Typed messages

Define the interface every message implements:

```go
type SEIMessage interface {
    Type() uint        // SEI payload type
    Size() uint        // size in bytes of the rbsp payload
    Payload() []byte   // the rbsp payload
    String() string    // human-readable description
}
```

Add a codec discriminator `type Codec` with exported values `AVC` and `HEVC`, and a decoder

```go
func DecodeSEIMessage(sd *SEIData, codec Codec) (SEIMessage, error)
```

that promotes a raw `SEIData` to a typed message. For payload types this package does not
specifically understand, it must fall back to returning a message that preserves the original
type and payload (never an error). Implement specific decoding for the two HDR static-metadata
messages:

- **Mastering display colour volume**, payload type **137**. Its 24-byte payload is, in order
  and big-endian: for each of three colour primaries a 16-bit X then a 16-bit Y value
  (`DisplayPrimariesX[0]`, `DisplayPrimariesY[0]`, … `DisplayPrimariesX[2]`,
  `DisplayPrimariesY[2]`), then a 16-bit white point X and white point Y, then a 32-bit max
  display mastering luminance and a 32-bit min display mastering luminance. Decode it to a
  `*MasteringDisplayColourVolumeSEI` exposing those values as exported fields
  `DisplayPrimariesX [3]uint16`, `DisplayPrimariesY [3]uint16`, `WhitePointX uint16`,
  `WhitePointY uint16`, `MaxDisplayMasteringLuminance uint32`, `MinDisplayMasteringLuminance uint32`.
  Its `Size()` is always 24.

- **Content light level information**, payload type **144**. Its 4-byte payload is two 16-bit
  big-endian values: max content light level then max picture average light level. Decode it
  to a `*ContentLightLevelInformationSEI` with exported fields `MaxContentLightLevel uint16`
  and `MaxPicAverageLightLevel uint16`. Its `Size()` is always 4.

For both of these, decoding a payload whose length does not match the fixed size must return
an error rather than a message. `Payload()` on a decoded message must reproduce the exact
payload bytes it was decoded from (round-trip), and must also work for a message built
directly from its fields.

## Type names

Provide a named type `type SEIType uint` whose `String()` method returns a human-readable
name followed by the numeric value in parentheses, e.g.:

- `SEIType(1).String()`   → `"SEIPicTimingType (1)"`
- `SEIType(137).String()` → `"SEIMasteringDisplayColourVolumeType (137)"`
- `SEIType(144).String()` → `"SEIContentLightLevelInformationType (144)"`

Any type the package has no name for must still render with its number in parentheses,
e.g. `SEIType(200).String()` ends with `"(200)"`.

Also export the payload-type constants used above, including
`SEIMasteringDisplayColourVolumeType` (137), `SEIContentLightLevelInformationType` (144),
and `SEIPicTimingType` (1).
