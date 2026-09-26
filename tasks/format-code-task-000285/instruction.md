## Problem Statement

I'm using an async `@depends_on` listener to initialize a client, and when I call `validate_all_configs(include_listeners=True)` at startup I see a `coroutine was never awaited` warning. The listener body doesn't seem to run during validation, and the singleton it returns is still missing until later. I might be wiring it wrong, but the same startup validation does run my sync listeners.

## Expected outcomes

- Startup validation with async listeners: when async `@depends_on` listeners are included in startup validation, an awaited validation call completes their initialization during validation, without leaking un-awaited coroutine warnings.
- Await boundary: if `include_listeners=True` reaches at least one async listener, `validate_all_configs(include_listeners=True)` provides an awaitable validation operation, and listener initialization should not happen merely by creating that operation.
- Sync compatibility: when only synchronous listeners are involved, `validate_all_configs(include_listeners=True)` remains a synchronous call and still eagerly loads configs and runs those listeners without requiring `await`.
- Documentation: the listener usage documentation describes the async-listener startup-validation pattern, including that the validation call is awaited when async listeners are included.

## Implementation notes

- Preserve the existing public API names and normal synchronous behavior for applications that only use synchronous listeners.
- The internal scheduling approach, listener bookkeeping, and validation structure are implementation details.
- Initialization failures from listeners should still surface during startup validation rather than being silently delayed or swallowed.
