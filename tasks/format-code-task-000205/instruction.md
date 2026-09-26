# Preserve module state across hot updates

Our Hot Module Replacement support lets a project's JS files talk to the bundler through
`module.hot` — they can register `accept` and `dispose` handlers, query the current status, and
so on. The one thing that's missing is a way to carry a little bit of state from an old version
of a module to the version that replaces it.

Right now, when a module is hot-swapped its `dispose` handler fires, but there's no channel for
that handler to hand anything off to the incoming copy of the module. As soon as the new code
runs, whatever the old instance knew is gone. That makes it impossible to do things like keep a
scroll position, a timer handle, or some accumulated counter alive across an edit.

Add the standard "hot data" mechanism that other bundlers expose:

- A module's `dispose` callback should be invoked with a single argument: a plain, initially-empty
  object that the handler can write into. This is the module's chance to stash anything it wants
  to survive the swap.
- When the replacement version of that same module initializes, it should be able to read back
  exactly that object as `module.hot.data`.
- A module that has not been replaced yet (its very first run) must see `module.hot.data` as
  `undefined` — there's nothing to restore.
- Each hot update gets its own fresh hand-off object. The object a `dispose` handler receives must
  start empty every time; state from earlier updates only carries forward if the module
  deliberately reads `module.hot.data` and copies it into the new object. Data is tracked per
  module, so unrelated modules never see each other's hand-off objects.

The existing `module.hot` behavior (accept, dispose firing, status reporting, the websocket update
flow) must keep working unchanged.
