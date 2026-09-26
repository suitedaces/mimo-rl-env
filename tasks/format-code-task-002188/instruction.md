## Problem Statement

我用了 flask-security 做认证，现在发现一个问题：当客户端带着 `Accept: application/json` 去访问受保护的接口、但没登录的时候，请求直接 500 了，报错是 `Object of type Response is not JSON serializable`。

我这套接口还接了 flask-restplus，感觉是 flask-security 返回的 401 响应被 restplus 拿去又序列化了一遍才炸的？正常没登录不应该就是干净返回个 401 JSON 吗，怎么会崩成 500。

复现很简单，就是个普通的受保护端点，发个未认证的 JSON 请求过去就触发了。

## Expected outcomes

- Unauthenticated requests that prefer JSON, such as requests with `Accept: application/json`, should receive a normal Flask HTTP response instead of causing a server error or producing a value that cooperating Flask extensions may try to serialize again.
- For unauthenticated JSON requests to protected endpoints, the response should be HTTP 401, have a JSON content type, and contain a parseable JSON error payload rather than an empty body or a 500 serialization failure.
- The unauthenticated JSON error payload should include the default message `You are not authenticated. Please supply the correct credentials.` unless the application config overrides it with `SECURITY_MSG_UNAUTHENTICATED`.
- Authenticated users who are not allowed to access a JSON endpoint should receive HTTP 403 with a parseable JSON error payload that includes `You do not have permission to view this resource.`.
- Existing non-JSON and backwards-compatibility unauthenticated behavior should continue to work as before, including authentication challenge headers where applicable.

## Implementation notes

- The exact internal location, helper structure, and data flow used to build these responses are up to the implementation.
- Preserve the library’s existing JSON response conventions and configuration-message conventions when adding or reusing error payloads.
- The fix should be compatible with normal Flask response handling and with extensions layered around Flask routes.
