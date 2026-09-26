## Allow extra binding options (e.g. `namespace`) when registering artifacts on an Application

### What I'm trying to do

I'm building a sub-application that's mounted inside a larger LoopBack 4 app. I want the sub-app's artifacts (controllers, repositories, services, components, etc.) to be registered into **its own namespace** rather than into the default top-level ones like `controllers.*` / `repositories.*` / `services.*`. That way the parent app and the sub-app can have artifacts with the same class name without their bindings colliding, and consumers can address them under a clear prefix.

### The problem

The artifact registration methods on `Application` (and the repository / service mixins) only let me override the `name`:

```ts
app.controller(MyController, 'CustomName');
app.repository(MyRepository, 'CustomName');
app.component(MyComponent, 'CustomName');
app.server(MyServer, 'CustomName');
app.lifeCycleObserver(MyObserver, 'CustomName');
app.dataSource(MyDataSource, 'CustomName');
```

There's no way to pass other options that `createBindingFromClass` already supports — most importantly `namespace`. The methods hard-code the namespace internally (`controllers`, `repositories`, `components`, `servers`, ...) and there's no hook to override it from the caller side.

So in my sub-application I can't do something like "register all my controllers under `my-sub-app.controllers.*`". I either have to give up on isolation, or bypass these helpers entirely and call `createBindingFromClass` + `app.add(...)` myself for every single artifact, which defeats the purpose of having those convenience methods.

### What I'd like

These registration methods should accept either a name (current behavior, for backwards compatibility) **or** a full options object — at minimum `namespace` and `name`, but ideally any option `createBindingFromClass` already understands. Roughly:

```ts
// still works
app.controller(MyController, 'CustomName');

// new: customize namespace (and other options)
app.controller(MyController, {name: 'CustomName', namespace: 'my-sub-app.controllers'});
```

Same idea for `server`, `component`, `lifeCycleObserver`, `repository`, `dataSource`, and `service` (which already takes an options object — its options should extend the same shape so `namespace` works there too).

`app.service(...)` already accepts an options object, so the pattern isn't foreign — it just needs to be available on the rest of the artifact registration APIs and the mixin methods so sub-apps and other advanced use cases can configure binding location, not just the binding name.
