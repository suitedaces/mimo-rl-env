## Allow custom metadata in avro files

The Avro spec says the file header `meta` map can hold arbitrary user-defined keys alongside `avro.schema` / `avro.codec`, but `fastavro` doesn't seem to expose this either way:

**On write:** `writer(fo, schema, records, codec=...)` doesn't take any way to add my own entries. I'd like to stamp things like the producer name / version, build id, source system, etc. into the file header so consumers (including non-Python tools) can pick them up. Right now I'd have to fork the library to do that.

**On read:** when I open a file with `iter_avro(fo)`, I can get `.schema` and `.codec` back, but there's no way to see the rest of the metadata that's actually sitting in the file header — including stuff written by other Avro implementations. So even if I write the file with another tool that does support custom meta, fastavro can't surface it on read.

Could `fastavro` support reading and writing user-defined header metadata? Round-tripping would be nice — i.e. whatever I attach on the write side I should be able to read back when I open the file later. I'd imagine the API to look something like `writer(..., metadata={...})` on the write side and a `.metadata` attribute on the reader side, but whatever naming makes sense is fine.
