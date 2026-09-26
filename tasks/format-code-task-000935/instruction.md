Certain errors result in request being null
If an error occurs before the Validation part of the lifecycle, `request` is `null` in:

+ The `onSend` hook

 ```js
fastify.addHook('onSend', function(request, reply, payload, next) {
   console.log(request) // null
})
```

+ Any custom error handler

```js
fastify.setErrorHandler(function(err, reply) {
  console.log(reply.request) // null
})
```

This is very much unexpected in the `onSend` hook and this also makes it more difficult to access the `req` object in the error handler.

See PR #551 for a potential fix.
