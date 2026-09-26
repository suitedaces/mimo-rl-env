Mime subtype containing `@` is invalid and breaks serving
xref https://www.w3.org/Protocols/rfc1341/4_Content-Type.html

```
Content-Type := type "/" subtype *[";" parameter] 

type :=          "application"     / "audio" 
          / "image"           / "message" 
          / "multipart"  / "text" 
          / "video"           / x-token 

x-token := <The two characters "X-" followed, with no 
           intervening white space, by any token> 

subtype := token 

parameter := attribute "=" value 

attribute := token 

value := token / quoted-string 

token := 1*<any CHAR except SPACE, CTLs, or tspecials> 

tspecials :=  "(" / ")" / "<" / ">" / "@"  ; Must be in 
           /  "," / ";" / ":" / "\" / <">  ; quoted-string, 
           /  "/" / "[" / "]" / "?" / "."  ; to use within 
           /  "="                        ; parameter values
```

When we started setting content-type in responses, it broke serving of openapi docs with this error:

> Error from server (InternalError): Internal error occurred: mime: unexpected content after media subtype

Coming from here:

https://cs.opensource.google/go/go/+/release-branch.go1.19:src/mime/mediatype.go;l=103-122

https://cs.opensource.google/go/go/+/release-branch.go1.19:src/mime/grammar.go;l=11-32;drc=119f679a3bd2e60cfc990920f82fd1a5cb006f4c

I'm not actually sure where the `application/com.github.proto-openapi.spec.v3@v1.0+protobuf` and `application/com.github.proto-openapi.spec.v2@v1.0+protobuf` mime types originated... I can't find references to them outside of Kubernetes.

I would suggest:
1. coming up with alternatives that do not contain @
2. update our clients' `Accept` headers to accept both (to support old servers), preferring the new one without the @ subtype
3. update our serving/handling code to continue to answer requests for either (to support old clients), and set Content-Type to the one that does not contain the `@` subtype

cc @apelisse @Jefftree
