## Can't tell which script a console log / assertion belongs to

I'm building an integration on top of postman-runtime. I subscribe to the callbacks from `run.start({...})` — specifically `console`, `assertion`, `beforeScript`, and `script` — and surface them to the end user (per-script log panels, error markers, etc.).

The problem: when an item has more than one script of the same kind (e.g. multiple test scripts, or both folder-level + item-level prerequest scripts), I can't tell which script a particular callback came from.

Roughly what I'm doing:

```js
runner.run(collection, { /* ... */ }, function (err, run) {
    run.start({
        console: function (cursor, level, ...logs) {
            // I want to attach this log line to a specific script in the UI.
            // But cursor only tells me where I am in the run
            // (position, iteration, ref, etc.) — nothing that says
            // "this came from script X on event Y".
            console.log(cursor, level, logs);
        },

        assertion: function (cursor, assertions) {
            // same problem — if an item has multiple test scripts and
            // both produce assertions, I can't group them by script.
        },

        beforeScript: function (err, cursor, script, event, item) { /* ... */ },
        script:       function (err, cursor, result, script, event, item) { /* ... */ }
    });
});
```

For `beforeScript` / `script` it's not as bad because the `script` and `event` objects are passed in directly, so I can read their ids. But `console` and `assertion` only get a `cursor` — and the cursor is identical across every script that runs for the same item/iteration. So if a prerequest script and a test script (or two test scripts) both call `console.log(...)`, both log lines arrive with effectively the same cursor and I have no way to route them to the right place in my UI.

It would be great if the cursor that's threaded through these callbacks carried enough information to trace a log / error / assertion back to the specific script (and the event that owns it) that produced it. That way every callback that receives a cursor has a consistent way to identify the originating script, without me having to correlate by timing or maintain my own state machine around `beforeScript` / `script`.

The new fields I'd expect on the cursor would be something like `scriptId` and `eventId`.
