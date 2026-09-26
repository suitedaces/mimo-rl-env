WFE2: support POST-as-GET for directory/newNonce endpoints
[RFC 8555 §6.3](https://tools.ietf.org/html/rfc8555#section-6.3) says the server's `directory` and `newNonce` endpoints should support POST-as-GET as well as GET. 

Presently Boulder only supports GET requests for the directory endpoint and GET/HEAD requests for the newNonce endpoint.

See also https://github.com/letsencrypt/pebble/issues/291
