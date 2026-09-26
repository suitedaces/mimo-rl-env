lite2: HTTP light client should default to http:// scheme
The HTTP light client parses URLs without an explicit scheme as a relative URL, such that e.g. `192.168.0.1:26657` errors. It should default to using `http://` scheme when not given.

____

#### For Admin Use

- [x] Not duplicate issue
- [x] Appropriate labels applied
- [x] Appropriate contributors tagged
- [x] Contributor assigned/self-assigned
