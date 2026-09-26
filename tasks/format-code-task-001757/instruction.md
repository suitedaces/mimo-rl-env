## `onSuccess` / `onFailure` not firing correctly for closure scheduled tasks

I'm scheduling a closure task and attaching success/failure callbacks like this:

```php
$schedule->call(function () {
    // ... do some work ...
    return false; // signal failure
})->onSuccess(function () {
    Log::info('task succeeded');
})->onFailure(function () {
    Log::info('task failed');
});
```

Per the docs, returning `false` from a scheduled closure should mark the task as failed, so I'd expect `onFailure` to run here. But what I actually see is that `onSuccess` fires instead — regardless of whether the closure returns `false` or returns normally. So I have no way to react to the actual outcome of the closure.

For scheduled commands (`$schedule->command(...)`) the `onSuccess` / `onFailure` callbacks fire correctly based on the command's exit status, so the behavior for closure tasks looks inconsistent with that.
