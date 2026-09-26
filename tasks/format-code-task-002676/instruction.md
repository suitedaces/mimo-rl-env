## `Slim\Http\Stream` doesn't work with streams opened via `popen()`

I'm using Slim to wrap the output of a shell command into a PSR-7 response. The pattern looks roughly like this:

```php
$app->get('/export', function ($request, $response) {
    $pipe = popen('/usr/local/bin/my-export-tool --format=csv', 'r');
    $stream = new \Slim\Http\Stream($pipe);
    return $response
        ->withHeader('Content-Type', 'text/csv')
        ->withBody($stream);
});
```

This is a fairly natural thing to do when you want to stream the output of an external CLI tool straight back to the client without buffering it all into memory first.

The problem is that `Slim\Http\Stream` doesn't really cope with pipe resources returned by `popen()`. The response body comes back empty — when I dig into it, `isReadable()` on the stream returns `false`, even though the pipe was opened in read mode and I can `fread()` from the underlying resource just fine outside of Slim.

On top of that, a few other operations don't behave sensibly on a pipe:

- `getSize()` reports something derived from `fstat`, but pipes don't really have a meaningful size — the value you get back is misleading.
- `tell()` and the seek-related methods don't make sense for a pipe at all (pipes aren't positional / seekable), but the current code treats it like any other stream and ends up in odd states instead of cleanly reporting "not supported".
- When the stream goes out of scope / gets closed at the end of the request, the resource isn't being cleaned up the way a pipe resource should be cleaned up, which feels wrong even if I don't see an immediate error every time.

It would be great if `Slim\Http\Stream` detected when the underlying resource is a pipe and handled all of the above appropriately — at minimum so that reading from a `popen()`-backed stream actually works end-to-end through a Slim response, and the size/position/seek operations behave in a way that makes sense for a non-seekable, non-positional stream.

It would also be useful if the class exposed a small public predicate (something like `isPipe()`) so callers / tests can ask whether the underlying resource is a pipe.
