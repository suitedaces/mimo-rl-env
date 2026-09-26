## Problem Statement

我想在 Node 里用 undici 的 fetch 按浏览器那套方式提交表单：直接从 `require('undici')` 拿 `FormData`/`File`，把 FormData 当 body 发出去时能正常变成 multipart 请求；另外收到 `application/x-www-form-urlencoded` 的响应时也希望能直接 `response.formData()` 读字段。

## Expected outcomes

- Public fetch-related exports:
  - In environments where undici exposes its fetch API, `require('undici').FormData` is available as a constructable browser-style FormData API, including normal field append/read behavior such as `append()`, `get()`, `getAll()`, and iteration.
  - In environments where undici exposes its fetch API, `require('undici').File` is available as a constructable browser-style File API that can be used as a form field value.

- Sending forms with fetch:
  - Passing an undici `FormData` instance as a `fetch()` request body sends a `multipart/form-data` request and automatically supplies a `Content-Type` header with a boundary.
  - String fields in the submitted `FormData` are represented as normal multipart form fields.
  - File-like or Blob-like values in the submitted `FormData` are represented as file parts with the expected public metadata and bytes.

- Reading form bodies:
  - Calling `.formData()` on a `Response` or `Request` whose `Content-Type` is `application/x-www-form-urlencoded` parses the body and resolves to a `FormData` containing the decoded fields.
  - Multipart form body parsing through `.formData()` is not added here; attempts to parse such bodies should reject with a clear unsupported-form error rather than being silently parsed incorrectly.

## Implementation notes

- The concrete internal representation of `FormData`, `File`, body streams, boundaries, and parsing helpers is up to the implementation.
- Tests and users should rely on the public undici exports and fetch/body APIs, not on private modules or helper names.
