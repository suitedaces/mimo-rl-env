I’m using this in an asyncio app and I’d like to keep a single Ruuvi tag object around the same way I can with `RuuviTag`, but without having to call a blocking `update()`. Could we have an async-friendly version where I can read the tag’s `mac`/current state and refresh it with `await`?

Expected outcomes:
- Async single-tag API: `ruuvitag_sensor.ruuvitag.RuuviTagAsync` is available as a public class for representing one tag in async code.
- Instance state access: a `RuuviTagAsync` instance exposes readable `mac` and `state` properties analogous to the synchronous single-tag object; a newly created instance starts with an empty current state.
- Awaitable refresh: `RuuviTagAsync.update()` can be awaited, refreshes the represented tag without requiring callers to invoke the blocking single-tag update path, returns the latest decoded state for the current underlying tag data, and keeps the instance’s `state` cache in sync with that return value.
- No-data refresh: if an async refresh finds no current data for the tag, `RuuviTagAsync.update()` returns `{}` and the instance’s cached `state` becomes `{}`.
- Repeated-data refresh: if an async refresh observes the same underlying tag data as the previous refresh, `RuuviTagAsync.update()` returns the already cached state for that data rather than producing a different state.
- Documentation: the README’s single-sensor guidance mentions the async single-tag convenience class alongside the existing synchronous one where it discusses alternatives for single-sensor access.

Implementation notes:
- The concrete internal structure, sharing of code with the synchronous class, and exact validation location are up to the implementation.
- The async implementation should integrate with the project’s existing asynchronous sensor-reading capabilities rather than forcing users of `RuuviTagAsync` to call the blocking single-tag update method themselves.
- Preserve the existing synchronous `RuuviTag` public behavior while adding the async-friendly variant.
