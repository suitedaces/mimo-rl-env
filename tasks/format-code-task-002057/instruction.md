# Host multiple applications behind one server

Right now a server `Application` only ever serves itself. We want a single running server to be
able to host several independent sub-applications and route each incoming HTTP request to whichever
one should handle it. Think multi-tenant: one process, many self-contained apps that each have
their own resources/plugins but can share infrastructure such as a database.

Please add an **application manager** to the server and expose it as `appManager` on every
`Application` instance. It should support the following observable behavior.

## Managing sub-applications

- `appManager.createApplication(name, options)` builds a new `Application` from the given
  application options, registers it under `name`, and returns the newly created instance.
- The registered sub-applications are reachable through `appManager.applications`, a `Map` keyed by
  the name they were registered with.
- `appManager.getApplication(name)` resolves (it is asynchronous) to the application registered
  under `name`, or to `undefined` when nothing is registered under that name. Every call must emit
  an asynchronous `beforeGetApplication` event *before* resolving, passing a single payload that
  carries the manager (`appManager`) and the requested `name`. This hook is the extension point
  that lets a listener register an application on demand, so a lookup that finds no app initially
  must still return one that a listener registered while handling the event.
- `appManager.removeApplication(name)` tears the application down and removes it from the manager.
  Removing a name that was never registered is a no-op (it must not throw).

## Routing requests

- `appManager.callback()` returns a Node HTTP request handler `(req, res)` that dispatches each
  request to the application chosen by a configurable selector.
- The selector receives the incoming request and returns either an `Application` instance (used
  directly) or a string (treated as the name of a registered sub-application).
- The default selector routes every request to the main application.
- `appManager.setAppSelector(fn)` replaces the selector.
- When the selector returns a name, the matching registered sub-application handles the request. If
  no application is registered under that name — even after the `beforeGetApplication` hook has had
  its chance to register one — the request falls back to the main application.

## Lifecycle propagation

- When the main application stops, every registered sub-application is stopped as well.
- When the main application is destroyed, every registered sub-application is destroyed as well.

Existing single-application behavior must keep working unchanged.
