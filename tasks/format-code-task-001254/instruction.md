# Problem Statement

我这边用 openapi3filter 校验一个 `Content-Type: application/zip` 的接口时，现在还得自己额外注册 body decoder，不然直接卡在不支持这个 media type 上。能不能让 `application/zip` 默认就能被识别并解出来，后面照常走 schema 校验？

# Expected outcomes

- `openapi3filter` 在默认配置下应支持 `application/zip` 请求体的 body decoding；调用方不需要额外注册 decoder，也不应再因为该 media type 缺少内置 decoder 而在解码阶段失败。
- 当 `Content-Type` 为 `application/zip` 且 body 是有效 zip archive 时，验证流程应将 zip 中的文件内容解码为可用于后续 schema 校验的字符串值。
- `openapi3filter.ZipFileBodyDecoder` 应作为可复用的公开 body decoder 提供，并能从 zip archive 中读取文件内容，以 `string` 形式返回；如果读取 body 或解析 zip archive 失败，应返回错误。
- 当 `Content-Type` 为 `application/zip` 但 body 不是合法 zip archive 时，失败应来自 zip 解码/解析过程，而不是缺少或不支持 `application/zip` decoder。

# Implementation notes

- 具体的读取方式、缓冲策略、错误包装方式以及 decoder 注册位置由实现者决定。
- 只要外部行为满足上述结果，可以复用现有 body decoder 机制或以等价方式接入验证流程。
