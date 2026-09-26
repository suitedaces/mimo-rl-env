res.redirect using the object argument can be inconsistent
- [x] Used appropriate template for the issue type
- [x] Searched both open and closed issues for duplicates of this issue
- [x] Title adequately and _concisely_ reflects the feature or the bug

# Bug Report

res.redirect generates malformed location headers on the response under certain scenarios.

## Restify Version

4.x+

## Node.js Version

All

## Repro case

```js
const restify = require('restify');
const server = restify.createServer({ name: 'foo' });

server.get('/redirect', function(req, res, next) {
    return res.redirect({ pathname: '/' }, next);
});

server.get('/', function(req, res, next) {
    res.send(200, 'hello world');
    return next();
})

server.listen(3000);
```

```sh
$ curl -iL localhost:3000/redirect
HTTP/1.1 302 Found
Server: foo
Location: http:/
Content-Type: application/json
Content-Length: 4
Date: Thu, 14 Sep 2017 00:26:30 GMT
Connection: keep-alive

HTTP/1.1 404 Not Found
Server: foo
Content-Type: application/json
Content-Length: 62
Date: Thu, 14 Sep 2017 00:26:30 GMT
Connection: keep-alive

{"code":"ResourceNotFound","message":"/http:/ does not exist"}
```

## Cause

Looks like the reconstruction of the URL has some bad assumptions about host and protocol when using the object argument. Either we should enforce passing of certain params (incl hostname) if the object argument is used, or else avoid attaching a protocol to the generated URL. 

https://github.com/restify/node-restify/blob/master/lib/response.js#L603

## Are you willing and able to fix this?

Yes
