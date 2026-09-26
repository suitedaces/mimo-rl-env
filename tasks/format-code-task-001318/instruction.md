I want Goby programs that `require "net/http"` to have one-shot class methods on `Net::HTTP` for simple outbound requests without creating a client object.

`Net::HTTP.get(url: String, *path_parts: String) -> String` should send a GET request and return the response body text when the server returns HTTP 200. If extra string path parts are provided, they should be joined onto the parsed URL path before the request, so `Net::HTTP.get("http://127.0.0.1:3000", "index")` should request `/index` and return that response body.

`Net::HTTP.post(url: String, content_type: String, body: String) -> String` should send the body with the provided content type and return the HTTP 200 response body text. For example, posting `"Hi Again"` as `"text/plain"` to a test endpoint that echoes or acknowledges the request should return that endpoint's response body.

`Net::HTTP.head(url: String, *path_parts: String) -> Hash`, `Net::HTTP.delete(url: String, *path_parts: String) -> Hash`, and `Net::HTTP.options(url: String, *path_parts: String) -> Hash` should send the corresponding HTTP method and return a Goby hash of response headers for HTTP 200 responses, with multi-value headers joined into a single string separated by spaces.

These helpers should validate their arguments. `get`, `head`, `delete`, and `options` require at least one string URL; `post` requires exactly three string arguments. Non-string URLs, non-string path parts, missing arguments, or too many `post` arguments should raise Goby `ArgumentError`s. URL parse failures, connection failures, and non-200 responses should raise Goby `HTTPError`s; non-200 errors should include the HTTP status text and numeric status code.
