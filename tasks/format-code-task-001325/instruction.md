> This issue is a sub-task of the OCI Conformance testing epic (#11943)

```
~~~ REQUEST ~~~
PUT  /v2/conformance/testrepo/manifests/sha256:totallywrong  HTTP/1.1
HOST   : ******
HEADERS:
	Accept: application/vnd.oci.image.manifest.v1+json
	Authorization: Bearer *****
	Content-Type: application/vnd.oci.image.manifest.v1+json
	User-Agent: distribution-spec-conformance-tests
BODY   :
"YmxhYmxhYmxh"
------------------------------------------------------------------------------
~~~ RESPONSE ~~~
STATUS       : 500 Internal Server Error
RECEIVED AT  : 2020-05-15T06:41:38.199810825Z
TIME DURATION: 8.643892ms
HEADERS      :
	Connection: keep-alive
	Content-Length: 66
	Content-Type: application/json; charset=utf-8
	Date: Fri, 15 May 2020 06:41:38 GMT
	Server: nginx
	Set-Cookie: sid=a0d91728358ca52e853f5bc7cf19c4fb; Path=/; HttpOnly
	X-Request-Id: 5b012de1-4dcd-473b-b4e5-c2b9be273def
BODY         :
{
   "errors": [
      {
         "code": "UNKNOWN",
         "message": "internal server error"
      }
   ]
}

```
Expected
    <int>: 500
To satisfy at least one of these matchers: [%!s(*matchers.EqualMatcher=&{400}) %!s(*matchers.EqualMatcher=&{404})]
