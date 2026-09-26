# Problem Statement

我在用 go-ole 调 COM 的时候，很多 GUID 都是文档里直接给的 `{...}` 字符串，现在还得自己拆开填 GUID 结构体，挺容易写错；而且 fmt 打印出来也是结构体 dump，不方便对照。能不能让库直接从 GUID 字符串生成 GUID，并且打印时就是常见的 GUID 文本格式？

# Expected outcomes

- GUID parsing: `NewGUID(guid string) *GUID` should construct a `*GUID` from valid GUID text in any of these common forms: 32 contiguous hexadecimal characters, 36 characters with hyphens, or 38 characters with braces and hyphens.
- GUID parsing should be case-insensitive for hexadecimal characters and should preserve the represented GUID value.
- Invalid GUID text should fail clearly by returning `nil`, including malformed lengths, missing required braces or hyphens for formatted inputs, or non-hexadecimal characters.
- GUID formatting: `(*GUID).String() string` should return the common brace-wrapped, hyphenated GUID text format using uppercase hexadecimal characters.
- `fmt` formatting of a non-nil `*GUID` should use the same common GUID text representation rather than a Go struct dump.
- Calling `String()` on a nil `*GUID` should return the empty GUID text `{00000000-0000-0000-0000-000000000000}`.

# Implementation notes

- Keep the behavior available through the public `ole` package API; the internal parsing and formatting approach is up to the implementer.
- The implementation should remain pure Go and should not require callers to manually split GUID strings into struct fields.
- Preserve existing GUID equality and COM interop behavior for GUID values constructed by other means.
