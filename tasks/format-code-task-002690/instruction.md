# Extension logging API

Extension authors have no good way to print debugging output from their extensions, and end users
have no way to silence noisy extensions. Add a logging capability to the extension API so that
extensions can log to the console, while users stay in control of which extensions are allowed to
log.

## What to build

Add `log` to the `app` namespace of the extension API:

```ts
export function log(message?: any, ...optionalParams: any[]): void
```

An extension calls `sourcegraph.app.log(...)` to emit a console message. Because every extension
shares the same console, a log message must be attributed to the extension that produced it and
must be suppressible per-extension.

### Behavior

- **Gating by user settings.** A new user setting `extensions.activeLoggers` holds an array of
  extension IDs. `app.log` only emits a message when the calling extension's ID is present in the
  `extensions.activeLoggers` array of the *final* (merged) settings. If the extension's ID is not
  listed, the call does nothing.
- **Reactive.** Gating reflects the current settings at the moment `log` is called. Adding or
  removing an extension's ID from `extensions.activeLoggers` at runtime immediately changes whether
  subsequent `log` calls emit.
- **Robust to malformed settings.** If `extensions.activeLoggers` is missing, `null`, or not an
  array, no extension is allowed to log (no call should throw).
- **Attribution.** When a message is emitted, it is forwarded to the main thread to be printed
  there (the extension host and the main thread may live on different pages, so logging must happen
  on the main thread). The forwarded arguments must (a) include the originating extension's ID
  somewhere, and (b) preserve the original `message` / `optionalParams` the extension passed,
  in their original order, as the trailing arguments. The main-thread side exposes a dedicated
  capability for receiving these messages, named `logExtensionMessage`, alongside the other
  main-thread API methods.
- **Per-extension binding.** Each extension must receive an API whose `log` is bound to that
  extension's own ID, so messages are attributed correctly. The existing way an extension API is
  constructed should accept the extension's ID. Constructing an extension API without an associated
  extension ID must still work and yield a `log` that is a safe no-op (it must be a callable
  function that emits nothing).

## Notes

- Existing extension-API construction call sites that do not pass an extension ID must keep working
  unchanged.
- Do not change the behavior of any other `app`, `configuration`, `workspace`, etc. methods.
