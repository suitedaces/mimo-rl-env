# Problem Statement

我在用 YARP.parse 解析带中文或 `# encoding:` magic comment 的 Ruby 文件时，`result.source.source.encoding` 看到的是 `ASCII-8BIT`，后面从 location/token slice 出来的字符串编码也跟着不对；同样的输入走 `YARP.load(input, serialized)` 反序列化后也会出现这个现象，感觉像是解析时识别到的 encoding 没落到 Source 字符串上。

# Expected outcomes

- Direct parsing should preserve the encoding detected for the Ruby source on the `Source` string returned in the parse result, so `result.source.source.encoding` reflects the detected source encoding rather than an unrelated binary/default encoding.
- Strings derived from parsed source locations or slices should carry the same detected source encoding as the underlying `Source` string.
- Loading a result through `YARP.load(input, serialized)` should preserve the detected source encoding on the `Source` string in the loaded result.
- The behavior should work both for non-ASCII source content and for source files whose encoding is declared by a Ruby `# encoding:` magic comment.

# Implementation notes

- The exact place where encoding information is propagated is up to the implementation.
- Keep existing public API behavior and object relationships intact; this is a bug fix to the encoding metadata visible through existing parse/load results.
