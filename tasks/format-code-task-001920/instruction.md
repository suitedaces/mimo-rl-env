# Collect a web router table from controllers

The core package can already start a web framework and register controllers at
runtime, but there is no way to obtain the routing information of an application
*without* booting a real HTTP server. Tooling such as route listing, doc
generation and serverless adapters needs to know, ahead of time, every route an
application declares through the `@Controller` / `@Get` / `@Post` / ... family
of decorators.

Add a reusable **web router collector** to `@midwayjs/core` that statically
analyzes a Midway application directory and returns the routes it declares. It
should load the application's controller modules (given the application's source
base directory) and read the metadata attached by the routing decorators — no
HTTP framework should need to be started.

Expose it as a public `WebRouterCollector` class, constructed with the
application base directory. It must provide three async accessors:

- `getRouterTable()` → a `Map` whose keys are controller prefixes and whose
  values are the list of routes declared under that prefix.
- `getFlattenRouterTable()` → a single flat array containing every route from
  every prefix.
- `getRoutePriorityList()` → one entry per prefix describing that prefix's
  routing priority.

### Route shape

Each collected route must describe at least the following, derived from the
controller and method decorators:

- `prefix` — the owning controller's prefix.
- `url` — the route path as declared on the method (without the prefix).
- `requestMethod` — the HTTP verb (e.g. `get`, `post`).
- `method` — the controller method name the route maps to.
- `routerName` — the alias given to the route, or `''` when none was provided.
- `description` / `summary` — the corresponding decorator options, each
  defaulting to `''` when absent.
- `controllerId` — the provide id of the owning controller (a non-empty string).
- `handlerName` — the controller method's fully-qualified handler key, formed as
  `` `${controllerId}.${method}` ``.
- `requestMetadata` — the parameter metadata for the handler's arguments
  (an array; empty when the handler has no parameter decorators).
- `responseMetadata` — the response metadata declared on the handler
  (an array; empty when no response decorator was used).

### Ordering rules

Within a single prefix, routes must be ordered by path specificity: a route with
more path segments comes before one with fewer, and among routes with the same
number of segments the one with the longer literal path comes first.

`getRoutePriorityList()` must be sorted from highest priority to lowest. A
controller's priority comes from its `@Priority` decorator; controllers without
one use a default priority, and an explicit priority outranks the default. A
controller mounted at the root prefix `/` that has no explicit priority is
treated as the lowest priority of all, so it always sorts last. Each priority
entry must expose at least the `prefix`, its `priority`, and the owning
`controllerId`.

The accessors may be called more than once and must return consistent results.
