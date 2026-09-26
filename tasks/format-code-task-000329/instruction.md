# Problem Statement
I'm running into a sync failure with the S3 source when the file format is `jsonl`: rows that include a nested object field like `{"meta": {"foo": "bar"}}` fail before any Airbyte records are produced, while similar JSONL files with only flat scalar fields sync fine. I first thought my S3 config was wrong, but it seems tied to nested objects in the JSONL payload.

# Expected outcomes
- JSONL files that contain nested object fields should sync successfully instead of failing before any records are produced.
- Flat scalar JSONL files should continue to sync normally, and nested-object JSONL should still emit records for each input row.
- The S3 source's published version metadata should be updated consistently to `0.1.20` in its public definition/spec and built image metadata.

# Implementation notes
具体的解析策略、内部数据结构、以及校验放置位置由实现者自行决定；只要外部可见的同步结果、记录产出、以及公开版本元数据满足上述行为即可。
