## Allow remapping Watermill's log levels when using the slog adapter

I'm using `NewSlogLogger` to plug Watermill into my application's `slog`-based logging setup. The integration itself works fine, but Watermill emits a lot of messages at `Info` level (router lifecycle, handler start/stop, subscribe acks, etc.) that I really don't want showing up alongside my application's own `Info` logs in production — they're more like debug/diagnostic information from my point of view.

The obvious workaround would be to raise the global slog level to `Warn`, but then I lose my own application's `Info` logs too. I want to silence/demote *Watermill's* noise specifically, while keeping the rest of my app's logging at `Info`.

Right now there doesn't seem to be a way to do this with the slog adapter — whatever level Watermill chooses internally is exactly the level slog sees. It would be great if, when constructing the slog adapter, I could say something like "treat Watermill's Info as slog Debug" (and similarly for other levels I might want to shift), so the routing of levels happens at the adapter boundary instead of forcing me to fiddle with slog handlers or global levels.

Existing usage that I'd like to keep working unchanged:

```go
logger := watermill.NewSlogLogger(slog.Default())
```

For users that don't care about remapping, the default behavior should stay the same as today (Watermill Info → slog Info, Debug → Debug, etc.).

A separate constructor along the lines of `NewSlogLoggerWithLevelMapping(...)` that takes the underlying `*slog.Logger` plus a level-to-level mapping would be a natural way to expose this.
